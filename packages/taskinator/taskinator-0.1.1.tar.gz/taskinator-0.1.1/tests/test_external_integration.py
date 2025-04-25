"""Tests for external integration functionality."""

import json
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import patch, MagicMock

# Update imports to use the correct module directly
from taskinator.external_integration.sync_metadata_store import SyncMetadataStore
# Import from the module file directly, not the package
from taskinator import external_integration
from taskinator.external_integration import SyncMetadataStore

class TestExternalIntegration(unittest.TestCase):
    """Test external integration functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
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
        
        self.sample_metadata = external_integration.ExternalSyncMetadata(
            system=external_integration.ExternalSystem.NEXTCLOUD,
            external_id="123",
            external_url="https://nextcloud.example.com/tasks/123",
            etag="abc123",
            last_sync=datetime.now().timestamp(),
            sync_status=external_integration.SyncStatus.SYNCED,
            version_history=[],
            additional_data={}
        )
    
    def test_version_info(self):
        """Test VersionInfo class."""
        # Create a version info
        version_info = external_integration.VersionInfo(
            version=1,
            last_modified=datetime.now().timestamp(),
            modified_by="local",
            changes=[{"field": "title", "old": "Old Title", "new": "New Title"}]
        )
        
        # Convert to dict and back
        version_dict = version_info.to_dict()
        version_info2 = external_integration.VersionInfo.from_dict(version_dict)
        
        # Check values
        self.assertEqual(version_info.version, version_info2.version)
        self.assertEqual(version_info.last_modified, version_info2.last_modified)
        self.assertEqual(version_info.modified_by, version_info2.modified_by)
        self.assertEqual(version_info.changes, version_info2.changes)
    
    def test_external_sync_metadata(self):
        """Test ExternalSyncMetadata class."""
        # Create metadata
        metadata = self.sample_metadata
        
        # Convert to dict and back
        metadata_dict = metadata.to_dict()
        metadata2 = external_integration.ExternalSyncMetadata.from_dict(metadata_dict)
        
        # Check values
        self.assertEqual(metadata.system, metadata2.system)
        self.assertEqual(metadata.external_id, metadata2.external_id)
        self.assertEqual(metadata.external_url, metadata2.external_url)
        self.assertEqual(metadata.etag, metadata2.etag)
        self.assertEqual(metadata.last_sync, metadata2.last_sync)
        self.assertEqual(metadata.sync_status, metadata2.sync_status)
        self.assertEqual(metadata.version_history, metadata2.version_history)
        self.assertEqual(metadata.additional_data, metadata2.additional_data)
    
    def test_add_version(self):
        """Test adding a version to metadata."""
        metadata = self.sample_metadata
        
        # Add a version
        changes = [{"field": "title", "old": "Old Title", "new": "New Title"}]
        metadata.add_version(changes, "local")
        
        # Check version was added
        self.assertEqual(len(metadata.version_history), 1)
        self.assertEqual(metadata.version_history[0]["version"], 1)
        self.assertEqual(metadata.version_history[0]["modified_by"], "local")
        self.assertEqual(metadata.version_history[0]["changes"], changes)
        
        # Add another version
        changes2 = [{"field": "status", "old": "pending", "new": "done"}]
        metadata.add_version(changes2, "nextcloud")
        
        # Check version was added
        self.assertEqual(len(metadata.version_history), 2)
        self.assertEqual(metadata.version_history[1]["version"], 2)
        self.assertEqual(metadata.version_history[1]["modified_by"], "nextcloud")
        self.assertEqual(metadata.version_history[1]["changes"], changes2)
    
    def test_get_external_metadata(self):
        """Test getting external metadata from a task."""
        # Task with no metadata
        task = self.sample_task.copy()
        metadata = external_integration.get_external_metadata(task, external_integration.ExternalSystem.NEXTCLOUD)
        
        # Should return empty metadata
        self.assertIsInstance(metadata, external_integration.ExternalSyncMetadata)
        self.assertEqual(metadata.system, external_integration.ExternalSystem.NEXTCLOUD)
        self.assertEqual(metadata.external_id, "")
        
        # Task with metadata
        task["external_sync"] = [self.sample_metadata.to_dict()]
        metadata = external_integration.get_external_metadata(task, external_integration.ExternalSystem.NEXTCLOUD)
        
        # Should return the metadata
        self.assertIsInstance(metadata, external_integration.ExternalSyncMetadata)
        self.assertEqual(metadata.system, external_integration.ExternalSystem.NEXTCLOUD)
        self.assertEqual(metadata.external_id, "123")
        
        # Task with multiple metadata
        gitlab_metadata = external_integration.ExternalSyncMetadata(
            system=external_integration.ExternalSystem.GITLAB,
            external_id="456",
            external_url="https://gitlab.example.com/issues/456",
            etag="def456",
            last_sync=datetime.now().timestamp(),
            sync_status=external_integration.SyncStatus.SYNCED,
            version_history=[],
            additional_data={}
        )
        
        task["external_sync"] = [self.sample_metadata.to_dict(), gitlab_metadata.to_dict()]
        
        # Get NextCloud metadata
        metadata = external_integration.get_external_metadata(task, external_integration.ExternalSystem.NEXTCLOUD)
        self.assertEqual(metadata.system, external_integration.ExternalSystem.NEXTCLOUD)
        self.assertEqual(metadata.external_id, "123")
        
        # Get GitLab metadata
        metadata = external_integration.get_external_metadata(task, external_integration.ExternalSystem.GITLAB)
        self.assertEqual(metadata.system, external_integration.ExternalSystem.GITLAB)
        self.assertEqual(metadata.external_id, "456")
        
        # Get any metadata (should return first one)
        metadata = external_integration.get_external_metadata(task)
        self.assertEqual(metadata.system, external_integration.ExternalSystem.NEXTCLOUD)
        self.assertEqual(metadata.external_id, "123")
    
    def test_update_external_metadata(self):
        """Test updating external metadata in a task."""
        # Task with no metadata
        task = self.sample_task.copy()
        updated_task = external_integration.update_external_metadata(task, self.sample_metadata)
        
        # Should add metadata
        self.assertIn("external_sync", updated_task)
        self.assertEqual(len(updated_task["external_sync"]), 1)
        self.assertEqual(updated_task["external_sync"][0]["system"], external_integration.ExternalSystem.NEXTCLOUD.value)
        self.assertEqual(updated_task["external_sync"][0]["external_id"], "123")
        
        # Task with existing metadata for same system
        task = self.sample_task.copy()
        task["external_sync"] = [self.sample_metadata.to_dict()]
        
        # Update metadata
        updated_metadata = external_integration.ExternalSyncMetadata(
            system=external_integration.ExternalSystem.NEXTCLOUD,
            external_id="789",
            external_url="https://nextcloud.example.com/tasks/789",
            etag="xyz789",
            last_sync=datetime.now().timestamp(),
            sync_status=external_integration.SyncStatus.SYNCED,
            version_history=[],
            additional_data={}
        )
        
        updated_task = external_integration.update_external_metadata(task, updated_metadata)
        
        # Should update existing metadata
        self.assertEqual(len(updated_task["external_sync"]), 1)
        self.assertEqual(updated_task["external_sync"][0]["system"], external_integration.ExternalSystem.NEXTCLOUD.value)
        self.assertEqual(updated_task["external_sync"][0]["external_id"], "789")
        
        # Task with existing metadata for different system
        task = self.sample_task.copy()
        task["external_sync"] = [
            external_integration.ExternalSyncMetadata(
                system=external_integration.ExternalSystem.GITLAB,
                external_id="456",
                external_url="https://gitlab.example.com/issues/456",
                etag="def456",
                last_sync=datetime.now().timestamp(),
                sync_status=external_integration.SyncStatus.SYNCED,
                version_history=[],
                additional_data={}
            ).to_dict()
        ]
        
        # Add metadata for NextCloud
        updated_task = external_integration.update_external_metadata(task, self.sample_metadata)
        
        # Should add new metadata
        self.assertEqual(len(updated_task["external_sync"]), 2)
        self.assertEqual(updated_task["external_sync"][0]["system"], external_integration.ExternalSystem.GITLAB.value)
        self.assertEqual(updated_task["external_sync"][1]["system"], external_integration.ExternalSystem.NEXTCLOUD.value)
    
    def test_detect_changes(self):
        """Test detecting changes between local and remote tasks."""
        # Local task
        local_task = self.sample_task.copy()
        local_task["title"] = "Local Title"
        local_task["description"] = "Local Description"
        local_task["status"] = "pending"
        local_task["updated"] = datetime.now().timestamp()
        
        # Add sync metadata with last sync in the past
        metadata = external_integration.ExternalSyncMetadata(
            system=external_integration.ExternalSystem.NEXTCLOUD,
            last_sync=datetime.now().timestamp() - 7200,  # 2 hours ago
            sync_status=external_integration.SyncStatus.SYNCED,
            version_history=[{
                "version": 1,
                "last_modified": datetime.now().timestamp() - 7200,
                "modified_by": "local",
                "changes": []
            }]
        )
        
        local_task["external_sync"] = [metadata.to_dict()]
        
        # Remote task (mapped to local field names)
        remote_task = {
            "title": "Remote Title",
            "description": "Remote Description",
            "status": "done",
            "updated": datetime.now().timestamp() - 3600  # 1 hour ago
        }
        
        # Field mapping
        field_mapping = {
            "title": "title",
            "description": "description",
            "status": "status"
        }
        
        # Detect changes
        changes, has_conflict = external_integration.detect_changes(local_task, remote_task, field_mapping)
        
        # Should detect changes in all fields
        self.assertEqual(len(changes), 3)
        
        # Should not have conflict because only one side changed since last sync
        # Set local update time to be before last sync
        local_task["updated"] = datetime.now().timestamp() - 10000  # Older than last sync
        changes, has_conflict = external_integration.detect_changes(local_task, remote_task, field_mapping)
        self.assertFalse(has_conflict)
        
        # Check changes
        title_change = next((c for c in changes if c["field"] == "title"), None)
        self.assertIsNotNone(title_change)
        self.assertEqual(title_change["local_value"], "Local Title")
        self.assertEqual(title_change["remote_value"], "Remote Title")
        
        # Test conflict detection
        # Both local and remote updated since last sync
        local_task["updated"] = datetime.now().timestamp() - 3600  # 1 hour ago
        remote_task["updated"] = datetime.now().timestamp() - 3600  # 1 hour ago
        
        # Detect changes
        changes, has_conflict = external_integration.detect_changes(local_task, remote_task, field_mapping)
        
        # Should detect conflict
        self.assertTrue(has_conflict)


if __name__ == "__main__":
    unittest.main()
