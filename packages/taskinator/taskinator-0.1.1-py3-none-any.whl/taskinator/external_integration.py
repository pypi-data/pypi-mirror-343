"""External integration utilities for Taskinator."""

import json
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Union

from .utils import logger

class SyncStatus(str, Enum):
    """Synchronization status for tasks."""
    PENDING = "pending"
    SYNCED = "synced"
    CONFLICT = "conflict"
    ERROR = "error"
    DELETED = "deleted"

class SyncDirection(str, Enum):
    """Direction of synchronization."""
    LOCAL_TO_REMOTE = "local_to_remote"
    REMOTE_TO_LOCAL = "remote_to_local"
    BIDIRECTIONAL = "bidirectional"

class ExternalSystem(str, Enum):
    """Supported external systems for integration."""
    NEXTCLOUD = "nextcloud"
    GITLAB = "gitlab"
    AZURE_DEVOPS = "azure_devops"
    # Add more systems as needed

class VersionInfo:
    """Version information for task conflict resolution."""
    
    def __init__(
        self,
        version: int = 1,
        last_modified: float = None,
        modified_by: str = "local",
        changes: List[Dict[str, Any]] = None
    ):
        """Initialize version information.
        
        Args:
            version: Version number
            last_modified: Timestamp of last modification
            modified_by: Who made the modification ('local' or external system name)
            changes: List of changes made in this version
        """
        self.version = version
        self.last_modified = last_modified or datetime.now().timestamp()
        self.modified_by = modified_by
        self.changes = changes or []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "version": self.version,
            "last_modified": self.last_modified,
            "modified_by": self.modified_by,
            "changes": self.changes
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "VersionInfo":
        """Create from dictionary."""
        return cls(
            version=data.get("version", 1),
            last_modified=data.get("last_modified"),
            modified_by=data.get("modified_by", "local"),
            changes=data.get("changes", [])
        )

