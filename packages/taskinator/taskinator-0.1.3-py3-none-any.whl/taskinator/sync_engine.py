"""Synchronization engine for NextCloud integration."""

import asyncio
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, Union

from .conflict_resolver import ConflictResolver, ConflictResolutionStrategy
from .nextcloud_client import NextCloudClient, NextCloudTask
from .nextcloud_sync import (
    NextCloudSyncMetadata,
    SyncDirection,
    SyncStatus,
    TaskFieldMapping,
    get_nextcloud_metadata,
    update_nextcloud_metadata
)
from .utils import logger


class SyncEngine:
    """Engine for synchronizing tasks between Taskinator and NextCloud."""
    
    def __init__(
        self,
        nextcloud_client: NextCloudClient,
        conflict_strategy: ConflictResolutionStrategy = ConflictResolutionStrategy.NEWEST_WINS
    ):
        """Initialize the sync engine.
        
        Args:
            nextcloud_client: NextCloud client
            conflict_strategy: Strategy for resolving conflicts
        """
        self.nextcloud_client = nextcloud_client
        self.conflict_resolver = ConflictResolver(default_strategy=conflict_strategy)
    
    async def sync_task(
        self,
        task: Dict[str, Any],
        direction: SyncDirection = SyncDirection.BIDIRECTIONAL
    ) -> Dict[str, Any]:
        """Synchronize a single task.
        
        Args:
            task: Task to synchronize
            direction: Direction of synchronization
            
        Returns:
            Updated task
        """
        # Get metadata
        metadata = get_nextcloud_metadata(task)
        
        # Check if we have a NextCloud ID
        if not metadata.fileid and direction != SyncDirection.LOCAL_TO_REMOTE:
            # We can't sync from remote without an ID
            logger.info(f"No NextCloud ID for task {task.get('id')}, forcing LOCAL_TO_REMOTE")
            direction = SyncDirection.LOCAL_TO_REMOTE
        
        try:
            if direction == SyncDirection.LOCAL_TO_REMOTE:
                # Push local changes to NextCloud
                updated_task = await self._push_to_nextcloud(task)
            elif direction == SyncDirection.REMOTE_TO_LOCAL:
                # Pull remote changes to local
                updated_task = await self._pull_from_nextcloud(task)
            else:  # BIDIRECTIONAL
                # Perform bidirectional sync
                updated_task = await self._sync_bidirectional(task)
            
            return updated_task
            
        except Exception as e:
            logger.error(f"Error syncing task {task.get('id')}: {e}")
            
            # Update metadata to reflect error
            metadata.sync_status = SyncStatus.ERROR
            return update_nextcloud_metadata(task, metadata)
    
    async def sync_all_tasks(
        self,
        tasks: List[Dict[str, Any]],
        direction: SyncDirection = SyncDirection.BIDIRECTIONAL
    ) -> List[Dict[str, Any]]:
        """Synchronize all tasks.
        
        Args:
            tasks: List of tasks to synchronize
            direction: Direction of synchronization
            
        Returns:
            List of updated tasks
        """
        updated_tasks = []
        
        for task in tasks:
            updated_task = await self.sync_task(task, direction)
            updated_tasks.append(updated_task)
            
            # Process subtasks if any
            if "subtasks" in task and task["subtasks"]:
                updated_subtasks = []
                for subtask in task["subtasks"]:
                    # Add parent task ID to subtask for reference
                    subtask_with_parent = subtask.copy()
                    subtask_with_parent["parent_id"] = task["id"]
                    
                    updated_subtask = await self.sync_task(subtask_with_parent, direction)
                    updated_subtasks.append(updated_subtask)
                
                # Update subtasks in the task
                updated_task["subtasks"] = updated_subtasks
        
        return updated_tasks
    
    async def _push_to_nextcloud(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Push a task to NextCloud.
        
        Args:
            task: Task to push
            
        Returns:
            Updated task
        """
        # Get metadata
        metadata = get_nextcloud_metadata(task)
        
        # Map task to NextCloud format
        nextcloud_task_data = TaskFieldMapping.map_local_to_remote(task)
        
        try:
            if metadata.fileid:
                # Update existing task
                logger.info(f"Updating NextCloud task {metadata.fileid} for local task {task.get('id')}")
                logger.debug(f"About to call update_unified_task with data: {nextcloud_task_data}")
                remote_task = await self.nextcloud_client.update_unified_task(metadata.fileid, nextcloud_task_data)
                logger.debug(f"Type after update_unified_task: {type(remote_task)}, value: {remote_task}")
            else:
                # Create new task
                logger.info(f"Creating new NextCloud task for local task {task.get('id')}")
                logger.debug(f"About to call create_unified_task with data: {nextcloud_task_data}")
                remote_task = await self.nextcloud_client.create_unified_task(nextcloud_task_data)
                logger.debug(f"Type after create_unified_task: {type(remote_task)}, value: {remote_task}")
            
            # Debug log for etag
            logger.debug(f"remote_task.etag: {getattr(remote_task, 'etag', None)}")
            # Update metadata
            metadata.etag = getattr(remote_task, 'etag', '') or ''
            metadata.fileid = getattr(remote_task, 'id', '') or getattr(remote_task, 'fileid', '')
            metadata.last_sync = datetime.now().timestamp()
            metadata.sync_status = SyncStatus.SYNCED
            
            # Record changes in version history
            changes = [{"field": field, "value": task.get(field)} for field in TaskFieldMapping.LOCAL_TO_REMOTE.keys() if field in task]
            metadata.add_version(changes=changes, modified_by="local")
            
            # Update task with metadata
            updated_task = update_nextcloud_metadata(task, metadata)
            
            return updated_task
            
        except Exception as e:
            logger.error(f"Error pushing task {task.get('id')} to NextCloud: {e}")
            metadata.sync_status = SyncStatus.ERROR
            return update_nextcloud_metadata(task, metadata)
    
    async def _pull_from_nextcloud(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Pull a task from NextCloud.
        
        Args:
            task: Task to update
            
        Returns:
            Updated task
        """
        # Get metadata
        metadata = get_nextcloud_metadata(task)
        
        if not metadata.fileid:
            logger.error(f"Cannot pull task {task.get('id')} from NextCloud: No fileid")
            metadata.sync_status = SyncStatus.ERROR
            return update_nextcloud_metadata(task, metadata)
        
        try:
            # Get task from NextCloud
            logger.info(f"Pulling NextCloud task {metadata.fileid} for local task {task.get('id')}")
            remote_tasks = await self.nextcloud_client.get_tasks()
            
            # Find the task by ID
            remote_task = None
            for t in remote_tasks:
                if t.id == metadata.fileid:
                    remote_task = t
                    break
            
            if not remote_task:
                logger.error(f"NextCloud task {metadata.fileid} not found")
                metadata.sync_status = SyncStatus.ERROR
                return update_nextcloud_metadata(task, metadata)
            
            # Check for conflicts
            if self.conflict_resolver.detect_conflict(task, remote_task):
                # Resolve conflict
                resolved_task, had_conflict = self.conflict_resolver.resolve_conflict(task, remote_task)
                if had_conflict:
                    logger.info(f"Conflict detected and resolved for task {task.get('id')}")
                    # If conflict was resolved, update fields from resolved_task
                    task = resolved_task
            
            # Map NextCloud task to local format
            remote_data = TaskFieldMapping.map_remote_to_local(remote_task)
            
            # Update local task with remote data
            updated_task = task.copy()
            for field, value in remote_data.items():
                updated_task[field] = value
            
            # Update metadata
            etag = getattr(remote_task, 'etag', None)
            if not etag and hasattr(remote_task, 'model_dump'):
                etag = remote_task.model_dump().get('etag', '')
            if not etag and hasattr(remote_task, '_etag'):
                etag = getattr(remote_task, '_etag', '')
            metadata.etag = etag or ''
            metadata.fileid = remote_task.id
            metadata.last_sync = datetime.now().timestamp()
            metadata.sync_status = SyncStatus.SYNCED
            
            # Record changes in version history
            changes = [{"field": field, "value": remote_data.get(field)} for field in TaskFieldMapping.REMOTE_TO_LOCAL.keys() if field in remote_data]
            metadata.add_version(changes=changes, modified_by="nextcloud")
            
            # Update task with metadata
            updated_task = update_nextcloud_metadata(updated_task, metadata)
            
            return updated_task
            
        except Exception as e:
            logger.error(f"Error pulling task {task.get('id')} from NextCloud: {e}")
            metadata.sync_status = SyncStatus.ERROR
            return update_nextcloud_metadata(task, metadata)
    
    async def _sync_bidirectional(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Perform bidirectional synchronization.
        
        Args:
            task: Task to synchronize
            
        Returns:
            Updated task
        """
        # Get metadata
        metadata = get_nextcloud_metadata(task)
        
        if not metadata.fileid:
            # No remote ID, push to NextCloud
            return await self._push_to_nextcloud(task)
        
        try:
            # Get task from NextCloud
            logger.info(f"Bidirectional sync for task {task.get('id')} with NextCloud task {metadata.fileid}")
            remote_tasks = await self.nextcloud_client.get_tasks()
            
            # Find the task by ID
            remote_task = None
            for t in remote_tasks:
                if t.id == metadata.fileid:
                    remote_task = t
                    break
            
            if not remote_task:
                logger.warning(f"NextCloud task {metadata.fileid} not found, creating new task")
                return await self._push_to_nextcloud(task)
            
            # Check for conflicts
            if self.conflict_resolver.detect_conflict(task, remote_task):
                # Resolve conflict
                resolved_task, had_conflict = self.conflict_resolver.resolve_conflict(task, remote_task)
                if had_conflict:
                    logger.info(f"Conflict detected and resolved for task {task.get('id')}")
                    
                    # If conflict was resolved with local winning, push to NextCloud
                    if metadata.sync_status == SyncStatus.SYNCED:
                        return await self._push_to_nextcloud(resolved_task)
                    
                    return resolved_task
            
            # Determine which side has changed
            local_updated = task.get("updated", 0)
            remote_updated = remote_task.modified.timestamp() if remote_task.modified else 0
            
            if local_updated > metadata.last_sync and remote_updated <= metadata.last_sync:
                # Local changes only, push to NextCloud
                return await self._push_to_nextcloud(task)
                
            elif local_updated <= metadata.last_sync and remote_updated > metadata.last_sync:
                # Remote changes only, pull from NextCloud
                return await self._pull_from_nextcloud(task)
                
            elif local_updated > metadata.last_sync and remote_updated > metadata.last_sync:
                # Both sides changed, this should be handled by conflict resolution
                logger.warning(f"Both sides changed for task {task.get('id')} but no conflict detected")
                if local_updated > remote_updated:
                    return await self._push_to_nextcloud(task)
                else:
                    return await self._pull_from_nextcloud(task)
            
            else:
                # No changes on either side
                logger.info(f"No changes detected for task {task.get('id')}")
                return task
            
        except Exception as e:
            logger.error(f"Error in bidirectional sync for task {task.get('id')}: {e}")
            metadata.sync_status = SyncStatus.ERROR
            return update_nextcloud_metadata(task, metadata)
