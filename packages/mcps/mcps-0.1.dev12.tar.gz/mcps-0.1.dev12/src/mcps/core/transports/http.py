import requests
from typing import Dict, Any, Optional
from .base import BaseTransport, AuthToken, Response

class HTTPTransport(BaseTransport):
    """HTTP transport implementation using requests library"""
    
    def __init__(self, base_url: str, timeout: int = 30):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session: Optional[requests.Session] = None
        self._auth_token: Optional[AuthToken] = None
    
    def connect(self, endpoint: str, credentials: AuthToken) -> None:
        """Establish HTTP connection with authentication
        
        Args:
            endpoint: Service endpoint URL
            credentials: Authentication credentials
        """
        self.session = requests.Session()
        self._auth_token = credentials
        
        # Set default headers
        self.session.headers.update({
            'Authorization': f"{credentials.token_type} {credentials.token}",
            'Content-Type': 'application/json'
        })
        
        # Test connection
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=self.timeout)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Failed to connect to {endpoint}: {str(e)}")
    
    def send_request(self, payload: Dict[str, Any]) -> Response:
        """Send HTTP request and receive response
        
        Args:
            payload: Request payload as dictionary
            
        Returns:
            Response object containing the service response
        """
        if not self.session:
            raise RuntimeError("Transport not connected. Call connect() first.")
        
        try:
            response = self.session.post(
                f"{self.base_url}/api/v1/invoke",
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            return Response(
                data=response.json(),
                status_code=response.status_code
            )
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Request failed: {str(e)}")
    
    def close(self) -> None:
        """Close HTTP session and release resources"""
        if self.session:
            self.session.close()
            self.session = None
            self._auth_token = None 