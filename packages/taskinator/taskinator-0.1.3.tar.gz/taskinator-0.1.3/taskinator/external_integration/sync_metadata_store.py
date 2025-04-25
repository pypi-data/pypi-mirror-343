"""Sync metadata store for external integrations."""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

import logging

log = logging.getLogger(__name__)

class SyncMetadataStore:
    """Store for synchronization metadata.
    
    This class provides a persistent storage mechanism for synchronization metadata,
    decoupling it from the tasks themselves. This allows for more robust synchronization
    even when tasks are deleted or modified on either side.
    """
    
    def __init__(self, store_dir: Path):
        """Initialize the sync metadata store.
        
        Args:
            store_dir: Directory to store metadata in
        """
        self.store_dir = store_dir
        self.store_file = store_dir / "sync_metadata.json"
        self.metadata = self._load_metadata()
    
    def _load_metadata(self) -> Dict[str, Dict[str, Any]]:
        """Load metadata from disk.
        
        Returns:
            Dictionary of metadata keyed by task ID and system
        """
        if not self.store_file.exists():
            return {}
        
        try:
            with open(self.store_file, "r") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading sync metadata: {e}")
            return {}
    
    def _save_metadata(self):
        """Save metadata to disk."""
        # Ensure directory exists
        os.makedirs(self.store_dir, exist_ok=True)
        
        try:
            with open(self.store_file, "w") as f:
                json.dump(self.metadata, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving sync metadata: {e}")
    
    def get_metadata(self, task_id: int, system: str) -> Dict[str, Any]:
        """Get metadata for a task and system.
        
        Args:
            task_id: Task ID
            system: External system name
            
        Returns:
            Metadata dictionary
        """
        task_key = str(task_id)
        if task_key not in self.metadata:
            return {}
        
        return self.metadata[task_key].get(system, {})
    
    def update_metadata(self, task_id: int, system: str, metadata: Dict[str, Any]):
        """Update metadata for a task and system.
        
        Args:
            task_id: Task ID
            system: External system name
            metadata: Metadata dictionary
        """
        task_key = str(task_id)
        if task_key not in self.metadata:
            self.metadata[task_key] = {}
        
        # Add timestamp
        metadata["last_updated"] = datetime.now().timestamp()
        
        self.metadata[task_key][system] = metadata
        self._save_metadata()
    
    def delete_metadata(self, task_id: int, system: Optional[str] = None):
        """Delete metadata for a task.
        
        Args:
            task_id: Task ID
            system: External system name, or None to delete all metadata for the task
        """
        task_key = str(task_id)
        if task_key not in self.metadata:
            return
        
        if system is None:
            # Delete all metadata for the task
            del self.metadata[task_key]
        elif system in self.metadata[task_key]:
            # Delete metadata for the specific system
            del self.metadata[task_key][system]
            
            # If no more systems, delete the task entry
            if not self.metadata[task_key]:
                del self.metadata[task_key]
        
        self._save_metadata()
    
    def list_tasks(self, system: Optional[str] = None) -> List[int]:
        """List tasks that have metadata.
        
        Args:
            system: External system name, or None to list all tasks
            
        Returns:
            List of task IDs
        """
        if system is None:
            # Return all tasks
            return [int(task_id) for task_id in self.metadata.keys()]
        
        # Return tasks for the specific system
        return [
            int(task_id) for task_id, systems in self.metadata.items()
            if system in systems
        ]
    
    def get_external_id(self, task_id: int, system: str) -> Optional[str]:
        """Get external ID for a task and system.
        
        Args:
            task_id: Task ID
            system: External system name
            
        Returns:
            External ID or None if not found
        """
        metadata = self.get_metadata(task_id, system)
        return metadata.get("external_id")
    
    def set_external_id(self, task_id: int, system: str, external_id: str):
        """Set external ID for a task and system.
        
        Args:
            task_id: Task ID
            system: External system name
            external_id: External ID
        """
        metadata = self.get_metadata(task_id, system)
        metadata["external_id"] = external_id
        self.update_metadata(task_id, system, metadata)
    
    def get_sync_status(self, task_id: int, system: str) -> str:
        """Get sync status for a task and system.
        
        Args:
            task_id: Task ID
            system: External system name
            
        Returns:
            Sync status or "unknown" if not found
        """
        metadata = self.get_metadata(task_id, system)
        return metadata.get("sync_status", "unknown")
    
    def set_sync_status(self, task_id: int, system: str, status: str):
        """Set sync status for a task and system.
        
        Args:
            task_id: Task ID
            system: External system name
            status: Sync status
        """
        metadata = self.get_metadata(task_id, system)
        metadata["sync_status"] = status
        self.update_metadata(task_id, system, metadata)
