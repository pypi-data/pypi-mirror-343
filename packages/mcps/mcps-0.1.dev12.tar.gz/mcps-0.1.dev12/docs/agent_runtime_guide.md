# MCPS Agent Runtime Guide

## Overview

The MCPS Agent Runtime system provides a comprehensive framework for managing the complete lifecycle of intelligent agents, from discovery to execution and termination. This guide explains the core components, workflows, and best practices for working with the MCPS agent runtime.

## Core Components

### 1. Agent Discovery

The agent discovery system allows finding agents based on natural language queries or specific capabilities:

```python
from mcps.agents.discovery.local import LocalAgentDiscoverer

# Initialize with a directory containing agent packages
discoverer = LocalAgentDiscoverer("/path/to/agents")

# Find agents by natural language query
matches = discoverer.find_by_query("weather forecast")

# Find agents by specific capabilities
matches = discoverer.find_by_capabilities(["text", "websocket"])
```

Agent packages must include:
- `main.py`: The main agent implementation
- `config.json`: Agent metadata and configuration
- Additional resources like prompt templates

### 2. Agent Lifecycle Management

The lifecycle manager handles agent deployment, initialization, execution, and termination:

```python
from mcps.agents.lifecycle.standard import StandardLifecycleManager
from mcps.agents.runtime.docker import DockerSandboxRuntime
from mcps.agents.runtime.python import PythonRuntime
from mcps.agents.runtime.base import RuntimeEnvironment

# Create runtime environments
docker_env = RuntimeEnvironment(
    container_type="docker",
    resources={
        "image": "repositorys.services/repository/dockerhost/prismer/cpu_container:base",
        "memory": "256m",
        "cpu": 0.5,
        "timeout": 30
    }
)

python_env = RuntimeEnvironment(
    container_type="python",
    resources={"timeout": 30}
)

# Initialize runtimes
docker_runtime = DockerSandboxRuntime(docker_env)
python_runtime = PythonRuntime(python_env)

# Register runtimes
runtime_registry = {
    "docker": docker_runtime,
    "python": python_runtime
}

# Create lifecycle manager
lifecycle_manager = StandardLifecycleManager(runtime_registry)

# Deploy and manage agents
deployment_id = lifecycle_manager.deploy("agent-001", "/path/to/agent/package")
lifecycle_manager.start(deployment_id)
lifecycle_manager.execute(deployment_id, "Hello, agent!")
lifecycle_manager.stop(deployment_id)
lifecycle_manager.cleanup(deployment_id)
```

### 3. Runtime Environments

MCPS supports multiple runtime environments:

#### Python Runtime

Executes agents directly in the Python interpreter:

```python
from mcps.agents.runtime.python import PythonRuntime
from mcps.agents.runtime.base import RuntimeEnvironment

env = RuntimeEnvironment(
    container_type="python",
    resources={"timeout": 30},
    network_config={"disable": False},
    env_vars={"API_KEY": "your-api-key"}
)

runtime = PythonRuntime(env)
```

#### Docker Runtime

Executes agents in isolated Docker containers:

```python
from mcps.agents.runtime.docker import DockerSandboxRuntime
from mcps.agents.runtime.base import RuntimeEnvironment

env = RuntimeEnvironment(
    container_type="docker",
    resources={
        "image": "repositorys.services/repository/dockerhost/prismer/cpu_container:base",
        "memory": "256m",
        "cpu": 0.5,
        "timeout": 30
    },
    network_config={"disable": False},
    env_vars={"API_KEY": "your-api-key"}
)

runtime = DockerSandboxRuntime(env)
```

### 4. Agent Manager

The high-level interface for working with agents:

```python
from mcps.agents.agent_manager import AgentManager
from mcps.agents.discovery.local import LocalAgentDiscoverer
from mcps.agents.lifecycle.standard import StandardLifecycleManager

# Initialize components
discoverer = LocalAgentDiscoverer("/path/to/agents")
lifecycle_manager = StandardLifecycleManager(runtime_registry)

# Create agent manager
manager = AgentManager(
    discoverer=discoverer,
    lifecycle_manager=lifecycle_manager,
    runtime_registry=runtime_registry,
    cache_dir="/path/to/cache"
)

# Find agents
matches = manager.find_agents_by_query("weather forecast")

# Deploy and run agents
deployment_id = manager.deploy_agent("agent-001")
manager.start_agent(deployment_id)
output, cache_path = manager.run_query(deployment_id, "What's the weather in New York?")
manager.stop_agent(deployment_id)
manager.cleanup_agent(deployment_id)
```

## Global Cache Strategy

MCPS implements a comprehensive caching system for efficient agent management:

