"""Mock data for service testing."""

from datetime import datetime

MOCK_SERVICE_DESCRIPTORS = {
    "service1": {
        "id": "service1",
        "name": "Test Service 1",
        "description": "A test service for testing purposes",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "metrics": "/metrics",
            "api": "/api/v1"
        },
        "metadata": {
            "owner": "test-team",
            "environment": "testing",
            "tags": ["test", "mock"]
        },
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    },
    "service2": {
        "id": "service2",
        "name": "Test Service 2",
        "description": "Another test service for testing purposes",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "metrics": "/metrics",
            "api": "/api/v1"
        },
        "metadata": {
            "owner": "test-team",
            "environment": "testing",
            "tags": ["test", "mock"]
        },
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
}

MOCK_SERVICE_REGISTRATIONS = {
    "service1": {
        "service_id": "service1",
        "instance_id": "instance1",
        "host": "localhost",
        "port": 8080,
        "status": "healthy",
        "last_heartbeat": datetime.now().isoformat(),
        "metadata": {
            "region": "us-west",
            "zone": "zone1",
            "instance_type": "small"
        }
    },
    "service2": {
        "service_id": "service2",
        "instance_id": "instance1",
        "host": "localhost",
        "port": 8081,
        "status": "healthy",
        "last_heartbeat": datetime.now().isoformat(),
        "metadata": {
            "region": "us-west",
            "zone": "zone1",
            "instance_type": "small"
        }
    }
}

MOCK_SERVICE_POLICIES = {
    "service1": {
        "max_instances": 3,
        "min_instances": 1,
        "max_memory": 1024,
        "max_cpu": 1.0,
        "timeout": 30,
        "retry_count": 3,
        "health_check_interval": 30,
        "health_check_timeout": 5
    },
    "service2": {
        "max_instances": 2,
        "min_instances": 1,
        "max_memory": 512,
        "max_cpu": 0.5,
        "timeout": 15,
        "retry_count": 2,
        "health_check_interval": 15,
        "health_check_timeout": 3
    }
} 