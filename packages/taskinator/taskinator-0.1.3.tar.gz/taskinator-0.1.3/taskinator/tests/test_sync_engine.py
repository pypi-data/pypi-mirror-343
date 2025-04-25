"""Tests for NextCloud synchronization engine."""

import asyncio
import unittest
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch

from taskinator.nextcloud_client import NextCloudClient, NextCloudTask
from taskinator.nextcloud_sync import (
    NextCloudSyncMetadata,
    SyncDirection,
    SyncStatus,
    get_nextcloud_metadata,
    update_nextcloud_metadata
)
from taskinator.conflict_resolver import ConflictResolutionStrategy
from taskinator.sync_engine import SyncEngine


class TestSyncEngine(unittest.IsolatedAsyncioTestCase):
    """Test synchronization engine functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a mock NextCloud client
        self.mock_client = MagicMock(spec=NextCloudClient)
        self.mock_client.get_tasks = AsyncMock()
        self.mock_client.create_task = AsyncMock()
        self.mock_client.update_task = AsyncMock()
        self.mock_client.delete_task = AsyncMock()
        
        # Create the sync engine
        self.sync_engine = SyncEngine(
            nextcloud_client=self.mock_client,
            conflict_strategy=ConflictResolutionStrategy.NEWEST_WINS
        )
        
        # Create a local task without NextCloud ID
        self.new_local_task = {
            "id": 1,
            "title": "New Local Task",
            "description": "New Local Description",
            "status": "pending",
            "priority": "high",
            "updated": datetime.now().timestamp(),
            "nextcloud": {
                "etag": "",
                "fileid": "",
                "last_sync": 0,
                "sync_status": "pending",
                "version_history": []
            }
        }
        
        # Create a local task with NextCloud ID
        self.existing_local_task = {
            "id": 2,
            "title": "Existing Local Task",
            "description": "Existing Local Description",
            "status": "pending",
            "priority": "medium",
            "updated": datetime.now().timestamp() - 3600,  # 1 hour ago
            "nextcloud": {
                "etag": "etag123",
                "fileid": "file123",
                "last_sync": datetime.now().timestamp() - 7200,  # 2 hours ago
                "sync_status": "synced",
                "version_history": []
            }
        }
        
        # Create a remote task
        self.remote_task = NextCloudTask(
            id="file123",
            title="Remote Task",
            description="Remote Description",
            completed=True,
            priority=1,
            modified=datetime.now() - timedelta(hours=1.5)  # 1.5 hours ago
        )
    
    @patch('taskinator.sync_engine.datetime')
    async def test_push_to_nextcloud_new_task(self, mock_datetime):
        """Test pushing a new task to NextCloud."""
        # Set up mock datetime
        mock_now = datetime.now()
        mock_datetime.now.return_value = mock_now
        
        # Set up mock client response
        new_remote_task = NextCloudTask(
            id="new_file_id",
            title="New Local Task",
            description="New Local Description",
            completed=False,
            priority=1,
            etag="new_etag"
        )
        self.mock_client.create_task.return_value = new_remote_task
        
        # Sync the task
        updated_task = await self.sync_engine.sync_task(
            self.new_local_task,
            direction=SyncDirection.LOCAL_TO_REMOTE
        )
        
        # Verify client was called
        self.mock_client.create_task.assert_called_once()
        
        # Verify task was updated with NextCloud metadata
        metadata = get_nextcloud_metadata(updated_task)
        self.assertEqual(metadata.fileid, "new_file_id")
        self.assertEqual(metadata.etag, "new_etag")
        self.assertEqual(metadata.sync_status, SyncStatus.SYNCED)
        self.assertEqual(metadata.last_sync, mock_now.timestamp())
        
        # Verify version history was updated
        self.assertEqual(len(metadata.version_history), 1)
        version = metadata.version_history[0]
        self.assertEqual(version["modified_by"], "local")
    
    @patch('taskinator.sync_engine.datetime')
    async def test_push_to_nextcloud_existing_task(self, mock_datetime):
        """Test pushing an existing task to NextCloud."""
        # Set up mock datetime
        mock_now = datetime.now()
        mock_datetime.now.return_value = mock_now
        
        # Set up mock client response
        updated_remote_task = NextCloudTask(
            id="file123",
            title="Existing Local Task",
            description="Existing Local Description",
            completed=False,
            priority=5,
            etag="updated_etag"
        )
        self.mock_client.update_task.return_value = updated_remote_task
        
        # Sync the task
        updated_task = await self.sync_engine.sync_task(
            self.existing_local_task,
            direction=SyncDirection.LOCAL_TO_REMOTE
        )
        
        # Verify client was called
        self.mock_client.update_task.assert_called_once_with(
            "file123",
            self.mock_client.update_task.call_args[0][1]
        )
        
        # Verify task was updated with NextCloud metadata
        metadata = get_nextcloud_metadata(updated_task)
        self.assertEqual(metadata.fileid, "file123")
        self.assertEqual(metadata.etag, "updated_etag")
        self.assertEqual(metadata.sync_status, SyncStatus.SYNCED)
        self.assertEqual(metadata.last_sync, mock_now.timestamp())
        
        # Verify version history was updated
        self.assertEqual(len(metadata.version_history), 1)
        version = metadata.version_history[0]
        self.assertEqual(version["modified_by"], "local")
    
    async def test_pull_from_nextcloud(self):
        """Test pulling a task from NextCloud."""
        # Set up mock client response
        self.mock_client.get_tasks.return_value = [self.remote_task]
        
        # Sync the task
        updated_task = await self.sync_engine.sync_task(
            self.existing_local_task,
            direction=SyncDirection.REMOTE_TO_LOCAL
        )
        
        # Verify client was called
        self.mock_client.get_tasks.assert_called_once()
        
        # Verify task was updated with remote data
        self.assertEqual(updated_task["title"], "Remote Task")
        self.assertEqual(updated_task["description"], "Remote Description")
        self.assertEqual(updated_task["status"], "done")  # completed=True -> status="done"
        self.assertEqual(updated_task["priority"], "high")  # priority=1 -> priority="high"
        
        # Verify metadata was updated
        metadata = get_nextcloud_metadata(updated_task)
        self.assertEqual(metadata.sync_status, SyncStatus.SYNCED)
        
        # Verify version history was updated
        self.assertEqual(len(metadata.version_history), 1)
        version = metadata.version_history[0]
        self.assertEqual(version["modified_by"], "nextcloud")
    
    async def test_bidirectional_sync_local_newer(self):
        """Test bidirectional sync when local is newer."""
        # Set up mock client response
        self.mock_client.get_tasks.return_value = [self.remote_task]
        
        # Make local task newer than remote and last sync
        self.existing_local_task["updated"] = datetime.now().timestamp()
        
        # Sync the task
        updated_task = await self.sync_engine.sync_task(
            self.existing_local_task,
            direction=SyncDirection.BIDIRECTIONAL
        )
        
        # Verify client methods were called
        self.mock_client.get_tasks.assert_called_once()
        self.mock_client.update_task.assert_called_once()
        
        # Verify local data was preserved
        self.assertEqual(updated_task["title"], "Existing Local Task")
        self.assertEqual(updated_task["description"], "Existing Local Description")
    
    async def test_bidirectional_sync_remote_newer(self):
        """Test bidirectional sync when remote is newer."""
        # Set up mock client response with a very recent remote task
        recent_remote_task = NextCloudTask(
            id="file123",
            title="Recent Remote Task",
            description="Recent Remote Description",
            completed=True,
            priority=1,
            modified=datetime.now()  # Just now
        )
        self.mock_client.get_tasks.return_value = [recent_remote_task]
        
        # Sync the task
        updated_task = await self.sync_engine.sync_task(
            self.existing_local_task,
            direction=SyncDirection.BIDIRECTIONAL
        )
        
        # Verify client methods were called
        self.mock_client.get_tasks.assert_called_once()
        
        # Verify remote data was used
        self.assertEqual(updated_task["title"], "Recent Remote Task")
        self.assertEqual(updated_task["description"], "Recent Remote Description")
        self.assertEqual(updated_task["status"], "done")
    
    async def test_sync_all_tasks(self):
        """Test syncing all tasks."""
        # Set up mock client responses
        self.mock_client.get_tasks.return_value = [self.remote_task]
        
        new_remote_task = NextCloudTask(
            id="new_file_id",
            title="New Local Task",
            description="New Local Description",
            completed=False,
            priority=1,
            etag="new_etag"
        )
        self.mock_client.create_task.return_value = new_remote_task
        
        # Create a list of tasks to sync
        tasks = [self.new_local_task, self.existing_local_task]
        
        # Add a task with subtasks
        parent_task = {
            "id": 3,
            "title": "Parent Task",
            "description": "Parent Description",
            "status": "pending",
            "priority": "medium",
            "updated": datetime.now().timestamp(),
            "nextcloud": {
                "etag": "",
                "fileid": "",
                "last_sync": 0,
                "sync_status": "pending",
                "version_history": []
            },
            "subtasks": [
                {
                    "id": "3.1",
                    "title": "Subtask 1",
                    "description": "Subtask 1 Description",
                    "status": "pending",
                    "priority": "medium",
                    "updated": datetime.now().timestamp(),
                    "nextcloud": {
                        "etag": "",
                        "fileid": "",
                        "last_sync": 0,
                        "sync_status": "pending",
                        "version_history": []
                    }
                }
            ]
        }
        tasks.append(parent_task)
        
        # Sync all tasks
        updated_tasks = await self.sync_engine.sync_all_tasks(
            tasks,
            direction=SyncDirection.BIDIRECTIONAL
        )
        
        # Verify we got the right number of tasks back
        self.assertEqual(len(updated_tasks), 3)
        
        # Verify the parent task and its subtask were synced
        parent = next(t for t in updated_tasks if t["id"] == 3)
        self.assertEqual(len(parent["subtasks"]), 1)
        
        # Verify the subtask has parent_id
        subtask = parent["subtasks"][0]
        self.assertEqual(subtask["parent_id"], 3)
    
    async def test_handle_error(self):
        """Test error handling during sync."""
        # Make client raise an exception
        self.mock_client.get_tasks.side_effect = Exception("Test error")
        
        # Sync the task
        updated_task = await self.sync_engine.sync_task(
            self.existing_local_task,
            direction=SyncDirection.REMOTE_TO_LOCAL
        )
        
        # Verify error was handled
        metadata = get_nextcloud_metadata(updated_task)
        self.assertEqual(metadata.sync_status, SyncStatus.ERROR)


if __name__ == "__main__":
    asyncio.run(unittest.main())
