"""Resource governance for agent runtime."""

import os
import logging
import shutil
from typing import Dict, Any, Optional, List
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class ResourceQuota:
    """Resource quota configuration."""
    cpu: float  # CPU cores
    memory: int  # Memory in bytes
    disk: int  # Disk space in bytes
    network_in: int  # Network input bandwidth in bytes/sec
    network_out: int  # Network output bandwidth in bytes/sec

class ResourceGovernor:
    """Resource governor for agent runtime."""
    
    def __init__(self, cgroup_root: str = "/sys/fs/cgroup"):
        """Initialize resource governor.
        
        Args:
            cgroup_root: Root directory for cgroups
        """
        self.cgroup_root = cgroup_root
        self.active_quotas = {}
    
    def apply_quota(self, container_id: str, quota: ResourceQuota) -> bool:
        """Apply resource quota to container.
        
        Args:
            container_id: Container ID
            quota: Resource quota
            
        Returns:
            Success status
        """
        try:
            cg_path = f"{self.cgroup_root}/mcps_sandbox/{container_id}"
            os.makedirs(cg_path, exist_ok=True)
            
            with open(f"{cg_path}/cpu.max", "w") as f:
                f.write(f"{int(quota.cpu * 100000)} 100000")
                
            with open(f"{cg_path}/memory.max", "w") as f:
                f.write(str(quota.memory))
                
            with open(f"{cg_path}/io.max", "w") as f:
                f.write(f"rbps={quota.disk} wbps={quota.disk}")
                
            self.active_quotas[container_id] = {
                "path": cg_path,
                "quota": quota
            }
            
            return True
        except Exception as e:
            logger.error(f"Error applying resource quota: {e}")
            return False
    
    def update_quota(self, container_id: str, updates: Dict[str, Any]) -> bool:
        """Update resource quota.
        
        Args:
            container_id: Container ID
            updates: Dictionary of quota updates
            
        Returns:
            Success status
        """
        if container_id not in self.active_quotas:
            return False
            
        try:
            quota_data = self.active_quotas[container_id]
            cg_path = quota_data["path"]
            quota = quota_data["quota"]
            
            for key, value in updates.items():
                if hasattr(quota, key):
                    setattr(quota, key, value)
            
            if "cpu" in updates:
                with open(f"{cg_path}/cpu.max", "w") as f:
                    f.write(f"{int(quota.cpu * 100000)} 100000")
                    
            if "memory" in updates:
                with open(f"{cg_path}/memory.max", "w") as f:
                    f.write(str(quota.memory))
                    
            if "disk" in updates:
                with open(f"{cg_path}/io.max", "w") as f:
                    f.write(f"rbps={quota.disk} wbps={quota.disk}")
            
            self.active_quotas[container_id]["quota"] = quota
            
            return True
        except Exception as e:
            logger.error(f"Error updating resource quota: {e}")
            return False
    
    def get_quota(self, container_id: str) -> Optional[ResourceQuota]:
        """Get resource quota for container.
        
        Args:
            container_id: Container ID
            
        Returns:
            Resource quota or None if not found
        """
        if container_id not in self.active_quotas:
            return None
            
        return self.active_quotas[container_id]["quota"]
    
    def release_quota(self, container_id: str) -> bool:
        """Release resource quota.
        
        Args:
            container_id: Container ID
            
        Returns:
            Success status
        """
        if container_id not in self.active_quotas:
            return False
            
        try:
            cg_path = self.active_quotas[container_id]["path"]
            shutil.rmtree(cg_path)
            del self.active_quotas[container_id]
            return True
        except Exception as e:
            logger.error(f"Error releasing resource quota: {e}")
            return False
