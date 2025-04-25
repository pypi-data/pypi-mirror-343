"""Tests for dependency management functionality."""

import pytest

from taskinator.config import TaskStatus
from taskinator.dependency_manager import (
    _has_circular_dependency,
    _validate_single_task_dependencies,
    get_dependent_tasks,
    update_dependent_tasks_status,
    validate_and_fix_dependencies,
    validate_task_dependencies,
)


@pytest.fixture
def sample_tasks():
    """Fixture providing sample tasks for testing."""
    return [
        {
            "id": 1,
            "title": "Task 1",
            "status": "pending",
            "dependencies": []
        },
        {
            "id": 2,
            "title": "Task 2",
            "status": "pending",
            "dependencies": [1]
        },
        {
            "id": 3,
            "title": "Task 3",
            "status": "pending",
            "dependencies": [2]
        }
    ]


@pytest.fixture
def tasks_with_circular_deps():
    """Fixture providing tasks with circular dependencies."""
    return [
        {
            "id": 1,
            "title": "Task 1",
            "status": "pending",
            "dependencies": [3]
        },
        {
            "id": 2,
            "title": "Task 2",
            "status": "pending",
            "dependencies": [1]
        },
        {
            "id": 3,
            "title": "Task 3",
            "status": "pending",
            "dependencies": [2]
        }
    ]


def test_validate_task_dependencies(sample_tasks):
    """Test task dependency validation."""
    # Test valid dependencies
    is_valid, errors = validate_task_dependencies(sample_tasks)
    assert is_valid
    assert not errors
    
    # Test single task validation
    is_valid, errors = validate_task_dependencies(sample_tasks, task_id=2)
    assert is_valid
    assert not errors
    
    # Test non-existent task
    is_valid, errors = validate_task_dependencies(sample_tasks, task_id=999)
    assert not is_valid
    assert len(errors) == 1
    assert "not found" in errors[0]


def test_validate_single_task_dependencies(sample_tasks):
    """Test validation of a single task's dependencies."""
    # Test valid task
    errors = _validate_single_task_dependencies(sample_tasks[1], sample_tasks)
    assert not errors
    
    # Test task with non-existent dependency
    task = {"id": 4, "dependencies": [999]}
    errors = _validate_single_task_dependencies(task, sample_tasks)
    assert len(errors) == 1
    assert "non-existent task" in errors[0]
    
    # Test done task with undone dependency
    task = {
        "id": 4,
        "status": TaskStatus.DONE,
        "dependencies": [1]
    }
    errors = _validate_single_task_dependencies(task, sample_tasks)
    assert len(errors) == 1
    assert "depends on unfinished task" in errors[0]


def test_circular_dependency_detection(tasks_with_circular_deps):
    """Test detection of circular dependencies."""
    # Test direct circular dependency
    assert _has_circular_dependency("1", "1", tasks_with_circular_deps, set())
    
    # Test indirect circular dependency
    assert _has_circular_dependency("1", "2", tasks_with_circular_deps, set())
    
    # Test no circular dependency
    assert not _has_circular_dependency("1", "999", tasks_with_circular_deps, set())


def test_validate_and_fix_dependencies(sample_tasks):
    """Test dependency validation and auto-fixing."""
    # Add a task with invalid dependency
    tasks = sample_tasks.copy()
    tasks.append({
        "id": 4,
        "title": "Task 4",
        "status": "done",
        "dependencies": [999]
    })
    
    # Test validation without fixing
    is_valid, errors, updated_tasks = validate_and_fix_dependencies(tasks, auto_fix=False)
    assert not is_valid
    assert len(errors) > 0
    
    # Test validation with fixing
    is_valid, errors, updated_tasks = validate_and_fix_dependencies(tasks, auto_fix=True)
    assert len(errors) == 0
    
    # Verify fixes
    task_4 = next(t for t in updated_tasks if t["id"] == 4)
    assert task_4["dependencies"] == []  # Invalid dependency removed


def test_get_dependent_tasks(sample_tasks):
    """Test finding dependent tasks."""
    # Test finding direct dependents
    dependents = get_dependent_tasks(1, sample_tasks)
    assert len(dependents) == 1
    assert dependents[0]["id"] == 2
    
    # Test finding indirect dependents
    dependents = get_dependent_tasks(2, sample_tasks)
    assert len(dependents) == 1
    assert dependents[0]["id"] == 3
    
    # Test task with no dependents
    dependents = get_dependent_tasks(3, sample_tasks)
    assert len(dependents) == 0


def test_update_dependent_tasks_status(sample_tasks):
    """Test updating dependent tasks' status."""
    # Test marking a dependency as done
    updated_tasks = update_dependent_tasks_status(1, sample_tasks, TaskStatus.DONE)
    dependent_task = next(t for t in updated_tasks if t["id"] == 2)
    assert dependent_task["status"] == TaskStatus.PENDING
    
    # Test marking a dependency as not done
    updated_tasks = update_dependent_tasks_status(1, sample_tasks, TaskStatus.BLOCKED)
    dependent_task = next(t for t in updated_tasks if t["id"] == 2)
    assert dependent_task["status"] == TaskStatus.BLOCKED
    
    # Test invalid status
    with pytest.raises(ValueError):
        update_dependent_tasks_status(1, sample_tasks, "invalid")


def test_complex_dependency_chain(sample_tasks):
    """Test handling of complex dependency chains."""
    # Create a more complex dependency chain
    tasks = sample_tasks.copy()
    tasks.extend([
        {
            "id": 4,
            "title": "Task 4",
            "status": "pending",
            "dependencies": [1, 2]
        },
        {
            "id": 5,
            "title": "Task 5",
            "status": "pending",
            "dependencies": [3, 4]
        }
    ])
    
    # Test validation
    is_valid, errors = validate_task_dependencies(tasks)
    assert is_valid
    assert not errors
    
    # Test status propagation
    updated_tasks = update_dependent_tasks_status(1, tasks, TaskStatus.BLOCKED)
    task_4 = next(t for t in updated_tasks if t["id"] == 4)
    task_5 = next(t for t in updated_tasks if t["id"] == 5)
    assert task_4["status"] == TaskStatus.BLOCKED
    assert task_5["status"] == TaskStatus.BLOCKED


def test_subtask_dependencies(sample_tasks):
    """Test handling of subtask dependencies."""
    # Add a task with subtasks
    tasks = sample_tasks.copy()
    task_with_subtasks = {
        "id": 4,
        "title": "Task with subtasks",
        "status": "pending",
        "dependencies": [1],
        "subtasks": [
            {
                "id": 1,
                "title": "Subtask 1",
                "status": "pending",
                "dependencies": []
            },
            {
                "id": 2,
                "title": "Subtask 2",
                "status": "pending",
                "dependencies": ["4.1"]  # Reference to Subtask 1
            }
        ]
    }
    tasks.append(task_with_subtasks)
    
    # Test validation
    is_valid, errors = validate_task_dependencies(tasks)
    assert is_valid
    assert not errors
    
    # Test subtask dependency validation
    errors = _validate_single_task_dependencies(
        task_with_subtasks["subtasks"][1],
        tasks
    )
    assert not errors  # Subtask dependencies should be valid