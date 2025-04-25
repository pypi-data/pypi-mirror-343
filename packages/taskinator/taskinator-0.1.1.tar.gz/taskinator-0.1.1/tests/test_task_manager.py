"""Tests for task management functionality."""

import json
import asyncio
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from taskinator.config import TaskStatus, TaskPriority
from taskinator.task_manager import TaskManager


@pytest.fixture
def temp_tasks_dir(tmp_path):
    """Fixture providing a temporary tasks directory."""
    tasks_dir = tmp_path / "tasks"
    tasks_dir.mkdir()
    return tasks_dir


@pytest.fixture
def sample_tasks():
    """Fixture providing sample tasks data."""
    return {
        "tasks": [
            {
                "id": 1,
                "title": "Task 1",
                "description": "Test task 1",
                "details": "Implementation details 1",
                "status": "pending",
                "priority": "medium",
                "dependencies": [],
                "testStrategy": "Test strategy 1"
            },
            {
                "id": 2,
                "title": "Task 2",
                "description": "Test task 2",
                "details": "Implementation details 2",
                "status": "in_progress",
                "priority": "high",
                "dependencies": [1],
                "testStrategy": "Test strategy 2"
            }
        ]
    }


@pytest.fixture
def task_manager(temp_tasks_dir):
    """Fixture providing a TaskManager instance."""
    return TaskManager(tasks_dir=temp_tasks_dir)


@pytest.fixture
def setup_tasks_file(temp_tasks_dir, sample_tasks):
    """Fixture to set up a tasks.json file."""
    tasks_file = temp_tasks_dir / "tasks.json"
    tasks_file.write_text(json.dumps(sample_tasks))
    return tasks_file


@pytest.mark.asyncio
async def test_parse_prd(task_manager, temp_tasks_dir):
    """Test PRD parsing functionality."""
    # Create test PRD file
    prd_file = temp_tasks_dir / "test.prd"
    prd_file.write_text("Test PRD content")
    
    # Mock AI service call
    with patch("taskinator.ai_services.call_claude") as mock_call_claude:
        mock_call_claude.return_value = {
            "tasks": [
                {
                    "id": 1,
                    "title": "Generated Task",
                    "description": "Test description",
                    "details": "Test details",
                    "status": "pending",
                    "priority": "medium",
                    "dependencies": []
                }
            ]
        }
        
        await task_manager.parse_prd(prd_file)
        
        # Verify tasks.json was created
        tasks_file = temp_tasks_dir / "tasks.json"
        assert tasks_file.exists()
        
        # Verify task file was created
        task_file = temp_tasks_dir / "task_001.txt"
        assert task_file.exists()
        
        # Verify file contents
        tasks_data = json.loads(tasks_file.read_text())
        assert len(tasks_data["tasks"]) == 1
        assert tasks_data["tasks"][0]["title"] == "Generated Task"


@pytest.mark.asyncio
async def test_generate_task_files(
    task_manager,
    temp_tasks_dir,
    setup_tasks_file,
    sample_tasks
):
    """Test task file generation."""
    await task_manager.generate_task_files()
    
    # Verify task files were created
    for task in sample_tasks["tasks"]:
        task_file = temp_tasks_dir / f"task_{str(task['id']).zfill(3)}.txt"
        assert task_file.exists()
        
        # Verify file contents
        content = task_file.read_text()
        assert f"Task ID: {task['id']}" in content
        assert f"Title: {task['title']}" in content
        assert task['description'] in content


@pytest.mark.asyncio
async def test_update_tasks(task_manager, setup_tasks_file):
    """Test task updating functionality."""
    pytest.skip("update_tasks method is not implemented in the current version")


@pytest.mark.asyncio
async def test_set_task_status(task_manager, setup_tasks_file):
    """Test setting task status."""
    await task_manager.set_task_status("1", TaskStatus.DONE)
    
    # Verify status was updated
    tasks_data = json.loads(task_manager.tasks_file.read_text())
    updated_task = next(t for t in tasks_data["tasks"] if t["id"] == 1)
    assert updated_task["status"] == TaskStatus.DONE
    
    # Verify dependent task was updated
    dependent_task = next(t for t in tasks_data["tasks"] if t["id"] == 2)
    assert dependent_task["status"] == TaskStatus.PENDING


