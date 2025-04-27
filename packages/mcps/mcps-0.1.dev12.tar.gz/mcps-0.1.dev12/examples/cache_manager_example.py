"""Example of using the cache manager."""

import os
import json
import logging
from pathlib import Path

from mcps.config.cache import CacheManager

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Run the cache manager example."""
    logger.info("Starting cache manager example")
    
    cache_manager = CacheManager()
    
    config_data = {
        "name": "example_config",
        "version": "1.0.0",
        "settings": {
            "max_connections": 10,
            "timeout": 30,
            "retry_count": 3
        }
    }
    
    cache_manager.save_config("example_config", config_data)
    logger.info(f"Saved configuration: {config_data}")
    
    loaded_config = cache_manager.load_config("example_config")
    logger.info(f"Loaded configuration: {loaded_config}")
    
    agent_id = "example_agent"
    agent_dir = cache_manager.get_agent_cache_dir(agent_id)
    logger.info(f"Agent cache directory: {agent_dir}")
    
    agent_metadata = {
        "agent_id": agent_id,
        "name": "Example Agent",
        "description": "An example agent for testing cache",
        "version": "1.0.0",
        "capabilities": ["text", "image"],
        "created_at": "2025-04-26T12:00:00Z"
    }
    
    with open(agent_dir / "metadata.json", "w") as f:
        json.dump(agent_metadata, f, indent=2)
    logger.info(f"Saved agent metadata to {agent_dir / 'metadata.json'}")
    
    service_id = "example_service"
    service_dir = cache_manager.get_service_cache_dir(service_id)
    logger.info(f"Service cache directory: {service_dir}")
    
    service_metadata = {
        "service_id": service_id,
        "name": "Example Service",
        "description": "An example service for testing cache",
        "version": "1.0.0",
        "endpoints": ["/api/v1/example"],
        "created_at": "2025-04-26T12:00:00Z"
    }
    
    with open(service_dir / "metadata.json", "w") as f:
        json.dump(service_metadata, f, indent=2)
    logger.info(f"Saved service metadata to {service_dir / 'metadata.json'}")
    
    message_id = "example_message"
    message_data = {
        "id": message_id,
        "content": "Hello, world!",
        "timestamp": "2025-04-26T12:34:56Z",
        "sender": "example_agent",
        "recipient": "example_service"
    }
    
    cache_manager.save_message(message_id, message_data)
    logger.info(f"Saved message: {message_data}")
    
    loaded_message = cache_manager.load_message(message_id)
    logger.info(f"Loaded message: {loaded_message}")
    
    log_id = "example_log"
    log_data = "2025-04-26 12:34:56 INFO Example log message"
    
    cache_manager.save_log(log_id, log_data)
    logger.info(f"Saved log to {cache_manager.get_log_path(log_id)}")
    
    additional_log_data = "2025-04-26 12:35:00 INFO Another log message"
    cache_manager.save_log(log_id, additional_log_data)
    logger.info(f"Saved additional log entry")
    
    stats = cache_manager.get_cache_stats()
    logger.info(f"Cache statistics: {stats}")
    
    cache_manager.cleanup_temp()
    logger.info("Cleaned up temporary directory")
    
    logger.info("Cache manager example completed")
    return 0

if __name__ == "__main__":
    main()
