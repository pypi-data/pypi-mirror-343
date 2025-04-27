from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass
from datetime import datetime

@dataclass
class ToolMetadata:
    """Tool metadata information"""
    tool_id: str
    name: str
    description: str
    version: str
    category: str
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]
    required_permissions: List[str]
    created_at: datetime
    updated_at: datetime

@dataclass
class ToolExecutionResult:
    """Tool execution result"""
    success: bool
    result: Any
    error: Optional[str] = None
    execution_time: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None

class LocalToolManager(ABC):
    """Base class for local tool management"""
    
    @abstractmethod
    def register_tool(self, tool_id: str, tool_config: Dict[str, Any]) -> ToolMetadata:
        """Register a new local tool
        
        Args:
            tool_id: Tool identifier
            tool_config: Tool configuration
            
        Returns:
            Tool metadata
        """
        pass
    
    @abstractmethod
    def execute_tool(self, tool_id: str, params: Dict[str, Any]) -> ToolExecutionResult:
        """Execute a local tool
        
        Args:
            tool_id: Tool identifier
            params: Tool parameters
            
        Returns:
            Tool execution result
        """
        pass
    
    @abstractmethod
    def unregister_tool(self, tool_id: str) -> None:
        """Unregister a local tool
        
        Args:
            tool_id: Tool identifier
        """
        pass
    
    @abstractmethod
    def get_tool(self, tool_id: str) -> Optional[ToolMetadata]:
        """Get tool metadata
        
        Args:
            tool_id: Tool identifier
            
        Returns:
            Tool metadata if found
        """
        pass
    
    @abstractmethod
    def list_tools(self, category: Optional[str] = None) -> List[ToolMetadata]:
        """List registered tools
        
        Args:
            category: Optional category filter
            
        Returns:
            List of tool metadata
        """
        pass

class RemoteToolManager(ABC):
    """Base class for remote tool integration"""
    
    @abstractmethod
    def connect(self, endpoint: str, credentials: Dict[str, Any]) -> None:
        """Connect to remote tool service
        
        Args:
            endpoint: Remote service endpoint
            credentials: Authentication credentials
        """
        pass
    
    @abstractmethod
    def invoke_tool(self, tool_id: str, params: Dict[str, Any]) -> ToolExecutionResult:
        """Invoke a remote tool
        
        Args:
            tool_id: Tool identifier
            params: Tool parameters
            
        Returns:
            Tool execution result
        """
        pass
    
    @abstractmethod
    def get_available_tools(self) -> List[ToolMetadata]:
        """Get list of available remote tools
        
        Returns:
            List of available tool metadata
        """
        pass
    
    @abstractmethod
    def validate_tool(self, tool_id: str, params: Dict[str, Any]) -> bool:
        """Validate tool parameters
        
        Args:
            tool_id: Tool identifier
            params: Tool parameters to validate
            
        Returns:
            True if parameters are valid
        """
        pass 