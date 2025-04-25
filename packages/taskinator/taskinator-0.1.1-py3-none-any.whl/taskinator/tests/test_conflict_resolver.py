"""Tests for conflict resolution functionality."""

import unittest
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch

from taskinator.nextcloud_client import NextCloudTask
from taskinator.nextcloud_sync import (
    NextCloudSyncMetadata,
    SyncStatus,
    get_nextcloud_metadata,
    update_nextcloud_metadata
)
from taskinator.conflict_resolver import (
    ConflictResolver,
    ConflictResolutionStrategy,
    ManualConflictResolver
)


class TestConflictResolver(unittest.TestCase):
    """Test conflict resolver functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.resolver = ConflictResolver()
        
        # Create a local task
        self.local_task = {
            "id": 1,
            "title": "Local Title",
            "description": "Local Description",
            "status": "pending",
            "priority": "high",
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
            title="Remote Title",
            description="Remote Description",
            completed=True,
            priority=1,
            modified=datetime.now() - timedelta(hours=1.5)  # 1.5 hours ago
        )
    
    def test_detect_conflict(self):
        """Test conflict detection."""
        # Should detect conflict (both modified after last sync)
        self.assertTrue(self.resolver.detect_conflict(self.local_task, self.remote_task))
        
        # Update last_sync to be more recent than modifications
        metadata = get_nextcloud_metadata(self.local_task)
        metadata.last_sync = datetime.now().timestamp()
        updated_task = update_nextcloud_metadata(self.local_task, metadata)
        
        # Should not detect conflict (sync is more recent than modifications)
        self.assertFalse(self.resolver.detect_conflict(updated_task, self.remote_task))
    
    def test_resolve_conflict_local_wins(self):
        """Test conflict resolution with LOCAL_WINS strategy."""
        resolved_task, had_conflict = self.resolver.resolve_conflict(
            self.local_task,
            self.remote_task,
            strategy=ConflictResolutionStrategy.LOCAL_WINS
        )
        
        # Should have conflict
        self.assertTrue(had_conflict)
        
        # Local values should be preserved
        self.assertEqual(resolved_task["title"], "Local Title")
        self.assertEqual(resolved_task["description"], "Local Description")
        self.assertEqual(resolved_task["status"], "pending")
        self.assertEqual(resolved_task["priority"], "high")
        
        # Metadata should be updated
        metadata = get_nextcloud_metadata(resolved_task)
        self.assertEqual(metadata.sync_status, SyncStatus.CONFLICT)
        self.assertGreater(len(metadata.version_history), 0)
        
        # Version history should record the conflict
        last_version = metadata.version_history[-1]
        self.assertIn("changes", last_version)
        self.assertIn("resolution", last_version["changes"][0])
        self.assertEqual(last_version["changes"][0]["resolution"], "local")
    
    def test_resolve_conflict_remote_wins(self):
        """Test conflict resolution with REMOTE_WINS strategy."""
        resolved_task, had_conflict = self.resolver.resolve_conflict(
            self.local_task,
            self.remote_task,
            strategy=ConflictResolutionStrategy.REMOTE_WINS
        )
        
        # Should have conflict
        self.assertTrue(had_conflict)
        
        # Remote values should be used
        self.assertEqual(resolved_task["title"], "Remote Title")
        self.assertEqual(resolved_task["description"], "Remote Description")
        self.assertEqual(resolved_task["status"], "done")  # completed=True -> status="done"
        self.assertEqual(resolved_task["priority"], "high")  # priority=1 -> priority="high"
        
        # Metadata should be updated
        metadata = get_nextcloud_metadata(resolved_task)
        self.assertEqual(metadata.sync_status, SyncStatus.CONFLICT)
        self.assertGreater(len(metadata.version_history), 0)
        
        # Version history should record the conflict
        last_version = metadata.version_history[-1]
        self.assertIn("changes", last_version)
        self.assertIn("resolution", last_version["changes"][0])
        self.assertEqual(last_version["changes"][0]["resolution"], "remote")
    
    def test_resolve_conflict_newest_wins(self):
        """Test conflict resolution with NEWEST_WINS strategy."""
        # Make local task newer than remote
        self.local_task["updated"] = datetime.now().timestamp()
        
        resolved_task, had_conflict = self.resolver.resolve_conflict(
            self.local_task,
            self.remote_task,
            strategy=ConflictResolutionStrategy.NEWEST_WINS
        )
        
        # Should have conflict
        self.assertTrue(had_conflict)
        
        # Local values should be preserved (local is newer)
        self.assertEqual(resolved_task["title"], "Local Title")
        self.assertEqual(resolved_task["description"], "Local Description")
        
        # Make remote task newer than local
        self.local_task["updated"] = datetime.now().timestamp() - 7200  # 2 hours ago
        self.remote_task.modified = datetime.now()  # Now
        
        resolved_task, had_conflict = self.resolver.resolve_conflict(
            self.local_task,
            self.remote_task,
            strategy=ConflictResolutionStrategy.NEWEST_WINS
        )
        
        # Remote values should be used (remote is newer)
        self.assertEqual(resolved_task["title"], "Remote Title")
        self.assertEqual(resolved_task["description"], "Remote Description")
    
    def test_resolve_conflict_manual(self):
        """Test conflict resolution with MANUAL strategy."""
        resolved_task, had_conflict = self.resolver.resolve_conflict(
            self.local_task,
            self.remote_task,
            strategy=ConflictResolutionStrategy.MANUAL
        )
        
        # Should have conflict
        self.assertTrue(had_conflict)
        
        # Values should not be changed, just marked for manual resolution
        self.assertEqual(resolved_task["title"], "Local Title")
        self.assertEqual(resolved_task["description"], "Local Description")
        
        # Metadata should be updated
        metadata = get_nextcloud_metadata(resolved_task)
        self.assertEqual(metadata.sync_status, SyncStatus.CONFLICT)
        self.assertGreater(len(metadata.version_history), 0)
        
        # Version history should record the conflict for manual resolution
        last_version = metadata.version_history[-1]
        self.assertIn("changes", last_version)
        self.assertIn("resolution", last_version["changes"][0])
        self.assertEqual(last_version["changes"][0]["resolution"], "manual")


class TestManualConflictResolver(unittest.TestCase):
    """Test manual conflict resolver functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.resolver = ManualConflictResolver()
        
        # Create a task with manual conflict
        self.conflict_task = {
            "id": 1,
            "title": "Local Title",
            "description": "Local Description",
            "status": "pending",
            "priority": "high",
            "updated": datetime.now().timestamp() - 3600,
            "nextcloud": {
                "etag": "etag123",
                "fileid": "file123",
                "last_sync": datetime.now().timestamp() - 7200,
                "sync_status": "conflict",
                "version_history": [
                    {
                        "version": 1,
                        "last_modified": datetime.now().timestamp() - 3600,
                        "modified_by": "conflict_resolution_manual",
                        "changes": [
                            {
                                "field": "title",
                                "local_value": "Local Title",
                                "remote_value": "Remote Title",
                                "resolution": "manual"
                            },
                            {
                                "field": "status",
                                "local_value": "pending",
                                "remote_value": "done",
                                "resolution": "manual"
                            }
                        ]
                    }
                ]
            }
        }
    
    def test_get_field_conflicts(self):
        """Test getting field conflicts."""
        conflicts = self.resolver.get_field_conflicts(self.conflict_task)
        
        # Should have two conflicts
        self.assertEqual(len(conflicts), 2)
        
        # Check conflict details
        title_conflict = next(c for c in conflicts if c["field"] == "title")
        self.assertEqual(title_conflict["local_value"], "Local Title")
        self.assertEqual(title_conflict["remote_value"], "Remote Title")
        
        status_conflict = next(c for c in conflicts if c["field"] == "status")
        self.assertEqual(status_conflict["local_value"], "pending")
        self.assertEqual(status_conflict["remote_value"], "done")
    
    def test_resolve_field_conflict_local(self):
        """Test resolving a field conflict with local value."""
        resolved_task = self.resolver.resolve_field_conflict(
            self.conflict_task,
            field="title",
            resolution="local"
        )
        
        # Title should remain the local value
        self.assertEqual(resolved_task["title"], "Local Title")
        
        # Resolution should be updated in version history
        metadata = get_nextcloud_metadata(resolved_task)
        version = metadata.version_history[0]
        title_change = next(c for c in version["changes"] if c["field"] == "title")
        self.assertEqual(title_change["resolution"], "local")
        
        # Status conflict should still be unresolved
        status_change = next(c for c in version["changes"] if c["field"] == "status")
        self.assertEqual(status_change["resolution"], "manual")
        
        # Task should still be in conflict status
        self.assertEqual(metadata.sync_status, SyncStatus.CONFLICT)
    
    def test_resolve_field_conflict_remote(self):
        """Test resolving a field conflict with remote value."""
        resolved_task = self.resolver.resolve_field_conflict(
            self.conflict_task,
            field="status",
            resolution="remote"
        )
        
        # Status should be updated to remote value
        self.assertEqual(resolved_task["status"], "done")
        
        # Resolution should be updated in version history
        metadata = get_nextcloud_metadata(resolved_task)
        version = metadata.version_history[0]
        status_change = next(c for c in version["changes"] if c["field"] == "status")
        self.assertEqual(status_change["resolution"], "remote")
        
        # Title conflict should still be unresolved
        title_change = next(c for c in version["changes"] if c["field"] == "title")
        self.assertEqual(title_change["resolution"], "manual")
        
        # Task should still be in conflict status
        self.assertEqual(metadata.sync_status, SyncStatus.CONFLICT)
    
    def test_resolve_all_conflicts(self):
        """Test resolving all conflicts."""
        # Resolve title conflict with local value
        task = self.resolver.resolve_field_conflict(
            self.conflict_task,
            field="title",
            resolution="local"
        )
        
        # Resolve status conflict with remote value
        task = self.resolver.resolve_field_conflict(
            task,
            field="status",
            resolution="remote"
        )
        
        # Title should be local value
        self.assertEqual(task["title"], "Local Title")
        
        # Status should be remote value
        self.assertEqual(task["status"], "done")
        
        # All conflicts should be resolved
        metadata = get_nextcloud_metadata(task)
        version = metadata.version_history[0]
        title_change = next(c for c in version["changes"] if c["field"] == "title")
        self.assertEqual(title_change["resolution"], "local")
        status_change = next(c for c in version["changes"] if c["field"] == "status")
        self.assertEqual(status_change["resolution"], "remote")
        
        # Task should be pending sync now
        self.assertEqual(metadata.sync_status, SyncStatus.PENDING)


if __name__ == "__main__":
    unittest.main()
