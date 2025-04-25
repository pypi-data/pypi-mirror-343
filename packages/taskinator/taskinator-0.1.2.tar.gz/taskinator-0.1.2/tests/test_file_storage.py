"""Unit tests for the FileStorageManager class."""

import asyncio
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import pytest

from taskinator.file_storage import (
    FileStorageManager,
    FileStorageError,
    TaskFileNotFoundError,
    TaskFileParseError,
    TaskFileWriteError,
    TaskFileLockError,
    FileLock
)
from taskinator.config import TaskStatus, TaskPriority


class TestFileStorageManager(unittest.TestCase):
    """Test the FileStorageManager class."""
    
    def setUp(self):
        """Set up the test environment."""
        # Create a temporary directory for task files
        self.temp_dir = tempfile.TemporaryDirectory()
        self.tasks_dir = Path(self.temp_dir.name)
        
        # Create a FileStorageManager instance
        self.storage_manager = FileStorageManager(tasks_dir=self.tasks_dir, display_output=False)
        
        # Sample task data
        self.sample_tasks = {
            "tasks": [
                {
                    "id": 1,
                    "title": "Test Task 1",
                    "status": TaskStatus.PENDING,
                    "priority": TaskPriority.HIGH,
                    "description": "Test description 1",
                    "details": "Test details 1",
                    "testStrategy": "Test strategy 1",
                    "dependencies": []
                },
                {
                    "id": 2,
                    "title": "Test Task 2",
                    "status": TaskStatus.IN_PROGRESS,
                    "priority": TaskPriority.MEDIUM,
                    "description": "Test description 2",
                    "details": "Test details 2",
                    "testStrategy": "Test strategy 2",
                    "dependencies": [1]
                }
            ],
            "metadata": {
                "version": "1.0",
                "created": "2023-01-01T00:00:00"
            }
        }
    
    def tearDown(self):
        """Clean up the test environment."""
        # Clean up the temporary directory
        self.temp_dir.cleanup()
    
    def test_init(self):
        """Test the initialization of the FileStorageManager."""
        # Check that the tasks directory is created
        self.assertTrue(self.tasks_dir.exists())
        self.assertTrue(self.tasks_dir.is_dir())
        
        # Check that the locks directory is created
        locks_dir = self.tasks_dir / ".locks"
        self.assertTrue(locks_dir.exists())
        self.assertTrue(locks_dir.is_dir())
    
    @pytest.mark.asyncio
    async def test_read_tasks_empty(self):
        """Test reading tasks from an empty directory."""
        # Read tasks from an empty directory
        tasks_data = await self.storage_manager.read_tasks()
        
        # Check that the tasks data is empty
        self.assertIn("tasks", tasks_data)
        self.assertEqual(len(tasks_data["tasks"]), 0)
        self.assertIn("metadata", tasks_data)
        self.assertIn("version", tasks_data["metadata"])
        self.assertIn("created", tasks_data["metadata"])
    
    @pytest.mark.asyncio
    async def test_write_tasks(self):
        """Test writing tasks to a file."""
        # Write tasks to a file
        await self.storage_manager.write_tasks(self.sample_tasks)
        
        # Check that the tasks file exists
        tasks_file = self.tasks_dir / "tasks.json"
        self.assertTrue(tasks_file.exists())
        
        # Check that the task files exist
        task1_file = self.tasks_dir / "task_001.txt"
        task2_file = self.tasks_dir / "task_002.txt"
        self.assertTrue(task1_file.exists())
        self.assertTrue(task2_file.exists())
        
        # Check the content of the tasks file
        with open(tasks_file, "r") as f:
            tasks_data = json.load(f)
        
        self.assertEqual(len(tasks_data["tasks"]), 2)
        self.assertEqual(tasks_data["tasks"][0]["id"], 1)
        self.assertEqual(tasks_data["tasks"][1]["id"], 2)
    
    @pytest.mark.asyncio
    async def test_read_tasks(self):
        """Test reading tasks from a file."""
        # Write tasks to a file
        await self.storage_manager.write_tasks(self.sample_tasks)
        
        # Read tasks from the file
        tasks_data = await self.storage_manager.read_tasks()
        
        # Check that the tasks data matches the sample tasks
        self.assertEqual(len(tasks_data["tasks"]), 2)
        self.assertEqual(tasks_data["tasks"][0]["id"], 1)
        self.assertEqual(tasks_data["tasks"][1]["id"], 2)
    
    @pytest.mark.asyncio
    async def test_read_task_file(self):
        """Test reading a specific task file."""
        # Write tasks to a file
        await self.storage_manager.write_tasks(self.sample_tasks)
        
        # Read a specific task file
        task = await self.storage_manager.read_task_file(1)
        
        # Check that the task data matches the sample task
        self.assertEqual(task["id"], 1)
        self.assertEqual(task["title"], "Test Task 1")
        self.assertEqual(task["status"], TaskStatus.PENDING)
        self.assertEqual(task["priority"], TaskPriority.HIGH)
        self.assertEqual(task["description"], "Test description 1")
        self.assertEqual(task["details"], "Test details 1")
        self.assertEqual(task["testStrategy"], "Test strategy 1")
        self.assertEqual(task["dependencies"], [])
    
    @pytest.mark.asyncio
    async def test_read_task_file_not_found(self):
        """Test reading a task file that doesn't exist."""
        # Try to read a task file that doesn't exist
        with self.assertRaises(TaskFileNotFoundError):
            await self.storage_manager.read_task_file(999)
    
    @pytest.mark.asyncio
    async def test_write_task_file(self):
        """Test writing a specific task file."""
        # Sample task
        task = {
            "id": 3,
            "title": "Test Task 3",
            "status": TaskStatus.PENDING,
            "priority": TaskPriority.LOW,
            "description": "Test description 3",
            "details": "Test details 3",
            "testStrategy": "Test strategy 3",
            "dependencies": []
        }
        
        # Write the task file
        task_file = await self.storage_manager.write_task_file(task, [task])
        
        # Check that the task file exists
        self.assertTrue(task_file.exists())
        
        # Check the content of the task file
        content = task_file.read_text()
        self.assertIn("# Task ID: 3", content)
        self.assertIn("# Title: Test Task 3", content)
        self.assertIn("# Status: pending", content)
        self.assertIn("# Priority: low", content)
        self.assertIn("# Description: Test description 3", content)
        self.assertIn("# Details: Test details 3", content)
        self.assertIn("# Test Strategy:", content)
        self.assertIn("Test strategy 3", content)
    
    @pytest.mark.asyncio
    async def test_reintegrate_task_files(self):
        """Test reintegrating task files into the JSON data."""
        # Write tasks to a file
        await self.storage_manager.write_tasks(self.sample_tasks)
        
        # Modify a task file
        task1_file = self.tasks_dir / "task_001.txt"
        content = task1_file.read_text()
        content = content.replace("Test Task 1", "Modified Task 1")
        task1_file.write_text(content)
        
        # Reintegrate task files
        result = await self.storage_manager.reintegrate_task_files()
        
        # Check that the task was updated
        self.assertIn("task_001.txt", result["processed_files"])
        self.assertIn(1, result["updated_tasks"])
        
        # Check that the tasks data was updated
        tasks_data = result["tasks_data"]
        self.assertEqual(tasks_data["tasks"][0]["title"], "Modified Task 1")
    
    @pytest.mark.asyncio
    async def test_ensure_consistency(self):
        """Test ensuring consistency between JSON data and individual text files."""
        # Write tasks to a file
        await self.storage_manager.write_tasks(self.sample_tasks)
        
        # Delete a task file
        task1_file = self.tasks_dir / "task_001.txt"
        task1_file.unlink()
        
        # Ensure consistency
        changes = await self.storage_manager.ensure_consistency()
        
        # Check that the task file was recreated
        self.assertIn("task_001.txt", changes["added"])
        self.assertTrue(task1_file.exists())
    
    @pytest.mark.asyncio
    async def test_parse_task_file_content(self):
        """Test parsing task file content."""
        # Sample task file content
        content = """# Task ID: 4
# Title: Test Task 4
# Status: pending
# Dependencies: 1 (pending), 2 (in_progress)
# Priority: high
# Description: Test description 4
# Details: Test details 4
# Test Strategy:
Test strategy 4

# Subtasks:
## 1. Subtask 1 [pending]
### Dependencies: None
### Priority: medium
### Description: Subtask description 1
### Details:
Subtask details 1

## 2. Subtask 2 [in_progress]
### Dependencies: 1.1
### Priority: high
### Description: Subtask description 2
### Details:
Subtask details 2
"""
        
        # Parse the task file content
        task = self.storage_manager._parse_task_file_content(content)
        
        # Check that the task data was parsed correctly
        self.assertEqual(task["id"], 4)
        self.assertEqual(task["title"], "Test Task 4")
        self.assertEqual(task["status"], TaskStatus.PENDING)
        self.assertEqual(task["priority"], TaskPriority.HIGH)
        self.assertEqual(task["description"], "Test description 4")
        self.assertEqual(task["details"], "Test details 4")
        self.assertEqual(task["testStrategy"], "Test strategy 4")
        self.assertEqual(task["dependencies"], [1, 2])
        
        # Check that the subtasks were parsed correctly
        self.assertEqual(len(task["subtasks"]), 2)
        self.assertEqual(task["subtasks"][0]["id"], 1)
        self.assertEqual(task["subtasks"][0]["title"], "Subtask 1")
        self.assertEqual(task["subtasks"][0]["status"], TaskStatus.PENDING)
        self.assertEqual(task["subtasks"][0]["priority"], TaskPriority.MEDIUM)
        self.assertEqual(task["subtasks"][0]["description"], "Subtask description 1")
        self.assertEqual(task["subtasks"][0]["details"], "Subtask details 1")
        self.assertEqual(task["subtasks"][0]["dependencies"], [])
        
        self.assertEqual(task["subtasks"][1]["id"], 2)
        self.assertEqual(task["subtasks"][1]["title"], "Subtask 2")
        self.assertEqual(task["subtasks"][1]["status"], TaskStatus.IN_PROGRESS)
        self.assertEqual(task["subtasks"][1]["priority"], TaskPriority.HIGH)
        self.assertEqual(task["subtasks"][1]["description"], "Subtask description 2")
        self.assertEqual(task["subtasks"][1]["details"], "Subtask details 2")
        self.assertEqual(task["subtasks"][1]["dependencies"], ["1.1"])
    
    @pytest.mark.asyncio
    async def test_format_task_file_content(self):
        """Test formatting task content for file output."""
        # Sample task with subtasks
        task = {
            "id": 5,
            "title": "Test Task 5",
            "status": TaskStatus.PENDING,
            "priority": TaskPriority.HIGH,
            "description": "Test description 5",
            "details": "Test details 5",
            "testStrategy": "Test strategy 5",
            "dependencies": [],
            "subtasks": [
                {
                    "id": 1,
                    "title": "Subtask 1",
                    "status": TaskStatus.PENDING,
                    "priority": TaskPriority.MEDIUM,
                    "description": "Subtask description 1",
                    "details": "Subtask details 1",
                    "dependencies": []
                },
                {
                    "id": 2,
                    "title": "Subtask 2",
                    "status": TaskStatus.IN_PROGRESS,
                    "priority": TaskPriority.HIGH,
                    "description": "Subtask description 2",
                    "details": "Subtask details 2",
                    "dependencies": ["1.1"]
                }
            ]
        }
        
        # Format the task content
        content = self.storage_manager._format_task_file_content(task, [task])
        
        # Check that the content was formatted correctly
        self.assertIn("# Task ID: 5", content)
        self.assertIn("# Title: Test Task 5", content)
        self.assertIn("# Status: pending", content)
        self.assertIn("# Priority: high", content)
        self.assertIn("# Description: Test description 5", content)
        self.assertIn("# Details: Test details 5", content)
        self.assertIn("# Test Strategy:", content)
        self.assertIn("Test strategy 5", content)
        
        # Check that the subtasks were formatted correctly
        self.assertIn("# Subtasks:", content)
        self.assertIn("## 1. Subtask 1 [pending]", content)
        self.assertIn("### Dependencies: None", content)
        self.assertIn("### Priority: medium", content)
        self.assertIn("### Description: Subtask description 1", content)
        self.assertIn("### Details:", content)
        self.assertIn("Subtask details 1", content)
        
        self.assertIn("## 2. Subtask 2 [in_progress]", content)
        self.assertIn("### Dependencies: 1.1", content)
        self.assertIn("### Priority: high", content)
        self.assertIn("### Description: Subtask description 2", content)
        self.assertIn("### Details:", content)
        self.assertIn("Subtask details 2", content)
    
    @pytest.mark.asyncio
    async def test_tasks_differ(self):
        """Test checking if two tasks differ in content."""
        # Sample tasks
        task1 = {
            "id": 6,
            "title": "Test Task 6",
            "status": TaskStatus.PENDING,
            "priority": TaskPriority.HIGH,
            "description": "Test description 6",
            "details": "Test details 6",
            "testStrategy": "Test strategy 6",
            "dependencies": [1, 2],
            "subtasks": [
                {
                    "id": 1,
                    "title": "Subtask 1",
                    "status": TaskStatus.PENDING,
                    "priority": TaskPriority.MEDIUM,
                    "description": "Subtask description 1",
                    "details": "Subtask details 1",
                    "dependencies": []
                }
            ]
        }
        
        task2 = {
            "id": 6,
            "title": "Test Task 6",
            "status": TaskStatus.PENDING,
            "priority": TaskPriority.HIGH,
            "description": "Test description 6",
            "details": "Test details 6",
            "testStrategy": "Test strategy 6",
            "dependencies": [1, 2],
            "subtasks": [
                {
                    "id": 1,
                    "title": "Subtask 1",
                    "status": TaskStatus.PENDING,
                    "priority": TaskPriority.MEDIUM,
                    "description": "Subtask description 1",
                    "details": "Subtask details 1",
                    "dependencies": []
                }
            ]
        }
        
        # Check that the tasks are the same
        self.assertFalse(self.storage_manager._tasks_differ(task1, task2))
        
        # Modify task2
        task2["title"] = "Modified Task 6"
        
        # Check that the tasks are different
        self.assertTrue(self.storage_manager._tasks_differ(task1, task2))
        
        # Reset task2
        task2["title"] = "Test Task 6"
        
        # Modify a subtask
        task2["subtasks"][0]["title"] = "Modified Subtask 1"
        
        # Check that the tasks are different
        self.assertTrue(self.storage_manager._tasks_differ(task1, task2))
    
    @pytest.mark.asyncio
    async def test_file_lock(self):
        """Test the FileLock class."""
        # Create a lock file
        lock_file = self.tasks_dir / ".locks" / "test.lock"
        
        # Create a lock
        lock = FileLock(lock_file)
        
        # Acquire the lock
        async with lock:
            # Check that the lock file exists
            self.assertTrue(lock_file.exists())
            
            # Try to acquire the lock again (should raise an exception)
            with self.assertRaises(TaskFileLockError):
                async with FileLock(lock_file, timeout=0.1):
                    pass
        
        # Check that the lock file was removed
        self.assertFalse(lock_file.exists())
    
    @pytest.mark.asyncio
    async def test_error_handling(self):
        """Test error handling in the FileStorageManager."""
        # Mock the read_json function to raise an exception
        with mock.patch("taskinator.file_storage.read_json", side_effect=Exception("Test error")):
            # Try to read tasks
            with self.assertRaises(FileStorageError):
                await self.storage_manager.read_tasks()
        
        # Mock the write_json function to raise an exception
        with mock.patch("taskinator.file_storage.write_json", side_effect=Exception("Test error")):
            # Try to write tasks
            with self.assertRaises(FileStorageError):
                await self.storage_manager.write_tasks(self.sample_tasks)
        
        # Try to read a task file with invalid content
        task_file = self.tasks_dir / "task_001.txt"
        task_file.write_text("Invalid content")
        
        # Try to read the task file
        with self.assertRaises(TaskFileParseError):
            await self.storage_manager.read_task_file(1)
        
        # Try to write a task file without an ID
        with self.assertRaises(TaskFileWriteError):
            await self.storage_manager.write_task_file({}, [])


if __name__ == "__main__":
    unittest.main()
