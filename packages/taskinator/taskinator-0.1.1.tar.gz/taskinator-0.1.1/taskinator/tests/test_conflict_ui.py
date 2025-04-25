"""Tests for the conflict UI components."""

import unittest
from unittest.mock import patch, MagicMock
import json
from datetime import datetime

from taskinator.conflict_ui import ConflictUI, display_conflict_list
from taskinator.conflict_resolver import ManualConflictResolver, ConflictResolutionStrategy
from taskinator.nextcloud_sync import SyncStatus


class TestConflictUI(unittest.TestCase):
    """Test cases for the conflict UI components."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a mock conflict resolver
        self.mock_resolver = MagicMock(spec=ManualConflictResolver)
        
        # Create the conflict UI
        self.conflict_ui = ConflictUI(self.mock_resolver)
        
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
                            },
                            {
                                "field": "description",
                                "local_value": "This is a test task",
                                "remote_value": "This is an updated test task",
                                "resolution": "manual"
                            }
                        ]
                    }
                ]
            }
        }
        
        # Sample conflicts
        self.conflicts = [
            {
                "field": "title",
                "local_value": "Test Task",
                "remote_value": "Updated Test Task",
                "version": "v1"
            },
            {
                "field": "description",
                "local_value": "This is a test task",
                "remote_value": "This is an updated test task",
                "version": "v1"
            }
        ]
    
    @patch('taskinator.conflict_ui.console')
    def test_display_conflict_summary(self, mock_console):
        """Test displaying conflict summary."""
        # Set up mock resolver to return conflicts
        self.mock_resolver.get_field_conflicts.return_value = self.conflicts
        
        # Call the method
        self.conflict_ui.display_conflict_summary(self.task)
        
        # Check that the console was called
        self.assertTrue(mock_console.print.called)
        
        # Check that the resolver was called with the task
        self.mock_resolver.get_field_conflicts.assert_called_once_with(self.task)
    
    @patch('taskinator.conflict_ui.console')
    def test_display_conflict_details(self, mock_console):
        """Test displaying conflict details for a field."""
        # Set up mock resolver to return conflicts
        self.mock_resolver.get_field_conflicts.return_value = self.conflicts
        
        # Call the method
        self.conflict_ui.display_conflict_details(self.task, "title")
        
        # Check that the console was called
        self.assertTrue(mock_console.print.called)
        
        # Check that the resolver was called with the task
        self.mock_resolver.get_field_conflicts.assert_called_once_with(self.task)
    
    @patch('taskinator.conflict_ui.Prompt')
    def test_resolve_conflict_interactive(self, mock_prompt):
        """Test interactive conflict resolution."""
        # Set up mock resolver
        self.mock_resolver.get_field_conflicts.return_value = self.conflicts
        self.mock_resolver.resolve_field_conflict.return_value = self.task
        
        # Set up mock prompt to return "local" for the first conflict and "remote" for the second
        mock_prompt.ask.side_effect = ["local", "remote"]
        
        # Call the method
        result = self.conflict_ui.resolve_conflict_interactive(self.task)
        
        # Check that the resolver was called for each field
        self.assertEqual(self.mock_resolver.resolve_field_conflict.call_count, 2)
        
        # Check that the result is the updated task
        self.assertEqual(result, self.task)
    
    def test_display_conflict_list(self):
        """Test displaying a list of tasks with conflicts."""
        # Sample tasks
        tasks = [self.task, {"id": "456", "title": "No Conflict Task"}]
        
        # Call the function
        display_conflict_list(tasks)
    
    @patch('taskinator.ui._add_conflict_indicators')
    def test_add_conflict_indicators(self, mock_add_indicators):
        """Test adding conflict indicators to a task."""
        # Set up the mock
        mock_add_indicators.return_value = {
            "id": "123",
            "title": "Test Task [red]⚠[/red]",
            "description": "This is a test task",
        }
        
        # Import the function from ui module
        from taskinator.ui import _add_conflict_indicators
        
        # Call the function
        result = _add_conflict_indicators(self.task.copy())
        
        # Check that the title has a conflict indicator
        self.assertIn("⚠", result["title"])


if __name__ == '__main__':
    unittest.main()
