from abc import ABC, abstractmethod
from typing import Dict, Any

class AuthToken:
    """Authentication token class for transport layer"""
    def __init__(self, token: str, token_type: str = "Bearer"):
        self.token = token
        self.token_type = token_type

class Response:
    """Standard response class for transport layer"""
    def __init__(self, data: Dict[str, Any], status_code: int = 200):
        self.data = data
        self.status_code = status_code

class BaseTransport(ABC):
    """Base class for all transport implementations"""
    
    @abstractmethod
    def connect(self, endpoint: str, credentials: AuthToken) -> None:
        """Establish connection with the service endpoint
        
        Args:
            endpoint: Service endpoint URL
            credentials: Authentication credentials
        """
        pass
    
    @abstractmethod
    def send_request(self, payload: Dict[str, Any]) -> Response:
        """Send request and receive response
        
        Args:
            payload: Request payload as dictionary
            
        Returns:
            Response object containing the service response
        """
        pass
    
    @abstractmethod
    def close(self) -> None:
        """Release connection resources"""
        pass 