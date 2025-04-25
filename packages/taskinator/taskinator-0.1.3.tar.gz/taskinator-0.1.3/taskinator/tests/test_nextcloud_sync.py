"""Tests for NextCloud synchronization functionality."""

import json
import unittest
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

from taskinator.nextcloud_client import NextCloudTask
from taskinator.nextcloud_sync import (
    NextCloudSyncMetadata,
    SyncDirection,
    SyncStatus,
    TaskFieldMapping,
    TaskVersionInfo,
    get_nextcloud_metadata,
    update_nextcloud_metadata
)
from taskinator.conflict_resolver import (
    ConflictResolver,
    ConflictResolutionStrategy,
    ManualConflictResolver
)
from taskinator.sync_engine import SyncEngine
from taskinator.utils import ensure_task_structure


class TestNextCloudSyncMetadata(unittest.TestCase):
    """Test NextCloud synchronization metadata."""
    
    def test_init_defaults(self):
        """Test initialization with defaults."""
        metadata = NextCloudSyncMetadata()
        self.assertEqual(metadata.etag, "")
        self.assertEqual(metadata.fileid, "")
        self.assertIsNotNone(metadata.last_sync)
        self.assertEqual(metadata.sync_status, SyncStatus.PENDING)
        self.assertEqual(metadata.version_history, [])
    
    def test_to_dict(self):
        """Test conversion to dictionary."""
        metadata = NextCloudSyncMetadata(
            etag="etag123",
            fileid="file123",
            last_sync=1234567890.0,
            sync_status=SyncStatus.SYNCED,
            version_history=[{"version": 1}]
        )
        
        data = metadata.to_dict()
        self.assertEqual(data["etag"], "etag123")
        self.assertEqual(data["fileid"], "file123")
        self.assertEqual(data["last_sync"], 1234567890.0)
        self.assertEqual(data["sync_status"], "synced")
        self.assertEqual(data["version_history"], [{"version": 1}])
    
    def test_from_dict(self):
        """Test creation from dictionary."""
        data = {
            "etag": "etag123",
            "fileid": "file123",
            "last_sync": 1234567890.0,
            "sync_status": "synced",
            "version_history": [{"version": 1}]
        }
        
        metadata = NextCloudSyncMetadata.from_dict(data)
        self.assertEqual(metadata.etag, "etag123")
        self.assertEqual(metadata.fileid, "file123")
        self.assertEqual(metadata.last_sync, 1234567890.0)
        self.assertEqual(metadata.sync_status, SyncStatus.SYNCED)
        self.assertEqual(metadata.version_history, [{"version": 1}])
    
    def test_add_version(self):
        """Test adding a version to history."""
        metadata = NextCloudSyncMetadata()
        changes = [{"field": "title", "value": "New Title"}]
        
        metadata.add_version(changes=changes, modified_by="local")
        
        self.assertEqual(len(metadata.version_history), 1)
        version = metadata.version_history[0]
        self.assertEqual(version["version"], 1)
        self.assertEqual(version["modified_by"], "local")
        self.assertEqual(version["changes"], changes)
        
        # Add another version
        metadata.add_version(changes=[{"field": "status", "value": "done"}], modified_by="nextcloud")
        
        self.assertEqual(len(metadata.version_history), 2)
        version = metadata.version_history[1]
        self.assertEqual(version["version"], 2)
        self.assertEqual(version["modified_by"], "nextcloud")


class TestTaskFieldMapping(unittest.TestCase):
    """Test task field mapping."""
    
    def test_map_local_to_remote(self):
        """Test mapping from local to remote."""
        local_task = {
            "id": 1,
            "title": "Test Task",
            "description": "Test Description",
            "status": "done",
            "priority": "high",
            "due_date": 1234567890.0
        }
        
        remote_data = TaskFieldMapping.map_local_to_remote(local_task)
        
        self.assertEqual(remote_data["title"], "Test Task")
        self.assertEqual(remote_data["description"], "Test Description")
        self.assertTrue(remote_data["completed"])
        self.assertEqual(remote_data["priority"], 1)
        self.assertIsInstance(remote_data["due_date"], datetime)
    
    def test_map_remote_to_local(self):
        """Test mapping from remote to local."""
        remote_task = NextCloudTask(
            id="123",
            title="Remote Task",
            description="Remote Description",
            completed=True,
            priority=1,
            due_date=datetime.fromtimestamp(1234567890.0)
        )
        
        local_data = TaskFieldMapping.map_remote_to_local(remote_task)
        
        self.assertEqual(local_data["title"], "Remote Task")
        self.assertEqual(local_data["description"], "Remote Description")
        self.assertEqual(local_data["status"], "done")
        self.assertEqual(local_data["priority"], "high")
        self.assertEqual(local_data["due_date"], 1234567890.0)


