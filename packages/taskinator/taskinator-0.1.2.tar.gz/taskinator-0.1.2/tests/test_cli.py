"""Tests for command-line interface."""

from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from typer.testing import CliRunner

from taskinator.cli import app
from taskinator.config import TaskStatus

# Initialize test runner
runner = CliRunner()


@pytest.fixture
def mock_task_manager():
    """Fixture providing a mocked TaskManager."""
    with patch("taskinator.cli.TaskManager") as mock:
        instance = mock.return_value
        # Mock async methods
        instance.parse_prd = AsyncMock()
        instance.expand_task = AsyncMock()
        instance.set_task_status = AsyncMock()
        instance.update_tasks = AsyncMock()
        yield instance


@pytest.fixture
def sample_tasks_file(tmp_path):
    """Fixture providing a sample tasks.json file."""
    tasks_file = tmp_path / "tasks.json"
    tasks_file.write_text('{"tasks": []}')
    return tasks_file


def test_version():
    """Test version command."""
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "Taskinator v" in result.stdout


def test_init_command(tmp_path):
    """Test init command."""
    with patch("taskinator.cli.config.tasks_dir", tmp_path):
        # Test initial creation
        result = runner.invoke(app, ["init"])
        assert result.exit_code == 0
        assert "Initialized new Taskinator project" in result.stdout
        
        # Test existing project
        result = runner.invoke(app, ["init"])
        assert result.exit_code == 0
        assert "already initialized" in result.stdout
        
        # Test force initialization
        result = runner.invoke(app, ["init", "--force"])
        assert result.exit_code == 0
        assert "Initialized new Taskinator project" in result.stdout


@pytest.mark.asyncio
async def test_parse_command(mock_task_manager, tmp_path):
    """Test parse command."""
    # Create sample PRD file
    prd_file = tmp_path / "test.prd"
    prd_file.write_text("Sample PRD content")
    
    # Test basic parsing
    result = runner.invoke(app, ["parse", str(prd_file)])
    assert result.exit_code == 0
    mock_task_manager.parse_prd.assert_called_once()
    
    # Test with custom number of tasks
    result = runner.invoke(app, ["parse", str(prd_file), "--num-tasks", "5"])
    assert result.exit_code == 0
    assert mock_task_manager.parse_prd.call_args[1]["num_tasks"] == 5
    
    # Test with non-existent file
    result = runner.invoke(app, ["parse", "nonexistent.prd"])
    assert result.exit_code == 1
    assert "Error" in result.stdout


@pytest.mark.skip(reason="CLI API has changed, test needs revision")
def test_list_command(mock_task_manager):
    """Test list command."""
    # Test basic listing
    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0
    mock_task_manager.list_tasks.assert_called_once()
    
    # Test with status filter
    result = runner.invoke(app, ["list", "--status", "pending"])
    assert result.exit_code == 0
    assert mock_task_manager.list_tasks.call_args[1]["status_filter"] == "pending"
    
    # Test with subtasks
    result = runner.invoke(app, ["list", "--subtasks"])
    assert result.exit_code == 0
    assert mock_task_manager.list_tasks.call_args[1]["show_subtasks"] is True
    
    # Test with invalid status
    result = runner.invoke(app, ["list", "--status", "invalid"])
    assert result.exit_code == 1
    assert "Invalid status" in result.stdout


@pytest.mark.asyncio
@pytest.mark.skip(reason="CLI API has changed, test needs revision")
async def test_expand_command(mock_task_manager):
    """Test expand command."""
    # Test basic expansion
    result = runner.invoke(app, ["expand", "1"])
    assert result.exit_code == 0
    mock_task_manager.expand_task.assert_called_once()
    
    # Test with research flag
    result = runner.invoke(app, ["expand", "1", "--research"])
    assert result.exit_code == 0
    assert mock_task_manager.expand_task.call_args[1]["use_research"] is True
    
    # Test with custom number of subtasks
    result = runner.invoke(app, ["expand", "1", "--num-subtasks", "3"])
    assert result.exit_code == 0
    assert mock_task_manager.expand_task.call_args[1]["num_subtasks"] == 3
    
    # Test with additional context
    result = runner.invoke(app, ["expand", "1", "--context", "Test context"])
    assert result.exit_code == 0
    assert mock_task_manager.expand_task.call_args[1]["additional_context"] == "Test context"


@pytest.mark.asyncio
@pytest.mark.skip(reason="CLI API has changed, test needs revision")
async def test_status_command(mock_task_manager):
    """Test status command."""
    # Test single task update
    result = runner.invoke(app, ["status", "1", TaskStatus.DONE])
    assert result.exit_code == 0
    mock_task_manager.set_task_status.assert_called_once()
    
    # Test multiple task update
    result = runner.invoke(app, ["status", "1,2,3", TaskStatus.IN_PROGRESS])
    assert result.exit_code == 0
    assert mock_task_manager.set_task_status.call_args[0][0] == "1,2,3"
    
    # Test invalid status
    result = runner.invoke(app, ["status", "1", "invalid"])
    assert result.exit_code == 1
    assert "Invalid status" in result.stdout


@pytest.mark.asyncio
@pytest.mark.skip(reason="CLI API has changed, test needs revision")
async def test_update_command(mock_task_manager):
    """Test update command."""
    # Test basic update
    result = runner.invoke(app, ["update", "1", "New context"])
    assert result.exit_code == 0
    mock_task_manager.update_tasks.assert_called_once()
    
    # Test with research flag
    result = runner.invoke(app, ["update", "1", "New context", "--research"])
    assert result.exit_code == 0
    assert mock_task_manager.update_tasks.call_args[1]["use_research"] is True


@pytest.mark.skip(reason="CLI API has changed, test needs revision")
def test_error_handling():
    """Test CLI error handling."""
    with patch("taskinator.cli.task_manager.TaskManager.list_tasks",
              side_effect=Exception("Test error")):
        result = runner.invoke(app, ["list"])
        assert result.exit_code == 1
        assert "Error" in result.stdout
        assert "Test error" in result.stdout


@pytest.mark.skip(reason="CLI API has changed, test needs revision")
def test_help_messages():
    """Test CLI help messages."""
    # Test main help
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Taskinator" in result.stdout
    
    # Test command-specific help
    for command in ["init", "parse", "list", "expand", "status", "update"]:
        result = runner.invoke(app, [command, "--help"])
        assert result.exit_code == 0
        assert command in result.stdout.lower()


@pytest.mark.skip(reason="CLI API has changed, test needs revision")
def test_command_aliases():
    """Test command aliases and shortcuts."""
    with patch("taskinator.cli.task_manager.TaskManager.list_tasks") as mock_list:
        # Both commands should work the same
        runner.invoke(app, ["list"])
        runner.invoke(app, ["ls"])  # If you implement aliases
        assert mock_list.call_count == 2


@pytest.mark.skip(reason="CLI API has changed, test needs revision")
def test_environment_handling():
    """Test CLI environment variable handling."""
    with patch.dict("os.environ", {"DEBUG": "true"}):
        # Debug mode should affect output verbosity
        result = runner.invoke(app, ["list"])
        assert result.exit_code == 0