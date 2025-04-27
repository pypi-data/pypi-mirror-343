"""gRPC test agent for lifecycle testing."""

import os
import json
import sys
import logging
import time
from concurrent import futures
import grpc

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AgentService:
    """Simple gRPC service for agent."""
    
    def __init__(self, config):
        """Initialize with agent config."""
        self.config = config
        self.running = False
        
    def start(self):
        """Start the agent service."""
        logger.info(f"Starting gRPC agent {self.config['name']}")
        self.running = True
        return {"status": "running", "agent_id": self.config["agent_id"]}
        
    def stop(self):
        """Stop the agent service."""
        logger.info(f"Stopping gRPC agent {self.config['name']}")
        self.running = False
        return {"status": "stopped", "agent_id": self.config["agent_id"]}
        
    def process_query(self, query):
        """Process a query and return a response."""
        if not self.running:
            return {"status": "error", "message": "Agent is not running"}
            
        logger.info(f"Processing query: {query}")
        response = f"gRPC Agent {self.config['name']} processed: {query}"
        return {
            "response": response,
            "agent_id": self.config["agent_id"],
            "status": "success"
        }
        
    def get_status(self):
        """Get the current status of the agent."""
        status = "running" if self.running else "stopped"
        return {
            "status": status,
            "agent_id": self.config["agent_id"],
            "last_heartbeat": time.time()
        }

def load_config():
    """Load the agent configuration from config.json."""
    with open("config.json", "r") as f:
        return json.load(f)

def main():
    """Main entry point for the gRPC agent."""
    logger.info("Starting gRPC agent server")
    
    config = load_config()
    
    service = AgentService(config)
    
    service.start()
    
    logger.info(f"gRPC agent server started with ID: {config['agent_id']}")
    logger.info("Press Ctrl+C to stop")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        service.stop()
        logger.info("gRPC agent server stopped")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
