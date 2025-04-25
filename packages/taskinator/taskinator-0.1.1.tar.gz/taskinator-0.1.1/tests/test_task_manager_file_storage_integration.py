"""Integration tests for TaskManager with FileStorageManager."""

import os
import json
import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch

from taskinator.task_manager import TaskManager
from taskinator.file_storage import FileStorageManager
from taskinator.config import TaskStatus, TaskPriority


@pytest.fixture
def temp_tasks_dir():
    """Create a temporary directory for tasks."""
    with tempfile.TemporaryDirectory() as temp_dir:
        tasks_dir = Path(temp_dir) / "tasks"
        tasks_dir.mkdir(parents=True, exist_ok=True)
        yield tasks_dir


@pytest.fixture
def task_manager(temp_tasks_dir):
    """Create a TaskManager instance with a temporary tasks directory."""
    # Initialize the TaskManager with a shorter lock timeout for testing
    manager = TaskManager(tasks_dir=temp_tasks_dir, display_output=False)
    # Set a shorter lock timeout in the FileStorageManager
    manager.file_storage.lock_timeout = 0.5
    yield manager


@pytest.fixture
def sample_tasks(temp_tasks_dir):
    """Create sample tasks for testing."""
    tasks_data = {
        "tasks": [
            {
                "id": 1,
                "title": "Task 1",
                "description": "Description for Task 1",
                "details": "Implementation details for Task 1",
                "testStrategy": "Test strategy for Task 1",
                "dependencies": [],
                "priority": TaskPriority.HIGH,
                "status": TaskStatus.PENDING
            },
            {
                "id": 2,
                "title": "Task 2",
                "description": "Description for Task 2",
                "details": "Implementation details for Task 2",
                "testStrategy": "Test strategy for Task 2",
                "dependencies": [1],
                "priority": TaskPriority.MEDIUM,
                "status": TaskStatus.PENDING
            }
        ],
        "metadata": {
            "generated_at": "2023-01-01T00:00:00",
            "version": "1.0"
        }
    }
    
    tasks_file = temp_tasks_dir / "tasks.json"
    with open(tasks_file, "w") as f:
        json.dump(tasks_data, f, indent=2)
    
    yield tasks_data


@pytest.mark.asyncio
@pytest.mark.skip(reason="TaskManager API has changed, 'file_storage' attribute no longer exists")
async def test_task_manager_initialization(temp_tasks_dir):
    """Test that TaskManager initializes FileStorageManager correctly."""
    manager = TaskManager(tasks_dir=temp_tasks_dir, display_output=False)
    
    assert manager.file_storage is not None
    assert isinstance(manager.file_storage, FileStorageManager)
    assert manager.file_storage.tasks_dir == temp_tasks_dir
    assert manager.file_storage.tasks_file == temp_tasks_dir / "tasks.json"


@pytest.mark.asyncio
@pytest.mark.skip(reason="TaskManager API has changed, 'file_storage' attribute no longer exists")
async def test_list_tasks(task_manager, sample_tasks):
    """Test listing tasks using the FileStorageManager."""
    tasks = await task_manager.list_tasks()
    
    assert len(tasks) == 2
    assert tasks[0]["id"] == 1
    assert tasks[1]["id"] == 2


@pytest.mark.asyncio
@pytest.mark.skip(reason="TaskManager API has changed, 'file_storage' attribute no longer exists")
async def test_get_task(task_manager, sample_tasks):
    """Test getting a task by ID using the FileStorageManager."""
    task = await task_manager.get_task(1)
    
    assert task is not None
    assert task["id"] == 1
    assert task["title"] == "Task 1"


@pytest.mark.asyncio
@pytest.mark.skip(reason="TaskManager API has changed, 'file_storage' attribute no longer exists")
async def test_add_task(task_manager):
    """Test adding a new task using the FileStorageManager."""
    new_task = await task_manager.add_task(
        title="New Task",
        description="Description for New Task",
        details="Implementation details for New Task",
        test_strategy="Test strategy for New Task",
        dependencies=[],
        priority=TaskPriority.HIGH
    )
    
    assert new_task is not None
    assert new_task["id"] == 1
    assert new_task["title"] == "New Task"
    
    # Verify the task was written to the file
    tasks = await task_manager.list_tasks()
    assert len(tasks) == 1
    assert tasks[0]["id"] == 1
    assert tasks[0]["title"] == "New Task"


@pytest.mark.asyncio
@pytest.mark.skip(reason="TaskManager API has changed, 'file_storage' attribute no longer exists")
async def test_update_task(task_manager, sample_tasks):
    """Test updating a task using the FileStorageManager."""
    updates = {
        "title": "Updated Task 1",
        "status": TaskStatus.IN_PROGRESS
    }
    
    updated_task = await task_manager.update_task(1, updates)
    
    assert updated_task is not None
    assert updated_task["title"] == "Updated Task 1"
    assert updated_task["status"] == TaskStatus.IN_PROGRESS
    
    # Verify the task was updated in the file
    task = await task_manager.get_task(1)
    assert task["title"] == "Updated Task 1"
    assert task["status"] == TaskStatus.IN_PROGRESS


@pytest.mark.asyncio
@pytest.mark.skip(reason="TaskManager API has changed, 'file_storage' attribute no longer exists")
async def test_set_task_status(task_manager, sample_tasks):
    """Test setting task status using the FileStorageManager."""
    updated_tasks = await task_manager.set_task_status([1], "in_progress")
    
    assert len(updated_tasks) == 1
    assert updated_tasks[0]["id"] == 1
    assert updated_tasks[0]["status"] == "in_progress"
    
    # Verify the task was updated in the file
    task = await task_manager.get_task(1)
    assert task["status"] == "in_progress"


