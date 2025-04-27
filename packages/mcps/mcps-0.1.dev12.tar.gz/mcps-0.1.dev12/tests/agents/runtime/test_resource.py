"""Tests for resource governance."""

import os
import pytest
from unittest.mock import MagicMock, patch, mock_open

from mcps.agents.runtime.resource import ResourceGovernor, ResourceQuota

@pytest.fixture
def resource_quota():
    """Create resource quota for testing."""
    return ResourceQuota(
        cpu=0.5,
        memory=256 * 1024 * 1024,  # 256 MB
        disk=1024 * 1024 * 1024,  # 1 GB
        network_in=1024 * 1024,  # 1 MB/s
        network_out=1024 * 1024  # 1 MB/s
    )

@pytest.fixture
def resource_governor():
    """Create ResourceGovernor instance for testing."""
    with patch('os.makedirs'):
        return ResourceGovernor(cgroup_root="/sys/fs/cgroup")

def test_apply_quota(resource_governor, resource_quota):
    """Test applying resource quota."""
    container_id = "test_container_id"
    
    with patch('os.makedirs', return_value=None):
        m = mock_open()
        with patch('builtins.open', m):
            result = resource_governor.apply_quota(container_id, resource_quota)
    
    if result:
        assert container_id in resource_governor.active_quotas
        assert resource_governor.active_quotas[container_id]["quota"] == resource_quota
        
        m.assert_any_call("/sys/fs/cgroup/mcps_sandbox/test_container_id/cpu.max", "w")
        m.assert_any_call("/sys/fs/cgroup/mcps_sandbox/test_container_id/memory.max", "w")
        m.assert_any_call("/sys/fs/cgroup/mcps_sandbox/test_container_id/io.max", "w")
    else:
        assert "Error applying resource quota" in resource_governor.logger.error.call_args_list[0][0][0]

def test_update_quota(resource_governor, resource_quota):
    """Test updating resource quota."""
    container_id = "test_container_id"
    
    resource_governor.active_quotas[container_id] = {
        "path": "/sys/fs/cgroup/mcps_sandbox/test_container_id",
        "quota": resource_quota
    }
    
    updates = {
        "cpu": 1.0,
        "memory": 512 * 1024 * 1024
    }
    
    m = mock_open()
    with patch('builtins.open', m):
        result = resource_governor.update_quota(container_id, updates)
    
    assert result is True
    assert resource_governor.active_quotas[container_id]["quota"].cpu == 1.0
    assert resource_governor.active_quotas[container_id]["quota"].memory == 512 * 1024 * 1024
    
    m.assert_any_call("/sys/fs/cgroup/mcps_sandbox/test_container_id/cpu.max", "w")
    m.assert_any_call("/sys/fs/cgroup/mcps_sandbox/test_container_id/memory.max", "w")

def test_get_quota(resource_governor, resource_quota):
    """Test getting resource quota."""
    container_id = "test_container_id"
    
    resource_governor.active_quotas[container_id] = {
        "path": "/sys/fs/cgroup/mcps_sandbox/test_container_id",
        "quota": resource_quota
    }
    
    result = resource_governor.get_quota(container_id)
    
    assert result == resource_quota
    
    assert resource_governor.get_quota("non_existent") is None

def test_release_quota(resource_governor, resource_quota):
    """Test releasing resource quota."""
    container_id = "test_container_id"
    
    resource_governor.active_quotas[container_id] = {
        "path": "/sys/fs/cgroup/mcps_sandbox/test_container_id",
        "quota": resource_quota
    }
    
    with patch('shutil.rmtree') as mock_rmtree:
        result = resource_governor.release_quota(container_id)
    
    assert result is True
    assert container_id not in resource_governor.active_quotas
    assert mock_rmtree.called
    
    assert resource_governor.release_quota("non_existent") is False
