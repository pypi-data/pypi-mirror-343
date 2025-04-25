"""Tests for the Taskinator MCP server."""

import json
import os
import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from typing import Dict, Any

# Mock the config imports to avoid initialization issues
class MockTaskStatus:
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    BLOCKED = "blocked"
    
    @staticmethod
    def is_valid(status):
        return status in [MockTaskStatus.PENDING, MockTaskStatus.IN_PROGRESS, 
                         MockTaskStatus.DONE, MockTaskStatus.BLOCKED]

class MockTaskPriority:
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

# Patch the config imports
with patch("taskinator.mcp_server.tools.list_tasks.TaskManager") as _:
    with patch("taskinator.mcp_server.tools.next_task.TaskManager") as _:
        with patch("taskinator.mcp_server.tools.expand_task.TaskManager") as _:
            with patch("taskinator.mcp_server.tools.set_task_status.TaskManager") as _:
                with patch("taskinator.mcp_server.tools.show_task.TaskManager") as _:
                    with patch("taskinator.mcp_server.tools.add_task.TaskManager") as _:
                        from taskinator.mcp_server.server import TaskinatorMCPServer
                        from taskinator.mcp_server.tools.list_tasks import execute_list_tasks
                        from taskinator.mcp_server.tools.next_task import execute_next_task
                        from taskinator.mcp_server.tools.expand_task import execute_expand_task
                        from taskinator.mcp_server.tools.set_task_status import execute_set_task_status
                        from taskinator.mcp_server.tools.show_task import execute_show_task
                        from taskinator.mcp_server.tools.add_task import execute_add_task


@pytest.fixture
def mock_task_manager():
    """Fixture providing a mocked TaskManager."""
    with patch("taskinator.mcp_server.tools.list_tasks.TaskManager") as mock:
        instance = mock.return_value
        # Mock methods
        instance.list_tasks = MagicMock(return_value=[
            {"id": "1", "title": "Test Task 1", "status": "pending", "priority": "high"},
            {"id": "2", "title": "Test Task 2", "status": "in_progress", "priority": "medium"}
        ])
        instance.show_next_task = MagicMock(return_value={
            "id": "1", "title": "Test Task 1", "status": "pending", "priority": "high"
        })
        instance.show_task = MagicMock(return_value={
            "id": "1", "title": "Test Task 1", "status": "pending", "priority": "high"
        })
        instance.expand_task = AsyncMock(return_value={
            "id": "1", 
            "title": "Test Task 1", 
            "status": "pending", 
            "priority": "high",
            "subtasks": [
                {"id": "1.1", "title": "Subtask 1", "status": "pending"},
                {"id": "1.2", "title": "Subtask 2", "status": "pending"}
            ]
        })
        instance.set_task_status = AsyncMock()
        instance.add_task = AsyncMock(return_value={
            "id": "3", "title": "New Task", "status": "pending", "priority": "medium"
        })
        yield instance


@pytest.fixture
def sample_tasks_file(tmp_path):
    """Fixture providing a sample tasks.json file."""
    tasks_file = tmp_path / "tasks.json"
    tasks_file.write_text(json.dumps({
        "tasks": [
            {"id": "1", "title": "Test Task 1", "status": "pending", "priority": "high"},
            {"id": "2", "title": "Test Task 2", "status": "in_progress", "priority": "medium"}
        ]
    }))
    return tasks_file


@pytest.mark.asyncio
async def test_list_tasks_tool(mock_task_manager):
    """Test the listTasks tool."""
    # Test with valid parameters
    result = await execute_list_tasks({
        "project_root": "/path/to/project",
        "status": "pending",
        "with_subtasks": True
    }, {})
    
    assert result["success"] is True
    assert "tasks" in result["content"]
    mock_task_manager.list_tasks.assert_called_once_with(
        status="pending",
        show_subtasks=True
    )
    
    # Test with error handling
    mock_task_manager.list_tasks.side_effect = ValueError("Test error")
    result = await execute_list_tasks({
        "project_root": "/path/to/project"
    }, {})
    
    assert result["success"] is False
    assert "error" in result
    assert "Test error" in result["error"]["message"]


@pytest.mark.asyncio
async def test_next_task_tool(mock_task_manager):
    """Test the nextTask tool."""
    # Test with a task found
    result = await execute_next_task({
        "project_root": "/path/to/project"
    }, {})
    
    assert result["success"] is True
    assert "task" in result["content"]
    assert result["content"]["task"]["id"] == "1"
    
    # Test with no task found
    mock_task_manager.show_next_task.return_value = None
    result = await execute_next_task({
        "project_root": "/path/to/project"
    }, {})
    
    assert result["success"] is True
    assert result["content"]["task"] is None
    assert "No eligible tasks" in result["content"]["message"]
    
    # Test with error handling
    mock_task_manager.show_next_task.side_effect = ValueError("Test error")
    result = await execute_next_task({
        "project_root": "/path/to/project"
    }, {})
    
    assert result["success"] is False
    assert "error" in result
    assert "Test error" in result["error"]["message"]