class ExternalSyncMetadata:
    """Metadata for external system synchronization."""
    
    def __init__(
        self,
        system: Union[ExternalSystem, str] = None,
        external_id: str = "",
        external_url: str = "",
        etag: str = "",
        last_sync: float = None,
        sync_status: Union[SyncStatus, str] = SyncStatus.PENDING,
        version_history: List[Dict[str, Any]] = None,
        additional_data: Dict[str, Any] = None
    ):
        """Initialize synchronization metadata.
        
        Args:
            system: External system identifier
            external_id: ID of the task in the external system
            external_url: URL to the task in the external system
            etag: ETag or revision identifier for the task
            last_sync: Timestamp of last synchronization
            sync_status: Current synchronization status
            version_history: History of versions for conflict resolution
            additional_data: Additional system-specific data
        """
        self.system = system if isinstance(system, ExternalSystem) else ExternalSystem(system) if system else None
        self.external_id = external_id
        self.external_url = external_url
        self.etag = etag
        self.last_sync = last_sync or datetime.now().timestamp()
        self.sync_status = sync_status if isinstance(sync_status, SyncStatus) else SyncStatus(sync_status)
        self.version_history = version_history or []
        self.additional_data = additional_data or {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "system": self.system.value if self.system else None,
            "external_id": self.external_id,
            "external_url": self.external_url,
            "etag": self.etag,
            "last_sync": self.last_sync,
            "sync_status": self.sync_status.value,
            "version_history": self.version_history,
            "additional_data": self.additional_data
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ExternalSyncMetadata":
        """Create from dictionary."""
        if not data:
            return cls()
            
        return cls(
            system=data.get("system"),
            external_id=data.get("external_id", ""),
            external_url=data.get("external_url", ""),
            etag=data.get("etag", ""),
            last_sync=data.get("last_sync"),
            sync_status=data.get("sync_status", SyncStatus.PENDING),
            version_history=data.get("version_history", []),
            additional_data=data.get("additional_data", {})
        )
    
    def add_version(self, changes: List[Dict[str, Any]], modified_by: str = "local") -> None:
        """Add a new version to the history.
        
        Args:
            changes: List of changes made in this version
            modified_by: Who made the modification ('local' or external system name)
        """
        # Find the highest version number
        max_version = 0
        for version_data in self.version_history:
            version = version_data.get("version", 0)
            if version > max_version:
                max_version = version
        
        # Create a new version
        version_info = VersionInfo(
            version=max_version + 1,
            last_modified=datetime.now().timestamp(),
            modified_by=modified_by,
            changes=changes
        )
        
        # Add to history
        self.version_history.append(version_info.to_dict())
        
        # Update last sync time
        self.last_sync = version_info.last_modified

def get_external_metadata(task: Dict[str, Any], system: Union[ExternalSystem, str] = None) -> ExternalSyncMetadata:
    """Get external synchronization metadata from a task.
    
    Args:
        task: Task dictionary
        system: External system to get metadata for (if None, returns the first found)
        
    Returns:
        External synchronization metadata
    """
    if 'external_sync' not in task:
        logger.debug("No external sync metadata found for task")
        return ExternalSyncMetadata(system=system)
    
    # If system is specified, get that specific metadata
    if system:
        system_value = system.value if isinstance(system, ExternalSystem) else system
        for sync_data in task['external_sync']:
            if sync_data.get('system') == system_value:
                logger.debug(f"Found {system_value} metadata for task")
                return ExternalSyncMetadata.from_dict(sync_data)
        
        # If not found, return empty metadata for the specified system
        logger.debug(f"No {system_value} metadata found for task")
        return ExternalSyncMetadata(system=system)
    
    # If no system specified and there's metadata, return the first one
    if task['external_sync']:
        logger.debug(f"Returning first available external sync metadata for task")
        return ExternalSyncMetadata.from_dict(task['external_sync'][0])
    
    # No metadata found
    logger.debug("No external sync metadata found for task")
    return ExternalSyncMetadata()

def update_external_metadata(
    task: Dict[str, Any],
    metadata: ExternalSyncMetadata
) -> Dict[str, Any]:
    """Update external synchronization metadata in a task.
    
    Args:
        task: Task dictionary
        metadata: External synchronization metadata
        
    Returns:
        Updated task dictionary
    """
    task_copy = task.copy()
    
    # Initialize external_sync if it doesn't exist
    if 'external_sync' not in task_copy:
        task_copy['external_sync'] = []
    
    # Check if we already have metadata for this system
    if metadata.system:
        for i, sync_data in enumerate(task_copy['external_sync']):
            if sync_data.get('system') == metadata.system.value:
                # Update existing metadata
                task_copy['external_sync'][i] = metadata.to_dict()
                return task_copy
    
    # Add new metadata
    task_copy['external_sync'].append(metadata.to_dict())
    return task_copy

def detect_changes(
    local_task: Dict[str, Any],
    remote_task: Dict[str, Any],
    field_mapping: Dict[str, str],
    system: Optional[Union[str, ExternalSystem]] = ExternalSystem.NEXTCLOUD
) -> Tuple[List[Dict[str, Any]], bool]:
    """Detect changes between local and remote tasks.
    
    Args:
        local_task: Local task data
        remote_task: Remote task data (mapped to local field names)
        field_mapping: Mapping of local field names to remote field names
        system: External system identifier
        
    Returns:
        Tuple of (changes, has_conflict)
    """
    # Get external metadata
    metadata = get_external_metadata(local_task, system)
    
    # Get last sync timestamp
    last_sync = metadata.last_sync or 0
    
    # Get local and remote update timestamps
    local_updated = local_task.get("updated", 0)
    remote_updated = remote_task.get("updated", 0)
    
    # Detect changes
    changes = []
    for local_field, remote_field in field_mapping.items():
        if local_field in local_task and remote_field in remote_task:
            local_value = local_task[local_field]
            remote_value = remote_task[remote_field]
            
            if local_value != remote_value:
                changes.append({
                    "field": local_field,
                    "local_value": local_value,
                    "remote_value": remote_value
                })
    
    # Check for conflict
    has_conflict = False
    if changes and local_updated > last_sync and remote_updated > last_sync:
        has_conflict = True
    
    return changes, has_conflict
