from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Type, TypeVar, Generic, List
from dataclasses import dataclass
from datetime import datetime

# Crypto base classes
class CryptoProvider(ABC):
    """Base class for cryptographic operations"""
    
    @abstractmethod
    def encrypt(self, data: bytes, key: Optional[bytes] = None) -> bytes:
        """Encrypt data
        
        Args:
            data: Data to encrypt
            key: Optional encryption key
            
        Returns:
            Encrypted data
        """
        pass
    
    @abstractmethod
    def decrypt(self, data: bytes, key: Optional[bytes] = None) -> bytes:
        """Decrypt data
        
        Args:
            data: Data to decrypt
            key: Optional decryption key
            
        Returns:
            Decrypted data
        """
        pass
    
    @abstractmethod
    def generate_key(self, key_type: str = "aes") -> bytes:
        """Generate a new encryption key
        
        Args:
            key_type: Type of key to generate
            
        Returns:
            Generated key
        """
        pass

# Schema base classes
T = TypeVar('T')

class SchemaValidator(Generic[T]):
    """Base class for schema validation"""
    
    @abstractmethod
    def validate(self, data: Dict[str, Any], schema: Type[T]) -> T:
        """Validate data against schema
        
        Args:
            data: Data to validate
            schema: Schema type to validate against
            
        Returns:
            Validated and typed data
        """
        pass
    
    @abstractmethod
    def is_valid(self, data: Dict[str, Any], schema: Type[T]) -> bool:
        """Check if data is valid against schema
        
        Args:
            data: Data to check
            schema: Schema type to check against
            
        Returns:
            True if data is valid
        """
        pass

# State management base classes
class StateManager(ABC):
    """Base class for state management"""
    
    @abstractmethod
    def get_state(self, key: str, default: Any = None) -> Any:
        """Get state value
        
        Args:
            key: State key
            default: Default value if key not found
            
        Returns:
            State value
        """
        pass
    
    @abstractmethod
    def set_state(self, key: str, value: Any) -> None:
        """Set state value
        
        Args:
            key: State key
            value: State value
        """
        pass
    
    @abstractmethod
    def delete_state(self, key: str) -> None:
        """Delete state value
        
        Args:
            key: State key to delete
        """
        pass
    
    @abstractmethod
    def list_keys(self, pattern: Optional[str] = None) -> List[str]:
        """List state keys
        
        Args:
            pattern: Optional pattern to filter keys
            
        Returns:
            List of matching keys
        """
        pass
    
    @abstractmethod
    def clear_state(self) -> None:
        """Clear all state"""
        pass

@dataclass
class StateMetadata:
    """State metadata information"""
    key: str
    value_type: str
    created_at: datetime
    updated_at: datetime
    size: int
    tags: Dict[str, str] 