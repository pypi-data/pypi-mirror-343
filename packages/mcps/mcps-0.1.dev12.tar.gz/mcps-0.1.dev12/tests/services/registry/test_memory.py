"""Tests for in-memory service registry."""

import pytest
from datetime import datetime, timedelta
from mcps.services.registry.memory import InMemoryServiceRegistry
from tests.mock_data.services import (
    MOCK_SERVICE_DESCRIPTORS,
    MOCK_SERVICE_REGISTRATIONS,
    MOCK_SERVICE_POLICIES
)

@pytest.fixture
def registry():
    """Create an InMemoryServiceRegistry instance for testing."""
    return InMemoryServiceRegistry()

@pytest.fixture
def mock_services():
    """Create mock service data for testing."""
    return {
        "descriptors": MOCK_SERVICE_DESCRIPTORS,
        "registrations": MOCK_SERVICE_REGISTRATIONS,
        "policies": MOCK_SERVICE_POLICIES
    }

def test_registry_initialization(registry):
    """Test InMemoryServiceRegistry initialization."""
    assert registry is not None
    assert isinstance(registry, InMemoryServiceRegistry)
    assert registry._services == {}
    assert registry._instances == {}
    assert registry._policies == {}

def test_register_service(registry, mock_services):
    """Test service registration."""
    service_id = "service1"
    descriptor = mock_services["descriptors"][service_id]
    
    registry.register_service(service_id, descriptor)
    
    assert service_id in registry._services
    assert registry._services[service_id] == descriptor

def test_unregister_service(registry, mock_services):
    """Test service unregistration."""
    service_id = "service1"
    descriptor = mock_services["descriptors"][service_id]
    
    registry.register_service(service_id, descriptor)
    registry.unregister_service(service_id)
    
    assert service_id not in registry._services
    assert service_id not in registry._instances

def test_register_instance(registry, mock_services):
    """Test service instance registration."""
    service_id = "service1"
    descriptor = mock_services["descriptors"][service_id]
    registration = mock_services["registrations"][service_id]
    
    registry.register_service(service_id, descriptor)
    registry.register_instance(service_id, registration)
    
    assert service_id in registry._instances
    assert registration["instance_id"] in registry._instances[service_id]

def test_unregister_instance(registry, mock_services):
    """Test service instance unregistration."""
    service_id = "service1"
    descriptor = mock_services["descriptors"][service_id]
    registration = mock_services["registrations"][service_id]
    
    registry.register_service(service_id, descriptor)
    registry.register_instance(service_id, registration)
    registry.unregister_instance(service_id, registration["instance_id"])
    
    assert service_id in registry._instances
    assert registration["instance_id"] not in registry._instances[service_id]

def test_get_service_instances(registry, mock_services):
    """Test retrieving service instances."""
    service_id = "service1"
    descriptor = mock_services["descriptors"][service_id]
    registration = mock_services["registrations"][service_id]
    
    registry.register_service(service_id, descriptor)
    registry.register_instance(service_id, registration)
    
    instances = registry.get_service_instances(service_id)
    assert len(instances) == 1
    assert instances[0]["instance_id"] == registration["instance_id"]

def test_set_service_policy(registry, mock_services):
    """Test setting service policy."""
    service_id = "service1"
    policy = mock_services["policies"][service_id]
    
    registry.set_service_policy(service_id, policy)
    
    assert service_id in registry._policies
    assert registry._policies[service_id] == policy

def test_get_service_policy(registry, mock_services):
    """Test retrieving service policy."""
    service_id = "service1"
    policy = mock_services["policies"][service_id]
    
    registry.set_service_policy(service_id, policy)
    retrieved_policy = registry.get_service_policy(service_id)
    
    assert retrieved_policy == policy

def test_list_services(registry, mock_services):
    """Test listing all registered services."""
    # Register both services
    for service_id, descriptor in mock_services["descriptors"].items():
        registry.register_service(service_id, descriptor)
    
    services = registry.list_services()
    assert len(services) == 2
    assert all(service.id in mock_services["descriptors"] for service in services)

def test_heartbeat(registry, mock_services):
    """Test service instance heartbeat."""
    service_id = "service1"
    descriptor = mock_services["descriptors"][service_id]
    registration = mock_services["registrations"][service_id]
    
    registry.register_service(service_id, descriptor)
    registry.register_instance(service_id, registration)
    
    # Update heartbeat
    new_heartbeat = datetime.now().isoformat()
    registry.heartbeat(service_id, registration["instance_id"], new_heartbeat)
    
    instances = registry.get_service_instances(service_id)
    assert instances[0]["last_heartbeat"] == new_heartbeat

def test_cleanup_expired_instances(registry, mock_services):
    """Test cleanup of expired instances."""
    service_id = "service1"
    descriptor = mock_services["descriptors"][service_id]
    registration = mock_services["registrations"][service_id]
    
    # Set old heartbeat
    old_heartbeat = (datetime.now() - timedelta(minutes=5)).isoformat()
    registration["last_heartbeat"] = old_heartbeat
    
    registry.register_service(service_id, descriptor)
    registry.register_instance(service_id, registration)
    
    # Cleanup with 1-minute timeout
    registry.cleanup_expired_instances(timeout_seconds=60)
    
    instances = registry.get_service_instances(service_id)
    assert len(instances) == 0 