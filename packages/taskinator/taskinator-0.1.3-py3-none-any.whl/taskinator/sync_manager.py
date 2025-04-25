"""Synchronization manager for Taskinator."""

import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Union
from loguru import logger

from .external_adapters.nextcloud_adapter import NextCloudAdapter
from .sync_metadata_store import SyncMetadataStore
from .constants import SyncStatus, ExternalSystem
from .utils import read_json, write_json
from .version_tracker import VersionTracker, VersionInfo
from .conflict_ui import ConflictUI
from .conflict_presentation import conflict_presentation_system

class SyncDirection:
    """Synchronization direction constants."""
    BIDIRECTIONAL = "bidirectional"
    LOCAL_TO_REMOTE = "local_to_remote"
    REMOTE_TO_LOCAL = "remote_to_local"

class SyncManager:
    """Manager for synchronizing tasks with external systems."""
    
    def __init__(
        self, 
        tasks_file: Union[str, Path] = None,
        nextcloud_host: Optional[str] = None,
        nextcloud_username: Optional[str] = None,
        nextcloud_password: Optional[str] = None,
        nextcloud_token: Optional[str] = None,
        nextcloud_calendar: str = "Taskinator",
        verbose: bool = False
    ):
        """Initialize the sync manager.
        
        Args:
            tasks_file: Path to the tasks file
            nextcloud_host: NextCloud host
            nextcloud_username: NextCloud username
            nextcloud_password: NextCloud password
            nextcloud_token: NextCloud token
            nextcloud_calendar: Name of the NextCloud calendar to use
            verbose: Enable verbose logging
        """
        self.tasks_file = Path(tasks_file) if tasks_file else None
        self.verbose = verbose
        
        # Initialize metadata store
        if self.tasks_file:
            tasks_dir = self.tasks_file.parent
            self.metadata_store = SyncMetadataStore(base_dir=tasks_dir)
        else:
            self.metadata_store = SyncMetadataStore()
        
        # Initialize version tracker
        self.version_tracker = VersionTracker(metadata_store=self.metadata_store)
        
        # Initialize adapters
        self.adapters = {}
        
        # Initialize NextCloud adapter if credentials are provided
        if nextcloud_host and nextcloud_username and (nextcloud_password or nextcloud_token):
            # Log the credentials we're using
            if verbose:
                logger.info(f"Initializing NextCloud adapter with host: {nextcloud_host}")
                logger.info(f"Username: {nextcloud_username}")
                logger.info(f"Password: {'Set' if nextcloud_password else 'Not set'}")
                logger.info(f"Token: {'Set' if nextcloud_token else 'Not set'}")
                logger.info(f"Calendar: {nextcloud_calendar}")
            
            self.adapters[ExternalSystem.NEXTCLOUD] = NextCloudAdapter(
                host=nextcloud_host,
                username=nextcloud_username,
                password=nextcloud_password,
                token=nextcloud_token,
                calendar_name=nextcloud_calendar,
                metadata_store=self.metadata_store,
                verbose=verbose
            )
            
            if verbose:
                logger.info(f"Initialized NextCloud adapter with host: {nextcloud_host}")
        
        # Initialize conflict UI
        self.conflict_ui = ConflictUI()
    
    async def initialize(self):
        """Initialize the sync manager.
        
        This method should be called after creating the sync manager to ensure
        all adapters are properly initialized.
        
        Returns:
            Dict with initialization status for each adapter
        """
        # Initialize all adapters
        results = {}
        for system, adapter in self.adapters.items():
            if hasattr(adapter, 'initialize'):
                try:
                    calendar = await adapter.initialize()
                    # Check if calendar was successfully initialized
                    if system == ExternalSystem.NEXTCLOUD and not calendar:
                        results[system] = {
                            "status": "error",
                            "message": "Failed to initialize calendar"
                        }
                    else:
                        results[system] = {
                            "status": "success",
                            "message": "Initialized successfully"
                        }
                except Exception as e:
                    logger.error(f"Error initializing adapter for {system}: {e}")
                    results[system] = {
                        "status": "error",
                        "message": str(e)
                    }
        
        return results
    
    async def sync_all(
        self, 
        direction: str = SyncDirection.BIDIRECTIONAL,
        system: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None,
        auto_resolve: bool = False,
        resolution_strategy: Optional[str] = None,
        interactive: bool = False
    ) -> Dict[str, Any]:
        """Synchronize all tasks with external systems.
        
        Args:
            direction: Synchronization direction
            system: External system identifier (all if not specified)
            config: Configuration for the external system
            auto_resolve: Whether to automatically resolve conflicts
            resolution_strategy: Strategy for resolving conflicts
            interactive: Whether to use interactive conflict resolution
            
        Returns:
            Synchronization results
        """
        # Load tasks
        data = read_json(self.tasks_file)
        tasks = data.get("tasks", [])
        
        # Initialize results
        results = {
            "total": len(tasks),
            "synced": 0,
            "conflicts": 0,
            "errors": 0,
            "skipped": 0,
            "timestamp": datetime.now().timestamp(),
            "details": []
        }
        
        # Check if we have any adapters
        if not self.adapters:
            logger.warning("No adapters available for synchronization")
            return results
            
        # Sync each task
        for task in tasks:
            task_id = task.get("id")
            logger.info(f"Syncing task {task_id}")
            
            for system, adapter in self.adapters.items():
                try:
                    # Get metadata from the store
                    metadata = self.metadata_store.get_metadata(task_id, system)
                    
                    # Create metadata object
                    external_id = metadata.get("external_id")
                    sync_metadata = {
                        "system": system,
                        "external_id": external_id,
                        "external_url": metadata.get("external_url", ""),
                        "last_sync": metadata.get("last_sync", 0),
                        "sync_status": metadata.get("sync_status", "pending"),
                        "etag": metadata.get("etag", "")
                    }
                    
                    # Add metadata to task temporarily for sync
                    if "external_sync" not in task:
                        task["external_sync"] = []
                    
                    # Remove any existing metadata for this system
                    task["external_sync"] = [
                        m for m in task["external_sync"] 
                        if m.get("system") != system
                    ]
                    
                    # Add new metadata
                    task["external_sync"].append(sync_metadata)
                    
                    # Sync task
                    updated_task = await adapter.sync_task(task, direction)
                    
                    # Check if the task was synced successfully
                    if updated_task:
                        # Extract updated metadata
                        sync_status_found = False
                        for sync_data in updated_task.get("external_sync", []):
                            if sync_data.get("system") == system:
                                sync_status_found = True
                                # Update metadata in store
                                self.metadata_store.update_metadata(
                                    task_id, 
                                    system, 
                                    {
                                        "external_id": sync_data.get("external_id"),
                                        "external_url": sync_data.get("external_url", ""),
                                        "last_sync": sync_data.get("last_sync", 0),
                                        "sync_status": sync_data.get("sync_status", "pending"),
                                        "etag": sync_data.get("etag", "")
                                    }
                                )
                                
                                # Update results
                                status = sync_data.get("sync_status")
                                if status == SyncStatus.SYNCED:
                                    results["synced"] += 1
                                elif status == SyncStatus.ERROR:
                                    results["errors"] += 1
                                    logger.error(f"Error syncing task {task_id}: {sync_data.get('message', 'Unknown error')}")
                                elif status == SyncStatus.CONFLICT:
                                    results["conflicts"] += 1
                                elif status == SyncStatus.SKIPPED:
                                    results["skipped"] += 1
                                else:
                                    # Default to synced if status is not recognized
                                    results["synced"] += 1
                                    
                                # Add details
                                results["details"].append({
                                    "task_id": task_id,
                                    "system": system,
                                    "status": status,
                                    "message": sync_data.get("message", "")
                                })
                                
                                # Update task in the data
                                for i, t in enumerate(tasks):
                                    if t.get("id") == task_id:
                                        # Remove external_sync from task before saving
                                        if "external_sync" in updated_task:
                                            del updated_task["external_sync"]
                                        tasks[i] = updated_task
                                        break
                        
                        # If no sync status was found, mark as error by default
                        if not sync_status_found:
                            results["errors"] += 1
                            results["details"].append({
                                "task_id": task_id,
                                "system": system,
                                "status": SyncStatus.ERROR,
                                "message": "No sync status returned from adapter"
                            })
                    else:
                        # Task sync failed
                        results["errors"] += 1
                        results["details"].append({
                            "task_id": task_id,
                            "system": system,
                            "status": SyncStatus.ERROR,
                            "message": "Task sync failed"
                        })
                    
                except Exception as e:
                    logger.error(f"Error syncing task {task_id} with {system}: {e}")
                    results["errors"] += 1
                    results["details"].append({
                        "task_id": task_id,
                        "system": system,
                        "status": "error",
                        "message": str(e)
                    })
        
        # Save updated tasks
        data["tasks"] = tasks
        write_json(self.tasks_file, data)
        
        # Check for conflicts and resolve interactively
        if results["conflicts"] > 0:
            logger.info("Found conflicts during sync, resolving interactively")
            if interactive:
                # Use the conflict presentation system for interactive resolution
                conflict_presentation_system.display_dashboard(tasks)
            else:
                # Just notify about conflicts
                for task in tasks:
                    for sync_data in task.get("external_sync", []):
                        if sync_data.get("sync_status") == SyncStatus.CONFLICT:
                            system_name = sync_data.get("system", "unknown")
                            conflict_presentation_system.notify_conflict(task, system_name)
        
        return results
    
    async def sync_task(
        self, 
        task_id: Union[str, int], 
        direction: str = SyncDirection.BIDIRECTIONAL,
        system: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None,
        auto_resolve: bool = False,
        resolution_strategy: Optional[str] = None,
        interactive: bool = False
    ) -> Dict[str, Any]:
        """Synchronize a specific task with external systems.
        
        Args:
            task_id: ID of the task to synchronize
            direction: Synchronization direction
            system: External system identifier (all if not specified)
            config: Configuration for the external system
            auto_resolve: Whether to automatically resolve conflicts
            resolution_strategy: Strategy for resolving conflicts
            interactive: Whether to use interactive conflict resolution
            
        Returns:
            Synchronization results
        """
        if not self.adapters:
            logger.warning("No external adapters configured, skipping synchronization")
            return {"status": "error", "message": "No external adapters configured"}
        
        try:
            # Read tasks
            data = read_json(self.tasks_file)
            
            if not data or 'tasks' not in data:
                logger.warning(f"No tasks found in {self.tasks_file}")
                return {"status": "error", "message": "No tasks found"}
            
            # Find task
            task_id = str(task_id)
            task_index = None
            task = None
            
            for i, t in enumerate(data["tasks"]):
                if str(t.get("id", "")) == task_id:
                    task = t
                    task_index = i
                    break
            
            if task is None:
                logger.warning(f"Task {task_id} not found")
                return {"status": "error", "message": f"Task {task_id} not found"}
            
            # Track sync results
            results = {
                "task_id": task_id,
                "systems": [],
                "status": "success"
            }
            
            # Check if task has external sync metadata
            if "external_sync" in task and task["external_sync"]:
                # Process each external system
                for sync_data in task["external_sync"]:
                    system = sync_data.get("system")
                    if not system:
                        continue
                        
                    # Check if we have an adapter for this system
                    if system not in self.adapters:
                        logger.warning(f"No adapter found for system {system}, skipping")
                        results["systems"].append({
                            "system": system,
                            "status": "skipped",
                            "message": "No adapter configured"
                        })
                        continue
                    
                    # Update version information before sync
                    # This creates a new version for the local changes
                    if direction in [SyncDirection.BIDIRECTIONAL, SyncDirection.LOCAL_TO_REMOTE]:
                        # Get current version info
                        current_version = self.version_tracker.get_version_info(task_id, system)
                        base_version_id = current_version.version_id if current_version else None
                        
                        # Update version for this task
                        self.version_tracker.update_version(task_id, system, base_version_id)
                    
                    # Sync task with external system
                    try:
                        adapter = self.adapters[system]
                        updated_task = await adapter.sync_task(task, direction)
                        
                        # Update task in data
                        data["tasks"][task_index] = updated_task
                        
                        # Get sync status from metadata
                        metadata = self.metadata_store.get_metadata(task_id, system)
                        sync_status = metadata.get("sync_status", SyncStatus.PENDING)
                        
                        # If sync was successful, update version tracking
                        if sync_status == SyncStatus.SYNCED:
                            self.version_tracker.track_sync(task_id, system, SyncStatus.SYNCED)
                        
                        # Add result
                        results["systems"].append({
                            "system": system,
                            "status": sync_status,
                            "message": ""
                        })
                    except Exception as e:
                        logger.error(f"Error syncing task {task_id} with {system}: {e}")
                        results["systems"].append({
                            "system": system,
                            "status": "error",
                            "message": str(e)
                        })
            else:
                # No external sync metadata
                results["status"] = "skipped"
                results["message"] = "No external sync metadata"
            
            # Save updated tasks
            write_json(self.tasks_file, data)
            
            # Update results
            results["timestamp"] = datetime.now().timestamp()
            
            # Check for conflicts and resolve interactively
            if results["status"] == "success" and any(system["status"] == SyncStatus.CONFLICT for system in results["systems"]):
                logger.info("Found conflict during sync, resolving interactively")
                if interactive:
                    # Use the conflict presentation system for interactive resolution
                    updated_task = conflict_presentation_system.conflict_ui.resolve_conflict_interactive(task)
                    data["tasks"][task_index] = updated_task
                    write_json(self.tasks_file, data)
            
            return results
            
        except Exception as e:
            logger.error(f"Error syncing task {task_id}: {e}")
            return {
                "status": "error",
                "message": str(e),
                "timestamp": datetime.now().timestamp()
            }
    
    async def resolve_conflict(
        self, 
        task_id: Union[str, int], 
        system: str, 
        resolution: str = "local",
        config: Optional[Dict[str, Any]] = None
    ):
        """Resolve a synchronization conflict.
        
        Args:
            task_id: ID of the task with conflict
            system: External system identifier
            resolution: Conflict resolution strategy (local, remote, merge)
            config: Additional configuration
            
        Returns:
            Dict with status and result information
        """
        # Get task
        data = read_json(self.tasks_file)
        task_id = str(task_id)
        task_index = None
        task = None
        
        for i, t in enumerate(data["tasks"]):
            if str(t.get("id", "")) == task_id:
                task = t
                task_index = i
                break
        
        if not task:
            return {
                "status": "error",
                "task_id": task_id,
                "system": system,
                "message": f"Task with ID {task_id} not found"
            }
        
        # Get adapter for system
        adapter = self.adapters.get(system)
        if not adapter:
            return {
                "status": "error",
                "task_id": task_id,
                "system": system,
                "message": f"Unsupported external system: {system}"
            }
        
        # Get external metadata
        metadata = None
        for sync_data in task.get("external_sync", []):
            if sync_data.get("system") == system:
                metadata = sync_data
                break
        
        if metadata is None:
            return {
                "status": "error",
                "task_id": task_id,
                "system": system,
                "message": f"Task does not have external sync metadata for system {system}"
            }
        
        if metadata.get("sync_status") != SyncStatus.CONFLICT:
            return {
                "status": "error",
                "task_id": task_id,
                "system": system,
                "message": f"Task does not have a conflict status for system {system}"
            }
        
        try:
            # Get version information
            local_version = self.version_tracker.get_version_info(task_id, system)
            
            # Apply resolution strategy
            if resolution == "local":
                # Keep local version
                # Just update the metadata to mark as synced
                metadata["sync_status"] = SyncStatus.SYNCED
                metadata["last_sync"] = datetime.now().timestamp()
                self.metadata_store.save_metadata(task_id, system, metadata)
                
                # Sync the local task to the remote system
                updated_task = await adapter.sync_task(task, SyncDirection.LOCAL_TO_REMOTE)
                
                # Update version tracking
                self.version_tracker.track_sync(task_id, system, SyncStatus.SYNCED)
                
                if updated_task:
                    # Update task in data
                    data["tasks"][task_index] = updated_task
                    
                    # Write updated tasks back to file
                    write_json(self.tasks_file, data)
                    
                    return {
                        "status": "success",
                        "task_id": task_id,
                        "system": system,
                        "resolution": "local",
                        "message": f"Resolved conflict for task {task_id} with {system} using local version"
                    }
                else:
                    return {
                        "status": "error",
                        "task_id": task_id,
                        "system": system,
                        "message": f"Failed to sync local version of task {task_id} to {system}"
                    }
            elif resolution == "remote":
                # Use remote version
                # Get the remote task
                external_id = metadata.get("external_id")
                if not external_id:
                    logger.error(f"No external ID found for task {task_id} and system {system}")
                    return {
                        "status": "error",
                        "task_id": task_id,
                        "system": system,
                        "message": f"No external ID found for task {task_id} and system {system}"
                    }
                    
                # Get the remote task
                remote_task = await adapter.get_external_task(external_id)
                if not remote_task:
                    logger.error(f"Failed to get remote task {external_id} from {system}")
                    return {
                        "status": "error",
                        "task_id": task_id,
                        "system": system,
                        "message": f"Failed to get remote task {external_id} from {system}"
                    }
                    
                # Sync the remote task to local
                updated_task = await adapter._sync_remote_to_local(remote_task, metadata)
                
                if updated_task:
                    # Update task in data
                    for i, t in enumerate(data.get("tasks", [])):
                        if str(t.get("id")) == str(task_id):
                            data["tasks"][i] = updated_task
                            break
                            
                    # Write updated tasks back to file
                    write_json(self.tasks_file, data)
                    
                    # Update version tracking
                    self.version_tracker.track_sync(task_id, system, SyncStatus.SYNCED)
                    
                    return {
                        "status": "success",
                        "task_id": task_id,
                        "system": system,
                        "resolution": "remote",
                        "message": f"Resolved conflict for task {task_id} with {system} using remote version"
                    }
                else:
                    return {
                        "status": "error",
                        "task_id": task_id,
                        "system": system,
                        "message": f"Failed to sync remote version of task {task_id} to local"
                    }
            elif resolution == "merge":
                # Merge local and remote versions
                # Get the remote task
                external_id = metadata.get("external_id")
                if not external_id:
                    logger.error(f"No external ID found for task {task_id} and system {system}")
                    return {
                        "status": "error",
                        "task_id": task_id,
                        "system": system,
                        "message": f"No external ID found for task {task_id} and system {system}"
                    }
                    
                # Get the remote task
                remote_task = await adapter.get_external_task(external_id)
                if not remote_task:
                    logger.error(f"Failed to get remote task {external_id} from {system}")
                    return {
                        "status": "error",
                        "task_id": task_id,
                        "system": system,
                        "message": f"Failed to get remote task {external_id} from {system}"
                    }
                    
                # Merge the tasks
                merged_task = await self._merge_changes(task, system, adapter)
                
                if merged_task:
                    # Update task in data
                    for i, t in enumerate(data.get("tasks", [])):
                        if str(t.get("id")) == str(task_id):
                            data["tasks"][i] = merged_task
                            break
                            
                    # Write updated tasks back to file
                    write_json(self.tasks_file, data)
                    
                    # Update version tracking
                    self.version_tracker.track_sync(task_id, system, SyncStatus.SYNCED)
                    
                    return {
                        "status": "success",
                        "task_id": task_id,
                        "system": system,
                        "resolution": "merge",
                        "message": f"Resolved conflict for task {task_id} with {system} by merging versions"
                    }
                else:
                    return {
                        "status": "error",
                        "task_id": task_id,
                        "system": system,
                        "message": f"Failed to merge versions of task {task_id}"
                    }
            else:
                return {
                    "status": "error",
                    "task_id": task_id,
                    "system": system,
                    "message": f"Unknown resolution strategy: {resolution}"
                }
                
        except Exception as e:
            logger.error(f"Error resolving conflict for task {task_id} with {system}: {e}")
            return {
                "status": "error",
                "task_id": task_id,
                "system": system,
                "message": f"Error resolving conflict for task {task_id} with {system}: {e}"
            }
    
    async def _merge_changes(
        self,
        task: Dict[str, Any],
        system: str,
        adapter: Any
    ) -> Dict[str, Any]:
        """Merge changes from local and remote versions.
        
        This implements a simple field-based merge strategy:
        - For each field that has changed since the last sync:
          - If only changed in one version, use that change
          - If changed in both versions, use the most recent change
        - For fields that haven't changed, keep as is
        
        Args:
            task: Local task with conflict
            system: External system identifier
            adapter: Adapter for the external system
            
        Returns:
            Merged task
        """
        # Get metadata
        metadata = None
        for sync_data in task.get("external_sync", []):
            if sync_data.get("system") == system:
                metadata = sync_data
                break
        
        # Get remote task
        remote_task = await adapter.get_remote_task(task)
        if not remote_task:
            # If remote task doesn't exist, use local version
            return await adapter.sync_task(task, SyncDirection.LOCAL_TO_REMOTE)
        
        # Create a copy of the task to merge into
        merged_task = task.copy()
        
        # Get field mapping
        field_mapping = adapter.get_field_mapping()
        
        # Find the last common version in history
        last_common_version = None
        version_history = metadata.version_history
        
        if version_history:
            # Sort by version number
            sorted_history = sorted(version_history, key=lambda v: v["version"])
            last_common_version = sorted_history[0]
        
        # If no common version, use simple merge based on timestamps
        if not last_common_version:
            # For each field in mapping, compare and use most recent
            for local_field, remote_field in field_mapping.items():
                if local_field in task and remote_field in remote_task:
                    local_value = task[local_field]
                    remote_value = remote_task[remote_field]
                    
                    # If values are different, use the one from the most recently updated task
                    if local_value != remote_value:
                        if task.get("updated", 0) > remote_task.get("updated", 0):
                            # Local is newer, keep local value (already in merged_task)
                            pass
                        else:
                            # Remote is newer, use remote value
                            merged_task[local_field] = remote_value
        else:
            # Use version history for smarter merging
            # Group changes by field
            field_changes = {}
            
            for version in version_history:
                for change in version.get("changes", []):
                    field = change.get("field")
                    if field:
                        if field not in field_changes:
                            field_changes[field] = []
                        field_changes[field].append({
                            "version": version["version"],
                            "modified_by": version["modified_by"],
                            "last_modified": version["last_modified"],
                            "old": change.get("old"),
                            "new": change.get("new")
                        })
            
            # For each field with changes
            for field, changes in field_changes.items():
                # Sort by timestamp (newest first)
                sorted_changes = sorted(changes, key=lambda c: c["last_modified"], reverse=True)
                newest_change = sorted_changes[0]
                
                # Check if both local and remote modified this field
                local_modified = any(c["modified_by"] == "local" for c in changes)
                remote_modified = any(c["modified_by"] == "remote" for c in changes)
                
                if local_modified and remote_modified:
                    # Both modified, use newest change
                    if newest_change["modified_by"] == "local":
                        # Local is newer, keep local value (already in merged_task)
                        pass
                    else:
                        # Remote is newer, use remote value
                        if field in field_mapping:
                            remote_field = field_mapping[field]
                            if remote_field in remote_task:
                                merged_task[field] = remote_task[remote_field]
                elif remote_modified:
                    # Only remote modified, use remote value
                    if field in field_mapping:
                        remote_field = field_mapping[field]
                        if remote_field in remote_task:
                            merged_task[field] = remote_task[remote_field]
                # If only local modified, keep local value (already in merged_task)
        
        # Sync the merged task
        return await adapter.sync_task(merged_task, SyncDirection.LOCAL_TO_REMOTE)

    async def link_task(self, task: Dict[str, Any], system: str, external_id: str) -> Dict[str, Any]:
        """Link a local task with an external task.
        
        Args:
            task: The local task to link
            system: The external system to link with
            external_id: The external task ID to link with
            
        Returns:
            The updated task with link metadata
        """
        if not task:
            logger.error("Cannot link a null task")
            return None
            
        if not external_id:
            logger.error("Cannot link to a null external ID")
            return None
            
        # Get adapter for the system
        adapter = self.adapters.get(system)
        if not adapter:
            logger.error(f"No adapter found for system: {system}")
            return None
            
        try:
            # Get metadata for the task
            metadata = self.metadata_store.get_metadata(task["id"], system)
            
            # If no metadata exists, create a new one
            if not metadata:
                metadata = {
                    "system": system,
                    "task_id": task["id"],
                    "external_id": external_id,
                    "sync_status": SyncStatus.LINKED,
                    "last_sync": datetime.now().timestamp()
                }
            else:
                # Update existing metadata
                metadata["external_id"] = external_id
                metadata["sync_status"] = SyncStatus.LINKED
                metadata["last_sync"] = datetime.now().timestamp()
                
            # Save metadata
            self.metadata_store.save_metadata(task["id"], system, metadata)
            
            # Get the external task to verify it exists
            external_task = await adapter.get_external_task(external_id)
            if not external_task:
                logger.error(f"External task {external_id} not found in {system}")
                return None
                
            # Update metadata with external URL if available
            if hasattr(external_task, "url") and external_task.url:
                metadata["external_url"] = external_task.url
            elif system == ExternalSystem.NEXTCLOUD and adapter.client:
                # For NextCloud, construct the URL
                metadata["external_url"] = f"{adapter.client.base_url}/index.php/apps/tasks/#/tasks/{external_id}"
                
            # Add metadata to the task
            if "external_sync" not in task:
                task["external_sync"] = []
                
            # Remove any existing metadata for this system
            task["external_sync"] = [
                m for m in task["external_sync"] 
                if isinstance(m, dict) and m.get("system") != system
            ]
            
            # Add updated metadata
            task["external_sync"].append(metadata)
            
            logger.info(f"Linked task {task['id']} with external task {external_id} in {system}")
            
            return task
            
        except Exception as e:
            logger.error(f"Error linking task {task['id']} with external task {external_id} in {system}: {e}")
            return None
