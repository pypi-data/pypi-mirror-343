"""Example of agent lifecycle management."""

import os
import sys
import logging
import time
from datetime import datetime

from mcps.agents.lifecycle.standard import StandardLifecycleManager
from mcps.agents.lifecycle.base import AgentConfig
from mcps.agents.runtime.docker import DockerSandboxRuntime
from mcps.agents.runtime.python import PythonRuntime
from mcps.agents.runtime.base import RuntimeEnvironment

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Run the agent lifecycle example."""
    logger.info("Starting agent lifecycle example")
    
    docker_env = RuntimeEnvironment(
        container_type="docker",
        resources={
            "image": "python:3.9-slim",
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
    
    agent_config = AgentConfig(
        agent_id="example-agent-001",
        name="Example Agent",
        version="0.1.0",
        model_config={
            "code": """
import os
import sys
import json

query = os.environ.get("AGENT_QUERY", "")
if not query and len(sys.argv) > 1:
    query = sys.argv[1]

print(json.dumps({
    "response": f"Processed query: {query}",
    "status": "success"
}))
"""
        },
        resource_limits={"memory": "256m", "cpu": 0.5},
        environment={"container_type": "python"},
        dependencies=[],
        startup_timeout=30,
        shutdown_timeout=10
    )
    
    try:
        logger.info("Initializing agent")
        agent_id = lifecycle_manager.initialize(agent_config)
        logger.info(f"Agent initialized with ID: {agent_id}")
        
        state = lifecycle_manager.get_state(agent_id)
        logger.info(f"Agent state: {state.status}")
        
        logger.info("Starting agent")
        lifecycle_manager.start(agent_id)
        
        state = lifecycle_manager.get_state(agent_id)
        logger.info(f"Agent state after start: {state.status}")
        
        logger.info("Registering heartbeat")
        lifecycle_manager.register_heartbeat(agent_id, {
            "resource_usage": {"cpu": 0.2, "memory": 100},
            "status_info": "Running example task"
        })
        
        state = lifecycle_manager.get_state(agent_id)
        logger.info(f"Agent resource usage: {state.resource_usage}")
        logger.info(f"Agent metadata: {state.metadata}")
        
        agents = lifecycle_manager.list_agents()
        logger.info(f"Total agents: {len(agents)}")
        
        logger.info("Updating agent configuration")
        updated_config = lifecycle_manager.update_config(agent_id, {
            "name": "Updated Example Agent",
            "version": "0.2.0"
        })
        logger.info(f"Updated agent name: {updated_config.name}")
        logger.info(f"Updated agent version: {updated_config.version}")
        
        logger.info("Stopping agent")
        lifecycle_manager.stop(agent_id)
        
        state = lifecycle_manager.get_state(agent_id)
        logger.info(f"Agent state after stop: {state.status}")
        
    finally:
        logger.info("Cleaning up agent")
        lifecycle_manager.cleanup(agent_id)
        
        try:
            lifecycle_manager.get_state(agent_id)
            logger.error("Agent was not properly cleaned up")
        except ValueError:
            logger.info("Agent successfully cleaned up")
    
    logger.info("Agent lifecycle example completed")
    return 0

if __name__ == "__main__":
    sys.exit(main())
