from typing import Optional
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from ..base import CryptoProvider

class AESCryptoProvider(CryptoProvider):
    """AES-based implementation of cryptographic operations"""
    
    def __init__(self, key: Optional[bytes] = None, key_size: int = 32):
        """Initialize AES crypto provider
        
        Args:
            key: Optional encryption key (must be 16, 24, or 32 bytes)
            key_size: Key size in bytes (16, 24, or 32)
        """
        if key is None:
            key = os.urandom(key_size)
        elif len(key) not in (16, 24, 32):
            raise ValueError("Key must be 16, 24, or 32 bytes")
            
        self.key = key
        self.key_size = len(key)
    
    def encrypt(self, data: bytes, key: Optional[bytes] = None) -> bytes:
        """Encrypt data using AES
        
        Args:
            data: Data to encrypt
            key: Optional encryption key
            
        Returns:
            Encrypted data
        """
        key = key or self.key
        
        # Generate random IV
        iv = os.urandom(16)
        
        # Create cipher
        cipher = Cipher(
            algorithms.AES(key),
            modes.CBC(iv),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()
        
        # Pad data
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(data) + padder.finalize()
        
        # Encrypt
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
        
        # Combine IV and encrypted data
        return iv + encrypted_data
    
    def decrypt(self, data: bytes, key: Optional[bytes] = None) -> bytes:
        """Decrypt data using AES
        
        Args:
            data: Data to decrypt
            key: Optional decryption key
            
        Returns:
            Decrypted data
        """
        key = key or self.key
        
        # Extract IV
        iv = data[:16]
        encrypted_data = data[16:]
        
        # Create cipher
        cipher = Cipher(
            algorithms.AES(key),
            modes.CBC(iv),
            backend=default_backend()
        )
        decryptor = cipher.decryptor()
        
        # Decrypt
        padded_data = decryptor.update(encrypted_data) + decryptor.finalize()
        
        # Unpad
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        return unpadder.update(padded_data) + unpadder.finalize()
    
    def generate_key(self, key_type: str = "aes") -> bytes:
        """Generate a new encryption key
        
        Args:
            key_type: Type of key to generate (only "aes" supported)
            
        Returns:
            Generated key
        """
        if key_type.lower() != "aes":
            raise ValueError("Only AES keys are supported")
            
        return os.urandom(self.key_size) 