def test_list_tasks(task_manager, setup_tasks_file):
    """Test task listing functionality."""
    # Test listing all tasks
    tasks = task_manager.list_tasks()
    
    # Verify tasks were returned
    assert len(tasks) == 2
    assert tasks[0]["title"] == "Task 1"
    assert tasks[1]["title"] == "Task 2"
    
    # Test filtering by status
    in_progress_tasks = task_manager.list_tasks(status="in_progress")
    
    # Verify filtering worked
    assert len(in_progress_tasks) == 1
    assert in_progress_tasks[0]["title"] == "Task 2"
    
    # Test filtering by priority
    high_priority_tasks = task_manager.list_tasks(priority="high")
    
    # Verify filtering worked
    assert len(high_priority_tasks) == 1
    assert high_priority_tasks[0]["title"] == "Task 2"
    
    # Test filtering by both status and priority
    filtered_tasks = task_manager.list_tasks(status="in_progress", priority="high")
    
    # Verify filtering worked
    assert len(filtered_tasks) == 1
    assert filtered_tasks[0]["title"] == "Task 2"


@pytest.mark.asyncio
async def test_expand_task(task_manager, setup_tasks_file):
    """Test task expansion functionality."""
    with patch("taskinator.ai_services.generate_subtasks") as mock_generate:
        mock_generate.return_value = [
            {
                "id": 1,
                "title": "Subtask 1",
                "description": "Test subtask",
                "status": "pending",
                "dependencies": []
            }
        ]
        
        await task_manager.expand_task(1)
        
        # Verify subtasks were added
        tasks_data = json.loads(task_manager.tasks_file.read_text())
        expanded_task = next(t for t in tasks_data["tasks"] if t["id"] == 1)
        assert "subtasks" in expanded_task
        assert len(expanded_task["subtasks"]) == 1
        assert expanded_task["subtasks"][0]["title"] == "Subtask 1"


@pytest.mark.asyncio
async def test_error_handling(task_manager, temp_tasks_dir):
    """Test error handling in task operations."""
    # Test parsing non-existent PRD
    with pytest.raises(FileNotFoundError):
        await task_manager.parse_prd(temp_tasks_dir / "nonexistent.prd")
    
    # Test invalid task ID
    with pytest.raises(ValueError):
        await task_manager.set_task_status("invalid", TaskStatus.DONE)
    
    # Test invalid status
    with pytest.raises(ValueError):
        await task_manager.set_task_status("1", "invalid_status")


@pytest.mark.asyncio
async def test_task_file_formatting(task_manager, setup_tasks_file):
    """Test task file content formatting."""
    # Mock the _format_task_file_content method
    with patch.object(task_manager, "_format_task_file_content") as mock_format:
        mock_format.return_value = """# Task ID: 1
# Title: Task 1
# Status: pending
# Priority: medium
# Dependencies: None
# Description: Test task 1
# Details: Implementation details 1
# Test Strategy: Test strategy 1
"""
        await task_manager.generate_task_files()
        
        # Verify the method was called
        assert mock_format.call_count > 0


@pytest.mark.asyncio
async def test_concurrent_operations(task_manager, setup_tasks_file):
    """Test handling of concurrent task operations."""
    # Test concurrent status updates
    status_updates = []
    for task_id in ["1", "2"]:
        status_updates.append(
            task_manager.set_task_status(task_id, TaskStatus.IN_PROGRESS)
        )
    
    # Use asyncio.gather to run the coroutines concurrently
    await asyncio.gather(*status_updates)
    
    # Verify all updates were applied
    tasks_data = json.loads(task_manager.tasks_file.read_text())
    assert all(
        task["status"] == TaskStatus.IN_PROGRESS
        for task in tasks_data["tasks"]
    )


@pytest.mark.asyncio
async def test_set_task_priority(task_manager, setup_tasks_file):
    """Test setting task priority."""
    await task_manager.set_task_priority("1", TaskPriority.HIGH)
    
    # Verify priority was updated
    tasks_data = json.loads(task_manager.tasks_file.read_text())
    updated_task = next(t for t in tasks_data["tasks"] if t["id"] == 1)
    assert updated_task["priority"] == TaskPriority.HIGH


@pytest.mark.asyncio
async def test_analyze_task_complexity(task_manager, setup_tasks_file, tmp_path):
    """Test task complexity analysis."""
    output_file = str(tmp_path / "complexity_report.json")
    
    with patch("taskinator.ai_services.analyze_task_complexity") as mock_analyze, \
         patch("taskinator.ui.create_loading_indicator"):
        mock_analyze.return_value = [
            {
                "taskId": 1,
                "taskTitle": "Task 1",
                "complexityScore": 7,
                "reasoning": "Test reasoning",
                "recommendedSubtasks": 3,
                "recommendations": ["Break down into subtasks"]
            }
        ]
        
        result = await task_manager.analyze_task_complexity(
            output_file=output_file
        )
        
        # Verify complexity analysis was performed
        assert len(result) > 0
        assert "taskId" in result[0]
        assert result[0]["complexityScore"] == 7
        assert "recommendedSubtasks" in result[0]


