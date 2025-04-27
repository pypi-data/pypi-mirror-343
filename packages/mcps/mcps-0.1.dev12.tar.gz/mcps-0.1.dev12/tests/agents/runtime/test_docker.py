"""Tests for Docker sandbox runtime."""

import os
import pytest
import json
import tempfile
import shutil
from unittest.mock import MagicMock, patch
from datetime import datetime

from mcps.agents.runtime.base import RuntimeEnvironment, ExecutionSession
from mcps.agents.runtime.docker import DockerSandboxRuntime, DockerSandboxConfig

@pytest.fixture
def mock_docker():
    """Mock Docker client."""
    with patch('mcps.agents.runtime.docker.docker') as mock_docker:
        mock_container = MagicMock()
        mock_container.id = "test_container_id"
        mock_container.logs.return_value = b"Test output"
        mock_container.wait.return_value = {"StatusCode": 0}
        mock_container.attrs = {
            "State": {
                "StartedAt": "2023-01-01T00:00:00Z"
            }
        }
        
        mock_client = MagicMock()
        mock_client.containers.run.return_value = mock_container
        mock_docker.from_env.return_value = mock_client
        
        yield mock_docker

@pytest.fixture
def runtime_env():
    """Create runtime environment for testing."""
    return RuntimeEnvironment(
        container_type="docker",
        resources={
            "image": "python:3.9-slim",
            "memory": "256m",
            "cpu": 0.5
        },
        network_config={
            "disable": True
        },
        env_vars={
            "TEST_VAR": "test_value"
        }
    )

@pytest.fixture
def docker_runtime(runtime_env, mock_docker):
    """Create DockerSandboxRuntime instance for testing."""
    return DockerSandboxRuntime(runtime_env)

def test_deploy(docker_runtime, tmp_path, monkeypatch):
    """Test deploying agent package."""
    def mock_mkdtemp(prefix):
        os.makedirs(os.path.join(tmp_path, prefix), exist_ok=True)
        return os.path.join(tmp_path, prefix)
    
    monkeypatch.setattr('tempfile.mkdtemp', mock_mkdtemp)
    
    agent_package = {
        "code": "print('Hello, world!')",
        "dependencies": ["requests==2.28.1"]
    }
    
    deployment_id = docker_runtime.deploy(agent_package)
    
    assert deployment_id in docker_runtime.temp_dirs
    temp_dir = docker_runtime.temp_dirs[deployment_id]
    
    assert os.path.exists(os.path.join(temp_dir, "agent_code.py"))
    assert os.path.exists(os.path.join(temp_dir, "requirements.txt"))
    assert os.path.exists(os.path.join(temp_dir, "entrypoint.sh"))
    
    with open(os.path.join(temp_dir, "agent_code.py"), "r") as f:
        assert f.read() == agent_package["code"]
        
    with open(os.path.join(temp_dir, "requirements.txt"), "r") as f:
        assert f.read() == "requests==2.28.1"

def test_execute(docker_runtime, mock_docker):
    """Test executing agent task."""
    deployment_id = "test_deployment_id"
    docker_runtime.temp_dirs[deployment_id] = "/tmp/test_dir"
    
    session = ExecutionSession(
        session_id="test_session_id",
        agent_id=deployment_id,
        start_time=datetime.utcnow(),
        context={"test_key": "test_value"},
        tools=["test_tool"]
    )
    
    with patch('os.path.join', return_value="/tmp/test_dir/context.json"):
        with patch('builtins.open', MagicMock()):
            result = docker_runtime.execute(session)
    
    assert result.status == "success"
    assert mock_docker.from_env().containers.run.called
    
    container_config = mock_docker.from_env().containers.run.call_args[1]
    assert container_config["image"] == "python:3.9-slim"
    assert container_config["network_mode"] == "none"
    assert container_config["mem_limit"] == "256m"
    assert container_config["environment"] == {"TEST_VAR": "test_value"}

