from abc import ABC, abstractmethod
from typing import Dict, Optional, Any
import requests
from datetime import datetime, timedelta
import jwt
import os
from dotenv import load_dotenv
import time
import json

load_dotenv()

def get_required_env(key: str) -> str:
    """Get required environment variable or raise error"""
    value = os.getenv(key)
    if not value:
        raise ValueError(f"Required environment variable {key} is not set")
    return value

class AuthGateway(ABC):
    """Base class for all authentication methods"""
    
    # Class-level registry for auth gateways
    _registry: Dict[str, 'AuthGateway'] = {}
    
    def __init__(self, tool_name: str, tool_id: int, auth_config: Dict[str, Any]):
        self.tool_name = tool_name
        self.tool_id = tool_id
        self.auth_config = auth_config
        self.connection_status = 'not_connected'
        self.connected_at = None
    
    @classmethod
    def register_gateway(cls, tool_name: str, gateway: 'AuthGateway') -> None:
        """Register a new authentication gateway"""
        cls._registry[tool_name] = gateway
    
    @classmethod
    def get_gateway(cls, tool_name: str) -> 'AuthGateway':
        """Get authentication gateway for a specific tool"""
        if tool_name not in cls._registry:
            raise ValueError(f"No authentication method registered for {tool_name}")
        return cls._registry[tool_name]
    
    @classmethod
    def connect(cls, tool_name: str, tool_id: int, auth_strategy: str, auth_config: Dict[str, Any]) -> Dict[str, Any]:
        """Connect to a tool using the specified authentication strategy"""
        try:
            # Get the appropriate gateway based on auth strategy
            gateway_class = {
                'OAuthStrategy': OAuthGateway,
                'APIKeyStrategy': APIKeyGateway,
                'JWTAuthStrategy': JWTAuthGateway,
                'BasicAuthStrategy': BasicAuthGateway,
                'CustomHeaderStrategy': CustomHeaderGateway,
                'AccessKeyStrategy': AccessKeyGateway
            }.get(auth_strategy)
            
            if not gateway_class:
                raise ValueError(f"Unsupported authentication strategy: {auth_strategy}")
            
            # Create the gateway
            gateway = gateway_class(tool_name, tool_id, auth_config)
            
            # Connect and get the response
            response = gateway._connect()
            
            # Register the gateway if connection was successful
            cls._registry[tool_name] = gateway
            
            return response
            
        except Exception as e:
            raise ConnectionError(f"Failed to connect to {tool_name}: {str(e)}")

    @classmethod
    def validate(cls, tool_name: str) -> bool:
        """Validate the connection to a tool"""
        try:
            gateway = cls.get_gateway(tool_name)
            return gateway.is_auth_valid()
        except Exception:
            return False
    
    @abstractmethod
    def _connect(self) -> Dict[str, Any]:
        """Connect to the tool and return the authentication response"""
        pass
    
    @abstractmethod
    def is_auth_valid(self) -> bool:
        """Check if the authentication is valid"""
        pass
    
    @abstractmethod
    def refresh_auth(self) -> None:
        """Refresh the authentication if needed"""
        pass
    
    @abstractmethod
    def make_authenticated_request(self, method: str, url: str, **kwargs) -> requests.Response:
        """Make an authenticated request to the tool"""
        pass