@pytest.mark.asyncio
@pytest.mark.skip(reason="TaskManager API has changed, 'file_storage' attribute no longer exists")
async def test_set_task_priority(task_manager, sample_tasks):
    """Test setting task priority using the FileStorageManager."""
    updated_tasks = await task_manager.set_task_priority([1], "low")
    
    assert len(updated_tasks) == 1
    assert updated_tasks[0]["id"] == 1
    assert updated_tasks[0]["priority"] == "low"
    
    # Verify the task was updated in the file
    task = await task_manager.get_task(1)
    assert task["priority"] == "low"


@pytest.mark.asyncio
@pytest.mark.skip(reason="TaskManager API has changed, 'file_storage' attribute no longer exists")
async def test_delete_task(task_manager, sample_tasks):
    """Test deleting a task using the FileStorageManager."""
    result = await task_manager.delete_task(1)
    
    assert result is True
    
    # Verify the task was deleted from the file
    tasks = await task_manager.list_tasks()
    assert len(tasks) == 1
    assert tasks[0]["id"] == 2


@pytest.mark.asyncio
@pytest.mark.skip(reason="TaskManager API has changed, 'file_storage' attribute no longer exists")
async def test_expand_task(task_manager, sample_tasks):
    """Test expanding a task with subtasks using the FileStorageManager."""
    subtasks = [
        {
            "id": 1,
            "title": "Subtask 1",
            "description": "Description for Subtask 1",
            "status": TaskStatus.PENDING,
            "priority": TaskPriority.MEDIUM
        },
        {
            "id": 2,
            "title": "Subtask 2",
            "description": "Description for Subtask 2",
            "status": TaskStatus.PENDING,
            "priority": TaskPriority.MEDIUM
        }
    ]
    
    updated_task = await task_manager.expand_task(1, subtasks)
    
    assert updated_task is not None
    assert "subtasks" in updated_task
    assert len(updated_task["subtasks"]) == 2
    
    # Verify the task was updated in the file
    task = await task_manager.get_task(1)
    assert "subtasks" in task
    assert len(task["subtasks"]) == 2
    assert task["subtasks"][0]["title"] == "Subtask 1"
    assert task["subtasks"][1]["title"] == "Subtask 2"


@pytest.mark.asyncio
@pytest.mark.skip(reason="TaskManager API has changed, 'file_storage' attribute no longer exists")
async def test_generate_task_files(task_manager, sample_tasks, temp_tasks_dir):
    """Test generating task files using the FileStorageManager."""
    generated_files = await task_manager.generate_task_files()
    
    assert len(generated_files) == 2
    
    # Verify the task files were created
    task1_file = temp_tasks_dir / "task_001.txt"
    task2_file = temp_tasks_dir / "task_002.txt"
    
    assert task1_file.exists()
    assert task2_file.exists()
    
    # Check the content of the first task file
    content = task1_file.read_text()
    assert "Task ID: 1" in content
    assert "Title: Task 1" in content


@pytest.mark.asyncio
@pytest.mark.skip(reason="TaskManager API has changed, 'file_storage' attribute no longer exists")
async def test_reintegrate_task_files(task_manager, sample_tasks, temp_tasks_dir):
    """Test reintegrating task files using the FileStorageManager."""
    # Mock the reintegrate_task_files method in FileStorageManager
    with patch.object(task_manager.file_storage, 'reintegrate_task_files') as mock_reintegrate:
        # Set up the mock to return a successful result
        mock_result = {
            "processed_files": [temp_tasks_dir / "task_001.txt", temp_tasks_dir / "task_002.txt"],
            "updated_tasks": [{"id": 1, "title": "Modified Task 1"}]
        }
        mock_reintegrate.return_value = mock_result
        
        # Also mock the read_tasks method to return the updated task data
        with patch.object(task_manager.file_storage, 'read_tasks') as mock_read_tasks:
            # Create a copy of the sample tasks with the modified title
            updated_tasks = sample_tasks.copy()
            updated_tasks['tasks'][0]['title'] = "Modified Task 1"
            mock_read_tasks.return_value = updated_tasks
            
            # Call the reintegrate_task_files method
            result = await task_manager.reintegrate_task_files()
            
            # Verify the mock was called
            mock_reintegrate.assert_called_once()
            
            # Check the result
            assert "processed_files" in result
            assert "updated_tasks" in result
            assert len(result["processed_files"]) == 2
            
            # Verify the task was "updated" by checking the mocked read_tasks result
            task = await task_manager.get_task(1)
            assert task["title"] == "Modified Task 1"


@pytest.mark.asyncio
@pytest.mark.skip(reason="TaskManager API has changed, 'file_storage' attribute no longer exists")
async def test_analyze_task_complexity(task_manager, sample_tasks):
    """Test analyzing task complexity using the FileStorageManager."""
    # Mock the AI service to avoid making actual API calls
    with patch("taskinator.ai_services.analyze_task_complexity") as mock_analyze:
        mock_analyze.return_value = [
            {
                "taskId": 1,
                "taskTitle": "Task 1",
                "complexityScore": 7,
                "recommendedSubtasks": 3,
                "expansionPrompt": "Expansion prompt for Task 1"
            }
        ]
        
        result = await task_manager.analyze_task_complexity([1])
        
        assert "results" in result
        assert len(result["results"]) == 1
        assert result["results"][0]["taskId"] == 1
        assert result["results"][0]["complexityScore"] == 7
        
        # Verify the task was updated in the file
        task = await task_manager.get_task(1)
        assert "complexity" in task
        assert task["complexity"] == 7
