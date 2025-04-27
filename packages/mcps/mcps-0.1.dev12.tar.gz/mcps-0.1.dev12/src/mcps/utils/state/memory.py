from typing import Dict, Any, List, Optional
from datetime import datetime
import json
from ..base import StateManager, StateMetadata

class InMemoryStateManager(StateManager):
    """In-memory implementation of state management"""
    
    def __init__(self):
        self._state: Dict[str, Any] = {}
        self._metadata: Dict[str, StateMetadata] = {}
    
    def get_state(self, key: str, default: Any = None) -> Any:
        """Get state value
        
        Args:
            key: State key
            default: Default value if key not found
            
        Returns:
            State value
        """
        return self._state.get(key, default)
    
    def set_state(self, key: str, value: Any) -> None:
        """Set state value
        
        Args:
            key: State key
            value: State value
        """
        # Update state
        self._state[key] = value
        
        # Update metadata
        now = datetime.now()
        if key in self._metadata:
            self._metadata[key].updated_at = now
        else:
            self._metadata[key] = StateMetadata(
                key=key,
                value_type=type(value).__name__,
                created_at=now,
                updated_at=now,
                size=len(json.dumps(value).encode()),
                tags={}
            )
    
    def delete_state(self, key: str) -> None:
        """Delete state value
        
        Args:
            key: State key to delete
        """
        if key in self._state:
            del self._state[key]
        if key in self._metadata:
            del self._metadata[key]
    
    def list_keys(self, pattern: Optional[str] = None) -> List[str]:
        """List state keys
        
        Args:
            pattern: Optional pattern to filter keys
            
        Returns:
            List of matching keys
        """
        keys = list(self._state.keys())
        if pattern:
            import fnmatch
            keys = fnmatch.filter(keys, pattern)
        return keys
    
    def clear_state(self) -> None:
        """Clear all state"""
        self._state.clear()
        self._metadata.clear()
    
    def get_metadata(self, key: str) -> Optional[StateMetadata]:
        """Get state metadata
        
        Args:
            key: State key
            
        Returns:
            State metadata if found
        """
        return self._metadata.get(key)
    
    def set_tags(self, key: str, tags: Dict[str, str]) -> None:
        """Set state tags
        
        Args:
            key: State key
            tags: Tags to set
        """
        if key in self._metadata:
            self._metadata[key].tags.update(tags)
    
    def get_tags(self, key: str) -> Dict[str, str]:
        """Get state tags
        
        Args:
            key: State key
            
        Returns:
            State tags
        """
        if key in self._metadata:
            return self._metadata[key].tags.copy()
        return {}
    
    def find_by_tags(self, tags: Dict[str, str]) -> List[str]:
        """Find keys by tags
        
        Args:
            tags: Tags to match
            
        Returns:
            List of matching keys
        """
        matching_keys = []
        for key, metadata in self._metadata.items():
            if all(metadata.tags.get(k) == v for k, v in tags.items()):
                matching_keys.append(key)
        return matching_keys 