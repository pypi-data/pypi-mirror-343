#!/usr/bin/env python
"""Script to test the Taskinator MCP tools directly."""

import sys
import os
import json
import logging
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add the project root to the Python path
project_root = str(Path(__file__).parent.parent.absolute())
if project_root not in sys.path:
    sys.path.insert(0, project_root)
    print(f"Added {project_root} to Python path")

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Mock TaskManager to avoid dependency issues
class MockTaskManager:
    def __init__(self, tasks_dir=None, display_output=True):
        self.tasks_dir = tasks_dir
        self.display_output = display_output
        logger.info(f"Initialized MockTaskManager with tasks_dir={tasks_dir}")
        
    def list_tasks(self, status=None, priority=None, show_subtasks=False):
        logger.info(f"Called list_tasks with status={status}, priority={priority}, show_subtasks={show_subtasks}")
        return [
            {"id": "1", "title": "Test Task 1", "status": "pending", "priority": "high"},
            {"id": "2", "title": "Test Task 2", "status": "in_progress", "priority": "medium"}
        ]
        
    def show_next_task(self):
        logger.info("Called show_next_task")
        return {"id": "1", "title": "Test Task 1", "status": "pending", "priority": "high"}
        
    def show_task(self, task_id):
        logger.info(f"Called show_task with task_id={task_id}")
        return {"id": task_id, "title": f"Test Task {task_id}", "status": "pending", "priority": "high"}
        
    async def expand_task(self, task_id, num_subtasks=5, use_research=False, additional_context=""):
        logger.info(f"Called expand_task with task_id={task_id}, num_subtasks={num_subtasks}, use_research={use_research}")
        return {
            "id": task_id, 
            "title": f"Test Task {task_id}", 
            "status": "pending", 
            "priority": "high",
            "subtasks": [
                {"id": f"{task_id}.1", "title": "Subtask 1", "status": "pending"},
                {"id": f"{task_id}.2", "title": "Subtask 2", "status": "pending"}
            ]
        }
        
    async def set_task_status(self, task_id, status):
        logger.info(f"Called set_task_status with task_id={task_id}, status={status}")
        return {"id": task_id, "title": f"Test Task {task_id}", "status": status, "priority": "high"}
        
    async def add_task(self, title, description="", priority="medium"):
        logger.info(f"Called add_task with title={title}, priority={priority}")
        return {"id": "3", "title": title, "status": "pending", "priority": priority}


async def test_list_tasks_tool():
    """Test the listTasks tool with the correct parameters."""
    # Import the tool function
    with patch("taskinator.mcp_server.tools.list_tasks.TaskManager", MockTaskManager):
        from taskinator.mcp_server.tools.list_tasks import execute_list_tasks
        
        # Test with valid parameters
        result = await execute_list_tasks({
            "project_root": "/path/to/project",
            "status": "pending",
            "with_subtasks": True
        }, {})
        
        logger.info(f"list_tasks result: {json.dumps(result, indent=2)}")
        assert result["success"] is True
        assert "tasks" in result["content"]
        
        # Test with error parameters
        try:
            result = await execute_list_tasks({
                "project_root": "/path/to/project",
                "invalid_param": "value"
            }, {})
            logger.info(f"list_tasks error result: {json.dumps(result, indent=2)}")
        except Exception as e:
            logger.error(f"Error in list_tasks: {e}")


async def test_next_task_tool():
    """Test the nextTask tool with the correct parameters."""
    # Import the tool function
    with patch("taskinator.mcp_server.tools.next_task.TaskManager", MockTaskManager):
        from taskinator.mcp_server.tools.next_task import execute_next_task
        
        # Test with valid parameters
        result = await execute_next_task({
            "project_root": "/path/to/project"
        }, {})
        
        logger.info(f"next_task result: {json.dumps(result, indent=2)}")
        assert result["success"] is True
        assert "task" in result["content"]


async def test_expand_task_tool():
    """Test the expandTask tool with the correct parameters."""
    # Import the tool function
    with patch("taskinator.mcp_server.tools.expand_task.TaskManager", MockTaskManager):
        from taskinator.mcp_server.tools.expand_task import execute_expand_task
        
        # Test with valid parameters
        result = await execute_expand_task({
            "project_root": "/path/to/project",
            "id": "1",
            "num": 3,
            "research": True,
            "prompt": "Additional context"
        }, {})
        
        logger.info(f"expand_task result: {json.dumps(result, indent=2)}")
        assert result["success"] is True


async def run_tests():
    """Run all the tests."""
    logger.info("Starting MCP tool tests")
    
    await test_list_tasks_tool()
    await test_next_task_tool()
    await test_expand_task_tool()
    
    logger.info("All tests completed")


if __name__ == "__main__":
    import asyncio
    asyncio.run(run_tests())
