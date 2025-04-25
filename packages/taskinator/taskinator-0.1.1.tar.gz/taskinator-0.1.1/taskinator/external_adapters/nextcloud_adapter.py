"""NextCloud adapter for external integration."""

import json
import re
import uuid
from datetime import datetime
from enum import Enum, auto
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple, Union

from loguru import logger
import json
import traceback
from typing import Dict, Any, List, Optional, Tuple, Union
from datetime import datetime

from taskinator.constants import ExternalSystem, SyncStatus
from taskinator.external_adapters.base_adapter import ExternalAdapter
from taskinator.nextcloud_client import NextCloudClient, NextCloudTask
from taskinator.sync_errors import SyncError, wrap_error, with_retry
from taskinator.utils import read_json
from taskinator.sync_metadata_store import SyncMetadataStore
from taskinator.version_tracker import VersionTracker, VersionInfo

# Constants
NEXTCLOUD = ExternalSystem.NEXTCLOUD.value
SYNCED = SyncStatus.SYNCED
ERROR = SyncStatus.ERROR

class NextCloudAdapter(ExternalAdapter):
    """Adapter for synchronizing tasks with NextCloud."""
    
    # System ID and name as class properties
    system_id = ExternalSystem.NEXTCLOUD
    system_name = "NextCloud"
    
    # Mapping from Taskinator fields to NextCloud fields
    LOCAL_TO_REMOTE = {
        "title": "title",
        "description": "description",
        "status": "status",  # Special handling required
        "due_date": "due_date",
        "priority": "priority",  # Special handling required
    }
    
    # Mapping from NextCloud fields to Taskinator fields
    REMOTE_TO_LOCAL = {
        "title": "title",
        "description": "description",
        "status": "status",  # Special handling required
        "due_date": "due_date",
        "priority": "priority",  # Special handling required
    }
    
    def __init__(
        self, 
        host: str, 
        username: str, 
        password: str = None, 
        token: str = None,
        calendar_name: str = "Taskinator",
        metadata_store: SyncMetadataStore = None,
        verbose: bool = False
    ):
        """Initialize NextCloud adapter.
        
        Args:
            host: NextCloud host
            username: NextCloud username
            password: NextCloud password
            token: NextCloud token
            calendar_name: Name of the calendar to use for tasks
            metadata_store: Sync metadata store
            verbose: Enable verbose logging
        """
        self.host = host
        self.username = username
        self.password = password
        self.token = token
        self.calendar_name = calendar_name
        self.metadata_store = metadata_store
        self.verbose = verbose
        
        # Initialize version tracker if metadata store is provided
        self.version_tracker = VersionTracker(metadata_store=metadata_store) if metadata_store else None
        
        # Create NextCloud client
        self.client = NextCloudClient(
            host=host,
            username=username,
            password=password,
            token=token,
            calendar_name=calendar_name,  # Pass calendar_name to the client
            verbose=verbose
        )
        
    async def initialize(self) -> bool:
        """Initialize the adapter.
        
        Returns:
            True if initialization was successful, False otherwise
        """
        try:
            # Initialize the client
            await self.client.initialize()
            
            # Check if the calendar exists, create it if it doesn't
            calendar = await self.get_or_create_calendar(self.calendar_name)
            
            if calendar:
                # Set the calendar ID in the client
                self.client.calendar_id = calendar.id
                logger.info(f"Using calendar '{self.calendar_name}' with ID {calendar.id}")
                return True
            else:
                logger.error(f"Failed to get or create calendar '{self.calendar_name}'")
                return False
        except Exception as e:
            error = wrap_error(e)
            logger.error(f"Failed to initialize NextCloud adapter: {error}")
            return False
            
    async def close(self) -> None:
        """Close the adapter and release resources."""
        # Close the NextCloud client if needed
        if hasattr(self, 'client') and self.client:
            await self.client.close()
            logger.info("Closed NextCloud client")
            
    async def get_or_create_calendar(self, calendar_name: str) -> Optional[Dict[str, Any]]:
        """Get or create a calendar with the given name.
        
        Args:
            calendar_name: Name of the calendar
            
        Returns:
            Calendar object if found or created, None otherwise
        """
        try:
            # Get all calendars
            calendars = await self.client.get_calendars()
            
            # Normalize the calendar name for robust comparison
            def norm(name):
                return name.strip().lower() if isinstance(name, str) else ""
            target = norm(calendar_name)

            # Look for a calendar with the given name (case-insensitive, trimmed)
            for calendar in calendars:
                if norm(calendar.display_name) == target:
                    logger.info(f"Found existing calendar '{calendar.display_name}' with ID {calendar.id}")
                    return calendar
            
            # Calendar not found, create it
            logger.info(f"Creating new calendar '{calendar_name}'")
            calendar = await self.client.create_calendar(calendar_name)
            
            if calendar:
                logger.info(f"Created calendar '{calendar.display_name}' with ID {calendar.id}")
                
                # Since we created a new calendar, clear all external IDs in metadata
                if self.metadata_store:
                    logger.info("Clearing all NextCloud external IDs in metadata due to new calendar creation")
                    await self._reset_all_metadata()
                
                return calendar
            else:
                logger.error(f"Failed to create calendar '{calendar_name}'")
                return None
                
        except Exception as e:
            logger.error(f"Error getting or creating calendar '{calendar_name}': {e}")
            return None
    
    async def _reset_all_metadata(self):
        """Reset all NextCloud metadata due to calendar recreation.
        
        This clears external IDs from all tasks' metadata to force recreation
        of tasks in the new calendar.
        """
        try:
            # Get all task IDs with NextCloud metadata
            task_ids = self.metadata_store.get_all_task_ids(NEXTCLOUD)
            
            logger.info(f"Resetting NextCloud metadata for {len(task_ids)} tasks")
            
            # For each task, clear the external ID
            for task_id in task_ids:
                metadata = self.metadata_store.get_metadata(task_id, NEXTCLOUD)
                if metadata and "external_id" in metadata:
                    # Clear external ID but keep other metadata
                    del metadata["external_id"]
                    metadata["sync_status"] = ERROR
                    metadata["message"] = "Calendar was recreated, task will be recreated on next sync"
                    
                    # Save updated metadata
                    self.metadata_store.save_metadata(task_id, NEXTCLOUD, metadata)
            
            logger.info("NextCloud metadata reset completed")
            
        except Exception as e:
            logger.error(f"Error resetting NextCloud metadata: {e}")
    
    async def sync_task(self, task: Dict[str, Any], direction: str = "bidirectional") -> Dict[str, Any]:
        """Sync a task with NextCloud.
        
        Args:
            task: Task to sync
            direction: Sync direction (push, pull, bidirectional)
            
        Returns:
            Updated task with sync status
        """
        try:
            # Get metadata for this task
            metadata = self._get_metadata(task)
            
            # Update metadata with task info
            metadata["local_id"] = task["id"]
            metadata["local_title"] = task["title"]
            
            # Determine sync direction
            if direction == "push":
                # Push local changes to NextCloud
                return await self._sync_local_to_remote(task, metadata)
            elif direction == "pull":
                # Pull remote changes to local
                return await self._sync_remote_to_local(task, metadata)
            else:
                # Bidirectional sync
                # First push local changes to NextCloud
                updated_task = await self._sync_local_to_remote(task, metadata)
                
                # Then pull remote changes to local
                return await self._sync_remote_to_local(updated_task, self._get_metadata(updated_task))
        except Exception as e:
            logger.error(f"Error syncing task {task.get('id')}: {e}")
            return {
                "sync_status": ERROR,
                "error": str(e)
            }
    
    def _get_metadata(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Get metadata for a task.
        
        Args:
            task: Task to get metadata for
            
        Returns:
            Metadata for the task
        """
        # Check if task has external_sync data
        if isinstance(task, dict) and "external_sync" in task and NEXTCLOUD in task["external_sync"]:
            return task["external_sync"][NEXTCLOUD]
        
        # Otherwise get from metadata store
        if self.metadata_store and isinstance(task, dict) and "id" in task:
            metadata = self.metadata_store.get_metadata(task["id"], NEXTCLOUD)
            if metadata:
                return metadata
        
        # Return empty metadata if none found
        return {}
    
    async def _sync_local_to_remote(self, task: Dict[str, Any], metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Sync a local task to NextCloud.
        
        Args:
            task: Local task
            metadata: Sync metadata
            
        Returns:
            Updated task with metadata
        """
        try:
            # Get existing metadata
            metadata = self._get_metadata(task)
            
            # If we have an external ID, try to update the task
            if metadata.get("external_id"):
                try:
                    # Update the task
                    updated_task = await self.client.update_task(metadata["external_id"], self.map_local_to_remote(task))
                    
                    if updated_task:
                        # Update metadata
                        metadata["last_sync"] = datetime.now().timestamp()
                        metadata["local_version"] = task.get("version", 1)
                        metadata["sync_status"] = SYNCED
                        metadata["message"] = "Task updated successfully in NextCloud"
                        
                        # Update task with metadata
                        updated_task_dict = task.copy()
                        if "external_sync" not in updated_task_dict:
                            updated_task_dict["external_sync"] = {}
                        updated_task_dict["external_sync"][NEXTCLOUD] = metadata
                        return updated_task_dict
                except Exception as e:
                    # If update fails, try to create a new task
                    logger.warning(f"Error updating task {metadata.get('external_id')}: {e}")
                    return await self._create_new_task(task, self.map_local_to_remote(task), metadata)
            else:
                # No external ID, try to create a new task
                return await self._create_new_task(task, self.map_local_to_remote(task), metadata)
        except Exception as e:
            logger.error(f"Error syncing task {task.get('id')} to NextCloud: {e}")
            return {
                "sync_status": ERROR,
                "error": str(e)
            }
    
    async def _sync_remote_to_local(self, remote_task: NextCloudTask, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Sync a task from remote to local.
        
        Args:
            remote_task: NextCloud task
            metadata: External sync metadata
            
        Returns:
            Updated task
        """
        try:
            # Map remote task to local format
            local_task = self.map_remote_to_local(remote_task)
            
            # Check if this is a subtask
            is_subtask = False
            parent_id = None
            
            # Check if this task has a RELATED-TO relationship
            if hasattr(remote_task, 'related_to') and remote_task.related_to:
                is_subtask = True
                parent_task = await self.client.get_task(remote_task.related_to)
                if parent_task:
                    # Try to find the parent task ID in our system
                    if self.metadata_store:
                        metadata = self.metadata_store.find_by_external_id(
                            NEXTCLOUD, 
                            parent_task.id
                        )
                        if metadata and "task_id" in metadata:
                            parent_id = metadata["task_id"]
            
            # If this is a subtask and we found the parent, handle differently
            if is_subtask and parent_id:
                # This is a subtask, we'll handle it through the parent task
                logger.info(f"Task {remote_task.id} is a subtask of {parent_id}, will be handled through parent")
                
                # Update metadata to indicate this is a subtask
                metadata["is_subtask"] = True
                metadata["parent_id"] = parent_id
                metadata["external_id"] = remote_task.id
                metadata["external_url"] = f"{self.client.base_url}/index.php/apps/tasks/#/tasks/{remote_task.id}"
                metadata["etag"] = remote_task.etag or ""
                metadata["last_sync"] = datetime.now().timestamp()
                metadata["sync_status"] = SYNCED
                
                # Return a minimal task with metadata
                task = {
                    "id": f"{parent_id}.{local_task.get('id', '')}",
                    "title": local_task.get("title", ""),
                    "status": local_task.get("status", "pending"),
                    "external_sync": [metadata]
                }
                
                return task
            
            # Regular task (not a subtask)
            # Try to get subtasks if available
            try:
                if hasattr(self.client, 'get_subtasks'):
                    subtasks = await self.client.get_subtasks(remote_task.id)
                    if subtasks:
                        logger.info(f"Found {len(subtasks)} subtasks for task {remote_task.id}")
                        # Process subtasks
                        for subtask in subtasks:
                            # Map the subtask to local format
                            local_subtask = self.map_remote_to_local(subtask)
                            
                            # Create subtask ID based on parent ID
                            if "id" in local_task:
                                # Extract the numeric part after the dot if it exists
                                subtask_id_match = re.search(r'(\d+)$', local_subtask.get("id", ""))
                                if subtask_id_match:
                                    subtask_id = subtask_id_match.group(1)
                                else:
                                    # Generate a unique ID for the subtask
                                    subtask_id = str(uuid.uuid4())[:8]
                                    
                                local_subtask["id"] = subtask_id
                            
                            # Add subtask metadata
                            subtask_metadata = {
                                "system": NEXTCLOUD,
                                "external_id": subtask.id,
                                "external_url": f"{self.client.base_url}/index.php/apps/tasks/#/tasks/{subtask.id}",
                                "etag": subtask.etag or "",
                                "last_sync": datetime.now().timestamp(),
                                "sync_status": SYNCED,
                                "is_subtask": True,
                                "parent_id": local_task.get("id", "")
                            }
                            
                            if "external_sync" not in local_subtask:
                                local_subtask["external_sync"] = {}
                                
                            local_subtask["external_sync"][NEXTCLOUD] = subtask_metadata
                            
                            # Add subtask to the task
                            if "subtasks" not in local_task:
                                local_task["subtasks"] = []
                            local_task["subtasks"].append(local_subtask)
            except Exception as e:
                logger.warning(f"Error getting subtasks for task {remote_task.id}: {e}")
            
            # Update metadata
            metadata["external_id"] = remote_task.id
            metadata["external_url"] = f"{self.client.base_url}/index.php/apps/tasks/#/tasks/{remote_task.id}"
            metadata["etag"] = remote_task.etag or ""
            metadata["last_sync"] = datetime.now().timestamp()
            metadata["sync_status"] = SYNCED
            metadata["message"] = "Task synced successfully from NextCloud"
            
            # Check if the task is already completed in our system
            # If it is, we don't want to update the status from NextCloud
            task_id = metadata.get("task_id")
            if task_id:
                try:
                    # Get the task from our system
                    data = read_json("tasks/tasks.json")
                    tasks = data.get("tasks", [])
                    for task in tasks:
                        if task.get("id") == task_id:
                            # If the task is already completed in our system, don't update the status
                            if task.get("status") in ["done", "blocked"]:
                                logger.info(f"Task {task_id} is already completed in our system, not updating status from NextCloud")
                                # Keep the local status
                                local_task["status"] = task.get("status")
                            break
                except Exception as e:
                    logger.warning(f"Error checking task status in our system: {e}")
            
            # Add metadata to the task
            if "external_sync" not in local_task:
                local_task["external_sync"] = {}
                
            local_task["external_sync"][NEXTCLOUD] = metadata
            
            return local_task
            
        except Exception as e:
            import traceback
            logger.error(f"Error syncing task {remote_task.id} from NextCloud: {e}")
            logger.debug(f"Traceback: {traceback.format_exc()}")
            
            # Create a minimal task with error metadata
            metadata["sync_status"] = ERROR
            
            task = {
                "title": remote_task.title,
                "external_sync": [metadata]
            }
            
            return task

    async def get_external_task(self, external_id: str) -> Optional[NextCloudTask]:
        """Get a task from NextCloud by its ID.
        
        Args:
            external_id: External ID of the task
            
        Returns:
            NextCloudTask or None if not found
        """
        try:
            return await self.client.get_task(external_id)
        except Exception as e:
            error = wrap_error(e, context={"external_id": external_id, "system": NEXTCLOUD})
            logger.error(f"Error getting task {external_id} from NextCloud: {error}")
            
            # If it's a not found error, return None
            if error.category == ErrorCategory.NOT_FOUND:
                return None
                
            # Otherwise, raise the error
            raise error
    
    def map_local_to_remote(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Map a local task to a remote task.
        
        Args:
            task: Local task
            
        Returns:
            Remote task
        """
        # Include task ID in the title
        task_id = task.get("id", "")
        title = f"{task_id}: {task.get('title', '')}"
        
        remote_task = {
            "title": title,
            "status": self._map_status_to_remote(task.get("status", "pending")),
            "priority": self._map_priority_to_remote(task.get("priority", "medium")),
        }
        
        # Add due date if present
        if task.get("due_date"):
            remote_task["due_date"] = task["due_date"]
            
        # Add categories for dependencies
        categories = []
        
        # Add dependencies as categories
        if "dependencies" in task and task["dependencies"]:
            for dep_id in task["dependencies"]:
                categories.append(f"Depends on: {dep_id}")
                
        if categories:
            remote_task["categories"] = categories
            
        # Format description with Markdown to include all task details
        description = ""
        
        # Create a formatted task details box
        description += "# Task Details\n\n"
        
        # Add task header
        description += f"## {task_id}: {task.get('title', '')}\n\n"
        
        # Add status and priority
        description += f"**Status:** {task.get('status', 'pending')}\n"
        description += f"**Priority:** {task.get('priority', 'medium')}\n"
        
        # Add dependencies if present
        if "dependencies" in task and task["dependencies"]:
            deps_str = ", ".join(str(dep) for dep in task["dependencies"])
            description += f"**Dependencies:** {deps_str}\n"
        
        description += "\n"
        
        # Add description section
        if task.get("description"):
            description += "## Description\n\n"
            description += f"{task.get('description')}\n\n"
        
        # Add details section
        if task.get("details"):
            description += "## Details\n\n"
            description += f"{task.get('details')}\n\n"
        
        # Add test strategy section
        if task.get("test_strategy"):
            description += "## Test Strategy\n\n"
            description += f"{task.get('test_strategy')}\n\n"
        
        # Store the formatted description
        remote_task["description"] = description
        
        if self.verbose:
            logger.info(f"Mapped local task {task.get('id')} to remote format")
            
        return remote_task
    
    def map_remote_to_local(self, remote_task: NextCloudTask) -> Dict[str, Any]:
        """Map a NextCloud task to local format.
        
        Args:
            remote_task: NextCloud task
            
        Returns:
            Task in local format
        """
        # Create a new task with basic fields
        task = {
            "id": remote_task.id,
            "title": remote_task.title,
            "description": remote_task.description or "",
            "status": self._map_nextcloud_status_to_local(remote_task.status),
            "priority": self._map_nextcloud_priority_to_local(remote_task.priority),
        }
        
        # Add due date if available
        if remote_task.due_date:
            task["due_date"] = remote_task.due_date
            
        # Preserve existing metadata like dependencies if available
        # This is important for maintaining task relationships
        try:
            # Look for existing task with this ID in our system
            if self.metadata_store:
                metadata = self.metadata_store.find_by_external_id(NEXTCLOUD, remote_task.id)
                if metadata and "task_id" in metadata:
                    task_id = metadata["task_id"]
                    # Get the existing task from our system
                    data = read_json("tasks/tasks.json")
                    tasks = data.get("tasks", [])
                    for existing_task in tasks:
                        if existing_task.get("id") == task_id:
                            # If the task is already completed in our system, don't update the status
                            if existing_task.get("status") in ["done", "blocked"]:
                                logger.info(f"Task {task_id} is already completed in our system, not updating status from NextCloud")
                                # Keep the local status
                                task["status"] = existing_task.get("status")
                            break
        except Exception as e:
            logger.warning(f"Error preserving task metadata: {e}")
        
        return task

    def _map_status_to_remote(self, status: str) -> str:
        """Map Taskinator status to NextCloud status.
        
        Args:
            status: Taskinator status
            
        Returns:
            NextCloud status
        """
        if status == "done":
            return "COMPLETED"
        elif status == "in_progress":
            return "IN-PROCESS"
        elif status == "blocked":
            return "CANCELLED"
        else:
            return "NEEDS-ACTION"
    
    def _map_status_to_local(self, status: str) -> str:
        """Map NextCloud status to Taskinator status.
        
        Args:
            status: NextCloud status
            
        Returns:
            Taskinator status
        """
        if status == "COMPLETED":
            return "done"
        elif status == "IN-PROCESS":
            return "in_progress"
        elif status == "CANCELLED":
            return "blocked"
        else:
            return "pending"
    
    def _map_priority_to_remote(self, priority: str) -> int:
        """Map Taskinator priority to NextCloud priority.
        
        Args:
            priority: Taskinator priority
            
        Returns:
            NextCloud priority
        """
        if priority == "high":
            return 1
        elif priority == "medium":
            return 5
        else:
            return 9
    
    def _map_priority_to_local(self, priority: Any) -> str:
        """Map NextCloud priority to Taskinator priority.
        
        Args:
            priority: NextCloud priority
            
        Returns:
            Taskinator priority
        """
        if priority is None:
            return "medium"
            
        try:
            priority_int = int(priority)
            if priority_int <= 3:
                return "high"
            elif priority_int <= 6:
                return "medium"
            else:
                return "low"
        except (ValueError, TypeError):
            return "medium"

    def _map_nextcloud_status_to_local(self, status: str) -> str:
        """Map NextCloud status to Taskinator status.
        
        Args:
            status: NextCloud status
            
        Returns:
            Taskinator status
        """
        # Map NextCloud status to Taskinator status
        status_map = {
            "NEEDS-ACTION": "pending",
            "IN-PROCESS": "in_progress",
            "COMPLETED": "done",
            "CANCELLED": "blocked"
        }
        
        return status_map.get(status, "pending")
        
    def _map_nextcloud_priority_to_local(self, priority: Optional[int]) -> str:
        """Map NextCloud priority to Taskinator priority.
        
        Args:
            priority: NextCloud priority
            
        Returns:
            Taskinator priority
        """
        # Map NextCloud priority to Taskinator priority
        if priority is None:
            return "medium"
            
        # Convert priority to int if it's a string
        try:
            priority_int = int(priority)
        except (ValueError, TypeError):
            # If conversion fails, default to medium
            return "medium"
            
        if priority_int <= 3:
            return "low"
        elif priority_int <= 6:
            return "medium"
        else:
            return "high"
    
    def _detect_changes(self, local_task: Dict[str, Any], remote_task: Dict[str, Any]) -> tuple:
        """Detect changes between local and remote tasks.
        
        Args:
            local_task: Local task
            remote_task: Remote task
            
        Returns:
            Tuple of (changes, has_conflict)
        """
        changes = False
        has_conflict = False
        
        # Check for changes in basic fields
        for field in ["title", "description", "status", "priority", "details", "test_strategy"]:
            if field in remote_task and field in local_task:
                if remote_task[field] != local_task[field]:
                    changes = True
                    # Check for conflicts (both sides changed)
                    if field in ["title", "description", "details", "test_strategy"]:
                        has_conflict = True
        
        return changes, has_conflict
    
    def _update_task_metadata(self, task: Dict[str, Any], metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Update task with metadata.
        
        Args:
            task: Task to update
            metadata: Metadata to add
            
        Returns:
            Updated task
        """
        # Ensure task has external_sync field
        if "external_sync" not in task:
            task["external_sync"] = {}
            
        # Add system key to metadata if not present
        if "system" not in metadata:
            metadata["system"] = NEXTCLOUD
            
        # Add updated metadata
        task["external_sync"][NEXTCLOUD] = metadata
        
        # Log the task structure for debugging
        logger.debug(f"Updated task with metadata: {task}")
        
        return task

    def _format_subtask_description(self, subtask_data: Dict[str, Any], parent_id: str) -> str:
        """Format subtask description with Markdown.
        
        Args:
            subtask_data: Subtask data
            parent_id: Parent task ID
            
        Returns:
            Formatted description
        """
        # Format description with Markdown to include all subtask details
        description = ""
        
        # Create a formatted task details box
        description += "# Subtask Details\n\n"
        
        # Add subtask header with parent reference
        subtask_id = subtask_data.get("id", "")
        full_id = f"{parent_id}.{subtask_id}"
        description += f"## {full_id}: {subtask_data.get('title', '')}\n\n"
        
        # Add status and priority
        description += f"**Status:** {subtask_data.get('status', 'pending')}\n"
        description += f"**Priority:** {subtask_data.get('priority', 'medium')}\n"
        description += f"**Parent Task:** {parent_id}\n"
        
        description += "\n"
        
        # Add description section
        if subtask_data.get("description"):
            description += "## Description\n\n"
            description += f"{subtask_data.get('description')}\n\n"
        
        # Add details section
        if subtask_data.get("details"):
            description += "## Details\n\n"
            description += f"{subtask_data.get('details')}\n\n"
        
        return description

    async def _create_new_task(self, task: Dict[str, Any], nextcloud_task: Dict[str, Any], metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new task in NextCloud.
        
        Args:
            task: Local task
            nextcloud_task: NextCloud task
            metadata: Sync metadata
            
        Returns:
            Updated task with metadata
        """
        try:
            logger.info(f"Creating task {task['id']} in NextCloud")
            logger.debug(f"Task data: {task}")
            logger.debug(f"NextCloud task data: {nextcloud_task}")
            logger.debug(f"Metadata: {metadata}")
            
            # Create the task in NextCloud using retry logic
            created = await with_retry(
                self.client.create_task,
                max_retries=3,
                initial_delay=1.0,
                backoff_factor=2.0,
                task_data=nextcloud_task
            )
            
            if created and hasattr(created, "id"):
                # Update metadata with external ID
                metadata["external_id"] = created.id
                metadata["sync_status"] = SYNCED
                metadata["last_sync"] = datetime.now().timestamp()
                metadata["etag"] = getattr(created, "etag", "")
                metadata["message"] = "Task created successfully"
                
                # Add external URL if available
                if hasattr(self.client, "base_url"):
                    metadata["external_url"] = f"{self.client.base_url}/index.php/apps/tasks/#/tasks/{created.id}"
                
                # Save the updated metadata
                if self.metadata_store:
                    try:
                        self.metadata_store.save_metadata(task["id"], NEXTCLOUD, metadata)
                        logger.debug(f"Saved metadata for task {task['id']}: {metadata}")
                    except Exception as e:
                        logger.error(f"Error saving metadata: {e}")
                
                # Log success
                logger.info(f"Task {task['id']} created successfully in NextCloud with ID {created.id}")
                
                # Update task with metadata and return
                try:
                    # Check if task is a dictionary
                    if not isinstance(task, dict):
                        logger.error(f"Task is not a dictionary: {type(task)}")
                        return {
                            "sync_status": ERROR,
                            "error": f"Task is not a dictionary: {type(task)}",
                            "message": "Internal error: Task data has incorrect format"
                        }
                    
                    logger.debug(f"Task before copy: {type(task)}, keys: {task.keys() if isinstance(task, dict) else 'N/A'}")
                    updated_task = task.copy()
                    logger.debug("Task copied successfully")
                    
                    logger.debug(f"Adding external_sync to task")
                    if "external_sync" not in updated_task:
                        updated_task["external_sync"] = {}
                    
                    # Check if external_sync is a list instead of a dict
                    if isinstance(updated_task["external_sync"], list):
                        # Convert to a dictionary
                        logger.debug("Converting external_sync from list to dictionary")
                        external_sync_dict = {}
                        external_sync_dict[NEXTCLOUD] = metadata
                        updated_task["external_sync"] = external_sync_dict
                    else:
                        # It's already a dictionary, just add the metadata
                        logger.debug(f"Adding metadata to external_sync[{NEXTCLOUD}]")
                        updated_task["external_sync"][NEXTCLOUD] = metadata
                    
                    logger.debug(f"Metadata added successfully")
                    logger.debug(f"Updated task with metadata: {updated_task}")
                    return updated_task
                except Exception as e:
                    logger.error(f"Error updating task with metadata: {e}")
                    return {
                        "sync_status": ERROR,
                        "error": str(e)
                    }
            else:
                # Creation failed
                metadata["sync_status"] = ERROR
                metadata["error"] = "Failed to create task in NextCloud"
                metadata["message"] = "Failed to create task in NextCloud"
                if self.metadata_store:
                    self.metadata_store.save_metadata(task["id"], NEXTCLOUD, metadata)
                
                # Update task with metadata and return
                try:
                    # Check if task is a dictionary
                    if not isinstance(task, dict):
                        logger.error(f"Task is not a dictionary: {type(task)}")
                        return {
                            "sync_status": ERROR,
                            "error": f"Task is not a dictionary: {type(task)}",
                            "message": "Internal error: Task data has incorrect format"
                        }
                    
                    updated_task = task.copy()
                    if "external_sync" not in updated_task:
                        updated_task["external_sync"] = {}
                    
                    # Check if external_sync is a list instead of a dict
                    if isinstance(updated_task["external_sync"], list):
                        # Convert to a dictionary
                        logger.debug("Converting external_sync from list to dictionary")
                        external_sync_dict = {}
                        external_sync_dict[NEXTCLOUD] = metadata
                        updated_task["external_sync"] = external_sync_dict
                    else:
                        # It's already a dictionary, just add the metadata
                        logger.debug(f"Adding metadata to external_sync[{NEXTCLOUD}]")
                        updated_task["external_sync"][NEXTCLOUD] = metadata
                    
                    logger.debug(f"Metadata added successfully")
                    logger.debug(f"Updated task with metadata: {updated_task}")
                    return updated_task
                except Exception as e:
                    logger.error(f"Error updating task with metadata: {e}")
                    return {
                        "sync_status": ERROR,
                        "error": str(e)
                    }
        except SyncError as e:
            logger.error(f"Error creating task in NextCloud: {e.get_user_friendly_message()}")
            
            # Update metadata with error
            metadata["sync_status"] = ERROR
            metadata["error"] = str(e)
            metadata["message"] = e.get_user_friendly_message()
            if self.metadata_store:
                self.metadata_store.save_metadata(task["id"], NEXTCLOUD, metadata)
            
            # Update task with metadata and return
            try:
                # Check if task is a dictionary
                if not isinstance(task, dict):
                    logger.error(f"Task is not a dictionary: {type(task)}")
                    return {
                        "sync_status": ERROR,
                        "error": f"Task is not a dictionary: {type(task)}",
                        "message": "Internal error: Task data has incorrect format"
                    }
                
                updated_task = task.copy()
                if "external_sync" not in updated_task:
                    updated_task["external_sync"] = {}
                
                # Check if external_sync is a list instead of a dict
                if isinstance(updated_task["external_sync"], list):
                    # Convert to a dictionary
                    logger.debug("Converting external_sync from list to dictionary")
                    external_sync_dict = {}
                    external_sync_dict[NEXTCLOUD] = metadata
                    updated_task["external_sync"] = external_sync_dict
                else:
                    # It's already a dictionary, just add the metadata
                    logger.debug(f"Adding metadata to external_sync[{NEXTCLOUD}]")
                    updated_task["external_sync"][NEXTCLOUD] = metadata
                
                logger.debug(f"Metadata added successfully")
                logger.debug(f"Updated task with metadata: {updated_task}")
                return updated_task
            except Exception as e:
                logger.error(f"Error updating task with metadata: {e}")
                return {
                    "sync_status": ERROR,
                    "error": str(e)
                }
        except Exception as error:
            logger.error(f"Error creating task in NextCloud: {error}")
            logger.exception("Exception details:")
            
            # Update metadata with error
            metadata["sync_status"] = ERROR
            metadata["error"] = str(error)
            metadata["message"] = f"An unknown error occurred. (Task ID: {task['id']}) (System: {NEXTCLOUD})"
            if self.metadata_store:
                try:
                    self.metadata_store.save_metadata(task["id"], NEXTCLOUD, metadata)
                except Exception as e:
                    logger.error(f"Error saving metadata: {e}")
            
            # Update task with metadata and return
            try:
                # Check if task is a dictionary
                if not isinstance(task, dict):
                    logger.error(f"Task is not a dictionary: {type(task)}")
                    return {
                        "sync_status": ERROR,
                        "error": f"Task is not a dictionary: {type(task)}",
                        "message": "Internal error: Task data has incorrect format"
                    }
                
                updated_task = task.copy()
                if "external_sync" not in updated_task:
                    updated_task["external_sync"] = {}
                
                # Check if external_sync is a list instead of a dict
                if isinstance(updated_task["external_sync"], list):
                    # Convert to a dictionary
                    logger.debug("Converting external_sync from list to dictionary")
                    external_sync_dict = {}
                    external_sync_dict[NEXTCLOUD] = metadata
                    updated_task["external_sync"] = external_sync_dict
                else:
                    # It's already a dictionary, just add the metadata
                    logger.debug(f"Adding metadata to external_sync[{NEXTCLOUD}]")
                    updated_task["external_sync"][NEXTCLOUD] = metadata
                
                logger.debug(f"Metadata added successfully")
                logger.debug(f"Updated task with metadata: {updated_task}")
                return updated_task
            except Exception as e:
                logger.error(f"Error updating task with metadata: {e}")
                return {
                    "sync_status": ERROR,
                    "error": str(e)
                }
    
    async def find_completed_tasks(self) -> List[NextCloudTask]:
        """Find completed tasks in NextCloud.
        
        Returns:
            List of completed NextCloudTask objects
        """
        try:
            return await self.client.find_tasks_by_status("COMPLETED")
        except Exception as e:
            logger.error(f"Error finding completed tasks: {e}")
            return []

    async def find_tasks_by_query(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Find tasks in NextCloud that match the query.
        
        Args:
            query: Query parameters
            
        Returns:
            List of matching tasks
        """
        logger.debug(f"Finding tasks in NextCloud with query: {query}")
        
        try:
            # Get all tasks from NextCloud
            all_tasks = await self.client.get_all_tasks()
            
            # Filter tasks based on query parameters
            filtered_tasks = []
            for task in all_tasks:
                # Check if task matches all query parameters
                match = True
                for key, value in query.items():
                    if key == 'title' and value:
                        # Partial match for title
                        if not value.lower() in task.get('summary', '').lower():
                            match = False
                            break
                    elif key == 'description' and value:
                        # Partial match for description
                        if not value.lower() in task.get('description', '').lower():
                            match = False
                            break
                    elif key == 'status' and value:
                        # Exact match for status
                        if task.get('status') != value:
                            match = False
                            break
                    elif key == 'due_date' and value:
                        # Match for due date (exact or range)
                        task_due = task.get('due')
                        if not task_due:
                            match = False
                            break
                        
                        if isinstance(value, dict):
                            # Range match
                            if 'from' in value and task_due < value['from']:
                                match = False
                                break
                            if 'to' in value and task_due > value['to']:
                                match = False
                                break
                        else:
                            # Exact match
                            if task_due != value:
                                match = False
                                break
                
                # Add matching task to results
                if match:
                    # Convert NextCloud task to Taskinator format
                    taskinator_task = self._convert_from_nextcloud(task)
                    filtered_tasks.append(taskinator_task)
            
            logger.debug(f"Found {len(filtered_tasks)} matching tasks in NextCloud")
            return filtered_tasks
            
        except Exception as e:
            logger.error(f"Error finding tasks in NextCloud: {e}")
            return []

    def _convert_from_nextcloud(self, task: NextCloudTask) -> Dict[str, Any]:
        """Convert a NextCloud task to Taskinator format.
        
        Args:
            task: NextCloud task
            
        Returns:
            Task in Taskinator format
        """
        # Create a new task with basic fields
        taskinator_task = {
            "id": task.id,
            "title": task.title,
            "description": task.description or "",
            "status": self._map_nextcloud_status_to_local(task.status),
            "priority": self._map_nextcloud_priority_to_local(task.priority),
        }
        
        # Add due date if available
        if task.due_date:
            taskinator_task["due_date"] = task.due_date
            
        return taskinator_task
