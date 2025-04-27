from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class Credentials:
    """Base credentials class"""
    api_key: str
    token_type: str = "Bearer"
    expires_at: Optional[datetime] = None
    
    def is_expired(self) -> bool:
        """Check if credentials are expired
        
        Returns:
            True if credentials are expired, False otherwise
        """
        if not self.expires_at:
            return False
        return datetime.now() >= self.expires_at

@dataclass
class User:
    """User information"""
    user_id: str
    username: str
    email: str
    roles: list[str]
    permissions: list[str]
    created_at: datetime
    last_login: datetime

class AuthProvider(ABC):
    """Base class for authentication providers"""
    
    @abstractmethod
    def authenticate(self, credentials: Credentials) -> User:
        """Authenticate user with credentials
        
        Args:
            credentials: User credentials
            
        Returns:
            Authenticated user information
        """
        pass
    
    @abstractmethod
    def validate_token(self, token: str) -> bool:
        """Validate authentication token
        
        Args:
            token: Authentication token to validate
            
        Returns:
            True if token is valid, False otherwise
        """
        pass
    
    @abstractmethod
    def refresh_token(self, token: str) -> Credentials:
        """Refresh authentication token
        
        Args:
            token: Current authentication token
            
        Returns:
            New credentials with refreshed token
        """
        pass
    
    @abstractmethod
    def revoke_token(self, token: str) -> None:
        """Revoke authentication token
        
        Args:
            token: Token to revoke
        """
        pass

class AuthManager:
    """Authentication manager for handling credentials and tokens"""
    
    def __init__(self, provider: AuthProvider):
        self.provider = provider
        self._current_credentials: Optional[Credentials] = None
        self._current_user: Optional[User] = None
    
    def login(self, api_key: str) -> User:
        """Login with API key
        
        Args:
            api_key: API key for authentication
            
        Returns:
            Authenticated user information
        """
        credentials = Credentials(api_key=api_key)
        user = self.provider.authenticate(credentials)
        
        self._current_credentials = credentials
        self._current_user = user
        return user
    
    def logout(self) -> None:
        """Logout current user"""
        if self._current_credentials:
            self.provider.revoke_token(self._current_credentials.api_key)
            self._current_credentials = None
            self._current_user = None
    
    def get_current_user(self) -> Optional[User]:
        """Get current authenticated user
        
        Returns:
            Current user if authenticated, None otherwise
        """
        return self._current_user
    
    def get_credentials(self) -> Optional[Credentials]:
        """Get current credentials
        
        Returns:
            Current credentials if authenticated, None otherwise
        """
        return self._current_credentials
    
    def refresh_credentials(self) -> Credentials:
        """Refresh current credentials
        
        Returns:
            New credentials with refreshed token
        """
        if not self._current_credentials:
            raise RuntimeError("No credentials to refresh")
            
        new_credentials = self.provider.refresh_token(self._current_credentials.api_key)
        self._current_credentials = new_credentials
        return new_credentials 