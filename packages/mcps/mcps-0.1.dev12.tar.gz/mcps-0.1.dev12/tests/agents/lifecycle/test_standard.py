"""Tests for StandardLifecycleManager."""

import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta
import uuid
import time

from mcps.agents.lifecycle.base import AgentState, AgentConfig
from mcps.agents.lifecycle.standard import StandardLifecycleManager
from mcps.agents.runtime.base import AgentRuntime

@pytest.fixture
def mock_runtime():
    """Create mock runtime."""
    runtime = MagicMock(spec=AgentRuntime)
    runtime.deploy.return_value = "test-deployment-id"
    return runtime

@pytest.fixture
def runtime_registry(mock_runtime):
    """Create runtime registry with mock runtime."""
    return {"docker": mock_runtime, "python": mock_runtime}

@pytest.fixture
def lifecycle_manager(runtime_registry):
    """Create lifecycle manager with mock runtime registry."""
    return StandardLifecycleManager(runtime_registry)

@pytest.fixture
def sample_config():
    """Create sample agent configuration."""
    return AgentConfig(
        agent_id="test-agent",
        name="Test Agent",
        version="1.0.0",
        model_config={"code": "print('Hello, world!')"},
        resource_limits={"memory": "256m", "cpu": 0.5},
        environment={"container_type": "docker", "TEST_VAR": "test_value"},
        dependencies=["requests==2.28.1"],
        startup_timeout=30,
        shutdown_timeout=10
    )

def test_initialize(lifecycle_manager, sample_config, mock_runtime):
    """Test agent initialization."""
    agent_id = lifecycle_manager.initialize(sample_config)
    
    assert agent_id == "test-agent"
    assert mock_runtime.deploy.called
    
    state = lifecycle_manager.get_state(agent_id)
    assert state.agent_id == agent_id
    assert state.status == "initialized"

def test_initialize_generates_id(lifecycle_manager, sample_config, mock_runtime):
    """Test agent initialization with generated ID."""
    sample_config.agent_id = None
    
    with patch('uuid.uuid4', return_value=uuid.UUID('12345678-1234-5678-1234-567812345678')):
        agent_id = lifecycle_manager.initialize(sample_config)
    
    assert agent_id == "agent-12345678-1234-5678-1234-567812345678"
    assert mock_runtime.deploy.called
    
    state = lifecycle_manager.get_state(agent_id)
    assert state.agent_id == agent_id
    assert state.status == "initialized"

def test_start(lifecycle_manager, sample_config):
    """Test agent start."""
    agent_id = lifecycle_manager.initialize(sample_config)
    lifecycle_manager.start(agent_id)
    
    state = lifecycle_manager.get_state(agent_id)
    assert state.status == "running"

def test_stop(lifecycle_manager, sample_config):
    """Test agent stop."""
    agent_id = lifecycle_manager.initialize(sample_config)
    lifecycle_manager.start(agent_id)
    lifecycle_manager.stop(agent_id)
    
    state = lifecycle_manager.get_state(agent_id)
    assert state.status == "stopped"

def test_cleanup(lifecycle_manager, sample_config, mock_runtime):
    """Test agent cleanup."""
    agent_id = lifecycle_manager.initialize(sample_config)
    lifecycle_manager.cleanup(agent_id)
    
    assert mock_runtime.cleanup.called
    
    with pytest.raises(ValueError):
        lifecycle_manager.get_state(agent_id)

def test_get_state_nonexistent(lifecycle_manager):
    """Test getting state for nonexistent agent."""
    with pytest.raises(ValueError):
        lifecycle_manager.get_state("nonexistent-agent")

def test_update_config(lifecycle_manager, sample_config):
    """Test agent configuration update."""
    agent_id = lifecycle_manager.initialize(sample_config)
    
    updates = {
        "name": "Updated Agent",
        "version": "1.1.0"
    }
    
    updated_config = lifecycle_manager.update_config(agent_id, updates)
    
    assert updated_config.name == "Updated Agent"
    assert updated_config.version == "1.1.0"
    assert updated_config.dependencies == sample_config.dependencies

def test_list_agents(lifecycle_manager, sample_config):
    """Test listing agents."""
    agent1_id = lifecycle_manager.initialize(sample_config)
    
    sample_config.agent_id = "test-agent-2"
    agent2_id = lifecycle_manager.initialize(sample_config)
    
    lifecycle_manager.start(agent1_id)
    
    all_agents = lifecycle_manager.list_agents()
    assert len(all_agents) == 2
    
    running_agents = lifecycle_manager.list_agents(status="running")
    assert len(running_agents) == 1
    assert running_agents[0].agent_id == agent1_id
    
    initialized_agents = lifecycle_manager.list_agents(status="initialized")
    assert len(initialized_agents) == 1
    assert initialized_agents[0].agent_id == agent2_id

def test_register_heartbeat(lifecycle_manager, sample_config):
    """Test agent heartbeat registration."""
    agent_id = lifecycle_manager.initialize(sample_config)
    
    state_before = lifecycle_manager.get_state(agent_id)
    initial_heartbeat = state_before.last_heartbeat
    
    time.sleep(0.1)
    
    metadata = {
        "key": "value",
        "resource_usage": {"cpu": 0.7, "memory": 300}
    }
    lifecycle_manager.register_heartbeat(agent_id, metadata)
    
    state_after = lifecycle_manager.get_state(agent_id)
    assert state_after.last_heartbeat > initial_heartbeat
    assert state_after.metadata["key"] == "value"
    assert state_after.resource_usage["cpu"] == 0.7
    assert state_after.resource_usage["memory"] == 300

def test_register_heartbeat_nonexistent(lifecycle_manager):
    """Test registering heartbeat for nonexistent agent."""
    with pytest.raises(ValueError):
        lifecycle_manager.register_heartbeat("nonexistent-agent")

def test_start_nonexistent(lifecycle_manager):
    """Test starting nonexistent agent."""
    with pytest.raises(ValueError):
        lifecycle_manager.start("nonexistent-agent")

def test_stop_nonexistent(lifecycle_manager):
    """Test stopping nonexistent agent."""
    with pytest.raises(ValueError):
        lifecycle_manager.stop("nonexistent-agent")

def test_cleanup_nonexistent(lifecycle_manager):
    """Test cleaning up nonexistent agent."""
    with pytest.raises(ValueError):
        lifecycle_manager.cleanup("nonexistent-agent")

def test_update_config_nonexistent(lifecycle_manager):
    """Test updating config for nonexistent agent."""
    with pytest.raises(ValueError):
        lifecycle_manager.update_config("nonexistent-agent", {"name": "Updated"})