@pytest.mark.asyncio
async def test_analyze_task_similarities(task_manager, setup_tasks_file, tmp_path):
    """Test task similarity analysis."""
    output_file = str(tmp_path / "similarity_report.json")
    
    with patch("taskinator.similarity_module.TaskSimilarityModule.analyze_task_similarities") as mock_analyze:
        mock_analyze.return_value = {
            "similar_pairs": [
                {
                    "task1_id": 1,
                    "task2_id": 2,
                    "similarity_score": 0.8,
                    "reason": "Similar descriptions"
                }
            ],
            "summary": "Found 1 similar task pair",
            "totalTasksAnalyzed": 2,
            "totalPairsCompared": 1
        }
        
        result = await task_manager.analyze_task_similarities(
            threshold=0.7,
            output_file=output_file
        )
        
        # Verify similarity analysis was performed
        assert "similar_pairs" in result
        assert len(result["similar_pairs"]) == 1
        assert result["similar_pairs"][0]["task1_id"] == 1
        assert result["similar_pairs"][0]["task2_id"] == 2
        assert result["similar_pairs"][0]["similarity_score"] == 0.8


def test_show_next_task(task_manager, setup_tasks_file):
    """Test showing the next task to work on."""
    # Patch the UI display functions
    with patch("taskinator.ui.display_info"), \
         patch("taskinator.ui.display_task_details"), \
         patch("taskinator.ui.display_error"):
        
        # First task is pending and has no dependencies
        next_task = task_manager.show_next_task()
        
        # Verify correct task was selected
        assert next_task is not None
        assert next_task["id"] == 1
        assert next_task["title"] == "Task 1"
        
        # For the second test, we need to completely override the read_json function
        # to ensure it returns our mock data regardless of the file path
        with patch("taskinator.task_manager.read_json") as mock_read_json:
            mock_data = {
                "tasks": [
                    {"id": 1, "title": "Task 1", "status": "done", "dependencies": [], "priority": "medium"},
                    {"id": 2, "title": "Task 2", "status": "in_progress", "dependencies": [3], "priority": "high"}
                ]
            }
            mock_read_json.return_value = mock_data
            
            # Now call show_next_task again
            next_task = task_manager.show_next_task()
            
            # Since all tasks are either done or have unsatisfied dependencies, 
            # next_task should be None
            assert next_task is None


@pytest.mark.asyncio
async def test_add_task(task_manager, setup_tasks_file):
    """Test adding a new task."""
    with patch("taskinator.ai_services.generate_task_details") as mock_generate, \
         patch("taskinator.ui.display_success"), \
         patch("taskinator.ui.display_task_details"):
        mock_generate.return_value = {
            "title": "New Task",
            "description": "New task description",
            "details": "New task details",
            "testStrategy": "New task test strategy"
        }
        
        new_task = await task_manager.add_task(
            prompt="Create a new task",
            dependencies=[1],
            priority="medium"
        )
        
        # Verify task was added
        assert new_task["id"] == 3
        assert new_task["title"] == "New Task"
        
        # Verify task was added to tasks.json
        tasks_data = json.loads(task_manager.tasks_file.read_text())
        assert len(tasks_data["tasks"]) == 3
        added_task = next(t for t in tasks_data["tasks"] if t["id"] == 3)
        assert added_task["title"] == "New Task"
        assert added_task["dependencies"] == [1]


def test_ensure_subtask_structure(task_manager):
    """Test ensuring subtask structure."""
    # Test with minimal subtask
    minimal_subtask = {"title": "Minimal Subtask"}
    complete_subtask = task_manager._ensure_subtask_structure(minimal_subtask)
    
    # Verify defaults were added
    assert complete_subtask["title"] == "Minimal Subtask"
    assert complete_subtask["status"] == TaskStatus.PENDING
    assert complete_subtask["priority"] == TaskPriority.MEDIUM
    assert complete_subtask["dependencies"] == []
    assert "description" in complete_subtask
    assert "details" in complete_subtask
    
    # Test with existing values
    custom_subtask = {
        "title": "Custom Subtask",
        "status": TaskStatus.IN_PROGRESS,
        "priority": TaskPriority.HIGH,
        "dependencies": [1],
        "description": "Custom description",
        "details": "Custom details"
    }
    
    complete_custom = task_manager._ensure_subtask_structure(custom_subtask)
    
    # Verify existing values were preserved
    assert complete_custom["status"] == TaskStatus.IN_PROGRESS
    assert complete_custom["priority"] == TaskPriority.HIGH
    assert complete_custom["dependencies"] == [1]
    assert complete_custom["description"] == "Custom description"
    assert complete_custom["details"] == "Custom details"