def test_execute_error(docker_runtime, mock_docker):
    """Test executing agent task with error."""
    deployment_id = "test_deployment_id"
    docker_runtime.temp_dirs[deployment_id] = "/tmp/test_dir"
    
    mock_docker.from_env().containers.run.return_value.wait.return_value = {"StatusCode": 1}
    
    session = ExecutionSession(
        session_id="test_session_id",
        agent_id=deployment_id,
        start_time=datetime.utcnow(),
        context={"test_key": "test_value"},
        tools=["test_tool"]
    )
    
    with patch('os.path.join', return_value="/tmp/test_dir/context.json"):
        with patch('builtins.open', MagicMock()):
            result = docker_runtime.execute(session)
    
    assert result.status == "error"
    assert result.error is not None

def test_snapshot(docker_runtime, mock_docker):
    """Test getting runtime state snapshot."""
    mock_container = mock_docker.from_env().containers.run.return_value
    mock_container.stats.return_value = {
        "cpu_stats": {
            "cpu_usage": {
                "total_usage": 1000000
            },
            "system_cpu_usage": 10000000
        },
        "memory_stats": {
            "usage": 1024 * 1024  # 1MB
        }
    }
    
    docker_runtime.containers["test_session_id"] = mock_container
    
    snapshot = docker_runtime.snapshot()
    
    assert snapshot.session_id == "all"
    assert "active_containers" in snapshot.state
    assert snapshot.state["active_containers"] == 1
    assert "container_ids" in snapshot.state
    assert "test_session_id" in snapshot.state["container_ids"]
    assert "total_cpu" in snapshot.metrics
    assert "total_memory" in snapshot.metrics
    assert isinstance(snapshot.metrics["total_cpu"], float)
    assert isinstance(snapshot.metrics["total_memory"], float)

def test_cleanup(docker_runtime, mock_docker):
    """Test cleaning up resources."""
    session_id = "test_session_id"
    docker_runtime.containers[session_id] = mock_docker.from_env().containers.run.return_value
    docker_runtime.temp_dirs[session_id] = "/tmp/test_dir"
    
    with patch('shutil.rmtree') as mock_rmtree:
        docker_runtime.cleanup(session_id)
    
    assert session_id not in docker_runtime.containers
    assert session_id not in docker_runtime.temp_dirs
    assert mock_rmtree.called
    assert mock_docker.from_env().containers.run.return_value.remove.called

def test_real_docker_container(monkeypatch):
    """Test creating and running a real Docker container.
    
    This test will be skipped if Docker is not available.
    """
    try:
        import docker
        client = docker.from_env()
        client.ping()  # Check Docker connection
    except (ImportError, Exception) as e:
        pytest.skip(f"Docker not available: {e}")
    
    temp_dir = tempfile.mkdtemp(prefix="mcps_docker_test_")
    
    try:
        agent_code = "print('Hello from Docker container!')"
        
        with open(os.path.join(temp_dir, "agent_code.py"), "w") as f:
            f.write(agent_code)
        
        with open(os.path.join(temp_dir, "requirements.txt"), "w") as f:
            f.write("")  # No dependencies
        
        with open(os.path.join(temp_dir, "entrypoint.sh"), "w") as f:
            f.write("""#!/bin/bash
set -e
python agent_code.py
""")
        os.chmod(os.path.join(temp_dir, "entrypoint.sh"), 0o755)
        
        with open(os.path.join(temp_dir, "context.json"), "w") as f:
            json.dump({"test_key": "test_value"}, f)
        
        env = RuntimeEnvironment(
            container_type="docker",
            resources={
                "image": "python:3.9-slim",  # Using confirmed available image
                "memory": "128m",
                "cpu": 0.2,
                "timeout": 10
            },
            network_config={
                "disable": True
            },
            env_vars={
                "TEST_ENV_VAR": "test_value"
            }
        )
        
        runtime = DockerSandboxRuntime(env)
        
        deployment_id = "test_real_deployment"
        runtime.temp_dirs[deployment_id] = temp_dir
        
        session = ExecutionSession(
            session_id="test_real_session",
            agent_id=deployment_id,
            start_time=datetime.utcnow(),
            context={"test_key": "test_value"},
            tools=[]
        )
        
        result = runtime.execute(session)
        
        assert result.status in ["success", "error"]
        assert "container_id" in result.metadata
        assert "exit_code" in result.metadata
        
    finally:
        try:
            if "session" in locals():
                runtime.cleanup(session.session_id)
            shutil.rmtree(temp_dir)
        except Exception as e:
            print(f"Cleanup error: {e}")
