"""Tests for in-memory tool manager."""

import pytest
from datetime import datetime
from mcps.tools.local.memory import InMemoryToolManager
from tests.mock_data.tools import MOCK_TOOL_METADATA, MOCK_TOOL_EXECUTIONS

@pytest.fixture
def tool_manager():
    """Create an InMemoryToolManager instance for testing."""
    return InMemoryToolManager()

@pytest.fixture
def mock_tools():
    """Create mock tool data for testing."""
    return {
        "metadata": MOCK_TOOL_METADATA,
        "executions": MOCK_TOOL_EXECUTIONS
    }

def test_tool_manager_initialization(tool_manager):
    """Test InMemoryToolManager initialization."""
    assert tool_manager is not None
    assert isinstance(tool_manager, InMemoryToolManager)
    assert tool_manager._tools == {}
    assert tool_manager._executions == {}

def test_register_tool(tool_manager, mock_tools):
    """Test tool registration."""
    tool_id = "tool1"
    metadata = mock_tools["metadata"][tool_id]
    
    # Create a simple handler function
    def handler(input_data, options=None):
        return {"result": f"processed {input_data['input']}"}
    
    tool_manager.register_tool(tool_id, metadata, handler)
    
    assert tool_id in tool_manager._tools
    assert tool_manager._tools[tool_id]["metadata"] == metadata
    assert callable(tool_manager._tools[tool_id]["handler"])

def test_unregister_tool(tool_manager, mock_tools):
    """Test tool unregistration."""
    tool_id = "tool1"
    metadata = mock_tools["metadata"][tool_id]
    
    def handler(input_data, options=None):
        return {"result": f"processed {input_data['input']}"}
    
    tool_manager.register_tool(tool_id, metadata, handler)
    tool_manager.unregister_tool(tool_id)
    
    assert tool_id not in tool_manager._tools

def test_execute_tool(tool_manager, mock_tools):
    """Test tool execution."""
    tool_id = "tool1"
    metadata = mock_tools["metadata"][tool_id]
    execution = mock_tools["executions"][tool_id]
    
    def handler(input_data, options=None):
        return {"result": f"processed {input_data['input']}"}
    
    tool_manager.register_tool(tool_id, metadata, handler)
    result = tool_manager.execute_tool(tool_id, execution["input"])
    
    assert result is not None
    assert result.status == "completed"
    assert result.duration_ms > 0
    assert result.output["result"] == f"processed {execution['input']['input']}"

def test_get_tool(tool_manager, mock_tools):
    """Test retrieving tool metadata."""
    tool_id = "tool1"
    metadata = mock_tools["metadata"][tool_id]
    
    def handler(input_data, options=None):
        return {"result": f"processed {input_data['input']}"}
    
    tool_manager.register_tool(tool_id, metadata, handler)
    tool = tool_manager.get_tool(tool_id)
    
    assert tool is not None
    assert tool.metadata == metadata
    assert callable(tool.handler)

def test_list_tools(tool_manager, mock_tools):
    """Test listing all registered tools."""
    # Register both tools
    for tool_id, metadata in mock_tools["metadata"].items():
        def handler(input_data, options=None):
            return {"result": f"processed {input_data['input']}"}
        tool_manager.register_tool(tool_id, metadata, handler)
    
    tools = tool_manager.list_tools()
    assert len(tools) == 2
    assert all(tool.metadata["id"] in mock_tools["metadata"] for tool in tools)

def test_execute_tool_with_error(tool_manager, mock_tools):
    """Test tool execution with error."""
    tool_id = "tool1"
    metadata = mock_tools["metadata"][tool_id]
    
    def handler(input_data, options=None):
        raise ValueError("Test error")
    
    tool_manager.register_tool(tool_id, metadata, handler)
    result = tool_manager.execute_tool(tool_id, {"input": "test"})
    
    assert result is not None
    assert result.status == "error"
    assert "Test error" in result.error
    assert result.duration_ms > 0

def test_execute_tool_with_invalid_input(tool_manager, mock_tools):
    """Test tool execution with invalid input."""
    tool_id = "tool1"
    metadata = mock_tools["metadata"][tool_id]
    
    def handler(input_data, options=None):
        return {"result": f"processed {input_data['input']}"}
    
    tool_manager.register_tool(tool_id, metadata, handler)
    result = tool_manager.execute_tool(tool_id, {})  # Missing required 'input' field
    
    assert result is not None
    assert result.status == "error"
    assert "input" in result.error.lower()

def test_execute_tool_with_options(tool_manager, mock_tools):
    """Test tool execution with options."""
    tool_id = "tool1"
    metadata = mock_tools["metadata"][tool_id]
    execution = mock_tools["executions"][tool_id]
    
    def handler(input_data, options=None):
        case_sensitive = options.get("case_sensitive", True)
        result = input_data["input"]
        if not case_sensitive:
            result = result.lower()
        return {"result": f"processed {result}"}
    
    tool_manager.register_tool(tool_id, metadata, handler)
    result = tool_manager.execute_tool(tool_id, execution["input"])
    
    assert result is not None
    assert result.status == "completed"
    assert result.output["result"] == f"processed {execution['input']['input']}" 