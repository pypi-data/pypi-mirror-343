"""Tests for the conflict presentation system."""

import unittest
from unittest.mock import patch, MagicMock
import json
import os
from datetime import datetime
from pathlib import Path

from taskinator.conflict_presentation import (
    ConflictNotificationManager,
    ConflictSummaryView,
    ConflictDashboard,
    ConflictHistoryView,
    ConflictPreferenceManager,
    ConflictPresentationSystem
)
from taskinator.conflict_resolver import ConflictResolver, ManualConflictResolver, ConflictResolutionStrategy
from taskinator.nextcloud_sync import SyncStatus


class TestConflictNotificationManager(unittest.TestCase):
    """Test cases for the ConflictNotificationManager."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.notification_manager = ConflictNotificationManager([])
        
        # Sample task with conflicts
        self.task = {
            "id": "123",
            "title": "Test Task",
            "description": "This is a test task",
            "status": "in_progress",
            "priority": "medium",
            "updated": datetime.now().timestamp(),
            "nextcloud": {
                "sync_status": SyncStatus.CONFLICT.value,
                "version_history": [
                    {
                        "version": "v1",
                        "changes": [
                            {
                                "field": "title",
                                "local_value": "Test Task",
                                "remote_value": "Updated Test Task",
                                "resolution": "manual"
                            }
                        ]
                    }
                ]
            }
        }
    
    def test_add_notification_handler(self):
        """Test adding a notification handler."""
        # Create a mock handler
        mock_handler = MagicMock()
        
        # Add the handler
        self.notification_manager.add_notification_handler(mock_handler)
        
        # Check that the handler was added
        self.assertIn(mock_handler, self.notification_manager.notification_handlers)
    
    def test_notify_conflict(self):
        """Test notifying about a conflict."""
        # Create a mock handler
        mock_handler = MagicMock()
        
        # Add the handler
        self.notification_manager.add_notification_handler(mock_handler)
        
        # Notify about a conflict
        self.notification_manager.notify_conflict(self.task, "nextcloud")
        
        # Check that the handler was called
        mock_handler.assert_called_once_with(self.task, "nextcloud")


class TestConflictSummaryView(unittest.TestCase):
    """Test cases for the ConflictSummaryView."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a mock conflict resolver
        self.mock_resolver = MagicMock(spec=ConflictResolver)
        
        # Create the summary view
        self.summary_view = ConflictSummaryView(self.mock_resolver)
        
        # Sample tasks with conflicts
        self.tasks = [
            {
                "id": "123",
                "title": "Test Task 1",
                "nextcloud": {
                    "sync_status": SyncStatus.CONFLICT.value
                }
            },
            {
                "id": "456",
                "title": "Test Task 2",
                "nextcloud": {
                    "sync_status": SyncStatus.CONFLICT.value
                }
            }
        ]
    
    @patch('taskinator.conflict_presentation.console')
    def test_display_conflict_summary(self, mock_console):
        """Test displaying conflict summary."""
        # Set up mock resolver to return tasks with conflicts
        self.mock_resolver.get_conflicts.return_value = self.tasks
        
        # Call the method
        self.summary_view.display_conflict_summary(self.tasks)
        
        # Check that the console was called
        self.assertTrue(mock_console.print.called)
        
        # Check that the resolver was called with the tasks
        self.mock_resolver.get_conflicts.assert_called_once_with(self.tasks)


