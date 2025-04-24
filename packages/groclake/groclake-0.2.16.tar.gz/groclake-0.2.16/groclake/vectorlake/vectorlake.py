import os
import random
import string
from datetime import datetime
import json
import pytz
import openai
import hashlib

from groclake.datalake import Datalake
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

class InvalidAuth(Exception):
    def __init__(self, message, error_code=401):
        self.http_code = error_code
        self.message = message
        super(InvalidAuth, self).__init__()

class DatabaseInsertion(Exception):
    def __init__(self, message, error_code=500):
        self.http_code = error_code
        self.message = message
        super(DatabaseInsertion, self).__init__()

class Config:
    # ES Configuration
    ES_CONFIG = {
        "host": os.getenv("ES_HOST"),
        "port": int(os.getenv("ES_PORT")),
        "api_key": os.getenv("ES_API_KEY"),
        "schema": os.getenv("ES_SCHEMA")
    }

    MYSQL_CONFIG = {
        'user': os.getenv('MYSQL_USER'),
        'passwd': os.getenv('MYSQL_PASSWORD'),
        'host': os.getenv('MYSQL_HOST'),
        'port': int(os.getenv('MYSQL_PORT')),
        'db': os.getenv('MYSQL_DB'),
        'charset': 'utf8'
    }

    REDIS_CONFIG = {
        "host": os.getenv("REDIS_HOST", "localhost"),
        "port": int(os.getenv("REDIS_PORT", 6379)),
    }

class DatalakeConnection(Datalake):
    def __init__(self):
        super().__init__()

        ES_CONFIG = Config.ES_CONFIG
        ES_CONFIG['connection_type'] = 'es'

        MYSQL_CONFIG = Config.MYSQL_CONFIG
        MYSQL_CONFIG['connection_type'] = 'sql'

        REDIS_CONFIG = Config.REDIS_CONFIG
        REDIS_CONFIG['connection_type'] = 'redis'

        self.plotch_pipeline = self.create_pipeline(name="groclake_pipeline")
        self.plotch_pipeline.add_connection(name="es_connection", config=ES_CONFIG)
        self.plotch_pipeline.add_connection(name="sql_connection", config=MYSQL_CONFIG)
        self.plotch_pipeline.add_connection(name="redis_connection", config=REDIS_CONFIG)

        self.execute_all()

        self.connections = {
            "es_connection": self.get_connection("es_connection"),
            "sql_connection": self.get_connection("sql_connection"),
            "redis_connection": self.get_connection("redis_connection")
        }

    def get_connection(self, connection_name):
        return self.plotch_pipeline.get_connection_by_name(connection_name)

datalake_connection = DatalakeConnection()
es_connection = datalake_connection.connections["es_connection"]
mysql_connection = datalake_connection.connections["sql_connection"]
redis_conn = datalake_connection.connections["redis_connection"]

