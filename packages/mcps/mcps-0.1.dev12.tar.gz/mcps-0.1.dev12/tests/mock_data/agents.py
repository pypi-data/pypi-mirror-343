"""Mock data for agent testing."""

from datetime import datetime

MOCK_AGENT_METADATA = {
    "agent1": {
        "id": "agent1",
        "name": "Test Agent 1",
        "description": "A test agent for testing purposes",
        "capabilities": ["text_processing", "data_analysis"],
        "version": "1.0.0",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    },
    "agent2": {
        "id": "agent2",
        "name": "Test Agent 2",
        "description": "Another test agent for testing purposes",
        "capabilities": ["image_processing", "object_detection"],
        "version": "1.0.0",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
}

MOCK_AGENT_STATES = {
    "agent1": {
        "status": "running",
        "last_heartbeat": datetime.now().isoformat(),
        "memory_usage": 1024,
        "cpu_usage": 0.5,
        "active_tasks": 2
    },
    "agent2": {
        "status": "idle",
        "last_heartbeat": datetime.now().isoformat(),
        "memory_usage": 512,
        "cpu_usage": 0.1,
        "active_tasks": 0
    }
}

MOCK_AGENT_CONFIGS = {
    "agent1": {
        "max_memory": 2048,
        "max_cpu": 1.0,
        "max_tasks": 5,
        "timeout": 30,
        "retry_count": 3
    },
    "agent2": {
        "max_memory": 1024,
        "max_cpu": 0.5,
        "max_tasks": 3,
        "timeout": 15,
        "retry_count": 2
    }
} 