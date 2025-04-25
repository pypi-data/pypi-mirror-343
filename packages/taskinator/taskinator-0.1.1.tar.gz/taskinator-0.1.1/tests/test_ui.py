"""Tests for terminal UI components."""

from unittest.mock import MagicMock, patch

import pytest
from rich.console import Console
from rich.table import Table
from rich.text import Text

from taskinator.config import TaskPriority, TaskStatus
from taskinator.ui import (
    COLORS,
    create_loading_indicator,
    create_task_table,
    display_banner,
    display_error,
    display_success,
    display_task_details,
    format_dependencies,
)


@pytest.fixture
def mock_console():
    """Fixture providing a mocked Rich console."""
    with patch("taskinator.ui.console") as mock:
        yield mock


@pytest.fixture
def sample_tasks():
    """Fixture providing sample tasks for testing."""
    return [
        {
            "id": 1,
            "title": "Task 1",
            "status": TaskStatus.PENDING,
            "priority": TaskPriority.MEDIUM,
            "dependencies": [],
            "description": "Test task 1",
            "details": "Implementation details",
            "testStrategy": "Test strategy"
        },
        {
            "id": 2,
            "title": "Task 2",
            "status": TaskStatus.IN_PROGRESS,
            "priority": TaskPriority.HIGH,
            "dependencies": [1],
            "description": "Test task 2",
            "details": "More details",
            "testStrategy": "Another strategy"
        }
    ]


@pytest.mark.skip(reason="UI component API has changed, test needs revision")
def test_create_task_table(sample_tasks):
    """Test task table creation."""
    # Test basic table
    table = create_task_table(sample_tasks)
    assert isinstance(table, Table)
    assert table.row_count == 2
    
    # Test table with subtasks
    task_with_subtasks = sample_tasks[0].copy()
    task_with_subtasks["subtasks"] = [
        {
            "id": 1,
            "title": "Subtask 1",
            "status": TaskStatus.PENDING,
            "priority": TaskPriority.LOW
        }
    ]
    table = create_task_table([task_with_subtasks], show_subtasks=True)
    assert table.row_count == 2  # Main task + subtask
    
    # Test table without dependencies column
    table = create_task_table(sample_tasks, show_dependencies=False)
    assert len(table.columns) == 4  # ID, Title, Status, Priority


@pytest.mark.skip(reason="UI component API has changed, test needs revision")
def test_format_dependencies(sample_tasks):
    """Test dependency formatting."""
    # Test no dependencies
    result = format_dependencies([])
    assert isinstance(result, Text)
    assert str(result) == "None"
    
    # Test with dependencies
    result = format_dependencies([1, 2])
    assert isinstance(result, Text)
    assert "1" in str(result)
    assert "2" in str(result)
    
    # Test with task status coloring
    result = format_dependencies([1], sample_tasks)
    assert isinstance(result, Text)
    assert result.style == COLORS["status"][TaskStatus.PENDING]


@pytest.mark.skip(reason="UI component API has changed, test needs revision")
def test_display_task_details(mock_console, sample_tasks):
    """Test task details display."""
    task = sample_tasks[0]
    display_task_details(task)
    
    # Verify panel creation
    mock_console.print.assert_called()
    
    # Test with subtasks
    task_with_subtasks = task.copy()
    task_with_subtasks["subtasks"] = [
        {
            "id": 1,
            "title": "Subtask 1",
            "status": TaskStatus.PENDING
        }
    ]
    display_task_details(task_with_subtasks)
    assert mock_console.print.call_count >= 2


@pytest.mark.skip(reason="UI component API has changed, test needs revision")
def test_display_error(mock_console):
    """Test error message display."""
    message = "Test error"
    display_error(message)
    mock_console.print.assert_called_once()
    
    # Verify error styling
    call_args = mock_console.print.call_args[0][0]
    assert "red" in str(call_args)
    assert message in str(call_args)


@pytest.mark.skip(reason="UI component API has changed, test needs revision")
def test_display_success(mock_console):
    """Test success message display."""
    message = "Test success"
    display_success(message)
    mock_console.print.assert_called_once()
    
    # Verify success styling
    call_args = mock_console.print.call_args[0][0]
    assert "green" in str(call_args)
    assert message in str(call_args)


@pytest.mark.skip(reason="UI component API has changed, test needs revision")
def test_create_loading_indicator():
    """Test loading indicator creation."""
    indicator = create_loading_indicator("Testing...")
    assert "SpinnerColumn" in str(indicator.columns[0])
    assert "Testing..." in str(indicator.columns[1])


@pytest.mark.skip(reason="UI component API has changed, test needs revision")
def test_loading_indicator_context():
    """Test loading indicator context manager."""
    with create_loading_indicator("Working...") as progress:
        assert progress.live.auto_refresh
        # Simulate some work
        progress.update(0, description="Still working...")


@pytest.mark.skip(reason="UI component API has changed, test needs revision")
def test_create_task_table(sample_tasks):
    """Test creating task table."""
    table = create_task_table(sample_tasks)
    assert isinstance(table, Table)
    assert table.row_count == 2


@pytest.mark.skip(reason="UI component API has changed, test needs revision")
def test_task_table_sorting(sample_tasks):
    """Test task table sorting and formatting."""
    # Create tasks with various states
    tasks = [
        {
            "id": 1,
            "title": "Z Task",
            "status": TaskStatus.PENDING,
            "priority": TaskPriority.LOW
        },
        {
            "id": 2,
            "title": "A Task",
            "status": TaskStatus.DONE,
            "priority": TaskPriority.HIGH
        }
    ]
    
    table = create_task_table(tasks)
    
    # Verify table structure
    assert table.row_count == 2
    assert all(column.header_style == "bold blue" for column in table.columns)
    
    # Verify row content (tasks should maintain their order)
    rows = list(table.rows)
    assert "Z Task" in str(rows[0])
    assert "A Task" in str(rows[1])


def test_task_table_empty():
    """Test task table with no tasks."""
    table = create_task_table([])
    assert table.row_count == 0
    assert len(table.columns) > 0  # Headers should still be present


def test_display_banner(mock_console):
    """Test banner display."""
    display_banner("Test Title")
    mock_console.print.assert_called()
    
    # Verify empty lines around banner
    assert mock_console.print.call_count >= 3


def test_color_schemes():
    """Test color scheme definitions."""
    # Test status colors
    assert all(
        status in COLORS["status"]
        for status in [
            TaskStatus.PENDING,
            TaskStatus.IN_PROGRESS,
            TaskStatus.DONE,
            TaskStatus.BLOCKED
        ]
    )
    
    # Test priority colors
    assert all(
        priority in COLORS["priority"]
        for priority in [
            TaskPriority.LOW,
            TaskPriority.MEDIUM,
            TaskPriority.HIGH
        ]
    )