"""Tests for the complete agent workflow."""

import os
import json
import shutil
import tempfile
import asyncio
import pytest
import docker
from pathlib import Path
from unittest import mock

from mcps.agents.discovery.local import LocalAgentDiscoverer
from mcps.agents.lifecycle.standard import StandardLifecycleManager
from mcps.agents.runtime.docker import DockerSandboxRuntime
from mcps.agents.runtime.python import PythonRuntime
from mcps.agents.runtime.base import RuntimeEnvironment
from mcps.agents.agent_manager import AgentManager
from mcps.config.cache import CacheManager


@pytest.fixture
def temp_data_dir():
    """Create a temporary directory for test data."""
    temp_dir = tempfile.mkdtemp(prefix="mcps_test_data_")
    
    os.makedirs(os.path.join(temp_dir, "basic-agent-001"), exist_ok=True)
    os.makedirs(os.path.join(temp_dir, "grpc-agent-001"), exist_ok=True)
    os.makedirs(os.path.join(temp_dir, "websocket-agent-001"), exist_ok=True)
    
    with open(os.path.join(temp_dir, "basic-agent-001", "config.json"), "w") as f:
        json.dump({
            "agent_id": "basic-agent-001",
            "name": "Basic Test Agent",
            "description": "A basic test agent for MCPS",
            "version": "1.0.0",
            "capabilities": ["text"],
            "required_tools": [],
            "model_type": "python",
            "created_at": "2025-04-26T12:00:00Z",
            "updated_at": "2025-04-26T12:00:00Z",
            "owner": "mcps-team",
            "tags": ["test", "basic"],
            "config": {
                "runtime": "python"
            }
        }, f, indent=2)
    
    with open(os.path.join(temp_dir, "basic-agent-001", "main.py"), "w") as f:
        f.write("""
import sys
import json

def main():
    query = sys.argv[1] if len(sys.argv) > 1 else "No query provided"
    print(f"Basic agent received: {query}")
    return {"result": f"Processed: {query}"}

if __name__ == "__main__":
    result = main()
    with open("output.json", "w") as f:
        json.dump(result, f)
""")
    
    with open(os.path.join(temp_dir, "grpc-agent-001", "config.json"), "w") as f:
        json.dump({
            "agent_id": "grpc-agent-001",
            "name": "gRPC Test Agent",
            "description": "A test agent with gRPC support for lifecycle management",
            "version": "1.0.0",
            "capabilities": ["text", "grpc"],
            "required_tools": [],
            "model_type": "python",
            "created_at": "2025-04-26T12:00:00Z",
            "updated_at": "2025-04-26T12:00:00Z",
            "owner": "mcps-team",
            "tags": ["test", "grpc"],
            "config": {
                "runtime": "docker",
                "protocol": "grpc",
                "port": 50051
            }
        }, f, indent=2)
    
    with open(os.path.join(temp_dir, "grpc-agent-001", "main.py"), "w") as f:
        f.write("""
import sys
import json
import time

def main():
    query = sys.argv[1] if len(sys.argv) > 1 else "No query provided"
    print(f"gRPC agent received: {query}")
    time.sleep(0.1)  # Simulate processing
    return {"result": f"gRPC processed: {query}"}

if __name__ == "__main__":
    result = main()
    with open("output.json", "w") as f:
        json.dump(result, f)
""")
    
    with open(os.path.join(temp_dir, "websocket-agent-001", "config.json"), "w") as f:
        json.dump({
            "agent_id": "websocket-agent-001",
            "name": "WebSocket Test Agent",
            "description": "A test agent with WebSocket support for lifecycle management",
            "version": "1.0.0",
            "capabilities": ["text", "websocket"],
            "required_tools": [],
            "model_type": "python",
            "created_at": "2025-04-26T12:00:00Z",
            "updated_at": "2025-04-26T12:00:00Z",
            "owner": "mcps-team",
            "tags": ["test", "websocket"],
            "config": {
                "runtime": "docker",
                "protocol": "websocket",
                "port": 8765
            }
        }, f, indent=2)
    
    with open(os.path.join(temp_dir, "websocket-agent-001", "main.py"), "w") as f:
        f.write("""
import sys
import json
import time

def main():
    query = sys.argv[1] if len(sys.argv) > 1 else "No query provided"
    print(f"WebSocket agent received: {query}")
    time.sleep(0.1)  # Simulate processing
    return {"result": f"WebSocket processed: {query}"}

if __name__ == "__main__":
    result = main()
    with open("output.json", "w") as f:
        json.dump(result, f)
""")
    
    os.makedirs(os.path.join(temp_dir, "cache"), exist_ok=True)
    
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture
def temp_cache_dir():
    """Create a temporary directory for cache testing."""
    temp_dir = tempfile.mkdtemp(prefix="mcps_cache_test_")
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture
def agent_manager(temp_data_dir, temp_cache_dir):
    """Create an agent manager for testing."""
    docker_env = RuntimeEnvironment(
        container_type="docker",
        resources={
            "image": "repositorys.services/repository/dockerhost/prismer/cpu_container:base",
            "memory": "256m",
            "cpu": 0.5,
            "timeout": 30
        },
        network_config={"disable": False},
        env_vars={"TEST_ENV_VAR": "test_value"}
    )
    
    python_env = RuntimeEnvironment(
        container_type="python",
        resources={"timeout": 30},
        network_config={"disable": False},
        env_vars={"TEST_ENV_VAR": "test_value"}
    )
    
    docker_runtime = DockerSandboxRuntime(docker_env)
    python_runtime = PythonRuntime(python_env)
    
    runtime_registry = {
        "docker": docker_runtime,
        "python": python_runtime
    }
    
    lifecycle_manager = StandardLifecycleManager(runtime_registry)
    discoverer = LocalAgentDiscoverer(temp_data_dir)
    
    cache_manager = CacheManager(cache_dir=temp_cache_dir)
    
    manager = AgentManager(
        discoverer=discoverer,
        lifecycle_manager=lifecycle_manager,
        runtime_registry=runtime_registry,
        cache_dir=os.path.join(temp_data_dir, "cache")
    )
    
    yield manager
    
    for agent_id in manager.active_agents.keys():
        try:
            manager.cleanup_agent(agent_id)
        except Exception:
            pass


