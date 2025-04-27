from typing import Dict, Any, List, Optional
import requests
from datetime import datetime
from ...core.transports.base import AuthToken
from ..base import RemoteToolManager, ToolMetadata, ToolExecutionResult

class HTTPToolManager(RemoteToolManager):
    """HTTP-based implementation of remote tool management"""
    
    def __init__(self, base_url: str, auth_token: Optional[AuthToken] = None):
        self.base_url = base_url.rstrip('/')
        self.auth_token = auth_token
        self._session = requests.Session()
        if auth_token:
            self._session.headers.update({
                'Authorization': f"{auth_token.token_type} {auth_token.token}"
            })
    
    def connect(self, endpoint: str, credentials: Dict[str, Any]) -> None:
        """Connect to remote tool service
        
        Args:
            endpoint: Remote service endpoint
            credentials: Authentication credentials
        """
        self.base_url = endpoint.rstrip('/')
        if 'token' in credentials:
            self.auth_token = AuthToken(
                token=credentials['token'],
                token_type=credentials.get('token_type', 'Bearer')
            )
            self._session.headers.update({
                'Authorization': f"{self.auth_token.token_type} {self.auth_token.token}"
            })
    
    def invoke_tool(self, tool_id: str, params: Dict[str, Any]) -> ToolExecutionResult:
        """Invoke a remote tool
        
        Args:
            tool_id: Tool identifier
            params: Tool parameters
            
        Returns:
            Tool execution result
        """
        url = f"{self.base_url}/tools/{tool_id}/invoke"
        start_time = datetime.now()
        
        try:
            response = self._session.post(url, json=params)
            response.raise_for_status()
            execution_time = (datetime.now() - start_time).total_seconds()
            
            result = response.json()
            return ToolExecutionResult(
                success=True,
                result=result.get('result'),
                execution_time=execution_time,
                metadata=result.get('metadata')
            )
        except requests.exceptions.RequestException as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            
            return ToolExecutionResult(
                success=False,
                result=None,
                error=str(e),
                execution_time=execution_time
            )
    
    def get_available_tools(self) -> List[ToolMetadata]:
        """Get list of available remote tools
        
        Returns:
            List of available tool metadata
        """
        url = f"{self.base_url}/tools"
        
        try:
            response = self._session.get(url)
            response.raise_for_status()
            
            tools_data = response.json()
            return [
                ToolMetadata(
                    tool_id=tool['tool_id'],
                    name=tool['name'],
                    description=tool['description'],
                    version=tool['version'],
                    category=tool['category'],
                    input_schema=tool['input_schema'],
                    output_schema=tool['output_schema'],
                    required_permissions=tool['required_permissions'],
                    created_at=datetime.fromisoformat(tool['created_at']),
                    updated_at=datetime.fromisoformat(tool['updated_at'])
                )
                for tool in tools_data
            ]
        except requests.exceptions.RequestException:
            return []
    
    def validate_tool(self, tool_id: str, params: Dict[str, Any]) -> bool:
        """Validate tool parameters
        
        Args:
            tool_id: Tool identifier
            params: Tool parameters to validate
            
        Returns:
            True if parameters are valid
        """
        url = f"{self.base_url}/tools/{tool_id}/validate"
        
        try:
            response = self._session.post(url, json=params)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False 