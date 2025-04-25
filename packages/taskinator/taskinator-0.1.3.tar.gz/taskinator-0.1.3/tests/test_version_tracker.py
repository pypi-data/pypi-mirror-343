"""Tests for the version tracking system."""

import pytest
import json
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta

from taskinator.version_tracker import VersionInfo, VersionTracker
from taskinator.constants import SyncStatus, ExternalSystem


class TestVersionInfo:
    """Tests for the VersionInfo class."""
    
    def test_init_with_defaults(self):
        """Test initialization with default values."""
        version_info = VersionInfo()
        
        assert version_info.version_id is not None
        assert version_info.timestamp is not None
        assert version_info.sequence == 1
        assert version_info.base_version_id is None
        assert version_info.system is None
    
    def test_init_with_values(self):
        """Test initialization with provided values."""
        version_id = "test-version-id"
        timestamp = 1234567890.0
        sequence = 5
        base_version_id = "base-version-id"
        system = ExternalSystem.NEXTCLOUD
        
        version_info = VersionInfo(
            version_id=version_id,
            timestamp=timestamp,
            sequence=sequence,
            base_version_id=base_version_id,
            system=system
        )
        
        assert version_info.version_id == version_id
        assert version_info.timestamp == timestamp
        assert version_info.sequence == sequence
        assert version_info.base_version_id == base_version_id
        assert version_info.system == system
    
    def test_to_dict(self):
        """Test conversion to dictionary."""
        version_id = "test-version-id"
        timestamp = 1234567890.0
        sequence = 5
        base_version_id = "base-version-id"
        system = ExternalSystem.NEXTCLOUD
        
        version_info = VersionInfo(
            version_id=version_id,
            timestamp=timestamp,
            sequence=sequence,
            base_version_id=base_version_id,
            system=system
        )
        
        version_dict = version_info.to_dict()
        
        assert version_dict["version_id"] == version_id
        assert version_dict["timestamp"] == timestamp
        assert version_dict["sequence"] == sequence
        assert version_dict["base_version_id"] == base_version_id
        assert version_dict["system"] == system
    
    def test_from_dict(self):
        """Test creation from dictionary."""
        version_dict = {
            "version_id": "test-version-id",
            "timestamp": 1234567890.0,
            "sequence": 5,
            "base_version_id": "base-version-id",
            "system": ExternalSystem.NEXTCLOUD
        }
        
        version_info = VersionInfo.from_dict(version_dict)
        
        assert version_info.version_id == version_dict["version_id"]
        assert version_info.timestamp == version_dict["timestamp"]
        assert version_info.sequence == version_dict["sequence"]
        assert version_info.base_version_id == version_dict["base_version_id"]
        assert version_info.system == version_dict["system"]