```python
from mcps.config.cache import CacheManager
from mcps.utils.cache import MessageCache, LogCache

# Initialize cache manager
cache_manager = CacheManager(cache_dir="~/.mcps")

# Cache directories
config_dir = cache_manager.cache_dir / "config"
agents_dir = cache_manager.cache_dir / "agents"
services_dir = cache_manager.cache_dir / "services"
logs_dir = cache_manager.cache_dir / "logs"
messages_dir = cache_manager.cache_dir / "messages"

# Save and load configuration
cache_manager.save_config("agent_config", {"timeout": 30})
config = cache_manager.load_config("agent_config")

# Message caching
message_cache = MessageCache()
message_cache.save_message("msg-001", {"content": "Hello, agent!"})
message = message_cache.load_message("msg-001")
messages = message_cache.search_messages("Hello")

# Log caching
log_cache = LogCache()
log_cache.save_log("agent-001", "Agent started")
log_cache.save_log("agent-001", "Query processed")
logs = log_cache.read_log_lines("agent-001", max_lines=10)
```

## Communication Protocols

MCPS supports multiple communication protocols for agent interaction:

### gRPC

For high-performance, structured communication:

```python
# Agent configuration
{
    "agent_id": "grpc-agent-001",
    "name": "gRPC Test Agent",
    "config": {
        "runtime": "docker",
        "protocol": "grpc",
        "port": 50051
    }
}
```

### WebSocket

For real-time, bidirectional communication:

```python
# Agent configuration
{
    "agent_id": "websocket-agent-001",
    "name": "WebSocket Test Agent",
    "config": {
        "runtime": "docker",
        "protocol": "websocket",
        "port": 8765
    }
}
```

## Workflow Testing

MCPS includes comprehensive tests for the agent workflow:

```python
import pytest
from mcps.agents.agent_manager import AgentManager

def test_agent_discovery(agent_manager):
    """Test agent discovery."""
    matches = agent_manager.find_agents_by_query("basic agent")
    assert len(matches) > 0
    assert any(match.agent.agent_id == "basic-agent-001" for match in matches)

def test_basic_agent_lifecycle(agent_manager):
    """Test basic agent lifecycle."""
    deployment_id = agent_manager.deploy_agent("basic-agent-001")
    agent_manager.start_agent(deployment_id)
    
    query = "Hello, basic agent!"
    output, cache_path = agent_manager.run_query(deployment_id, query)
    
    assert output.status == "success"
    assert "Processed: Hello, basic agent!" in output.result
    
    agent_manager.stop_agent(deployment_id)
    agent_manager.cleanup_agent(deployment_id)

def test_docker_container_verification(agent_manager):
    """Test Docker container verification."""
    docker_client = docker.from_env()
    
    deployment_id = agent_manager.deploy_agent("websocket-agent-001")
    agent_manager.start_agent(deployment_id)
    
    containers = docker_client.containers.list(all=True)
    agent_container = next((c for c in containers if deployment_id in c.name), None)
    
    assert agent_container is not None
    assert agent_container.status in ["running", "created", "exited"]
    
    agent_manager.stop_agent(deployment_id)
    agent_manager.cleanup_agent(deployment_id)

def test_cache_integration(agent_manager, temp_cache_dir):
    """Test cache integration with agent workflow."""
    cache_manager = CacheManager(cache_dir=temp_cache_dir)
    
    deployment_id = agent_manager.deploy_agent("basic-agent-001")
    agent_manager.start_agent(deployment_id)
    
    query = "Hello, cache test!"
    output, cache_path = agent_manager.run_query(deployment_id, query)
    
    with open(cache_path, "r") as f:
        cached_data = json.load(f)
    
    assert cached_data["query"] == query
    assert cached_data["agent_id"] == deployment_id
    
    agent_manager.stop_agent(deployment_id)
    agent_manager.cleanup_agent(deployment_id)
```

## Best Practices

1. **Agent Package Structure**
   - Organize agent packages with clear separation of code, configuration, and resources
   - Use standardized configuration format for consistent agent discovery

2. **Resource Management**
   - Set appropriate resource limits for Docker containers
   - Use timeouts to prevent runaway processes

3. **Error Handling**
   - Implement proper error handling for agent operations
   - Use the cache system to store logs and debug information

4. **Security**
   - Isolate agents in Docker containers for enhanced security
   - Disable network access for untrusted agents
   - Use environment variables for sensitive configuration

5. **Performance**
   - Use the appropriate runtime for each agent type
   - Implement caching for frequently used data
   - Clean up resources after agent execution

## Troubleshooting

### Common Issues

1. **Agent Discovery Failures**
   - Verify agent package structure and configuration
   - Check that the agent directory is accessible

2. **Docker Runtime Issues**
   - Ensure Docker is running and accessible
   - Verify that the base image is available
   - Check resource limits and container configuration

3. **Communication Protocol Errors**
   - Verify port configuration and availability
   - Check network settings and firewall rules

4. **Cache-Related Problems**
   - Ensure write permissions for cache directories
   - Check disk space availability
   - Verify cache path configuration

## Conclusion

The MCPS Agent Runtime provides a flexible and powerful framework for managing intelligent agents across different runtime environments. By following the guidelines in this document, you can effectively leverage the MCPS agent system for your applications.
