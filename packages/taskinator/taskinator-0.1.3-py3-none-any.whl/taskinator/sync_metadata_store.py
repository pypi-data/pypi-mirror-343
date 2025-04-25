"""Metadata store for external synchronization."""

import json
import logging
import os
from pathlib import Path
from typing import Dict, Any, List, Optional

from .constants import SyncStatus, ExternalSystem

log = logging.getLogger(__name__)

class SyncMetadataStore:
    """Store for synchronization metadata.
    
    This class provides methods for storing and retrieving metadata
    about external synchronization for tasks.
    """
    
    def __init__(self, base_dir: Optional[Path] = None):
        """Initialize the metadata store.
        
        Args:
            base_dir: Base directory for storing metadata files
        """
        self.base_dir = base_dir
        if self.base_dir:
            self.metadata_dir = self.base_dir / "sync_metadata"
            os.makedirs(self.metadata_dir, exist_ok=True)
        
    def get_metadata(self, task_id: int, system: str) -> Dict[str, Any]:
        """Get metadata for a task and system.
        
        Args:
            task_id: Task ID
            system: External system
            
        Returns:
            Metadata dictionary
        """
        if not self.base_dir:
            return {}
            
        metadata_file = self.metadata_dir / f"{task_id}_{system}.json"
        
        if not metadata_file.exists():
            return {}
            
        try:
            with open(metadata_file, "r") as f:
                return json.load(f)
        except Exception as e:
            log.error(f"Error reading metadata for task {task_id} and system {system}: {e}")
            return {}
            
    def save_metadata(self, task_id: int, system: str, metadata: Dict[str, Any]) -> None:
        """Save metadata for a task and system.
        
        Args:
            task_id: Task ID
            system: External system
            metadata: Metadata dictionary
        """
        if not self.base_dir:
            return
            
        metadata_file = self.metadata_dir / f"{task_id}_{system}.json"
        
        try:
            with open(metadata_file, "w") as f:
                json.dump(metadata, f, indent=2)
        except Exception as e:
            log.error(f"Error saving metadata for task {task_id} and system {system}: {e}")
            
    def update_metadata(self, task_id: int, system: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update metadata for a task and system.
        
        Args:
            task_id: Task ID
            system: External system
            updates: Updates to apply to metadata
            
        Returns:
            Updated metadata dictionary
        """
        metadata = self.get_metadata(task_id, system)
        metadata.update(updates)
        self.save_metadata(task_id, system, metadata)
        return metadata
        
    def delete_metadata(self, task_id: int, system: str) -> None:
        """Delete metadata for a task and system.
        
        Args:
            task_id: Task ID
            system: External system
        """
        if not self.base_dir:
            return
            
        metadata_file = self.metadata_dir / f"{task_id}_{system}.json"
        
        if metadata_file.exists():
            try:
                os.remove(metadata_file)
            except Exception as e:
                log.error(f"Error deleting metadata for task {task_id} and system {system}: {e}")
                
    def find_by_external_id(self, system: str, external_id: str) -> Optional[Dict[str, Any]]:
        """Find metadata by external ID.
        
        Args:
            system: External system
            external_id: External ID
            
        Returns:
            Metadata dictionary if found, None otherwise
        """
        if not self.base_dir:
            return None
            
        # Iterate through all metadata files for the system
        for metadata_file in self.metadata_dir.glob(f"*_{system}.json"):
            try:
                with open(metadata_file, "r") as f:
                    metadata = json.load(f)
                    
                if metadata.get("external_id") == external_id:
                    # Extract task ID from filename
                    filename = metadata_file.name
                    task_id = int(filename.split("_")[0])
                    metadata["task_id"] = task_id
                    return metadata
            except Exception as e:
                log.error(f"Error reading metadata file {metadata_file}: {e}")
                
        return None
        
    def get_all_task_ids(self, system: str) -> List[int]:
        """Get all task IDs that have metadata for a specific system.
        
        Args:
            system: External system
            
        Returns:
            List of task IDs
        """
        if not self.base_dir:
            return []
            
        task_ids = []
        
        # Iterate through all metadata files for the system
        for metadata_file in self.metadata_dir.glob(f"*_{system}.json"):
            try:
                # Extract task ID from filename
                filename = metadata_file.name
                task_id = int(filename.split("_")[0])
                task_ids.append(task_id)
            except Exception as e:
                log.error(f"Error extracting task ID from metadata file {metadata_file}: {e}")
                
        return task_ids
