"""NextCloud synchronization utilities for Taskinator."""

import json
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Tuple, Union
from loguru import logger

from .nextcloud_client import NextCloudTask


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


class TaskVersionInfo:
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
            modified_by: Who made the modification ('local' or 'nextcloud')
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
    def from_dict(cls, data: Dict[str, Any]) -> "TaskVersionInfo":
        """Create from dictionary."""
        return cls(
            version=data.get("version", 1),
            last_modified=data.get("last_modified"),
            modified_by=data.get("modified_by", "local"),
            changes=data.get("changes", [])
        )


class NextCloudSyncMetadata:
    """Metadata for NextCloud synchronization."""
    
    def __init__(
        self,
        etag: str = "",
        fileid: str = "",
        last_sync: float = None,
        sync_status: Union[SyncStatus, str] = SyncStatus.PENDING,
        version_history: List[Dict[str, Any]] = None
    ):
        """Initialize synchronization metadata.
        
        Args:
            etag: NextCloud ETag for the task
            fileid: NextCloud file ID for the task
            last_sync: Timestamp of last synchronization
            sync_status: Current synchronization status
            version_history: History of versions for conflict resolution
        """
        self.etag = etag
        self.fileid = fileid
        self.last_sync = last_sync or datetime.now().timestamp()
        self.sync_status = sync_status if isinstance(sync_status, SyncStatus) else SyncStatus(sync_status)
        self.version_history = version_history or []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "etag": self.etag,
            "fileid": self.fileid,
            "last_sync": self.last_sync,
            "sync_status": self.sync_status.value,
            "version_history": self.version_history
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "NextCloudSyncMetadata":
        """Create from dictionary."""
        if not data:
            return cls()
            
        return cls(
            etag=data.get("etag", ""),
            fileid=data.get("fileid", ""),
            last_sync=data.get("last_sync"),
            sync_status=data.get("sync_status", SyncStatus.PENDING),
            version_history=data.get("version_history", [])
        )
    
    def add_version(self, changes: List[Dict[str, Any]], modified_by: str = "local") -> None:
        """Add a new version to the history.
        
        Args:
            changes: List of changes made in this version
            modified_by: Who made the modification ('local' or 'nextcloud')
        """
        # Get the latest version number
        latest_version = 1
        if self.version_history:
            latest_version = max(v.get("version", 0) for v in self.version_history) + 1
        
        # Create new version info
        version_info = TaskVersionInfo(
            version=latest_version,
            last_modified=datetime.now().timestamp(),
            modified_by=modified_by,
            changes=changes
        )
        
        # Add to history
        self.version_history.append(version_info.to_dict())
        
        # Limit history to last 10 versions to avoid excessive growth
        if len(self.version_history) > 10:
            self.version_history = self.version_history[-10:]