class TestVersionTracker:
    """Tests for the VersionTracker class."""
    
    @pytest.fixture
    def mock_metadata_store(self):
        """Create a mock metadata store."""
        mock_store = MagicMock()
        mock_store.get_metadata.return_value = {}
        return mock_store
    
    def test_init(self, mock_metadata_store):
        """Test initialization."""
        tracker = VersionTracker(metadata_store=mock_metadata_store)
        assert tracker.metadata_store == mock_metadata_store
    
    def test_get_version_info_none(self, mock_metadata_store):
        """Test getting version info when none exists."""
        mock_metadata_store.get_metadata.return_value = None
        
        tracker = VersionTracker(metadata_store=mock_metadata_store)
        version_info = tracker.get_version_info(1, ExternalSystem.NEXTCLOUD)
        
        assert version_info is None
        mock_metadata_store.get_metadata.assert_called_once_with(1, ExternalSystem.NEXTCLOUD)
    
    def test_get_version_info_exists(self, mock_metadata_store):
        """Test getting version info when it exists."""
        version_dict = {
            "version_id": "test-version-id",
            "timestamp": 1234567890.0,
            "sequence": 5,
            "base_version_id": "base-version-id",
            "system": ExternalSystem.NEXTCLOUD
        }
        
        mock_metadata_store.get_metadata.return_value = {
            "version": version_dict
        }
        
        tracker = VersionTracker(metadata_store=mock_metadata_store)
        version_info = tracker.get_version_info(1, ExternalSystem.NEXTCLOUD)
        
        assert version_info is not None
        assert version_info.version_id == version_dict["version_id"]
        assert version_info.timestamp == version_dict["timestamp"]
        assert version_info.sequence == version_dict["sequence"]
        assert version_info.base_version_id == version_dict["base_version_id"]
        assert version_info.system == version_dict["system"]
        
        mock_metadata_store.get_metadata.assert_called_once_with(1, ExternalSystem.NEXTCLOUD)
    
    def test_update_version_new(self, mock_metadata_store):
        """Test updating version when none exists."""
        mock_metadata_store.get_metadata.return_value = None
        
        tracker = VersionTracker(metadata_store=mock_metadata_store)
        new_version = tracker.update_version(1, ExternalSystem.NEXTCLOUD)
        
        assert new_version is not None
        assert new_version.sequence == 1
        assert new_version.base_version_id is None
        assert new_version.system == ExternalSystem.NEXTCLOUD
        
        mock_metadata_store.get_metadata.assert_called_once_with(1, ExternalSystem.NEXTCLOUD)
        mock_metadata_store.save_metadata.assert_called_once()
        
        # Check that the saved metadata contains the new version
        saved_metadata = mock_metadata_store.save_metadata.call_args[0][2]
        assert "version" in saved_metadata
        assert saved_metadata["version"]["sequence"] == 1
        assert saved_metadata["version"]["system"] == ExternalSystem.NEXTCLOUD
    
    def test_update_version_existing(self, mock_metadata_store):
        """Test updating version when one already exists."""
        existing_version = {
            "version_id": "existing-id",
            "timestamp": 1234567890.0,
            "sequence": 3,
            "base_version_id": "old-base-id",
            "system": ExternalSystem.NEXTCLOUD
        }
        
        mock_metadata_store.get_metadata.return_value = {
            "version": existing_version
        }
        
        tracker = VersionTracker(metadata_store=mock_metadata_store)
        new_version = tracker.update_version(1, ExternalSystem.NEXTCLOUD)
        
        assert new_version is not None
        assert new_version.sequence == 4  # Incremented from 3
        assert new_version.base_version_id == "existing-id"  # Previous version ID becomes base
        assert new_version.system == ExternalSystem.NEXTCLOUD
        
        mock_metadata_store.get_metadata.assert_called_once_with(1, ExternalSystem.NEXTCLOUD)
        mock_metadata_store.save_metadata.assert_called_once()
        
        # Check that the saved metadata contains the new version
        saved_metadata = mock_metadata_store.save_metadata.call_args[0][2]
        assert "version" in saved_metadata
        assert saved_metadata["version"]["sequence"] == 4
        assert saved_metadata["version"]["base_version_id"] == "existing-id"
    
    def test_detect_conflict_same_base_different_versions(self):
        """Test detecting conflict when both versions have the same base but different IDs."""
        base_id = "base-version-id"
        
        local_version = VersionInfo(
            version_id="local-id",
            base_version_id=base_id,
            system=ExternalSystem.NEXTCLOUD
        )
        
        remote_version = VersionInfo(
            version_id="remote-id",
            base_version_id=base_id,
            system=ExternalSystem.NEXTCLOUD
        )
        
        tracker = VersionTracker()
        has_conflict = tracker.detect_conflict(local_version, remote_version)
        
        assert has_conflict is True
    
    def test_detect_conflict_one_based_on_other(self):
        """Test detecting conflict when one version is based on the other."""
        local_version = VersionInfo(
            version_id="local-id",
            base_version_id="remote-id",  # Local is based on remote
            system=ExternalSystem.NEXTCLOUD
        )
        
        remote_version = VersionInfo(
            version_id="remote-id",
            base_version_id="original-id",
            system=ExternalSystem.NEXTCLOUD
        )
        
        tracker = VersionTracker()
        has_conflict = tracker.detect_conflict(local_version, remote_version)
        
        assert has_conflict is False
    
    def test_get_newer_version_by_timestamp(self):
        """Test determining newer version by timestamp."""
        now = datetime.now().timestamp()
        
        older_version = VersionInfo(
            version_id="older-id",
            timestamp=now - 3600,  # 1 hour ago
            sequence=5,
            system=ExternalSystem.NEXTCLOUD
        )
        
        newer_version = VersionInfo(
            version_id="newer-id",
            timestamp=now,  # Now
            sequence=3,  # Lower sequence, but newer timestamp
            system=ExternalSystem.NEXTCLOUD
        )
        
        tracker = VersionTracker()
        result = tracker.get_newer_version(older_version, newer_version)
        
        assert result.version_id == newer_version.version_id
    
    def test_get_newer_version_by_sequence(self):
        """Test determining newer version by sequence when timestamps are equal."""
        now = datetime.now().timestamp()
        
        lower_sequence = VersionInfo(
            version_id="lower-seq-id",
            timestamp=now,
            sequence=3,
            system=ExternalSystem.NEXTCLOUD
        )
        
        higher_sequence = VersionInfo(
            version_id="higher-seq-id",
            timestamp=now,  # Same timestamp
            sequence=5,  # Higher sequence
            system=ExternalSystem.NEXTCLOUD
        )
        
        tracker = VersionTracker()
        result = tracker.get_newer_version(lower_sequence, higher_sequence)
        
        assert result.version_id == higher_sequence.version_id
    
    def test_track_sync(self, mock_metadata_store):
        """Test tracking a sync event."""
        existing_version = {
            "version_id": "existing-id",
            "timestamp": 1234567890.0,
            "sequence": 3,
            "base_version_id": "old-base-id",
            "system": ExternalSystem.NEXTCLOUD
        }
        
        mock_metadata_store.get_metadata.return_value = {
            "version": existing_version
        }
        
        tracker = VersionTracker(metadata_store=mock_metadata_store)
        metadata = tracker.track_sync(1, ExternalSystem.NEXTCLOUD, SyncStatus.SYNCED)
        
        assert metadata is not None
        assert "version" in metadata
        assert metadata["sync_status"] == SyncStatus.SYNCED
        assert "last_sync" in metadata
        
        # Check that the version was preserved but timestamp updated
        assert metadata["version"]["version_id"] == "existing-id"
        assert metadata["version"]["sequence"] == 3
        
        mock_metadata_store.get_metadata.assert_called_once_with(1, ExternalSystem.NEXTCLOUD)
        mock_metadata_store.save_metadata.assert_called_once()