class TestConflictHistoryView(unittest.TestCase):
    """Test cases for the ConflictHistoryView."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create the history view
        self.history_view = ConflictHistoryView()
        
        # Sample task with conflict history
        self.task = {
            "id": "123",
            "title": "Test Task",
            "nextcloud": {
                "sync_status": SyncStatus.SYNCED.value,
                "version_history": [
                    {
                        "version": "v1",
                        "timestamp": datetime.now().timestamp(),
                        "modified_by": "conflict_resolution_local_wins",
                        "changes": [
                            {
                                "field": "title",
                                "local_value": "Test Task",
                                "remote_value": "Updated Test Task",
                                "resolution": "local"
                            }
                        ]
                    }
                ]
            }
        }
    
    @patch('taskinator.conflict_presentation.console')
    def test_display_conflict_history(self, mock_console):
        """Test displaying conflict history."""
        # Call the method
        self.history_view.display_conflict_history(self.task)
        
        # Check that the console was called
        self.assertTrue(mock_console.print.called)


class TestConflictPreferenceManager(unittest.TestCase):
    """Test cases for the ConflictPreferenceManager."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary preferences file
        self.temp_dir = Path("temp_test_dir")
        self.temp_dir.mkdir(exist_ok=True)
        
        # Patch the config object
        self.patcher = patch('taskinator.conflict_presentation.config')
        self.mock_config = self.patcher.start()
        # Set config_dir as an attribute, not a property
        self.mock_config.config_dir = self.temp_dir
        
        # Create the preference manager
        self.preference_manager = ConflictPreferenceManager()
    
    def tearDown(self):
        """Tear down test fixtures."""
        self.patcher.stop()
        
        # Clean up temporary files
        if self.temp_dir.exists():
            for file in self.temp_dir.glob("*"):
                file.unlink()
            self.temp_dir.rmdir()
    
    def test_get_default_strategy(self):
        """Test getting the default strategy."""
        # Check the default value
        self.assertEqual(
            self.preference_manager.get_default_strategy(),
            ConflictResolutionStrategy.MANUAL.value
        )
    
    def test_set_default_strategy(self):
        """Test setting the default strategy."""
        # Set a new default strategy
        self.preference_manager.set_default_strategy(ConflictResolutionStrategy.LOCAL_WINS.value)
        
        # Check that it was updated
        self.assertEqual(
            self.preference_manager.get_default_strategy(),
            ConflictResolutionStrategy.LOCAL_WINS.value
        )
    
    def test_set_field_preference(self):
        """Test setting a field preference."""
        # Set a field preference
        self.preference_manager.set_field_preference("title", ConflictResolutionStrategy.REMOTE_WINS.value)
        
        # Check that it was updated
        self.assertEqual(
            self.preference_manager.get_field_preference("title"),
            ConflictResolutionStrategy.REMOTE_WINS.value
        )
    
    def test_set_system_preference(self):
        """Test setting a system preference."""
        # Set a system preference
        self.preference_manager.set_system_preference("nextcloud", ConflictResolutionStrategy.NEWEST_WINS.value)
        
        # Check that it was updated
        self.assertEqual(
            self.preference_manager.get_system_preference("nextcloud"),
            ConflictResolutionStrategy.NEWEST_WINS.value
        )
    
    @patch('taskinator.conflict_presentation.console')
    def test_display_preferences(self, mock_console):
        """Test displaying preferences."""
        # Set some preferences
        self.preference_manager.set_default_strategy(ConflictResolutionStrategy.LOCAL_WINS.value)
        self.preference_manager.set_field_preference("title", ConflictResolutionStrategy.REMOTE_WINS.value)
        self.preference_manager.set_system_preference("nextcloud", ConflictResolutionStrategy.NEWEST_WINS.value)
        
        # Call the method
        self.preference_manager.display_preferences()
        
        # Check that the console was called
        self.assertTrue(mock_console.print.called)