class TestTaskMetadataFunctions(unittest.TestCase):
    """Test task metadata functions."""
    
    def test_get_nextcloud_metadata(self):
        """Test getting NextCloud metadata from a task."""
        # Task without metadata
        task = {"id": 1, "title": "Test"}
        metadata = get_nextcloud_metadata(task)
        self.assertIsInstance(metadata, NextCloudSyncMetadata)
        self.assertEqual(metadata.etag, "")
        
        # Task with metadata
        task = {
            "id": 1,
            "title": "Test",
            "nextcloud": {
                "etag": "etag123",
                "fileid": "file123",
                "last_sync": 1234567890.0,
                "sync_status": "synced",
                "version_history": []
            }
        }
        
        metadata = get_nextcloud_metadata(task)
        self.assertEqual(metadata.etag, "etag123")
        self.assertEqual(metadata.fileid, "file123")
        self.assertEqual(metadata.last_sync, 1234567890.0)
        self.assertEqual(metadata.sync_status, SyncStatus.SYNCED)
    
    def test_update_nextcloud_metadata(self):
        """Test updating NextCloud metadata in a task."""
        task = {"id": 1, "title": "Test"}
        metadata = NextCloudSyncMetadata(
            etag="etag123",
            fileid="file123",
            last_sync=1234567890.0,
            sync_status=SyncStatus.SYNCED
        )
        
        updated_task = update_nextcloud_metadata(task, metadata)
        
        self.assertIn("nextcloud", updated_task)
        self.assertEqual(updated_task["nextcloud"]["etag"], "etag123")
        self.assertEqual(updated_task["nextcloud"]["fileid"], "file123")
        self.assertEqual(updated_task["nextcloud"]["last_sync"], 1234567890.0)
        self.assertEqual(updated_task["nextcloud"]["sync_status"], "synced")


class TestBackwardCompatibility(unittest.TestCase):
    """Test backward compatibility with existing functionality."""
    
    def test_ensure_task_structure_with_nextcloud(self):
        """Test that ensure_task_structure works with NextCloud metadata."""
        # Create a task with NextCloud metadata
        task = {
            "id": 1,
            "title": "Test Task",
            "nextcloud": {
                "etag": "etag123",
                "fileid": "file123",
                "last_sync": 1234567890.0,
                "sync_status": "synced",
                "version_history": []
            }
        }
        
        # Ensure task structure
        complete_task = ensure_task_structure(task)
        
        # Verify that NextCloud metadata is preserved
        self.assertIn("nextcloud", complete_task)
        self.assertEqual(complete_task["nextcloud"]["etag"], "etag123")
        self.assertEqual(complete_task["nextcloud"]["fileid"], "file123")
        
        # Verify that default fields are added
        self.assertIn("status", complete_task)
        self.assertIn("priority", complete_task)
        self.assertIn("dependencies", complete_task)
        self.assertIn("subtasks", complete_task)
    
    def test_ensure_task_structure_without_nextcloud(self):
        """Test that ensure_task_structure adds default NextCloud metadata."""
        # Create a task without NextCloud metadata
        task = {
            "id": 1,
            "title": "Test Task"
        }
        
        # Ensure task structure
        complete_task = ensure_task_structure(task)
        
        # Verify that NextCloud metadata is added with defaults
        self.assertIn("nextcloud", complete_task)
        self.assertEqual(complete_task["nextcloud"]["etag"], "")
        self.assertEqual(complete_task["nextcloud"]["fileid"], "")
        self.assertEqual(complete_task["nextcloud"]["sync_status"], "pending")
        
        # Verify that default fields are added
        self.assertIn("status", complete_task)
        self.assertIn("priority", complete_task)
        self.assertIn("dependencies", complete_task)
        self.assertIn("subtasks", complete_task)


if __name__ == "__main__":
    unittest.main()
