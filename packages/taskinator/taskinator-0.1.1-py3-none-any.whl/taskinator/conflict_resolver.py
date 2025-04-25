"""Conflict resolution for NextCloud task synchronization."""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Union
from loguru import logger

from .nextcloud_client import NextCloudTask
from .nextcloud_sync import (
    NextCloudSyncMetadata,
    SyncDirection,
    SyncStatus,
    TaskFieldMapping,
    get_nextcloud_metadata,
    update_nextcloud_metadata
)
from .resolution_strategies import StrategyFactory, ResolutionStrategy


class ConflictResolutionStrategy(str, Enum):
    """Strategy for resolving conflicts."""
    LOCAL_WINS = "local_wins"
    REMOTE_WINS = "remote_wins"
    NEWEST_WINS = "newest_wins"
    MANUAL = "manual"


class ConflictResolver:
    """Handles conflict detection and resolution between local and remote tasks."""
    
    def __init__(self, default_strategy: ConflictResolutionStrategy = ConflictResolutionStrategy.NEWEST_WINS):
        """Initialize conflict resolver.
        
        Args:
            default_strategy: Default strategy for resolving conflicts
        """
        self.default_strategy = default_strategy
    
    def detect_conflict(
        self,
        local_task: Dict[str, Any],
        remote_task: NextCloudTask
    ) -> bool:
        """Detect if there is a conflict between local and remote tasks.
        
        Args:
            local_task: Local task
            remote_task: Remote task
            
        Returns:
            True if there is a conflict, False otherwise
        """
        # Get metadata
        metadata = get_nextcloud_metadata(local_task)
        last_sync = metadata.last_sync
        
        # Check if both sides were modified since last sync
        local_modified = local_task.get("updated", 0) > last_sync
        
        remote_modified = False
        if remote_task.modified:
            remote_modified = remote_task.modified.timestamp() > last_sync
        
        return local_modified and remote_modified
    
    def resolve_conflict(
        self,
        local_task: Dict[str, Any],
        remote_task: NextCloudTask,
        strategy: Optional[ConflictResolutionStrategy] = None
    ) -> Tuple[Dict[str, Any], bool]:
        """Resolve conflict between local and remote tasks.
        
        Args:
            local_task: Local task
            remote_task: Remote task
            strategy: Strategy for resolving the conflict
            
        Returns:
            Tuple of (resolved task, was_conflict)
        """
        # Use default strategy if none provided
        if strategy is None:
            strategy = self.default_strategy
        
        # Check if there's a conflict
        if not self.detect_conflict(local_task, remote_task):
            return local_task, False
        
        # Get metadata
        metadata = get_nextcloud_metadata(local_task)
        
        # Mark as conflict in metadata
        metadata.sync_status = SyncStatus.CONFLICT
        
        # Create strategy instance using factory
        strategy_instance = StrategyFactory.create_strategy(strategy.value)
        
        # Resolve conflict using strategy
        resolved_task, changes = strategy_instance.resolve(local_task, remote_task)
        
        # Add version entry to track the conflict and resolution
        if changes:
            metadata.add_version(
                changes=changes,
                modified_by=f"conflict_resolution_{strategy.value}"
            )
        
        # Update metadata in the resolved task
        resolved_task = update_nextcloud_metadata(resolved_task, metadata)
        
        # Update timestamp
        resolved_task["updated"] = datetime.now().timestamp()
        
        return resolved_task, True
    
    def get_conflicts(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Get all tasks with conflicts.
        
        Args:
            tasks: List of tasks
            
        Returns:
            List of tasks with conflicts
        """
        return [
            task for task in tasks
            if "nextcloud" in task and task["nextcloud"].get("sync_status") == SyncStatus.CONFLICT.value
        ]


class ManualConflictResolver:
    """Handles manual resolution of conflicts."""
    
    def resolve_field_conflict(
        self,
        task: Dict[str, Any],
        field: str,
        resolution: str  # 'local' or 'remote'
    ) -> Dict[str, Any]:
        """Resolve a specific field conflict.
        
        Args:
            task: Task with conflict
            field: Field name to resolve
            resolution: Resolution choice ('local' or 'remote')
            
        Returns:
            Updated task
        """
        # Get metadata
        metadata = get_nextcloud_metadata(task)
        
        # Find the conflict in version history
        conflict_version = None
        for version in reversed(metadata.version_history):
            changes = version.get("changes", [])
            for change in changes:
                if change.get("field") == field and change.get("resolution") == "manual":
                    conflict_version = version
                    break
            if conflict_version:
                break
        
        if not conflict_version:
            logger.warning(f"No manual conflict found for field {field} in task {task.get('id')}")
            return task
        
        # Update the task based on resolution
        updated_task = task.copy()
        
        # Find the change for this field
        for change in conflict_version.get("changes", []):
            if change.get("field") == field:
                if resolution == "local":
                    # Keep local value (already in the task)
                    change["resolution"] = "local"
                else:
                    # Use remote value
                    updated_task[field] = change.get("remote_value")
                    change["resolution"] = "remote"
        
        # Check if all conflicts are resolved
        all_resolved = True
        for version in metadata.version_history:
            for change in version.get("changes", []):
                if change.get("resolution") == "manual":
                    all_resolved = False
                    break
            if not all_resolved:
                break
        
        # Only change status if all conflicts are resolved
        if all_resolved:
            metadata.sync_status = SyncStatus.PENDING
        else:
            # Keep the conflict status
            metadata.sync_status = SyncStatus.CONFLICT
        
        # Update metadata in the task
        updated_task = update_nextcloud_metadata(updated_task, metadata)
        
        # Update timestamp
        updated_task["updated"] = datetime.now().timestamp()
        
        return updated_task
    
    def get_field_conflicts(self, task: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get all field conflicts for a task.
        
        Args:
            task: Task to check
            
        Returns:
            List of field conflicts
        """
        conflicts = []
        
        # Get metadata
        metadata = get_nextcloud_metadata(task)
        
        # Check version history for manual conflicts
        for version in metadata.version_history:
            for change in version.get("changes", []):
                if change.get("resolution") == "manual":
                    conflicts.append({
                        "field": change.get("field"),
                        "local_value": change.get("local_value"),
                        "remote_value": change.get("remote_value"),
                        "version": version.get("version")
                    })
        
        return conflicts
