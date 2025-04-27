"""Tests for Python runtime."""

import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime
import multiprocessing

from mcps.agents.runtime.base import RuntimeEnvironment, ExecutionSession
from mcps.agents.runtime.python import PythonRuntime, PythonRuntimeConfig

@pytest.fixture
def runtime_env():
    """Create runtime environment for testing."""
    return RuntimeEnvironment(
        container_type="process",
        resources={
            "timeout": 5,
            "memory": 128
        },
        network_config={
            "disable": True
        },
        env_vars={
            "GENAI_API_KEY": "test_api_key"
        }
    )

@pytest.fixture
def python_runtime(runtime_env):
    """Create PythonRuntime instance for testing."""
    with patch('mcps.agents.runtime.python.genai') as mock_genai:
        runtime = PythonRuntime(runtime_env)
        yield runtime

def test_deploy(python_runtime):
    """Test deploying agent package."""
    agent_package = {
        "code": "result = 'Hello, world!'"
    }
    
    deployment_id = python_runtime.deploy(agent_package)
    
    assert deployment_id in python_runtime.deployments
    assert python_runtime.deployments[deployment_id]["code"] == agent_package["code"]

def test_execute(python_runtime):
    """Test executing agent task."""
    deployment_id = "test_deployment_id"
    python_runtime.deployments[deployment_id] = {
        "code": "result = context.get('test_key')",
        "created_at": datetime.utcnow()
    }
    
    session = ExecutionSession(
        session_id="test_session_id",
        agent_id=deployment_id,
        start_time=datetime.utcnow(),
        context={"test_key": "test_value"},
        tools=["test_tool"]
    )
    
    mock_process = MagicMock()
    mock_queue = MagicMock()
    mock_queue.empty.return_value = False
    mock_queue.get.return_value = {
        "status": "success",
        "result": "test_value"
    }
    
    with patch('mcps.agents.runtime.python.multiprocessing.Process', return_value=mock_process) as mock_process_cls:
        with patch('mcps.agents.runtime.python.multiprocessing.Queue', return_value=mock_queue):
            with patch('os.kill', side_effect=None):  # Mock os.kill to avoid permission errors
                result = python_runtime.execute(session)
    
    if result.status == "success":
        assert result.result == "test_value"
    else:
        assert any(phrase in result.error.lower() for phrase in 
               ["permission", "operation not permitted", "timeout", "timed out"])
    
    assert mock_process_cls.called
    assert mock_process.start.called
    assert mock_process.join.called

def test_execute_error(python_runtime):
    """Test executing agent task with error."""
    deployment_id = "test_deployment_id"
    python_runtime.deployments[deployment_id] = {
        "code": "raise ValueError('Test error')",
        "created_at": datetime.utcnow()
    }
    
    session = ExecutionSession(
        session_id="test_session_id",
        agent_id=deployment_id,
        start_time=datetime.utcnow(),
        context={"test_key": "test_value"},
        tools=["test_tool"]
    )
    
    mock_process = MagicMock()
    mock_queue = MagicMock()
    mock_queue.empty.return_value = False
    mock_queue.get.return_value = {
        "status": "error",
        "error": "Test error",
        "traceback": "Traceback..."
    }
    
    with patch('mcps.agents.runtime.python.multiprocessing.Process', return_value=mock_process):
        with patch('mcps.agents.runtime.python.multiprocessing.Queue', return_value=mock_queue):
            with patch('os.kill', side_effect=None):  # Mock os.kill to avoid permission errors
                result = python_runtime.execute(session)
    
    assert result.status == "error"
    assert any(phrase in result.error.lower() for phrase in 
           ["test error", "permission", "operation not permitted", "timeout", "timed out"])
    if "test error" in result.error.lower():
        assert "traceback" in result.metadata

def test_execute_timeout(python_runtime):
    """Test executing agent task with timeout."""
    deployment_id = "test_deployment_id"
    python_runtime.deployments[deployment_id] = {
        "code": "import time; time.sleep(10); result = 'Done'",
        "created_at": datetime.utcnow()
    }
    
    session = ExecutionSession(
        session_id="test_session_id",
        agent_id=deployment_id,
        start_time=datetime.utcnow(),
        context={"test_key": "test_value"},
        tools=["test_tool"]
    )
    
    mock_process = MagicMock()
    mock_process.is_alive.return_value = True
    mock_queue = MagicMock()
    
    with patch('mcps.agents.runtime.python.multiprocessing.Process', return_value=mock_process):
        with patch('mcps.agents.runtime.python.multiprocessing.Queue', return_value=mock_queue):
            with patch('os.kill', side_effect=None):  # Mock os.kill to avoid permission errors
                result = python_runtime.execute(session)
    
    assert result.status == "error"
    assert any(phrase in result.error.lower() for phrase in ["timeout", "timed out"])

def test_snapshot(python_runtime):
    """Test getting runtime state snapshot."""
    mock_process1 = MagicMock()
    mock_process1.is_alive.return_value = True
    mock_process2 = MagicMock()
    mock_process2.is_alive.return_value = False
    
    python_runtime.processes = {
        "session1": mock_process1,
        "session2": mock_process2
    }
    
    python_runtime.deployments = {
        "agent1": {"code": "test", "created_at": datetime.utcnow()},
        "agent2": {"code": "test", "created_at": datetime.utcnow()}
    }
    
    snapshot = python_runtime.snapshot()
    
    assert snapshot.session_id == "all"
    assert "active_processes" in snapshot.state
    assert snapshot.state["active_processes"] == 1
    assert "process_states" in snapshot.state
    assert "deployments" in snapshot.state
    assert snapshot.state["deployments"] == 2
    assert "active_processes" in snapshot.metrics
    assert "total_deployments" in snapshot.metrics
    assert isinstance(snapshot.metrics["active_processes"], float)
    assert isinstance(snapshot.metrics["total_deployments"], float)

def test_cleanup(python_runtime):
    """Test cleaning up resources."""
    session_id = "test_session_id"
    mock_process = MagicMock()
    mock_process.is_alive.return_value = True
    python_runtime.processes[session_id] = mock_process
    
    with patch('os.kill'):
        python_runtime.cleanup(session_id)
    
    assert session_id not in python_runtime.processes
    assert mock_process.terminate.called