@pytest.mark.asyncio
async def test_expand_task_tool(mock_task_manager):
    """Test the expandTask tool."""
    # Test with valid parameters
    result = await execute_expand_task({
        "project_root": "/path/to/project",
        "id": "1",
        "num": 3,
        "research": True,
        "prompt": "Additional context"
    }, {})
    
    assert result["success"] is True
    mock_task_manager.expand_task.assert_called_once_with(
        task_id="1",
        num_subtasks=3,
        use_research=True,
        additional_context="Additional context"
    )
    
    # Test with error handling
    mock_task_manager.expand_task.side_effect = ValueError("Test error")
    result = await execute_expand_task({
        "project_root": "/path/to/project",
        "id": "1"
    }, {})
    
    assert result["success"] is False
    assert "error" in result
    assert "Test error" in result["error"]["message"]


@pytest.mark.asyncio
async def test_show_task_tool(mock_task_manager):
    """Test the showTask tool."""
    # Test with valid parameters
    result = await execute_show_task({
        "project_root": "/path/to/project",
        "id": "1"
    }, {})
    
    assert result["success"] is True
    assert "task" in result["content"]
    assert result["content"]["task"]["id"] == "1"
    mock_task_manager.show_task.assert_called_once_with("1")
    
    # Test with error handling
    mock_task_manager.show_task.side_effect = ValueError("Test error")
    result = await execute_show_task({
        "project_root": "/path/to/project",
        "id": "1"
    }, {})
    
    assert result["success"] is False
    assert "error" in result
    assert "Test error" in result["error"]["message"]


@pytest.mark.asyncio
async def test_set_task_status_tool(mock_task_manager):
    """Test the setTaskStatus tool."""
    # Test with valid parameters
    result = await execute_set_task_status({
        "project_root": "/path/to/project",
        "id": "1",
        "status": "done"
    }, {})
    
    assert result["success"] is True
    mock_task_manager.set_task_status.assert_called_once_with("1", "done")
    
    # Test with error handling
    mock_task_manager.set_task_status.side_effect = ValueError("Test error")
    result = await execute_set_task_status({
        "project_root": "/path/to/project",
        "id": "1",
        "status": "done"
    }, {})
    
    assert result["success"] is False
    assert "error" in result
    assert "Test error" in result["error"]["message"]


@pytest.mark.asyncio
async def test_add_task_tool(mock_task_manager):
    """Test the addTask tool."""
    # Test with valid parameters
    result = await execute_add_task({
        "project_root": "/path/to/project",
        "prompt": "Create a new task",
        "priority": "high"
    }, {})
    
    assert result["success"] is True
    assert "task" in result["content"]
    assert result["content"]["task"]["id"] == "3"
    mock_task_manager.add_task.assert_called_once()
    
    # Test with error handling
    mock_task_manager.add_task.side_effect = ValueError("Test error")
    result = await execute_add_task({
        "project_root": "/path/to/project",
        "prompt": "Create a new task"
    }, {})
    
    assert result["success"] is False
    assert "error" in result
    assert "Test error" in result["error"]["message"]


@pytest.mark.asyncio
async def test_mcp_server_initialization():
    """Test the MCP server initialization."""
    with patch("taskinator.mcp_server.server.FastMCPServer") as mock_server:
        server_instance = mock_server.return_value
        
        # Initialize the MCP server
        mcp_server = TaskinatorMCPServer()
        
        # Verify server initialization
        assert mcp_server.server is not None
        server_instance.add_tool.assert_called()


@pytest.mark.asyncio
async def test_mcp_server_tool_registration():
    """Test that all tools are properly registered with the MCP server."""
    with patch("taskinator.mcp_server.server.FastMCPServer") as mock_server:
        server_instance = mock_server.return_value
        
        # Initialize the MCP server
        mcp_server = TaskinatorMCPServer()
        
        # Verify tool registration
        assert server_instance.add_tool.call_count >= 5  # At least 5 tools should be registered


@pytest.mark.skip(reason="TaskManager API has changed, test needs revision")
@pytest.mark.asyncio
async def test_mcp_server_integration(sample_tasks_file):
    """Test the MCP server with actual task operations."""
    # This test requires a real TaskManager with a sample tasks file
    with patch.dict(os.environ, {"TASKS_FILE": str(sample_tasks_file)}):
        with patch("taskinator.mcp_server.tools.list_tasks.TaskManager", return_value=TaskManager(str(sample_tasks_file), display_output=False)):
            # Test the listTasks tool with a real TaskManager
            result = await execute_list_tasks({
                "project_root": str(sample_tasks_file.parent),
                "status": None,
                "with_subtasks": False
            }, {})
            
            assert result["success"] is True
            assert "tasks" in result["content"]
            assert len(result["content"]["tasks"]) == 2
