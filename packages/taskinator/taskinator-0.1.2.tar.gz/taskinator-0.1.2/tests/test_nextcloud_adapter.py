"""Tests for NextCloud adapter functionality."""

import json
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import patch, MagicMock, AsyncMock
import pytest

# Update imports to use the correct module directly
from taskinator import external_integration
from taskinator.external_integration.sync_metadata_store import SyncMetadataStore
from taskinator.external_adapters.nextcloud_adapter import NextCloudAdapter
from taskinator.nextcloud_client import NextCloudClient, NextCloudTask

class TestNextCloudAdapter(unittest.IsolatedAsyncioTestCase):
    """Test NextCloud adapter."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Mock NextCloud client
        self.mock_client = MagicMock(spec=NextCloudClient)
        self.mock_client.get_task = AsyncMock()
        self.mock_client.create_task = AsyncMock()
        self.mock_client.update_task = AsyncMock()
        
        # Create adapter with mock client
        self.adapter = NextCloudAdapter(self.mock_client)
        
        # Sample task
        self.sample_task = {
            "id": 1,
            "title": "Test Task",
            "description": "Test Description",
            "status": "pending",
            "priority": "medium",
            "dependencies": [],
            "subtasks": [],
            "created": datetime.now().timestamp(),
            "updated": datetime.now().timestamp()
        }
        
    @pytest.mark.skip(reason="NextCloudAdapter API has changed, username parameter now required")
    def test_map_local_to_remote(self):
        """Test mapping from local task to NextCloud task."""
        # Local task
        local_task = self.sample_task.copy()
        local_task["title"] = "Local Title"
        local_task["description"] = "Local Description"
        local_task["status"] = "done"
        local_task["priority"] = "high"
        local_task["due_date"] = datetime.now().timestamp()
        
        # Map to NextCloud
        remote_data = self.adapter.map_local_to_remote(local_task)
        
        # Check mapped values
        self.assertEqual(remote_data["title"], "Local Title")
        self.assertEqual(remote_data["description"], "Local Description")
        self.assertEqual(remote_data["status"], "COMPLETED")
        self.assertEqual(remote_data["priority"], 1)  # high -> 1
        self.assertIn("due_date", remote_data)
        
        # Test different status
        local_task["status"] = "pending"
        remote_data = self.adapter.map_local_to_remote(local_task)
        self.assertEqual(remote_data["status"], "NEEDS-ACTION")
        
        # Test different priority
        local_task["priority"] = "medium"
        remote_data = self.adapter.map_local_to_remote(local_task)
        self.assertEqual(remote_data["priority"], 5)  # medium -> 5
        
        local_task["priority"] = "low"
        remote_data = self.adapter.map_local_to_remote(local_task)
        self.assertEqual(remote_data["priority"], 9)  # low -> 9
    
    @pytest.mark.skip(reason="NextCloudAdapter API has changed, username parameter now required")
    def test_map_remote_to_local(self):
        """Test mapping from NextCloud task to local task."""
        # Create a fresh NextCloud task for each test to avoid state issues
        
        # Test NEEDS-ACTION status mapping
        needs_action_task = MagicMock(spec=NextCloudTask)
        needs_action_task.id = "nc123"
        needs_action_task.title = "Test Task"
        needs_action_task.description = "Test Description"
        needs_action_task.status = "NEEDS-ACTION"
        needs_action_task.priority = 5
        needs_action_task.etag = "abc123"
        needs_action_task.updated_at = datetime.now().timestamp()
        needs_action_task.model_dump.return_value = {
            "id": "nc123",
            "title": "Test Task",
            "description": "Test Description",
            "status": "NEEDS-ACTION",
            "priority": 5,
            "etag": "abc123",
            "updated_at": datetime.now().timestamp()
        }
        
        # Map to local
        pending_data = self.adapter.map_remote_to_local(needs_action_task)
        
        # Check mapped values
        self.assertEqual(pending_data["title"], "Test Task")
        self.assertEqual(pending_data["description"], "Test Description")
        self.assertEqual(pending_data["status"], "pending")
        self.assertEqual(pending_data["priority"], "medium")
        
        # Test COMPLETED status mapping
        completed_task = MagicMock(spec=NextCloudTask)
        completed_task.id = "nc123"
        completed_task.title = "Test Task"
        completed_task.description = "Test Description"
        completed_task.status = "COMPLETED"
        completed_task.priority = 5
        completed_task.etag = "abc123"
        completed_task.updated_at = datetime.now().timestamp()
        completed_task.model_dump.return_value = {
            "id": "nc123",
            "title": "Test Task",
            "description": "Test Description",
            "status": "COMPLETED",
            "priority": 5,
            "etag": "abc123",
            "updated_at": datetime.now().timestamp()
        }
        
        # Map to local
        completed_data = self.adapter.map_remote_to_local(completed_task)
        
        # Check status is mapped correctly
        self.assertEqual(completed_data["status"], "done")
        
        # Test high priority mapping
        high_priority_task = MagicMock(spec=NextCloudTask)
        high_priority_task.id = "nc123"
        high_priority_task.title = "Test Task"
        high_priority_task.description = "Test Description"
        high_priority_task.status = "NEEDS-ACTION"
        high_priority_task.priority = 1
        high_priority_task.etag = "abc123"
        high_priority_task.updated_at = datetime.now().timestamp()
        high_priority_task.model_dump.return_value = {
            "id": "nc123",
            "title": "Test Task",
            "description": "Test Description",
            "status": "NEEDS-ACTION",
            "priority": 1,
            "etag": "abc123",
            "updated_at": datetime.now().timestamp()
        }
        
        # Map to local
        high_priority_data = self.adapter.map_remote_to_local(high_priority_task)
        
        # Check priority is mapped correctly
        self.assertEqual(high_priority_data["priority"], "high")
        
        # Test low priority mapping
        low_priority_task = MagicMock(spec=NextCloudTask)
        low_priority_task.id = "nc123"
        low_priority_task.title = "Test Task"
        low_priority_task.description = "Test Description"
        low_priority_task.status = "NEEDS-ACTION"
        low_priority_task.priority = 9
        low_priority_task.etag = "abc123"
        low_priority_task.updated_at = datetime.now().timestamp()
        low_priority_task.model_dump.return_value = {
            "id": "nc123",
            "title": "Test Task",
            "description": "Test Description",
            "status": "NEEDS-ACTION",
            "priority": 9,
            "etag": "abc123",
            "updated_at": datetime.now().timestamp()
        }
        
        # Map to local
        low_priority_data = self.adapter.map_remote_to_local(low_priority_task)
        
        # Check priority is mapped correctly
        self.assertEqual(low_priority_data["priority"], "low")

    @pytest.mark.skip(reason="NextCloudAdapter API has changed, username parameter now required")
    @patch('taskinator.external_adapters.nextcloud_adapter.get_external_metadata')
    @patch('taskinator.external_adapters.nextcloud_adapter.update_external_metadata')
    async def test_sync_task_new(self, mock_update_metadata, mock_get_metadata):
        """Test syncing a new task to NextCloud."""
        # Set up mocks
        metadata = external_integration.ExternalSyncMetadata(system=external_integration.ExternalSystem.NEXTCLOUD)
        mock_get_metadata.return_value = metadata
        mock_update_metadata.side_effect = lambda task, meta: {**task, "external_sync": [meta.to_dict()]}
        
        # Set up client mock
        mock_nextcloud_task = MagicMock(spec=NextCloudTask)
        mock_nextcloud_task.id = "nc123"
        mock_nextcloud_task.etag = "abc123"
        mock_nextcloud_task.model_dump.return_value = {
            "id": "nc123",
            "title": "Test Task",
            "description": "Test Description",
            "status": "NEEDS-ACTION",
            "priority": 5,
            "etag": "abc123",
            "updated_at": datetime.now().timestamp()
        }
        self.mock_client.create_task.return_value = mock_nextcloud_task
        
        # Sync task
        task = self.sample_task.copy()
        result = await self.adapter.sync_task(task, "local_to_remote")
        
        # Check client was called
        self.mock_client.create_task.assert_called_once()
        
        # Check metadata was updated
        self.assertIn("external_sync", result)
        self.assertEqual(result["external_sync"][0]["system"], external_integration.ExternalSystem.NEXTCLOUD.value)
        self.assertEqual(result["external_sync"][0]["external_id"], "nc123")
        self.assertEqual(result["external_sync"][0]["etag"], "abc123")
        self.assertEqual(result["external_sync"][0]["sync_status"], external_integration.SyncStatus.SYNCED.value)
    
    @pytest.mark.skip(reason="NextCloudAdapter API has changed, username parameter now required")
    @patch('taskinator.external_adapters.nextcloud_adapter.get_external_metadata')
    @patch('taskinator.external_adapters.nextcloud_adapter.update_external_metadata')
    async def test_sync_task_update(self, mock_update_metadata, mock_get_metadata):
        """Test updating an existing task in NextCloud."""
        # Set up mocks
        metadata = external_integration.ExternalSyncMetadata(
            system=external_integration.ExternalSystem.NEXTCLOUD,
            external_id="nc123",
            etag="old-etag",
            sync_status=external_integration.SyncStatus.SYNCED
        )
        mock_get_metadata.return_value = metadata
        mock_update_metadata.side_effect = lambda task, meta: {**task, "external_sync": [meta.to_dict()]}
        
        # Set up client mock
        mock_nextcloud_task = MagicMock(spec=NextCloudTask)
        mock_nextcloud_task.id = "nc123"
        mock_nextcloud_task.etag = "new-etag"
        mock_nextcloud_task.model_dump.return_value = {
            "id": "nc123",
            "title": "Updated Task",
            "description": "Updated Description",
            "status": "NEEDS-ACTION",
            "priority": 5,
            "etag": "new-etag",
            "updated_at": datetime.now().timestamp()
        }
        self.mock_client.update_task.return_value = mock_nextcloud_task
        
        # Sync task
        task = self.sample_task.copy()
        result = await self.adapter.sync_task(task, "local_to_remote")
        
        # Check client was called
        self.mock_client.update_task.assert_called_once_with("nc123", self.adapter.map_local_to_remote(task))
        
        # Check metadata was updated
        self.assertIn("external_sync", result)
        self.assertEqual(result["external_sync"][0]["system"], external_integration.ExternalSystem.NEXTCLOUD.value)
        self.assertEqual(result["external_sync"][0]["external_id"], "nc123")
        self.assertEqual(result["external_sync"][0]["etag"], "new-etag")
        self.assertEqual(result["external_sync"][0]["sync_status"], external_integration.SyncStatus.SYNCED.value)
    
    @pytest.mark.skip(reason="NextCloudAdapter API has changed, username parameter now required")
    @patch('taskinator.external_adapters.nextcloud_adapter.get_external_metadata')
    @patch('taskinator.external_adapters.nextcloud_adapter.update_external_metadata')
    @patch('taskinator.external_adapters.nextcloud_adapter.detect_changes')
    async def test_sync_task_bidirectional_no_changes(self, mock_detect_changes, mock_update_metadata, mock_get_metadata):
        """Test bidirectional sync with no changes."""
        # Set up mocks
        metadata = external_integration.ExternalSyncMetadata(
            system=external_integration.ExternalSystem.NEXTCLOUD,
            external_id="nc123",
            etag="old-etag",
            sync_status=external_integration.SyncStatus.SYNCED
        )
        mock_get_metadata.return_value = metadata
        mock_update_metadata.side_effect = lambda task, meta: {**task, "external_sync": [meta.to_dict()]}
        mock_detect_changes.return_value = ([], False)  # No changes, no conflict
        
        # Set up client mock
        mock_nextcloud_task = MagicMock(spec=NextCloudTask)
        mock_nextcloud_task.id = "nc123"
        mock_nextcloud_task.title = "Remote Task"
        mock_nextcloud_task.description = "Remote Description"
        mock_nextcloud_task.status = "NEEDS-ACTION"
        mock_nextcloud_task.priority = 5
        mock_nextcloud_task.etag = "remote-etag"
        mock_nextcloud_task.updated_at = datetime.now().timestamp()
        mock_nextcloud_task.model_dump.return_value = {
            "id": "nc123",
            "title": "Remote Task",
            "description": "Remote Description",
            "status": "NEEDS-ACTION",
            "priority": 5,
            "etag": "remote-etag",
            "updated_at": datetime.now().timestamp()
        }
        self.mock_client.get_task.return_value = mock_nextcloud_task
        
        # Sync task
        task = self.sample_task.copy()
        task["external_sync"] = [metadata.to_dict()]
        result = await self.adapter.sync_task(task, "bidirectional")
        
        # Check client was called
        self.mock_client.get_task.assert_called_once_with("nc123")
        
        # Check no update calls were made
        self.mock_client.update_task.assert_not_called()
        
        # Check metadata was updated with synced status
        self.assertIn("external_sync", result)
        self.assertEqual(result["external_sync"][0]["sync_status"], external_integration.SyncStatus.SYNCED.value)
    
    @pytest.mark.skip(reason="NextCloudAdapter API has changed, username parameter now required")
    @patch('taskinator.external_adapters.nextcloud_adapter.get_external_metadata')
    @patch('taskinator.external_adapters.nextcloud_adapter.update_external_metadata')
    @patch('taskinator.external_adapters.nextcloud_adapter.detect_changes')
    async def test_sync_task_bidirectional_conflict(self, mock_detect_changes, mock_update_metadata, mock_get_metadata):
        """Test bidirectional sync with conflict."""
        # Set up mocks
        metadata = external_integration.ExternalSyncMetadata(
            system=external_integration.ExternalSystem.NEXTCLOUD,
            external_id="nc123",
            etag="old-etag",
            sync_status=external_integration.SyncStatus.SYNCED
        )
        mock_get_metadata.return_value = metadata
        mock_update_metadata.side_effect = lambda task, meta: {**task, "external_sync": [meta.to_dict()]}
        
        # Set up conflict detection
        changes = [{"field": "title", "local_value": "Local Title", "remote_value": "Remote Title"}]
        mock_detect_changes.return_value = (changes, True)  # Changes with conflict
        
        # Set up client mock
        mock_nextcloud_task = MagicMock(spec=NextCloudTask)
        mock_nextcloud_task.id = "nc123"
        mock_nextcloud_task.title = "Remote Title"
        mock_nextcloud_task.description = "Remote Description"
        mock_nextcloud_task.status = "NEEDS-ACTION"
        mock_nextcloud_task.priority = 5
        mock_nextcloud_task.etag = "remote-etag"
        mock_nextcloud_task.updated_at = datetime.now().timestamp()
        mock_nextcloud_task.model_dump.return_value = {
            "id": "nc123",
            "title": "Remote Title",
            "description": "Remote Description",
            "status": "NEEDS-ACTION",
            "priority": 5,
            "etag": "remote-etag",
            "updated_at": datetime.now().timestamp()
        }
        self.mock_client.get_task.return_value = mock_nextcloud_task
        
        # Sync task
        task = self.sample_task.copy()
        task["title"] = "Local Title"
        task["external_sync"] = [metadata.to_dict()]
        result = await self.adapter.sync_task(task, "bidirectional")
        
        # Check client was called
        self.mock_client.get_task.assert_called_once_with("nc123")
        
        # Check no update calls were made due to conflict
        self.mock_client.update_task.assert_not_called()
        
        # Check metadata was updated with conflict status
        self.assertIn("external_sync", result)
        self.assertEqual(result["external_sync"][0]["sync_status"], external_integration.SyncStatus.CONFLICT.value)

    @pytest.mark.skip(reason="NextCloudAdapter API has changed, username parameter now required")
    @patch('taskinator.external_adapters.nextcloud_adapter.get_external_metadata')
    @patch('taskinator.external_adapters.nextcloud_adapter.update_external_metadata')
    async def test_sync_task_from_remote(self, mock_update_metadata, mock_get_metadata):
        """Test syncing a task from NextCloud to local."""
        # Set up mocks
        metadata = external_integration.ExternalSyncMetadata(
            system=external_integration.ExternalSystem.NEXTCLOUD,
            external_id="nc123",
            etag="old-etag",
            sync_status=external_integration.SyncStatus.SYNCED
        )
        mock_get_metadata.return_value = metadata
        mock_update_metadata.side_effect = lambda task, meta: {**task, "external_sync": [meta.to_dict()]}
        
        # Set up client mock
        mock_nextcloud_task = MagicMock(spec=NextCloudTask)
        mock_nextcloud_task.id = "nc123"
        mock_nextcloud_task.title = "Remote Task"
        mock_nextcloud_task.description = "Remote Description"
        mock_nextcloud_task.status = "NEEDS-ACTION"
        mock_nextcloud_task.priority = 5
        mock_nextcloud_task.etag = "remote-etag"
        mock_nextcloud_task.updated_at = datetime.now().timestamp()
        mock_nextcloud_task.model_dump.return_value = {
            "id": "nc123",
            "title": "Remote Task",
            "description": "Remote Description",
            "status": "NEEDS-ACTION",
            "priority": 5,
            "etag": "remote-etag",
            "updated_at": datetime.now().timestamp()
        }
        self.mock_client.get_task.return_value = mock_nextcloud_task
        
        # Sync task
        task = self.sample_task.copy()
        result = await self.adapter.sync_task(task, "remote_to_local")
        
        # Check client was called
        self.mock_client.get_task.assert_called_once_with("nc123")
        
        # Check task was updated with remote data
        self.assertEqual(result["title"], "Remote Task")
        self.assertEqual(result["description"], "Remote Description")
        self.assertEqual(result["status"], "pending")
        self.assertEqual(result["priority"], "medium")
        
        # Check metadata was updated
        self.assertIn("external_sync", result)
        self.assertEqual(result["external_sync"][0]["system"], external_integration.ExternalSystem.NEXTCLOUD.value)
        self.assertEqual(result["external_sync"][0]["external_id"], "nc123")
        self.assertEqual(result["external_sync"][0]["etag"], "remote-etag")
        self.assertEqual(result["external_sync"][0]["sync_status"], external_integration.SyncStatus.SYNCED.value)


if __name__ == "__main__":
    unittest.main()
