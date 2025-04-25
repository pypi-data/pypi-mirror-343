"""Tests for the resolution strategies."""

import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from typing import Dict, Any

from taskinator.resolution_strategies import (
    ResolutionStrategy,
    LocalWinsStrategy,
    RemoteWinsStrategy,
    NewestWinsStrategy,
    ManualStrategy,
    StrategyFactory
)
from taskinator.nextcloud_client import NextCloudTask
from taskinator.nextcloud_sync import TaskFieldMapping


class TestResolutionStrategies(unittest.TestCase):
    """Test cases for the resolution strategies."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Sample local task
        self.local_task = {
            "id": "123",
            "title": "Local Title",
            "description": "Local Description",
            "status": "in_progress",
            "priority": "medium",
            "updated": datetime.now().timestamp(),
            "nextcloud": {
                "sync_status": "pending",
                "last_sync": datetime.now().timestamp() - 3600,  # 1 hour ago
                "version_history": []
            }
        }
        
        # Sample remote task
        self.remote_task = MagicMock(spec=NextCloudTask)
        self.remote_task.id = "nc123"
        self.remote_task.summary = "Remote Title"
        self.remote_task.description = "Remote Description"
        self.remote_task.status = "IN-PROCESS"
        self.remote_task.priority = 5
        self.remote_task.modified = datetime.now()
        
        # Patch the TaskFieldMapping.map_remote_to_local method
        self.patcher = patch('taskinator.resolution_strategies.TaskFieldMapping.map_remote_to_local')
        self.mock_map = self.patcher.start()
        self.mock_map.return_value = {
            "id": "123",
            "title": "Remote Title",
            "description": "Remote Description",
            "status": "in_progress",
            "priority": "medium"
        }
        
        # Set up TaskFieldMapping.LOCAL_TO_REMOTE for testing
        self.local_to_remote_patcher = patch('taskinator.resolution_strategies.TaskFieldMapping.LOCAL_TO_REMOTE', 
                                            {"title": "summary", "description": "description", 
                                             "status": "status", "priority": "priority"})
        self.local_to_remote_patcher.start()
    
    def tearDown(self):
        """Tear down test fixtures."""
        self.patcher.stop()
        self.local_to_remote_patcher.stop()
    
    def test_local_wins_strategy(self):
        """Test the LocalWinsStrategy."""
        # Create strategy
        strategy = LocalWinsStrategy()
        
        # Resolve conflict
        resolved_task, changes = strategy.resolve(self.local_task, self.remote_task)
        
        # Check that the local task was not modified
        self.assertEqual(resolved_task["title"], "Local Title")
        self.assertEqual(resolved_task["description"], "Local Description")
        
        # Check that changes were recorded
        self.assertEqual(len(changes), 2)  # title and description differ
        
        # Check that all resolutions are "local"
        for change in changes:
            self.assertEqual(change["resolution"], "local")
    
    def test_remote_wins_strategy(self):
        """Test the RemoteWinsStrategy."""
        # Create strategy
        strategy = RemoteWinsStrategy()
        
        # Resolve conflict
        resolved_task, changes = strategy.resolve(self.local_task, self.remote_task)
        
        # Check that the task was updated with remote values
        self.assertEqual(resolved_task["title"], "Remote Title")
        self.assertEqual(resolved_task["description"], "Remote Description")
        
        # Check that changes were recorded
        self.assertEqual(len(changes), 2)  # title and description differ
        
        # Check that all resolutions are "remote"
        for change in changes:
            self.assertEqual(change["resolution"], "remote")
    
    def test_newest_wins_strategy_local_newer(self):
        """Test the NewestWinsStrategy when local is newer."""
        # Create strategy
        strategy = NewestWinsStrategy()
        
        # Make local task newer
        self.local_task["updated"] = datetime.now().timestamp()
        self.remote_task.modified = datetime.fromtimestamp(datetime.now().timestamp() - 3600)  # 1 hour ago
        
        # Resolve conflict
        resolved_task, changes = strategy.resolve(self.local_task, self.remote_task)
        
        # Check that the local values were kept
        self.assertEqual(resolved_task["title"], "Local Title")
        self.assertEqual(resolved_task["description"], "Local Description")
        
        # Check that changes were recorded
        self.assertEqual(len(changes), 2)  # title and description differ
        
        # Check that all resolutions are "local"
        for change in changes:
            self.assertEqual(change["resolution"], "local")
    
    def test_newest_wins_strategy_remote_newer(self):
        """Test the NewestWinsStrategy when remote is newer."""
        # Create strategy
        strategy = NewestWinsStrategy()
        
        # Make remote task newer
        self.local_task["updated"] = datetime.now().timestamp() - 3600  # 1 hour ago
        self.remote_task.modified = datetime.now()
        
        # Resolve conflict
        resolved_task, changes = strategy.resolve(self.local_task, self.remote_task)
        
        # Check that the remote values were used
        self.assertEqual(resolved_task["title"], "Remote Title")
        self.assertEqual(resolved_task["description"], "Remote Description")
        
        # Check that changes were recorded
        self.assertEqual(len(changes), 2)  # title and description differ
        
        # Check that all resolutions are "remote"
        for change in changes:
            self.assertEqual(change["resolution"], "remote")
    
    def test_manual_strategy(self):
        """Test the ManualStrategy."""
        # Create strategy
        strategy = ManualStrategy()
        
        # Resolve conflict
        resolved_task, changes = strategy.resolve(self.local_task, self.remote_task)
        
        # Check that the local task was not modified
        self.assertEqual(resolved_task["title"], "Local Title")
        self.assertEqual(resolved_task["description"], "Local Description")
        
        # Check that changes were recorded
        self.assertEqual(len(changes), 2)  # title and description differ
        
        # Check that all resolutions are "manual"
        for change in changes:
            self.assertEqual(change["resolution"], "manual")
    
    def test_strategy_factory(self):
        """Test the StrategyFactory."""
        # Test creating each strategy type
        local_strategy = StrategyFactory.create_strategy("local_wins")
        self.assertIsInstance(local_strategy, LocalWinsStrategy)
        
        remote_strategy = StrategyFactory.create_strategy("remote_wins")
        self.assertIsInstance(remote_strategy, RemoteWinsStrategy)
        
        newest_strategy = StrategyFactory.create_strategy("newest_wins")
        self.assertIsInstance(newest_strategy, NewestWinsStrategy)
        
        manual_strategy = StrategyFactory.create_strategy("manual")
        self.assertIsInstance(manual_strategy, ManualStrategy)
        
        # Test invalid strategy name
        with self.assertRaises(ValueError):
            StrategyFactory.create_strategy("invalid_strategy")


if __name__ == '__main__':
    unittest.main()