class OAuthGateway(AuthGateway):
    """OAuth 2.0 authentication implementation"""
    
    def __init__(self, tool_name: str, tool_id: int, auth_config: Dict[str, Any]):
        super().__init__(tool_name, tool_id, auth_config)
        self.client_id = auth_config.get('client_id')
        self.client_secret = auth_config.get('client_secret')
        self.auth_url = auth_config.get('auth_url')
        self.token_url = auth_config.get('token_url')
        self.redirect_uri = auth_config.get('redirect_uri')
        self.scopes = auth_config.get('scopes', [])
        self.access_token = None
        self.refresh_token = None
        self.token_expires_at = None

    def _connect(self) -> Dict[str, Any]:
        """Connect using OAuth and return the authorization URL"""
        self.connection_status = 'pending'
        return {
            "auth_url": self.get_oauth_authorization_url(),
            "message": "Please visit the authorization URL and enter the code"
        }

    def get_oauth_authorization_url(self) -> str:
        """Get the OAuth authorization URL"""
        params = {
            "client_id": self.client_id,
            "scope": " ".join(self.scopes),
            "redirect_uri": self.redirect_uri,
            "response_type": "code"
        }
        return f"{self.auth_url}?{'&'.join(f'{k}={v}' for k, v in params.items())}"

    def get_oauth_token(self, code: str) -> Dict[str, Any]:
        """Exchange authorization code for access token"""
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "redirect_uri": self.redirect_uri,
            "grant_type": "authorization_code"
        }
        response = requests.post(
            self.token_url,
            data=data,
            headers={"Accept": "application/json"}
        )
        if response.status_code == 200:
            token_data = response.json()
            self.access_token = token_data.get('access_token')
            self.refresh_token = token_data.get('refresh_token')
            self.token_expires_at = datetime.now() + timedelta(seconds=token_data.get('expires_in', 3600))
            self.connection_status = 'connected'
            self.connected_at = datetime.now()
            return token_data
        else:
            raise ValueError(f"Failed to exchange code for token: {response.text}")

    def is_auth_valid(self) -> bool:
        """Check if the OAuth token is valid"""
        if not self.access_token:
            return False
        if self.token_expires_at and datetime.now() >= self.token_expires_at:
            return False
        return True

    def refresh_auth(self) -> None:
        """Refresh the OAuth token"""
        if not self.refresh_token:
            raise ValueError("No refresh token available")
        
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": self.refresh_token,
            "grant_type": "refresh_token"
        }
        response = requests.post(
            self.token_url,
            data=data,
            headers={"Accept": "application/json"}
        )
        if response.status_code == 200:
            token_data = response.json()
            self.access_token = token_data.get('access_token')
            self.token_expires_at = datetime.now() + timedelta(seconds=token_data.get('expires_in', 3600))
        else:
            raise ValueError(f"Failed to refresh token: {response.text}")

    def make_authenticated_request(self, method: str, url: str, **kwargs) -> requests.Response:
        """Make an authenticated request with OAuth token"""
        if not self.is_auth_valid():
            self.refresh_auth()
        
        headers = kwargs.get('headers', {})
        headers['Authorization'] = f"Bearer {self.access_token}"
        kwargs['headers'] = headers
        return requests.request(method, url, **kwargs)

class APIKeyGateway(AuthGateway):
    """API Key authentication implementation"""
    
    def __init__(self, tool_name: str, tool_id: int, auth_config: Dict[str, Any]):
        super().__init__(tool_name, tool_id, auth_config)
        self.api_key = auth_config.get('api_key')
        self.header_name = auth_config.get('header_name', 'x-api-key')

    def _connect(self) -> Dict[str, Any]:
        """Connect using API Key"""
        self.connection_status = 'connected'
        self.connected_at = datetime.now()
        return {
            "status": "connected",
            "message": "Successfully connected using API Key"
        }

    def is_auth_valid(self) -> bool:
        """Check if API Key is valid"""
        return bool(self.api_key)

    def refresh_auth(self) -> None:
        """No refresh needed for API Key"""
        pass

    def make_authenticated_request(self, method: str, url: str, **kwargs) -> requests.Response:
        """Make an authenticated request with API Key"""
        headers = kwargs.get('headers', {})
        headers[self.header_name] = self.api_key
        kwargs['headers'] = headers
        return requests.request(method, url, **kwargs)