class Vectorlake:
    SUPPORTED_MODELS = {
        "text-embedding-ada-002": 1536,
        "text-embedding-3-small": 1536,
        "text-embedding-3-large": 3072,
        "text-embedding-004": 768
    }

    def __init__(self, index_uuid=None):
        self.conn = DatalakeConnection()
        self._database_handlers = {}  # Lazy-loaded handlers

    def _get_database_handler(self, database):
        """Initialize and return the database handler only when needed."""
        if database not in self._database_handlers:
            if database == 'elasticsearch':
                self._database_handlers[database] = self.ElasticsearchHandler(self.conn)
            else:
                raise ValueError(f"Unsupported database: {database}")
        return self._database_handlers[database]

    class ElasticsearchHandler:
        def __init__(self, conn):
            self.conn = conn

        def create_index(self, entity_id):
            es = self.conn.connections["es_connection"]
            index_body = {
                "settings": {
                    "number_of_shards": 3,
                    "number_of_replicas": 1,
                    "refresh_interval": "10s"
                },
                "mappings": {
                    "dynamic": "false",
                    "properties": {
                        "vector_id": {"type": "long"},
                        "groc_account_id": {"type": "keyword"},
                        "vector_type": {"type": "keyword"},
                        "metadata": {"type": "object", "enabled": True},
                        "query": {"type": "text"},
                        "vector_document": {"type": "text"},
                        "product_vector": {
                            "type": "dense_vector",
                            "dims": 768,
                            "index": True,
                            "similarity": "cosine",
                            "index_options": {
                                "type": "int8_hnsw",
                                "m": 16,
                                "ef_construction": 100
                            }
                        },
                        "vector": {
                            "type": "dense_vector",
                            "dims": 1536,
                            "index": True,
                            "similarity": "cosine",
                            "index_options": {
                                "type": "hnsw",
                                "m": 16,
                                "ef_construction": 100
                            }
                        }
                    }
                }
            }
            es.write(query={'index': entity_id, 'body': index_body})

        def insert_document(self, vector_id, groc_account_id, vector, vector_type, query, metadata, document_text, vectorlake_id):
            if len(vector) != 1536:
                raise ValueError(f"Error: document_vector has {len(vector)} dimensions, expected 1536.")

            if isinstance(metadata, str):
                try:
                    metadata = json.loads(metadata) if metadata.strip() else {}
                except json.JSONDecodeError:
                    metadata = {}
            elif not isinstance(metadata, dict):
                metadata = {}

            doc = {
                "vector_id": vector_id,
                "groc_account_id": groc_account_id,
                "product_vector": vector,
                "vector_type": vector_type,
                "query": query,
                "metadata": metadata,
                "vector_document": document_text,
            }

            try:
                es = self.conn.connections["es_connection"]
                response = es.write(query={'index': vectorlake_id, 'body': doc})
                return response
            except Exception as e:
                raise Exception(f"Error inserting document: {e}")

        def search(self, vector_embedding, vectorlake_id, category_name=None, num_items=10):
            if not vector_embedding:
                raise ValueError("Vector embedding is required")

            vector_field = "product_vector" if len(vector_embedding) == 768 else "vector"
            filter_conditions = [{"exists": {"field": vector_field}}]
            if category_name:
                filter_conditions.append({"term": {"groc_category.keyword": category_name}})

            es_query = {
                "query": {
                    "script_score": {
                        "query": {"bool": {"filter": filter_conditions}},
                        "script": {
                            "source": f"""
                                if (doc['{vector_field}'].size() > 0) {{
                                    return cosineSimilarity(params.query_vector, '{vector_field}') + 1.0;
                                }} else {{
                                    return 0;
                                }}
                            """,
                            "params": {"query_vector": vector_embedding}
                        }
                    }
                },
                "size": num_items,
                "sort": [{"_score": {"order": "desc"}}]
            }

            es_connection = self.conn.connections["es_connection"]
            data = es_connection.search(index=vectorlake_id, body=es_query)
            hits = data.get('hits', {}).get('hits', [])
            return {
                "api_action_status": "success",
                "results": [
                    {
                        'vector_document': hit.get('_source', {}).get('vector_document', ''),
                        'metadata': hit.get('_source', {}).get('metadata', {})
                    }
                    for hit in hits
                ]
            }

        def delete_index(self, vectorlake_id):
            try:
                es = self.conn.connections["es_connection"]
                response = es.delete(index=vectorlake_id, body={"query": {"match_all": {}}})
                return {'message': 'Vectorlake deleted successfully.'}
            except Exception as e:
                raise Exception(f"Error deleting vectors: {e}")

        def fetch_vectors(self, vectorlake_id):
            query_body = {
                "query": {"match_all": {}},
                "_source": ['metadata', 'groc_account_id', "product_vector", 'vector_type', 'query', "vector_id", "vector_document"]
            }
            try:
                response = self.conn.connections["es_connection"].search(index=vectorlake_id, body=query_body)
                return {'vectors': [hit['_source'] for hit in response.get('hits', {}).get('hits', [])]}
            except Exception as e:
                return {'vectors': []}

    # --- Core Methods (Lazy-Loaded) ---
    def _vector_create(self, vectorlake_name, groc_account_id, database='elasticsearch'):
        existing_data = self._get_existing_vectorlake_data(groc_account_id)
        if existing_data:
            return {
                'vectorlake_id': existing_data.get('entity_id'),
                'message': 'Vectorlake already exists.',
                'vectorlake_name': existing_data.get('name', '')
            }
        
        vectorlake_id = self._generate_unique_id(length=16)
        handler = self._get_database_handler(database)
        handler.create_index(vectorlake_id)
        
        db_params = {
            'entity_id': vectorlake_id,
            'entity_type': 'vectorlake',
            'created_at': self._get_current_datetime(),
            'groc_account_id': groc_account_id,
            'name': vectorlake_name
        }
        self._log_in_groclake_entity_master(db_params)
        return {'vectorlake_id': vectorlake_id, "vectorlake_name": vectorlake_name}

    def _vector_push(self, groc_account_id, vector, vector_type, query, metadata, document_text, vectorlake_id, database='elasticsearch'):
        db_params = {
            'groc_account_id': groc_account_id,
            'vector_embedding': json.dumps(vector),
            'created_at': self._get_current_datetime(),
            'vector_type': vector_type,
            'query': query,
            'metadata': json.dumps(metadata),
            "document_text": document_text,
            "vectorlake_id": vectorlake_id
        }

        vector_id = self._save_in_grocklake_vectors(db_params)
        handler = self._get_database_handler(database)
        handler.insert_document(vector_id, groc_account_id, vector, vector_type, query, metadata, document_text, vectorlake_id)
        return {'vector_id': vector_id}

    def _vector_search(self, vector_embedding, vectorlake_id, category_name=None, num_items=10, database='elasticsearch'):
        handler = self._get_database_handler(database)
        return handler.search(vector_embedding, vectorlake_id, category_name, num_items)

    def _vectorlake_delete(self, vectorlake_id, database='elasticsearch'):
        existing_vectorlake = self._get_existing_vectorlake(vectorlake_id)
        if not existing_vectorlake:
            return {"message": f"Vectorlake not found: {vectorlake_id}."}
        
        self._delete_vectorlake(vectorlake_id)
        self._delete_vectorlake_vectors(vectorlake_id)
        handler = self._get_database_handler(database)
        return handler.delete_index(vectorlake_id)

    def _vectors_fetch(self, vectorlake_id, database='elasticsearch'):
        handler = self._get_database_handler(database)
        return handler.fetch_vectors(vectorlake_id)

    # --- Utility Methods ---
    def _generate_unique_id(self, length=16):
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

    def _get_current_datetime(self):
        return datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%Y-%m-%d %H:%M:%S")

    def _save_cartesian_catalog_vector_query(self, vector_query, vector_embedding, vector_dimension, vector_model):
        query = ''' INSERT INTO groclake_cataloglake_catalog_vector_query 
            (vector_query, vector_embedding, vector_dimension, vector_model) VALUES (%s, %s, %s, %s)'''
        return mysql_connection.write(query, (vector_query, vector_embedding, vector_dimension, vector_model))

    def _fetch_cartesian_catalog_vector_query(self, vector_query, vector_model):
        query = ''' SELECT vector_embedding, vector_dimension FROM groclake_cataloglake_catalog_vector_query
            WHERE vector_query = %s AND vector_model = %s '''
        result = mysql_connection.read(query, (vector_query, vector_model), multiple=False)
        return result

    def _log_in_groclake_entity_master(self, db_params, table_name='groclake_entity_master'):
        query = "insert into " + table_name + " (" + ",".join(db_params.keys()) + ") VALUES (" + ",".join(['%s' for x in db_params.values()]) + ")"
        return mysql_connection.write(query, tuple(db_params.values()))

    def _save_in_grocklake_vectors(self, db_params, table_name='groclake_vectorlake_vectors_metadata'):
        query = "insert into " + table_name + " (" + ",".join(db_params.keys()) + ") VALUES (" + ",".join(['%s' for x in db_params.values()]) + ")"
        return mysql_connection.write(query, tuple(db_params.values()))

    def _get_existing_vectorlake_data(self, groc_account_id):
        query = '''SELECT * FROM groclake_entity_master 
                   WHERE groc_account_id = %s AND entity_type = 'vectorlake' 
                   ORDER BY created_at DESC LIMIT 1'''
        result = mysql_connection.read(query, (groc_account_id,), multiple=False)
        return result

    def _delete_vectorlake(self, vectorlake_id):
        query = """DELETE FROM groclake_entity_master WHERE entity_id = %s"""
        params = (vectorlake_id,)
        return mysql_connection.write(query, params)

    def _get_existing_vectorlake(self, vectorlake_id):
        condition_clause = "entity_id = %s"
        query = f"SELECT entity_id FROM groclake_entity_master WHERE {condition_clause}"
        params = (vectorlake_id,)
        result = mysql_connection.read(query, params, multiple=False)
        return result

    def _delete_vectorlake_vectors(self, vectorlake_id):
        query = """DELETE FROM groclake_vectorlake_vectors_metadata WHERE vectorlake_id = %s"""
        params = (vectorlake_id,)
        return mysql_connection.write(query, params)

    @staticmethod
    def _hash_query(query, model, model_provider):
        """Generates a hash for caching purposes."""
        hash_input = f"{query}:{model}:{model_provider}"
        return hashlib.sha256(hash_input.encode()).hexdigest()

    def _generate_vector(self, query, model="text-embedding-3-small", model_provider="openai"):
        """Generate vector using a language model."""
        if model_provider == "openai":
            if model not in self.SUPPORTED_MODELS:
                raise ValueError(f"Unsupported model. Please use one of: {', '.join(self.SUPPORTED_MODELS.keys())}")

            try:
                response = openai.embeddings.create(input=query, model=model)
                vector = response.data[0].embedding

                # Verify vector dimension matches expected dimension
                expected_dim = self.SUPPORTED_MODELS[model]
                if len(vector) != expected_dim:
                    raise ValueError(f"Generated vector dimension ({len(vector)}) does not match expected dimension ({expected_dim}) for model {model}")

                return vector
            except Exception as e:
                return {"error": f"OpenAI request failed: {str(e)}"}

        raise ValueError("Unsupported model provider. Please use 'openai'.")

    def _vector_fetch(self, query, model="text-embedding-3-small", model_provider="openai"):
        if not query or len(query) > 500:
            return {"error": "Vector could not be generated due to large query."}

        if model not in self.SUPPORTED_MODELS:
            return {"error": f"Unsupported model. Please use one of: {', '.join(self.SUPPORTED_MODELS.keys())}"}

        # Generate cache key for Redis
        cache_key = self._hash_query(query, model, model_provider)

        # Check Redis cache
        redis_conn = self.conn.connections["redis_connection"]
        vector = redis_conn.get(cache_key)
        if vector:
            return {"vector": json.loads(vector), "message": "Cached vector retrieved from Redis."}

        # Check MySQL database for existing vector
        result = self._fetch_cartesian_catalog_vector_query(query, model)

        if result:
            vector_str, stored_dim = result.get('vector_embedding'), result.get('vector_dimension')
            vector = [float(i) for i in vector_str.split(',')]

            if len(vector) != self.SUPPORTED_MODELS[model]:
                return {"error": f"Stored vector dimension mismatch for model {model}"}

            # Cache the result in Redis
            redis_conn.set(cache_key, json.dumps(vector))
            return {"vector": vector, "message": "Vector retrieved from MySQL and stored in Redis."}

        # Generate new vector
        vector = self._generate_vector(query, model, model_provider)
        if isinstance(vector, dict) and "error" in vector:
            raise Exception(vector["error"])

        vector_str = ','.join(map(str, vector))
        vector_dimension = len(vector)

        if vector_dimension != self.SUPPORTED_MODELS[model]:
            return {"error": f"Generated vector dimension mismatch for model {model}"}

        # Store new vector in MySQL
        try:
            self._save_cartesian_catalog_vector_query(query, vector_str, vector_dimension, model)
        except Exception as e:
            return {"error": f"Failed to store vector in MySQL: {str(e)}"}

        # Cache the new vector in Redis
        redis_conn.set(cache_key, json.dumps(vector))
        return {
            "vector": vector,
            "model": model,
            "model_provider": model_provider,
            "message": "Vector generated and stored successfully."
        }

    # --- Public Methods ---
    def generate(self, query, model="text-embedding-3-small", model_provider="openai"):
        """
        Generate a vector embedding for the given query using the specified model and provider.
        """
        try:
            vector = self._generate_vector(query, model, model_provider)
            if isinstance(vector, dict) and "error" in vector:
                return {"status": "error", "message": vector["error"]}
            return {"status": "success", "vector": vector, "model": model, "model_provider": model_provider}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def push(self, payload):
        """
        Push a vector and metadata into the vectorlake using payload dictionary.
        """
        try:
            required_fields = ["vector", "vectorlake_id"]
            for field in required_fields:
                if field not in payload:
                    return {"status": "error", "message": f"{field} is required"}

            result = self._vector_push(
                groc_account_id=str(self._add_groc_account_id()),
                vector=payload["vector"],
                vector_type=payload.get("vector_type", "text"),
                query=payload.get("query", ""),
                metadata=payload.get("metadata", {}),
                document_text=payload.get("vector_document", ""),
                vectorlake_id=payload["vectorlake_id"],
                database=payload.get("database", "elasticsearch")
            )
            return {"status": "success", "vector_id": result["vector_id"]}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def search(self, payload):
        """
        Search for similar vectors using payload dictionary.
        """
        try:
            if not payload.get("vector_embedding"):
                return {"status": "error", "message": "vector_embedding is required"}
            if not payload.get("vectorlake_id"):
                return {"status": "error", "message": "vectorlake_id is required"}

            results = self._vector_search(
                vector_embedding=payload["vector_embedding"],
                vectorlake_id=payload["vectorlake_id"],
                category_name=payload.get("vector_type"),
                num_items=payload.get("num_items", 10),
                database=payload.get("database", "elasticsearch")
            )

            # Optional score filtering
            if "min_score" in payload and results.get("results"):
                results["results"] = [
                    r for r in results["results"] 
                    if r.get("_score", 0) >= payload["min_score"]
                ]

            return {"status": "success", "results": results.get("results", [])}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def create(self, payload=None):
        """
        Create a new vectorlake using a payload dictionary.
        """
        try:
            if payload is None:
                payload = {}

            # Assign groc_account_id as vectorlake_name if not provided
            vectorlake_name = payload.get("vectorlake_name", str(self._add_groc_account_id()))

            result = self._vector_create(
                vectorlake_name=vectorlake_name,
                groc_account_id=str(self._add_groc_account_id()),
                database=payload.get("database", "elasticsearch")
            )

            return {
                "status": "success",
                "vectorlake_id": result["vectorlake_id"],
                "vectorlake_name": result["vectorlake_name"]
            }

        except Exception as e:
            return {"status": "error", "message": str(e)}

    def delete(self, vectorlake_id, database='elasticsearch'):
        """
        Delete a vectorlake and its associated vectors.
        """
        try:
            result = self._vectorlake_delete(vectorlake_id, database)
            return {"status": "success", "message": result["message"]}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def fetch(self, payload=None):
        """
        Fetch vectors from a vectorlake using payload dictionary.
        """
        try:
            if not payload.get("vectorlake_id"):
                return {"status": "error", "message": "vectorlake_id is required"}

            vectors = self._vectors_fetch(
                payload["vectorlake_id"],
                database=payload.get("database", "elasticsearch")
            )
            
            # Implement pagination
            page = max(1, payload.get("page", 1))
            per_page = max(1, min(100, payload.get("per_page", 10)))
            total = len(vectors["vectors"])
            paginated = vectors["vectors"][(page-1)*per_page : page*per_page]

            return {
                "status": "success",
                "vectors": paginated,
                "pagination": {
                    "page": page,
                    "per_page": per_page,
                    "total": total,
                    "pages": (total + per_page - 1) // per_page
                }
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @staticmethod
    def _get_groc_api_headers():
        return {'GROCLAKE-API-KEY': os.getenv('GROCLAKE_API_KEY')}
    
    @staticmethod
    def _add_groc_account_id():
        return {'groc_account_id': os.getenv('GROCLAKE_ACCOUNT_ID')}