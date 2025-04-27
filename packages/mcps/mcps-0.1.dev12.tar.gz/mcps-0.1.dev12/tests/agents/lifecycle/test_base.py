"""Tests for agent lifecycle base classes."""

import pytest
from datetime import datetime
from mcps.agents.lifecycle.base import AgentState, AgentConfig
from mcps.agents.runtime.base import RuntimeEnvironment

def test_agent_state_initialization():
    """Test AgentState initialization."""
    state = AgentState(
        agent_id="test-agent",
        status="running",
        current_task="test-task",
        last_heartbeat=datetime.utcnow(),
        resource_usage={"cpu": 0.5, "memory": 256},
        metadata={"key": "value"}
    )
    
    assert state.agent_id == "test-agent"
    assert state.status == "running"
    assert state.current_task == "test-task"
    assert isinstance(state.last_heartbeat, datetime)
    assert state.resource_usage == {"cpu": 0.5, "memory": 256}
    assert state.metadata == {"key": "value"}

def test_agent_config_initialization():
    """Test AgentConfig initialization."""
    config = AgentConfig(
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
    
    assert config.agent_id == "test-agent"
    assert config.name == "Test Agent"
    assert config.version == "1.0.0"
    assert config.model_config == {"code": "print('Hello, world!')"}
    assert config.resource_limits == {"memory": "256m", "cpu": 0.5}
    assert config.environment == {"container_type": "docker", "TEST_VAR": "test_value"}
    assert config.dependencies == ["requests==2.28.1"]
    assert config.startup_timeout == 30
    assert config.shutdown_timeout == 10