class JWTAuthGateway(AuthGateway):
    """JWT authentication implementation"""
    
    def __init__(self, tool_name: str, tool_id: int, auth_config: Dict[str, Any]):
        super().__init__(tool_name, tool_id, auth_config)
        self.jwt_token = auth_config.get('jwt_token')
        self.header_name = auth_config.get('header_name', 'Authorization')
        self.token_prefix = auth_config.get('token_prefix', 'Bearer')

    def _connect(self) -> Dict[str, Any]:
        """Connect using JWT"""
        self.connection_status = 'connected'
        self.connected_at = datetime.now()
        return {
            "status": "connected",
            "message": "Successfully connected using JWT"
        }

    def is_auth_valid(self) -> bool:
        """Check if JWT token is valid"""
        if not self.jwt_token:
            return False
        try:
            # Verify token is not expired
            decoded = jwt.decode(self.jwt_token, options={"verify_signature": False})
            exp = decoded.get('exp')
            if exp and datetime.fromtimestamp(exp) <= datetime.now():
                return False
            return True
        except:
            return False

    def refresh_auth(self) -> None:
        """No refresh mechanism for JWT"""
        pass

    def make_authenticated_request(self, method: str, url: str, **kwargs) -> requests.Response:
        """Make an authenticated request with JWT"""
        headers = kwargs.get('headers', {})
        headers[self.header_name] = f"{self.token_prefix} {self.jwt_token}"
        kwargs['headers'] = headers
        return requests.request(method, url, **kwargs)

class BasicAuthGateway(AuthGateway):
    """Basic authentication implementation"""
    
    def __init__(self, tool_name: str, tool_id: int, auth_config: Dict[str, Any]):
        super().__init__(tool_name, tool_id, auth_config)
        self.username = auth_config.get('username')
        self.password = auth_config.get('password')

    def _connect(self) -> Dict[str, Any]:
        """Connect using Basic Auth"""
        self.connection_status = 'connected'
        self.connected_at = datetime.now()
        return {
            "status": "connected",
            "message": "Successfully connected using Basic Auth"
        }

    def is_auth_valid(self) -> bool:
        """Check if Basic Auth credentials are valid"""
        return bool(self.username and self.password)

    def refresh_auth(self) -> None:
        """No refresh needed for Basic Auth"""
        pass

    def make_authenticated_request(self, method: str, url: str, **kwargs) -> requests.Response:
        """Make an authenticated request with Basic Auth"""
        kwargs['auth'] = (self.username, self.password)
        return requests.request(method, url, **kwargs)

class CustomHeaderGateway(AuthGateway):
    """Custom header authentication implementation"""
    
    def __init__(self, tool_name: str, tool_id: int, auth_config: Dict[str, Any]):
        super().__init__(tool_name, tool_id, auth_config)
        self.headers = auth_config

    def _connect(self) -> Dict[str, Any]:
        """Connect using Custom Headers"""
        self.connection_status = 'connected'
        self.connected_at = datetime.now()
        return {
            "status": "connected",
            "message": "Successfully connected using Custom Headers"
        }

    def is_auth_valid(self) -> bool:
        """Check if custom headers are valid"""
        return bool(self.headers)

    def refresh_auth(self) -> None:
        """No refresh needed for Custom Headers"""
        pass

    def make_authenticated_request(self, method: str, url: str, **kwargs) -> requests.Response:
        """Make an authenticated request with Custom Headers"""
        headers = kwargs.get('headers', {})
        headers.update(self.headers)
        kwargs['headers'] = headers
        return requests.request(method, url, **kwargs)

class AccessKeyGateway(AuthGateway):
    """AWS Access Key authentication implementation"""
    
    def __init__(self, tool_name: str, tool_id: int, auth_config: Dict[str, Any]):
        super().__init__(tool_name, tool_id, auth_config)
        self.access_key_id = auth_config.get('aws_access_key_id')
        self.secret_access_key = auth_config.get('aws_secret_access_key')

    def _connect(self) -> Dict[str, Any]:
        """Connect using AWS Access Key"""
        self.connection_status = 'connected'
        self.connected_at = datetime.now()
        return {
            "status": "connected",
            "message": "Successfully connected using AWS Access Key"
        }

    def is_auth_valid(self) -> bool:
        """Check if AWS credentials are valid"""
        return bool(self.access_key_id and self.secret_access_key)

    def refresh_auth(self) -> None:
        """No refresh needed for AWS Access Key"""
        pass

    def make_authenticated_request(self, method: str, url: str, **kwargs) -> requests.Response:
        """Make an authenticated request with AWS Access Key"""
        headers = kwargs.get('headers', {})
        headers['x-amz-access-key'] = self.access_key_id
        headers['x-amz-secret-key'] = self.secret_access_key
        kwargs['headers'] = headers
        return requests.request(method, url, **kwargs) 