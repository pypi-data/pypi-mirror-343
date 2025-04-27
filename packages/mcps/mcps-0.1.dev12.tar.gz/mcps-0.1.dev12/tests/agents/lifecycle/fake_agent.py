"""Fake agent implementations for testing lifecycle management."""

import logging
import threading
import time
import json
import asyncio
import websockets
from typing import Dict, Any, Optional, Callable, Coroutine
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

class BaseFakeAgent(ABC):
    """Base class for fake agent implementations."""
    
    def __init__(self, agent_id: str, config: Dict[str, Any]):
        """Initialize with agent ID and configuration.
        
        Args:
            agent_id: Agent identifier
            config: Agent configuration
        """
        self.agent_id = agent_id
        self.config = config
        self.running = False
        self.last_heartbeat = time.time()
        self.resource_usage = {"cpu": 0.0, "memory": 0.0}
        
    @abstractmethod
    def start(self) -> Dict[str, Any]:
        """Start the agent.
        
        Returns:
            Status information
        """
        pass
        
    @abstractmethod
    def stop(self) -> Dict[str, Any]:
        """Stop the agent.
        
        Returns:
            Status information
        """
        pass
        
    @abstractmethod
    def process_query(self, query: str) -> Dict[str, Any]:
        """Process a query.
        
        Args:
            query: Query string
            
        Returns:
            Response information
        """
        pass
        
    @abstractmethod
    def get_status(self) -> Dict[str, Any]:
        """Get the current status of the agent.
        
        Returns:
            Status information
        """
        pass
        
    def update_resource_usage(self) -> None:
        """Update resource usage metrics."""
        self.resource_usage = {
            "cpu": 0.1 + (0.4 * int(self.running)),  # Higher when running
            "memory": 50.0 + (100.0 * int(self.running))  # Higher when running
        }
        
    def register_heartbeat(self) -> None:
        """Register a heartbeat."""
        self.last_heartbeat = time.time()
        self.update_resource_usage()

class GrpcFakeAgent(BaseFakeAgent):
    """Fake agent implementation using gRPC."""
    
    def __init__(self, agent_id: str, config: Dict[str, Any]):
        """Initialize with agent ID and configuration."""
        super().__init__(agent_id, config)
        self.server_thread = None
        
    def start(self) -> Dict[str, Any]:
        """Start the agent."""
        logger.info(f"Starting gRPC agent {self.agent_id}")
        
        if self.running:
            return {"status": "already_running", "agent_id": self.agent_id}
            
        self.running = True
        
        self.server_thread = threading.Thread(target=self._run_server)
        self.server_thread.daemon = True
        self.server_thread.start()
        
        self.register_heartbeat()
        return {"status": "running", "agent_id": self.agent_id}
        
    def stop(self) -> Dict[str, Any]:
        """Stop the agent."""
        logger.info(f"Stopping gRPC agent {self.agent_id}")
        
        if not self.running:
            return {"status": "not_running", "agent_id": self.agent_id}
            
        self.running = False
        
        if self.server_thread and self.server_thread.is_alive():
            self.server_thread.join(timeout=2.0)
            
        self.register_heartbeat()
        return {"status": "stopped", "agent_id": self.agent_id}
        
        
    def process_query(self, query: str) -> Dict[str, Any]:
        """Process a query."""
        logger.info(f"Processing query with gRPC agent {self.agent_id}: {query}")
        
        if not self.running:
            return {"status": "error", "message": "Agent is not running", "agent_id": self.agent_id}
            
        time.sleep(0.5)
        
        self.register_heartbeat()
        return {
            "status": "success",
            "agent_id": self.agent_id,
            "response": f"gRPC Agent {self.agent_id} processed: {query}"
        }
        
    def get_status(self) -> Dict[str, Any]:
        """Get the current status of the agent."""
        status = "running" if self.running else "stopped"
        
        self.register_heartbeat()
        return {
            "status": status,
            "agent_id": self.agent_id,
            "last_heartbeat": self.last_heartbeat,
            "resource_usage": self.resource_usage
        }
        
    def _run_server(self) -> None:
        """Run the fake gRPC server."""
        logger.info(f"gRPC server for agent {self.agent_id} started")
        
        while self.running:
            time.sleep(1.0)
            self.register_heartbeat()
            
        logger.info(f"gRPC server for agent {self.agent_id} stopped")

