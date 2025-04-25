"""Version tracking system for Taskinator.

This module provides version tracking functionality for tasks to detect
conflicts between local and remote changes during synchronization.
"""

import uuid
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple, Union

from .constants import SyncStatus, ExternalSystem

log = logging.getLogger(__name__)

class VersionInfo:
    """Version information for a task.
    
    Attributes:
        version_id: Unique identifier for this version
        timestamp: Timestamp when this version was created
        sequence: Sequence number for this version
        base_version_id: ID of the version this was based on
        system: External system identifier
    """
    
    def __init__(
        self,
        version_id: str = None,
        timestamp: float = None,
        sequence: int = 1,
        base_version_id: str = None,
        system: str = None
    ):
        """Initialize version information.
        
        Args:
            version_id: Unique identifier for this version
            timestamp: Timestamp when this version was created
            sequence: Sequence number for this version
            base_version_id: ID of the version this was based on
            system: External system identifier
        """
        self.version_id = version_id or str(uuid.uuid4())
        self.timestamp = timestamp or datetime.now().timestamp()
        self.sequence = sequence
        self.base_version_id = base_version_id
        self.system = system
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary.
        
        Returns:
            Dictionary representation of this version info
        """
        return {
            "version_id": self.version_id,
            "timestamp": self.timestamp,
            "sequence": self.sequence,
            "base_version_id": self.base_version_id,
            "system": self.system
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'VersionInfo':
        """Create from dictionary.
        
        Args:
            data: Dictionary representation of version info
            
        Returns:
            VersionInfo instance
        """
        return cls(
            version_id=data.get("version_id"),
            timestamp=data.get("timestamp"),
            sequence=data.get("sequence", 1),
            base_version_id=data.get("base_version_id"),
            system=data.get("system")
        )


class VersionTracker:
    """Version tracking system for tasks.
    
    This class provides functionality for tracking versions of tasks
    and detecting conflicts between local and remote changes.
    """
    
    def __init__(self, metadata_store=None):
        """Initialize version tracker.
        
        Args:
            metadata_store: Metadata store for persisting version information
        """
        self.metadata_store = metadata_store
    
    def get_version_info(self, task_id: Union[str, int], system: str) -> Optional[VersionInfo]:
        """Get version information for a task.
        
        Args:
            task_id: Task ID
            system: External system identifier
            
        Returns:
            VersionInfo if found, None otherwise
        """
        if not self.metadata_store:
            return None
            
        metadata = self.metadata_store.get_metadata(task_id, system)
        if not metadata or "version" not in metadata:
            return None
            
        return VersionInfo.from_dict(metadata["version"])
    
    def update_version(
        self, 
        task_id: Union[str, int], 
        system: str,
        base_version_id: str = None
    ) -> VersionInfo:
        """Update version information for a task.
        
        Args:
            task_id: Task ID
            system: External system identifier
            base_version_id: ID of the version this was based on
            
        Returns:
            Updated VersionInfo
        """
        if not self.metadata_store:
            return None
            
        # Get current metadata
        metadata = self.metadata_store.get_metadata(task_id, system)
        
        # Get current version info if it exists
        current_version = None
        if metadata and "version" in metadata:
            current_version = VersionInfo.from_dict(metadata["version"])
            
        # Create new version info
        new_version = VersionInfo(
            sequence=(current_version.sequence + 1 if current_version else 1),
            base_version_id=base_version_id or (current_version.version_id if current_version else None),
            system=system
        )
        
        # Update metadata with new version
        if not metadata:
            metadata = {
                "task_id": task_id,
                "system": system,
                "version": new_version.to_dict()
            }
        else:
            metadata["version"] = new_version.to_dict()
            
        # Save updated metadata
        self.metadata_store.save_metadata(task_id, system, metadata)
        
        return new_version
    
    def detect_conflict(
        self, 
        local_version: VersionInfo, 
        remote_version: VersionInfo
    ) -> bool:
        """Detect if there is a conflict between versions.
        
        A conflict exists when both local and remote versions have been
        modified since their common base version.
        
        Args:
            local_version: Local version info
            remote_version: Remote version info
            
        Returns:
            True if conflict detected, False otherwise
        """
        if not local_version or not remote_version:
            return False
            
        # If they have the same base version but different version IDs,
        # then they've both been modified since the common base
        if (local_version.base_version_id == remote_version.base_version_id and
            local_version.version_id != remote_version.version_id):
            return True
            
        # If one is based on the other but has been modified since,
        # then there's no conflict (one-way change)
        if local_version.base_version_id == remote_version.version_id:
            return False
            
        if remote_version.base_version_id == local_version.version_id:
            return False
            
        # If they have different base versions, we need more analysis
        # This could indicate a complex conflict scenario
        if local_version.base_version_id != remote_version.base_version_id:
            # If we can't determine the relationship, assume conflict
            return True
            
        return False
    
    def get_newer_version(
        self, 
        version1: VersionInfo, 
        version2: VersionInfo
    ) -> VersionInfo:
        """Determine which version is newer.
        
        Args:
            version1: First version
            version2: Second version
            
        Returns:
            The newer version, or version1 if they're equal
        """
        if not version1:
            return version2
            
        if not version2:
            return version1
            
        # Compare timestamps first
        if version1.timestamp > version2.timestamp:
            return version1
        elif version2.timestamp > version1.timestamp:
            return version2
            
        # If timestamps are equal, compare sequence numbers
        if version1.sequence > version2.sequence:
            return version1
        elif version2.sequence > version1.sequence:
            return version2
            
        # If everything is equal, return version1
        return version1
    
    def track_sync(
        self, 
        task_id: Union[str, int], 
        system: str, 
        status: str = SyncStatus.SYNCED
    ) -> Dict[str, Any]:
        """Track a synchronization event.
        
        Args:
            task_id: Task ID
            system: External system identifier
            status: Sync status
            
        Returns:
            Updated metadata
        """
        if not self.metadata_store:
            return {}
            
        # Get current metadata
        metadata = self.metadata_store.get_metadata(task_id, system)
        if not metadata:
            metadata = {
                "task_id": task_id,
                "system": system,
                "sync_status": status,
                "last_sync": datetime.now().timestamp()
            }
        else:
            metadata["sync_status"] = status
            metadata["last_sync"] = datetime.now().timestamp()
            
        # Update version info if this was a successful sync
        if status == SyncStatus.SYNCED:
            # Get current version info
            current_version = None
            if "version" in metadata:
                current_version = VersionInfo.from_dict(metadata["version"])
                
            # Create new version with the same ID but updated timestamp
            # This represents that local and remote are now in sync
            new_version = VersionInfo(
                version_id=current_version.version_id if current_version else None,
                sequence=current_version.sequence if current_version else 1,
                base_version_id=current_version.version_id if current_version else None,
                system=system
            )
            
            metadata["version"] = new_version.to_dict()
            
        # Save updated metadata
        self.metadata_store.save_metadata(task_id, system, metadata)
        
        return metadata
