"""Resolution strategies for conflict resolution in Taskinator."""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Tuple, Union
from datetime import datetime
from loguru import logger

from .nextcloud_client import NextCloudTask
from .nextcloud_sync import (
    NextCloudSyncMetadata,
    SyncStatus,
    TaskFieldMapping,
    get_nextcloud_metadata,
    update_nextcloud_metadata
)


class ResolutionStrategy(ABC):
    """Abstract base class for conflict resolution strategies."""
    
    @abstractmethod
    def resolve(
        self,
        local_task: Dict[str, Any],
        remote_task: NextCloudTask
    ) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        """Resolve conflict between local and remote tasks.
        
        Args:
            local_task: Local task
            remote_task: Remote task
            
        Returns:
            Tuple of (resolved task, changes)
        """
        pass
    
    def _get_common_changes(
        self,
        local_task: Dict[str, Any],
        remote_dict: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Get common changes between local and remote tasks.
        
        Args:
            local_task: Local task
            remote_dict: Remote task in local format
            
        Returns:
            List of changes
        """
        changes = []
        for field in TaskFieldMapping.LOCAL_TO_REMOTE.keys():
            if field in local_task and field in remote_dict and local_task[field] != remote_dict[field]:
                changes.append({
                    "field": field,
                    "local_value": local_task[field],
                    "remote_value": remote_dict[field],
                    "resolution": None  # Will be set by the specific strategy
                })
        return changes


class LocalWinsStrategy(ResolutionStrategy):
    """Strategy that always chooses local values over remote values."""
    
    def resolve(
        self,
        local_task: Dict[str, Any],
        remote_task: NextCloudTask
    ) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        """Resolve conflict by keeping local values.
        
        Args:
            local_task: Local task
            remote_task: Remote task
            
        Returns:
            Tuple of (resolved task, changes)
        """
        logger.info(f"Conflict resolved with LOCAL_WINS for task {local_task.get('id')}")
        
        # Convert remote task to local format for comparison
        remote_dict = TaskFieldMapping.map_remote_to_local(remote_task)
        
        # Get changes
        changes = self._get_common_changes(local_task, remote_dict)
        
        # Mark all changes as using local values
        for change in changes:
            change["resolution"] = "local"
        
        # Local wins, so just return the local task unchanged
        return local_task.copy(), changes


class RemoteWinsStrategy(ResolutionStrategy):
    """Strategy that always chooses remote values over local values."""
    
    def resolve(
        self,
        local_task: Dict[str, Any],
        remote_task: NextCloudTask
    ) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        """Resolve conflict by using remote values.
        
        Args:
            local_task: Local task
            remote_task: Remote task
            
        Returns:
            Tuple of (resolved task, changes)
        """
        logger.info(f"Conflict resolved with REMOTE_WINS for task {local_task.get('id')}")
        
        # Convert remote task to local format for comparison
        remote_dict = TaskFieldMapping.map_remote_to_local(remote_task)
        
        # Create a copy of the local task to modify
        resolved_task = local_task.copy()
        
        # Get changes
        changes = self._get_common_changes(local_task, remote_dict)
        
        # Update with remote values and mark all changes as using remote values
        for change in changes:
            change["resolution"] = "remote"
            field = change["field"]
            resolved_task[field] = remote_dict[field]
        
        return resolved_task, changes


class NewestWinsStrategy(ResolutionStrategy):
    """Strategy that chooses the newest values based on timestamps."""
    
    def resolve(
        self,
        local_task: Dict[str, Any],
        remote_task: NextCloudTask
    ) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        """Resolve conflict by using the newest values.
        
        Args:
            local_task: Local task
            remote_task: Remote task
            
        Returns:
            Tuple of (resolved task, changes)
        """
        logger.info(f"Conflict resolved with NEWEST_WINS for task {local_task.get('id')}")
        
        # Convert remote task to local format for comparison
        remote_dict = TaskFieldMapping.map_remote_to_local(remote_task)
        
        # Create a copy of the local task to modify
        resolved_task = local_task.copy()
        
        # Get timestamps
        local_updated = local_task.get("updated", 0)
        remote_updated = remote_task.modified.timestamp() if remote_task.modified else 0
        
        # Get changes
        changes = self._get_common_changes(local_task, remote_dict)
        
        # Update based on which is newer
        for change in changes:
            field = change["field"]
            
            # Determine which version is newer
            if local_updated > remote_updated:
                # Local is newer
                change["resolution"] = "local"
            else:
                # Remote is newer
                change["resolution"] = "remote"
                resolved_task[field] = remote_dict[field]
        
        return resolved_task, changes


class ManualStrategy(ResolutionStrategy):
    """Strategy that marks conflicts for manual resolution."""
    
    def resolve(
        self,
        local_task: Dict[str, Any],
        remote_task: NextCloudTask
    ) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        """Mark conflicts for manual resolution.
        
        Args:
            local_task: Local task
            remote_task: Remote task
            
        Returns:
            Tuple of (resolved task, changes)
        """
        logger.info(f"Conflict marked for MANUAL resolution for task {local_task.get('id')}")
        
        # Convert remote task to local format for comparison
        remote_dict = TaskFieldMapping.map_remote_to_local(remote_task)
        
        # Get changes
        changes = self._get_common_changes(local_task, remote_dict)
        
        # Mark all changes for manual resolution
        for change in changes:
            change["resolution"] = "manual"
        
        # Return the local task unchanged, but with conflicts marked
        return local_task.copy(), changes


class StrategyFactory:
    """Factory for creating resolution strategies."""
    
    @staticmethod
    def create_strategy(strategy_name: str) -> ResolutionStrategy:
        """Create a resolution strategy based on the strategy name.
        
        Args:
            strategy_name: Name of the strategy
            
        Returns:
            Resolution strategy
            
        Raises:
            ValueError: If the strategy name is invalid
        """
        if strategy_name == "local_wins":
            return LocalWinsStrategy()
        elif strategy_name == "remote_wins":
            return RemoteWinsStrategy()
        elif strategy_name == "newest_wins":
            return NewestWinsStrategy()
        elif strategy_name == "manual":
            return ManualStrategy()
        else:
            raise ValueError(f"Invalid strategy name: {strategy_name}")