class WebSocketFakeAgent(BaseFakeAgent):
    """Fake agent implementation using WebSocket."""
    
    def __init__(self, agent_id: str, config: Dict[str, Any]):
        """Initialize with agent ID and configuration."""
        super().__init__(agent_id, config)
        self.server_task = None
        self.loop = asyncio.new_event_loop()
        self.server = None
        
    def start(self) -> Dict[str, Any]:
        """Start the agent."""
        logger.info(f"Starting WebSocket agent {self.agent_id}")
        
        if self.running:
            return {"status": "already_running", "agent_id": self.agent_id}
            
        self.running = True
        
        server_thread = threading.Thread(target=self._run_server)
        server_thread.daemon = True
        server_thread.start()
        
        time.sleep(0.5)
        
        self.register_heartbeat()
        return {"status": "running", "agent_id": self.agent_id}
        
    def stop(self) -> Dict[str, Any]:
        """Stop the agent."""
        logger.info(f"Stopping WebSocket agent {self.agent_id}")
        
        if not self.running:
            return {"status": "not_running", "agent_id": self.agent_id}
            
        self.running = False
        
        if self.server: 
            asyncio.run_coroutine_threadsafe(self._stop_server(), self.loop)
            
        self.register_heartbeat()
        return {"status": "stopped", "agent_id": self.agent_id}
        
    def process_query(self, query: str) -> Dict[str, Any]:
        """Process a query."""
        logger.info(f"Processing query with WebSocket agent {self.agent_id}: {query}")
        
        if not self.running:
            return {"status": "error", "message": "Agent is not running", "agent_id": self.agent_id}
            
        time.sleep(0.5)
        
        self.register_heartbeat()
        return {
            "status": "success",
            "agent_id": self.agent_id,
            "response": f"WebSocket Agent {self.agent_id} processed: {query}"
        }
        
    def get_status(self) -> Dict[str, Any]:
        """Get the current status of the agent."""
        status = "running" if self.running else "stopped"
        
        self.register_heartbeat()
        return {
            "status": status,
            "agent_id": self.agent_id,
            "last_heartbeat": self.last_heartbeat,
            "resource_usage": self.resource_usage
        }
        
    def _run_server(self) -> None:
        """Run the fake WebSocket server."""
        asyncio.set_event_loop(self.loop)
        
        async def handler(websocket):
            """Handle WebSocket connections."""
            async for message in websocket:
                if not self.running:
                    await websocket.send(json.dumps({
                        "status": "error",
                        "message": "Agent is not running"
                    }))
                    continue
                    
                try:
                    data = json.loads(message)
                    cmd = data.get("command")
                    
                    if cmd == "query":
                        response = self.process_query(data.get("query", ""))
                    elif cmd == "status":
                        response = self.get_status()
                    else:
                        response = {
                            "status": "error",
                            "message": f"Unknown command: {cmd}"
                        }
                        
                    await websocket.send(json.dumps(response))
                    
                except Exception as e:
                    logger.error(f"Error handling WebSocket message: {e}")
                    await websocket.send(json.dumps({
                        "status": "error",
                        "message": str(e)
                    }))
        
        async def start_server():
            """Start the WebSocket server."""
            port = self.config.get("config", {}).get("port", 8765)
            self.server = await websockets.serve(handler, "localhost", port)
            logger.info(f"WebSocket server for agent {self.agent_id} started on port {port}")
            await self.server.wait_closed()
            
        self.loop.run_until_complete(start_server())
        self.loop.run_forever()
        
    async def _stop_server(self) -> None:
        """Stop the WebSocket server."""
        if self.server:
            self.server.close()
            logger.info(f"WebSocket server for agent {self.agent_id} stopped")
