"""Basic test agent for lifecycle testing."""

import os
import json
import sys
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_prompt():
    """Load the prompt template from prompt.txt."""
    with open("prompt.txt", "r") as f:
        return f.read()

def load_config():
    """Load the agent configuration from config.json."""
    with open("config.json", "r") as f:
        return json.load(f)

def main():
    """Main entry point for the agent."""
    logger.info("Starting basic agent")
    
    prompt = load_prompt()
    config = load_config()
    
    query = os.environ.get("AGENT_QUERY", "")
    if not query and len(sys.argv) > 1:
        query = sys.argv[1]
        
    logger.info(f"Received query: {query}")
    
    response = f"Agent {config['name']} processed: {query}"
    
    result = {
        "response": response,
        "agent_id": config["agent_id"],
        "status": "success"
    }
    
    print(json.dumps(result))
    return 0

if __name__ == "__main__":
    sys.exit(main())