class TaskFieldMapping:
    """Mapping between Taskinator and NextCloud task fields."""
    
    # Mapping from Taskinator field to NextCloud field
    LOCAL_TO_REMOTE = {
        "title": "title",
        "description": "description",
        "status": "completed",  # Special handling required
        "priority": "priority",  # Special handling required
        "due_date": "due_date"  # Special handling required for date conversion
    }
    
    # Mapping from NextCloud field to Taskinator field
    REMOTE_TO_LOCAL = {
        "title": "title",
        "description": "description",
        "completed": "status",  # Special handling required
        "priority": "priority",  # Special handling required
        "due_date": "due_date"  # Special handling required for date conversion
    }
    
    @classmethod
    def map_local_to_remote(cls, task: Dict[str, Any]) -> Dict[str, Any]:
        """Map Taskinator task to NextCloud task.
        
        Args:
            task: Taskinator task
            
        Returns:
            Dictionary with NextCloud task fields
        """
        result = {}
        
        for local_field, remote_field in cls.LOCAL_TO_REMOTE.items():
            if local_field in task:
                # Special handling for status
                if local_field == "status":
                    result["completed"] = task["status"] == "done"
                # Special handling for priority
                elif local_field == "priority":
                    # Convert text priority to number (1-9, with 1 being highest)
                    if task["priority"] == "high":
                        result["priority"] = 1
                    elif task["priority"] == "medium":
                        result["priority"] = 5
                    else:  # low
                        result["priority"] = 9
                # Special handling for due date
                elif local_field == "due_date" and task.get("due_date"):
                    # Convert timestamp to datetime
                    result["due_date"] = datetime.fromtimestamp(task["due_date"])
                else:
                    result[remote_field] = task[local_field]
        
        return result
    
    @classmethod
    def map_remote_to_local(cls, remote_task: NextCloudTask) -> Dict[str, Any]:
        """Map NextCloud task to Taskinator task.
        
        Args:
            remote_task: NextCloud task
            
        Returns:
            Dictionary with Taskinator task fields
        """
        result = {}
        remote_dict = remote_task.model_dump()
        
        for remote_field, local_field in cls.REMOTE_TO_LOCAL.items():
            if remote_field in remote_dict:
                # Special handling for completed status
                if remote_field == "completed":
                    result["status"] = "done" if remote_dict["completed"] else "pending"
                # Special handling for priority
                elif remote_field == "priority" and remote_dict.get("priority") is not None:
                    # Convert number priority to text
                    priority = remote_dict["priority"]
                    if priority <= 3:
                        result["priority"] = "high"
                    elif priority <= 6:
                        result["priority"] = "medium"
                    else:
                        result["priority"] = "low"
                # Special handling for due date
                elif remote_field == "due_date" and remote_dict.get("due_date"):
                    # Convert datetime to timestamp
                    result["due_date"] = remote_dict["due_date"].timestamp()
                else:
                    result[local_field] = remote_dict[remote_field]
        
        return result


def get_nextcloud_metadata(task: Dict[str, Any]) -> NextCloudSyncMetadata:
    """Get NextCloud synchronization metadata from a task.
    
    Args:
        task: Task dictionary
        
    Returns:
        NextCloud synchronization metadata
    """
    if "nextcloud" not in task:
        logger.debug("No NextCloud metadata found for task")
        return NextCloudSyncMetadata()
    
    logger.debug("NextCloud metadata found for task: %s", task["nextcloud"])
    return NextCloudSyncMetadata.from_dict(task["nextcloud"])


def update_nextcloud_metadata(
    task: Dict[str, Any],
    metadata: NextCloudSyncMetadata
) -> Dict[str, Any]:
    """Update NextCloud synchronization metadata in a task.
    
    Args:
        task: Task dictionary
        metadata: NextCloud synchronization metadata
        
    Returns:
        Updated task dictionary
    """
    task_copy = task.copy()
    task_copy["nextcloud"] = metadata.to_dict()
    return task_copy


def detect_changes(
    local_task: Dict[str, Any],
    remote_task: NextCloudTask
) -> Tuple[List[Dict[str, Any]], bool]:
    """Detect changes between local and remote tasks.
    
    Args:
        local_task: Local task
        remote_task: Remote task
        
    Returns:
        Tuple of (list of changes, has_conflict)
    """
    changes = []
    has_conflict = False
    
    # Convert remote task to dictionary
    remote_dict = TaskFieldMapping.map_remote_to_local(remote_task)
    
    # Check each field in the mapping
    for local_field in TaskFieldMapping.LOCAL_TO_REMOTE.keys():
        if local_field in local_task and local_field in remote_dict:
            local_value = local_task[local_field]
            remote_value = remote_dict[local_field]
            
            if local_value != remote_value:
                changes.append({
                    "field": local_field,
                    "local_value": local_value,
                    "remote_value": remote_value
                })
                
                # Check for conflict (both sides modified)
                metadata = get_nextcloud_metadata(local_task)
                if metadata.version_history:
                    last_version = metadata.version_history[-1]
                    last_sync = metadata.last_sync
                    
                    # If both local and remote were modified since last sync
                    if (local_task["updated"] > last_sync and 
                            remote_task.modified and 
                            remote_task.modified.timestamp() > last_sync):
                        has_conflict = True
    
    return changes, has_conflict
