from typing import Dict, Any, List, Optional, Callable
from datetime import datetime
from ..base import LocalToolManager, ToolMetadata, ToolExecutionResult

class InMemoryToolManager(LocalToolManager):
    """In-memory implementation of local tool management"""
    
    def __init__(self):
        self._tools: Dict[str, ToolMetadata] = {}
        self._handlers: Dict[str, Callable] = {}
    
    def register_tool(self, tool_id: str, tool_config: Dict[str, Any]) -> ToolMetadata:
        """Register a new local tool
        
        Args:
            tool_id: Tool identifier
            tool_config: Tool configuration
            
        Returns:
            Tool metadata
        """
        if tool_id in self._tools:
            raise ValueError(f"Tool {tool_id} already registered")
            
        # Extract handler from config
        handler = tool_config.pop("handler", None)
        if not handler or not callable(handler):
            raise ValueError("Tool handler must be a callable")
            
        # Create metadata
        metadata = ToolMetadata(
            tool_id=tool_id,
            name=tool_config.get("name", tool_id),
            description=tool_config.get("description", ""),
            version=tool_config.get("version", "1.0.0"),
            category=tool_config.get("category", "general"),
            input_schema=tool_config.get("input_schema", {}),
            output_schema=tool_config.get("output_schema", {}),
            required_permissions=tool_config.get("required_permissions", []),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        # Store tool and handler
        self._tools[tool_id] = metadata
        self._handlers[tool_id] = handler
        
        return metadata
    
    def execute_tool(self, tool_id: str, params: Dict[str, Any]) -> ToolExecutionResult:
        """Execute a local tool
        
        Args:
            tool_id: Tool identifier
            params: Tool parameters
            
        Returns:
            Tool execution result
        """
        if tool_id not in self._tools:
            return ToolExecutionResult(
                success=False,
                result=None,
                error=f"Tool {tool_id} not found"
            )
            
        handler = self._handlers[tool_id]
        start_time = datetime.now()
        
        try:
            result = handler(**params)
            execution_time = (datetime.now() - start_time).total_seconds()
            
            return ToolExecutionResult(
                success=True,
                result=result,
                execution_time=execution_time
            )
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            
            return ToolExecutionResult(
                success=False,
                result=None,
                error=str(e),
                execution_time=execution_time
            )
    
    def unregister_tool(self, tool_id: str) -> None:
        """Unregister a local tool
        
        Args:
            tool_id: Tool identifier
        """
        if tool_id in self._tools:
            del self._tools[tool_id]
            del self._handlers[tool_id]
    
    def get_tool(self, tool_id: str) -> Optional[ToolMetadata]:
        """Get tool metadata
        
        Args:
            tool_id: Tool identifier
            
        Returns:
            Tool metadata if found
        """
        return self._tools.get(tool_id)
    
    def list_tools(self, category: Optional[str] = None) -> List[ToolMetadata]:
        """List registered tools
        
        Args:
            category: Optional category filter
            
        Returns:
            List of tool metadata
        """
        tools = self._tools.values()
        if category:
            tools = [t for t in tools if t.category == category]
        return list(tools) 