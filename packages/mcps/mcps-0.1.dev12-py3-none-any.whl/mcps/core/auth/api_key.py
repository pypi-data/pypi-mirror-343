"""API Key authentication provider for MCPS."""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from ..transports.base import AuthToken
from .base import AuthProvider, Credentials, User

class APIKeyAuthProvider(AuthProvider):
    """API Key-based authentication provider."""

    def __init__(self, api_keys: Optional[Dict[str, str]] = None):
        """Initialize the API Key provider.
        
        Args:
            api_keys: Optional dictionary mapping API keys to user IDs
        """
        self._api_keys = api_keys or {}

    def authenticate(self, credentials: Credentials) -> Optional[AuthToken]:
        """Authenticate using API key credentials.
        
        Args:
            credentials: Credentials containing the API key
            
        Returns:
            AuthToken if authentication successful, None otherwise
        """
        api_key = credentials.get("api_key")
        if not api_key or api_key not in self._api_keys:
            return None
            
        user_id = self._api_keys[api_key]
        return AuthToken(
            token=api_key,
            user_id=user_id,
            token_type="Bearer",
            expires_in=None  # API keys don't expire
        )

    def validate_token(self, token: AuthToken) -> bool:
        """Validate an API key token.
        
        Args:
            token: The token to validate
            
        Returns:
            True if token is valid, False otherwise
        """
        return token.token in self._api_keys

    def get_user(self, token: AuthToken) -> Optional[User]:
        """Get user information from an API key token.
        
        Args:
            token: The token containing user information
            
        Returns:
            User if token is valid, None otherwise
        """
        if not self.validate_token(token):
            return None
            
        user_id = self._api_keys[token.token]
        return User(
            id=user_id,
            username=user_id,  # Use user ID as username for API keys
            roles=["api_user"]  # Default role for API key users
        )

    def register_api_key(self, api_key: str, user_id: str) -> None:
        """Register a new API key.
        
        Args:
            api_key: The API key to register
            user_id: The user ID associated with the API key
        """
        self._api_keys[api_key] = user_id

    def revoke_api_key(self, api_key: str) -> bool:
        """Revoke an API key.
        
        Args:
            api_key: The API key to revoke
            
        Returns:
            True if key was revoked, False if key didn't exist
        """
        if api_key in self._api_keys:
            del self._api_keys[api_key]
            return True
        return False

    def list_api_keys(self) -> Dict[str, str]:
        """List all registered API keys.
        
        Returns:
            Dictionary mapping API keys to user IDs
        """
        return self._api_keys.copy() 