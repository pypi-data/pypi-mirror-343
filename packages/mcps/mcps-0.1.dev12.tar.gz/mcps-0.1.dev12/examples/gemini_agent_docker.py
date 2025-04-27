"""Example of running the Gemini agent in a Docker container.

This example demonstrates how to run the Gemini agent in a Docker container
using the MCPS Docker sandbox runtime.
"""

import os
import logging
import tempfile
import json
from typing import Optional
from mcps.agents.runtime.docker import DockerSandboxRuntime
from mcps.agents.runtime.base import RuntimeEnvironment, ExecutionSession
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_gemini_agent_in_docker(query: str, api_key: Optional[str] = None):
    """Run the Gemini agent in a Docker container.
    
    Args:
        query: Query to send to the Gemini agent
        api_key: Optional API key for the Gemini API
    
    Returns:
        Agent output
    """
    env = RuntimeEnvironment(
        container_type="docker",
        resources={
            "image": "python:3.9-slim",  # Using confirmed available image
            "memory": "512m",
            "cpu": 1.0,
            "timeout": 30
        },
        network_config={
            "disable": False  # Need network access to call the Gemini API
        },
        env_vars={
            "GEMINI_API_KEY": api_key or os.environ.get("GEMINI_API_KEY", "")
        }
    )
    
    runtime = DockerSandboxRuntime(env)
    
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode='w') as f:
        config_path = f.name
        json.dump({
            "api_key": api_key or os.environ.get("GEMINI_API_KEY", ""),
            "model": "gemini-2.0-flash"
        }, f)
    
    with open(os.path.join(os.path.dirname(__file__), "gemini_agent_config.py"), "r") as f:
        agent_code = f.read()
    
    agent_package = {
        "code": agent_code,
        "dependencies": ["google-genai"]
    }
    
    deployment_id = runtime.deploy(agent_package)
    
    try:
        session = ExecutionSession(
            session_id=f"gemini_agent_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            agent_id=deployment_id,
            start_time=datetime.utcnow(),
            context={
                "query": query,
                "config_path": "/runner/config.json"
            },
            tools=[]
        )
        
        output = runtime.execute(session)
        
        return output
    finally:
        runtime.cleanup(session.session_id)
        os.unlink(config_path)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        query = sys.argv[1]
    else:
        query = "Explain how AI works in a few words"
    
    output = run_gemini_agent_in_docker(query)
    
    print(f"Query: {query}")
    print(f"Status: {output.status}")
    
    if output.status == "success":
        print(f"Response: {output.result}")
    else:
        print(f"Error: {output.error}")
