"""Example of agent discovery and Docker integration."""

import os
import sys
import json
import logging
import time
from datetime import datetime

from mcps.agents.discovery.local import LocalAgentDiscoverer
from mcps.agents.lifecycle.standard import StandardLifecycleManager
from mcps.agents.runtime.docker import DockerSandboxRuntime
from mcps.agents.runtime.python import PythonRuntime
from mcps.agents.runtime.base import RuntimeEnvironment
from mcps.agents.agent_manager import AgentManager

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Run the agent discovery and Docker integration example."""
    logger.info("Starting agent discovery and Docker integration example")
    
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
    
    data_dir = os.path.join(os.getcwd(), "data")
    discoverer = LocalAgentDiscoverer(data_dir)
    
    agent_manager = AgentManager(
        discoverer=discoverer,
        lifecycle_manager=lifecycle_manager,
        runtime_registry=runtime_registry,
        cache_dir=os.path.join(data_dir, "cache")
    )
    
    try:
        query = "websocket communication"
        logger.info(f"Finding agents for query: '{query}'")
        
        matches = agent_manager.find_agents_by_query(query)
        
        if not matches:
            logger.error(f"No agents found for query: '{query}'")
            return 1
            
        top_match = matches[0]
        agent_id = top_match.agent.agent_id
        
        logger.info(f"Selected agent: {agent_id} (confidence: {top_match.confidence:.2f})")
        logger.info(f"Agent details: {top_match.agent.name} - {top_match.agent.description}")
        
        logger.info(f"Deploying agent: {agent_id}")
        deployment_id = agent_manager.deploy_agent(agent_id)
        
        logger.info(f"Starting agent: {agent_id}")
        agent_manager.start_agent(agent_id)
        
        state = agent_manager.get_agent_state(agent_id)
        logger.info(f"Agent state: {state['status']}")
        
        logger.info("Waiting for agent to initialize...")
        time.sleep(2)
        
        test_query = "Hello, websocket agent!"
        logger.info(f"Running query: '{test_query}'")
        
        output, cache_path = agent_manager.run_query(agent_id, test_query)
        
        logger.info(f"Agent output: {output.result}")
        logger.info(f"Output cached at: {cache_path}")
        
        logger.info("Verifying Docker container...")
        
        try:
            import docker
            client = docker.from_env()
            
            containers = client.containers.list(all=True)
            agent_container = None
            
            for container in containers:
                if deployment_id in container.name:
                    agent_container = container
                    break
                    
            if agent_container:
                logger.info(f"Docker container found: {agent_container.name} (ID: {agent_container.id})")
                logger.info(f"Container status: {agent_container.status}")
                logger.info(f"Container image: {agent_container.image.tags}")
            else:
                logger.warning("No Docker container found for the agent")
                
        except Exception as e:
            logger.error(f"Error verifying Docker container: {e}")
        
        logger.info(f"Stopping agent: {deployment_id}")
        agent_manager.stop_agent(deployment_id)
        
        state = agent_manager.get_agent_state(deployment_id)
        logger.info(f"Agent state after stop: {state['status']}")
        
    except Exception as e:
        logger.error(f"Error: {e}")
        return 1
        
    finally:
        if 'deployment_id' in locals():
            logger.info(f"Cleaning up agent: {deployment_id}")
            try:
                agent_manager.cleanup_agent(deployment_id)
                logger.info("Agent successfully cleaned up")
            except Exception as e:
                logger.error(f"Error cleaning up agent: {e}")
        else:
            logger.warning("No deployment_id available for cleanup")
    
    logger.info("Agent discovery and Docker integration example completed")
    return 0

if __name__ == "__main__":
    sys.exit(main())
