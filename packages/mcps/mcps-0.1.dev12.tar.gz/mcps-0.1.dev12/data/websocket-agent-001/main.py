"""WebSocket test agent for lifecycle testing."""

import os
import json
import sys
import logging
import asyncio
import websockets

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgentService:
    """Simple WebSocket service for agent."""
    
    def __init__(self, config):
        """Initialize with agent config."""
        self.config = config
        self.running = False
        self.clients = set()
        
    async def start(self):
        """Start the agent service."""
        logger.info(f"Starting WebSocket agent {self.config['name']}")
        self.running = True
        return {"status": "running", "agent_id": self.config["agent_id"]}
        
    async def stop(self):
        """Stop the agent service."""
        logger.info(f"Stopping WebSocket agent {self.config['name']}")
        self.running = False
        return {"status": "stopped", "agent_id": self.config["agent_id"]}
        
    async def process_query(self, query):
        """Process a query and return a response."""
        if not self.running:
            return {"status": "error", "message": "Agent is not running"}
            
        logger.info(f"Processing query: {query}")
        response = f"WebSocket Agent {self.config['name']} processed: {query}"
        return {
            "response": response,
            "agent_id": self.config["agent_id"],
            "status": "success"
        }
        
    async def get_status(self):
        """Get the current status of the agent."""
        status = "running" if self.running else "stopped"
        return {
            "status": status,
            "agent_id": self.config["agent_id"],
            "last_heartbeat": asyncio.get_event_loop().time()
        }
        
    async def handler(self, websocket):
        """Handle WebSocket connections."""
        self.clients.add(websocket)
        try:
            async for message in websocket:
                data = json.loads(message)
                cmd = data.get("command")
                
                if cmd == "start":
                    response = await self.start()
                elif cmd == "stop":
                    response = await self.stop()
                elif cmd == "query":
                    response = await self.process_query(data.get("query", ""))
                elif cmd == "status":
                    response = await self.get_status()
                else:
                    response = {"status": "error", "message": f"Unknown command: {cmd}"}
                    
                await websocket.send(json.dumps(response))
        finally:
            self.clients.remove(websocket)

def load_config():
    """Load the agent configuration from config.json."""
    with open("config.json", "r") as f:
        return json.load(f)

async def main():
    """Main entry point for the WebSocket agent."""
    logger.info("Starting WebSocket agent server")
    
    config = load_config()
    
    service = AgentService(config)
    
    port = config["config"].get("port", 8765)
    server = await websockets.serve(
        service.handler, 
        "localhost", 
        port
    )
    
    logger.info(f"WebSocket agent server started with ID: {config['agent_id']} on port {port}")
    logger.info("Press Ctrl+C to stop")
    
    try:
        await asyncio.Future()  # Run forever
    except KeyboardInterrupt:
        await service.stop()
        server.close()
        await server.wait_closed()
        logger.info("WebSocket agent server stopped")

if __name__ == "__main__":
    asyncio.run(main())
