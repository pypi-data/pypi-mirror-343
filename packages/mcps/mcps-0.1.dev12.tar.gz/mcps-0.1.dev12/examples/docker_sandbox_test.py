"""Test script for Docker sandbox runtime.

This script demonstrates the Docker sandbox runtime by creating and running
a real Docker container with a simple Python agent.
"""

import os
import sys
import logging
import json
import tempfile
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from mcps.agents.runtime.docker import DockerSandboxRuntime
from mcps.agents.runtime.base import RuntimeEnvironment, ExecutionSession

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_docker_sandbox():
    """Run a simple test using the Docker sandbox runtime."""
    print("Starting Docker sandbox test...")
    
    agent_code = '''
import os
import sys
import platform
import json

with open("context.json", "r") as f:
    context = json.load(f)

query = context.get("query", "No query provided")

print(f"Python version: {sys.version}")
print(f"Platform: {platform.platform()}")
print(f"Query: {query}")

with open("output.json", "w") as f:
    json.dump({
        "result": f"Processed query: {query} on {platform.node()} using Python {sys.version}"
    }, f)
'''

    env = RuntimeEnvironment(
        container_type="docker",
        resources={
            "image": "python:3.9-slim",  # Using confirmed available image
            "memory": "256m",
            "cpu": 0.5,
            "timeout": 30
        },
        network_config={
            "disable": False
        },
        env_vars={
            "TEST_ENV_VAR": "test_value"
        }
    )
    
    runtime = DockerSandboxRuntime(env)
    
    agent_package = {
        "code": agent_code,
        "dependencies": []  # No additional dependencies needed
    }
    
    deployment_id = runtime.deploy(agent_package)
    print(f"Deployed agent with ID: {deployment_id}")
    
    try:
        session = ExecutionSession(
            session_id=f"test_session_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            agent_id=deployment_id,
            start_time=datetime.utcnow(),
            context={
                "query": "Hello from Docker test!"
            },
            tools=[]
        )
        
        print(f"Session ID: {session.session_id}")
        print("Executing agent in Docker container...")
        
        output = runtime.execute(session)
        
        print("\nExecution completed!")
        print(f"Status: {output.status}")
        
        if output.status == "success":
            print(f"Result: {output.result}")
        else:
            print(f"Error: {output.error}")
            
        print("\nContainer metadata:")
        for key, value in output.metadata.items():
            print(f"  {key}: {value}")
            
        snapshot = runtime.snapshot()
        print("\nRuntime snapshot:")
        print(f"Active containers: {snapshot.state.get('active_containers', 0)}")
        
        return output.status == "success"
        
    finally:
        print(f"\nCleaning up session {session.session_id}...")
        runtime.cleanup(session.session_id)
        print("Cleanup completed")

if __name__ == "__main__":
    success = test_docker_sandbox()
    sys.exit(0 if success else 1)