class TestConflictPresentationSystem(unittest.TestCase):
    """Test cases for the ConflictPresentationSystem."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a mock conflict resolver
        self.mock_resolver = MagicMock(spec=ConflictResolver)
        self.mock_manual_resolver = MagicMock(spec=ManualConflictResolver)
        self.mock_conflict_ui = MagicMock()
        self.mock_notification_manager = MagicMock()
        self.mock_summary_view = MagicMock()
        self.mock_dashboard = MagicMock()
        self.mock_history_view = MagicMock()
        self.mock_preference_manager = MagicMock()
        
        # Create the presentation system
        self.presentation_system = ConflictPresentationSystem()
        
        # Replace components with mocks
        self.presentation_system.conflict_resolver = self.mock_resolver
        self.presentation_system.manual_resolver = self.mock_manual_resolver
        self.presentation_system.conflict_ui = self.mock_conflict_ui
        self.presentation_system.notification_manager = self.mock_notification_manager
        self.presentation_system.summary_view = self.mock_summary_view
        self.presentation_system.dashboard = self.mock_dashboard
        self.presentation_system.history_view = self.mock_history_view
        self.presentation_system.preference_manager = self.mock_preference_manager
        
        # Sample task with conflicts
        self.task = {
            "id": "123",
            "title": "Test Task",
            "nextcloud": {
                "sync_status": SyncStatus.CONFLICT.value
            }
        }
        
        # Sample tasks
        self.tasks = [self.task, {"id": "456", "title": "No Conflict Task"}]
    
    def test_notify_conflict(self):
        """Test notifying about a conflict."""
        # Call the method
        self.presentation_system.notify_conflict(self.task, "nextcloud")
        
        # Check that the notification manager was called
        self.mock_notification_manager.notify_conflict.assert_called_once_with(self.task, "nextcloud")
    
    def test_display_conflict_summary(self):
        """Test displaying conflict summary."""
        # Call the method
        self.presentation_system.display_conflict_summary(self.tasks)
        
        # Check that the summary view was called
        self.mock_summary_view.display_conflict_summary.assert_called_once_with(self.tasks)
    
    def test_display_dashboard(self):
        """Test displaying the dashboard."""
        # Call the method
        self.presentation_system.display_dashboard(self.tasks)
        
        # Check that the dashboard was called
        self.mock_dashboard.display_dashboard.assert_called_once_with(self.tasks)
    
    def test_display_conflict_history(self):
        """Test displaying conflict history."""
        # Call the method
        self.presentation_system.display_conflict_history(self.task)
        
        # Check that the history view was called
        self.mock_history_view.display_conflict_history.assert_called_once_with(self.task)
    
    def test_display_preferences(self):
        """Test displaying preferences."""
        # Call the method
        self.presentation_system.display_preferences()
        
        # Check that the preference manager was called
        self.mock_preference_manager.display_preferences.assert_called_once()
    
    def test_set_default_strategy(self):
        """Test setting the default strategy."""
        # Call the method
        self.presentation_system.set_default_strategy("local_wins")
        
        # Check that the preference manager was called
        self.mock_preference_manager.set_default_strategy.assert_called_once_with("local_wins")
    
    def test_set_field_preference(self):
        """Test setting a field preference."""
        # Call the method
        self.presentation_system.set_field_preference("title", "remote_wins")
        
        # Check that the preference manager was called
        self.mock_preference_manager.set_field_preference.assert_called_once_with("title", "remote_wins")
    
    def test_set_system_preference(self):
        """Test setting a system preference."""
        # Call the method
        self.presentation_system.set_system_preference("nextcloud", "newest_wins")
        
        # Check that the preference manager was called
        self.mock_preference_manager.set_system_preference.assert_called_once_with("nextcloud", "newest_wins")
    
    def test_get_preferred_strategy(self):
        """Test getting the preferred strategy."""
        # Set up mock preference manager
        self.mock_preference_manager.get_field_preference.return_value = None
        self.mock_preference_manager.get_system_preference.return_value = "newest_wins"
        
        # Call the method
        result = self.presentation_system.get_preferred_strategy(self.task, "title", "nextcloud")
        
        # Check that the preference manager was called
        self.mock_preference_manager.get_field_preference.assert_called_once_with("title")
        self.mock_preference_manager.get_system_preference.assert_called_once_with("nextcloud")
        
        # Check the result
        self.assertEqual(result, "newest_wins")


if __name__ == '__main__':
    unittest.main()
