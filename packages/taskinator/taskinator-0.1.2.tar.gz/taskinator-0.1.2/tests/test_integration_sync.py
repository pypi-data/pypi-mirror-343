"""Integration tests for the external synchronization system."""

import json
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import patch, MagicMock, AsyncMock
import os
import asyncio
import tempfile
import shutil

# Update imports to use the correct module directly
from taskinator import external_integration
from taskinator.external_integration.sync_metadata_store import SyncMetadataStore
from taskinator.external_adapters.nextcloud_adapter import NextCloudAdapter, NextCloudTask
from taskinator.sync_manager import SyncManager
from taskinator.task_manager import TaskManager


class TestIntegrationSync(unittest.IsolatedAsyncioTestCase):
    """Integration tests for the external synchronization system."""

    def setUp(self):
        """Set up test environment."""
        # Create a temporary tasks directory for testing
        self.temp_dir = tempfile.mkdtemp(prefix="taskinator_test_")
        self.tasks_data = {
            "tasks": [
                {
                    "id": 1,
                    "title": "Test Task 1",
                    "description": "Test Description 1",
                    "status": "pending",
                    "priority": "medium",
                    "created": datetime.now().timestamp(),
                    "updated": datetime.now().timestamp()
                },
                {
                    "id": 2,
                    "title": "Test Task 2",
                    "description": "Test Description 2",
                    "status": "pending",
                    "priority": "high",
                    "created": datetime.now().timestamp(),
                    "updated": datetime.now().timestamp()
                }
            ]
        }
        
        # Write tasks to file
        self.tasks_file = os.path.join(self.temp_dir, "tasks.json")
        with open(self.tasks_file, "w") as f:
            json.dump(self.tasks_data, f)

    def tearDown(self):
        """Clean up after tests."""
        # Remove temporary directory and all its contents
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    async def test_end_to_end_sync_new_task(self):
        """Test end-to-end synchronization of a new task to NextCloud."""
        # Create a mock SyncManager
        mock_sync_manager = MagicMock()
        mock_sync_manager.sync_task = AsyncMock(return_value={
            "status": "success",
            "details": [
                {
                    "task_id": 1,
                    "system": external_integration.ExternalSystem.NEXTCLOUD.value,
                    "status": "success",
                    "message": "Task synced successfully"
                }
            ]
        })
        
        # Patch the import inside the method
        with patch('taskinator.sync_manager.SyncManager', return_value=mock_sync_manager):
            # Create TaskManager
            task_manager = TaskManager(self.temp_dir)
            
            # Sync task 1 to NextCloud
            result = await task_manager.sync_tasks(
                system=external_integration.ExternalSystem.NEXTCLOUD.value,
                task_id=1,
                direction="local_to_remote"
            )
        
        # Verify result
        self.assertEqual(result["status"], "success")
        self.assertIn("details", result)
        self.assertEqual(len(result["details"]), 1)
        self.assertEqual(result["details"][0]["task_id"], 1)
        self.assertEqual(result["details"][0]["system"], external_integration.ExternalSystem.NEXTCLOUD.value)
        self.assertEqual(result["details"][0]["status"], "success")
        
        # Verify SyncManager was called correctly
        mock_sync_manager.sync_task.assert_called_once()
        call_args = mock_sync_manager.sync_task.call_args[0]
        self.assertEqual(str(call_args[0]), '1')  # task_id is converted to string
        self.assertEqual(call_args[1], "local_to_remote")  # direction

    async def test_end_to_end_bidirectional_sync(self):
        """Test end-to-end bidirectional synchronization with NextCloud."""
        # Create a mock SyncManager
        mock_sync_manager = MagicMock()
        mock_sync_manager.sync_task = AsyncMock(return_value={
            "status": "success",
            "details": [
                {
                    "task_id": 1,
                    "system": external_integration.ExternalSystem.NEXTCLOUD.value,
                    "status": "success",
                    "message": "Task synced successfully"
                }
            ]
        })
        
        # Patch the import inside the method
        with patch('taskinator.sync_manager.SyncManager', return_value=mock_sync_manager):
            # Create TaskManager
            task_manager = TaskManager(self.temp_dir)
            
            # Sync task 1 bidirectionally
            result = await task_manager.sync_tasks(
                system=external_integration.ExternalSystem.NEXTCLOUD.value,
                task_id=1,
                direction="bidirectional"
            )
        
        # Verify result
        self.assertEqual(result["status"], "success")
        self.assertIn("details", result)
        self.assertEqual(len(result["details"]), 1)
        self.assertEqual(result["details"][0]["task_id"], 1)
        self.assertEqual(result["details"][0]["system"], external_integration.ExternalSystem.NEXTCLOUD.value)
        self.assertEqual(result["details"][0]["status"], "success")
        
        # Verify SyncManager was called correctly
        mock_sync_manager.sync_task.assert_called_once()
        call_args = mock_sync_manager.sync_task.call_args[0]
        self.assertEqual(str(call_args[0]), '1')  # task_id is converted to string
        self.assertEqual(call_args[1], "bidirectional")  # direction

    async def test_end_to_end_conflict_resolution_local(self):
        """Test end-to-end conflict resolution with NextCloud using local strategy."""
        # Create a mock SyncManager for local resolution
        mock_sync_manager = MagicMock()
        mock_sync_manager.resolve_conflict = AsyncMock(return_value={
            "status": "success",
            "task_id": 1,
            "resolution": "local",
            "system": external_integration.ExternalSystem.NEXTCLOUD.value
        })
        
        # Patch the import inside the method
        with patch('taskinator.sync_manager.SyncManager', return_value=mock_sync_manager):
            # Create TaskManager
            task_manager = TaskManager(self.temp_dir)
            
            # Resolve conflict using "local" strategy
            result = await task_manager.resolve_conflict(
                task_id=1,
                system=external_integration.ExternalSystem.NEXTCLOUD.value,
                resolution="local"
            )
        
        # Verify result
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["task_id"], 1)
        self.assertEqual(result["resolution"], "local")
        
        # Verify SyncManager was called correctly
        mock_sync_manager.resolve_conflict.assert_called_once()
        call_args = mock_sync_manager.resolve_conflict.call_args[0]
        self.assertEqual(str(call_args[0]), '1')  # task_id is converted to string
        self.assertEqual(call_args[1], external_integration.ExternalSystem.NEXTCLOUD.value)  # system
        self.assertEqual(call_args[2], "local")  # resolution

    async def test_end_to_end_conflict_resolution_remote(self):
        """Test end-to-end conflict resolution with NextCloud using remote strategy."""
        # Create a mock SyncManager for remote resolution
        mock_sync_manager = MagicMock()
        mock_sync_manager.resolve_conflict = AsyncMock(return_value={
            "status": "success",
            "task_id": 1,
            "resolution": "remote",
            "system": external_integration.ExternalSystem.NEXTCLOUD.value
        })
        
        # Patch the import inside the method
        with patch('taskinator.sync_manager.SyncManager', return_value=mock_sync_manager):
            # Create TaskManager
            task_manager = TaskManager(self.temp_dir)
            
            # Resolve conflict using "remote" strategy
            result = await task_manager.resolve_conflict(
                task_id=1,
                system=external_integration.ExternalSystem.NEXTCLOUD.value,
                resolution="remote"
            )
        
        # Verify result
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["task_id"], 1)
        self.assertEqual(result["resolution"], "remote")
        
        # Verify SyncManager was called correctly
        mock_sync_manager.resolve_conflict.assert_called_once()
        call_args = mock_sync_manager.resolve_conflict.call_args[0]
        self.assertEqual(str(call_args[0]), '1')  # task_id is converted to string
        self.assertEqual(call_args[1], external_integration.ExternalSystem.NEXTCLOUD.value)  # system
        self.assertEqual(call_args[2], "remote")  # resolution

    async def test_end_to_end_bulk_sync(self):
        """Test end-to-end bulk synchronization with NextCloud."""
        # Create a mock SyncManager
        mock_sync_manager = MagicMock()
        mock_sync_manager.sync_all = AsyncMock(return_value={
            "status": "success",
            "total": 2,
            "synced": 2,
            "errors": 0,
            "conflicts": 0,
            "skipped": 0,
            "details": [
                {
                    "task_id": 1,
                    "system": external_integration.ExternalSystem.NEXTCLOUD.value,
                    "status": "success",
                    "message": "Task synced successfully"
                },
                {
                    "task_id": 2,
                    "system": external_integration.ExternalSystem.NEXTCLOUD.value,
                    "status": "success",
                    "message": "Task synced successfully"
                }
            ]
        })
        
        # Patch the import inside the method
        with patch('taskinator.sync_manager.SyncManager', return_value=mock_sync_manager):
            # Create TaskManager
            task_manager = TaskManager(self.temp_dir)
            
            # Sync all tasks
            result = await task_manager.sync_tasks(system=external_integration.ExternalSystem.NEXTCLOUD.value)
        
        # Verify result
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["total"], 2)
        self.assertEqual(result["synced"], 2)
        self.assertEqual(result["errors"], 0)
        self.assertEqual(result["conflicts"], 0)
        self.assertEqual(result["skipped"], 0)
        
        # Verify SyncManager was called correctly
        mock_sync_manager.sync_all.assert_called_once()
        call_args = mock_sync_manager.sync_all.call_args[0]
        self.assertEqual(call_args[0], "bidirectional")  # direction


if __name__ == "__main__":
    unittest.main()