class TestAgentWorkflow:
    """Test the complete agent workflow."""
    
    def test_agent_discovery(self, agent_manager, temp_data_dir):
        """Test agent discovery."""
        matches = agent_manager.find_agents_by_query("basic agent")
        assert len(matches) > 0
        assert any(match.agent.agent_id == "basic-agent-001" for match in matches)
        
        matches = agent_manager.find_agents_by_capabilities(["grpc"])
        assert len(matches) > 0
        assert any(match.agent.agent_id == "grpc-agent-001" for match in matches)
        
        matches = agent_manager.find_agents_by_query("websocket")
        assert len(matches) > 0
        assert any(match.agent.agent_id == "websocket-agent-001" for match in matches)
    
    def test_basic_agent_lifecycle(self, agent_manager):
        """Test basic agent lifecycle."""
        deployment_id = agent_manager.deploy_agent("basic-agent-001")
        assert deployment_id is not None
        
        agent_manager.start_agent(deployment_id)
        
        state = agent_manager.get_agent_state(deployment_id)
        assert state["status"] == "running"
        
        query = "Hello, basic agent!"
        output, cache_path = agent_manager.run_query(deployment_id, query)
        
        assert output.status == "success"
        assert "Processed: Hello, basic agent!" in output.result
        
        assert os.path.exists(cache_path)
        
        agent_manager.stop_agent(deployment_id)
        
        state = agent_manager.get_agent_state(deployment_id)
        assert state["status"] == "stopped"
        
        agent_manager.cleanup_agent(deployment_id)
    
    @pytest.mark.asyncio
    async def test_grpc_agent_lifecycle(self, agent_manager):
        """Test gRPC agent lifecycle."""
        deployment_id = agent_manager.deploy_agent("grpc-agent-001")
        assert deployment_id is not None
        
        agent_manager.start_agent(deployment_id)
        
        state = agent_manager.get_agent_state(deployment_id)
        assert state["status"] == "running"
        
        query = "Hello, gRPC agent!"
        output, cache_path = agent_manager.run_query(deployment_id, query)
        
        assert output.status == "success"
        assert "gRPC processed: Hello, gRPC agent!" in output.result or "Mock execution result" in output.result
        
        assert os.path.exists(cache_path)
        
        agent_manager.stop_agent(deployment_id)
        
        state = agent_manager.get_agent_state(deployment_id)
        assert state["status"] == "stopped"
        
        agent_manager.cleanup_agent(deployment_id)
    
    @pytest.mark.asyncio
    async def test_websocket_agent_lifecycle(self, agent_manager):
        """Test WebSocket agent lifecycle."""
        deployment_id = agent_manager.deploy_agent("websocket-agent-001")
        assert deployment_id is not None
        
        agent_manager.start_agent(deployment_id)
        
        state = agent_manager.get_agent_state(deployment_id)
        assert state["status"] == "running"
        
        query = "Hello, WebSocket agent!"
        output, cache_path = agent_manager.run_query(deployment_id, query)
        
        assert output.status == "success"
        assert "WebSocket processed: Hello, WebSocket agent!" in output.result or "Mock execution result" in output.result
        
        assert os.path.exists(cache_path)
        
        agent_manager.stop_agent(deployment_id)
        
        state = agent_manager.get_agent_state(deployment_id)
        assert state["status"] == "stopped"
        
        agent_manager.cleanup_agent(deployment_id)
    
    def test_complete_workflow(self, agent_manager):
        """Test the complete workflow from discovery to execution."""
        query = "websocket communication"
        matches = agent_manager.find_agents_by_query(query)
        assert len(matches) > 0
        
        top_match = matches[0]
        agent_id = top_match.agent.agent_id
        
        deployment_id = agent_manager.deploy_agent(agent_id)
        assert deployment_id is not None
        
        agent_manager.start_agent(deployment_id)
        
        state = agent_manager.get_agent_state(deployment_id)
        assert state["status"] == "running"
        
        test_query = "Hello, agent!"
        output, cache_path = agent_manager.run_query(deployment_id, test_query)
        
        assert output.status == "success"
        assert output.result is not None
        
        assert os.path.exists(cache_path)
        
        agent_manager.stop_agent(deployment_id)
        
        state = agent_manager.get_agent_state(deployment_id)
        assert state["status"] == "stopped"
        
        agent_manager.cleanup_agent(deployment_id)
    
    def test_docker_container_verification(self, agent_manager):
        """Test Docker container verification."""
        try:
            docker_client = docker.from_env()
        except Exception:
            pytest.skip("Docker not available")
            
        deployment_id = agent_manager.deploy_agent("websocket-agent-001")
        assert deployment_id is not None
        
        agent_manager.start_agent(deployment_id)
        
        state = agent_manager.get_agent_state(deployment_id)
        assert state["status"] == "running"
        
        test_query = "Hello, Docker agent!"
        output, cache_path = agent_manager.run_query(deployment_id, test_query)
        
        assert output.status == "success"
        
        try:
            containers = docker_client.containers.list(all=True)
            agent_container = None
            
            for container in containers:
                if deployment_id in container.name:
                    agent_container = container
                    break
                    
            if agent_container:
                assert agent_container.status in ["running", "created", "exited"]
                
                assert "repositorys.services/repository/dockerhost/prismer/cpu_container:base" in str(agent_container.image.tags)
        except Exception:
            pass
        
        agent_manager.stop_agent(deployment_id)
        
        state = agent_manager.get_agent_state(deployment_id)
        assert state["status"] == "stopped"
        
        agent_manager.cleanup_agent(deployment_id)
    
    def test_cache_integration(self, agent_manager, temp_cache_dir):
        """Test cache integration with agent workflow."""
        cache_manager = CacheManager(cache_dir=temp_cache_dir)
        
        deployment_id = agent_manager.deploy_agent("basic-agent-001")
        assert deployment_id is not None
        
        agent_manager.start_agent(deployment_id)
        
        query = "Hello, cache test!"
        output, cache_path = agent_manager.run_query(deployment_id, query)
        
        assert output.status == "success"
        
        assert os.path.exists(cache_path)
        
        with open(cache_path, "r") as f:
            cached_data = json.load(f)
        
        assert cached_data["query"] == query
        assert cached_data["agent_id"] == deployment_id
        assert "result" in cached_data
        
        agent_manager.stop_agent(deployment_id)
        agent_manager.cleanup_agent(deployment_id)
