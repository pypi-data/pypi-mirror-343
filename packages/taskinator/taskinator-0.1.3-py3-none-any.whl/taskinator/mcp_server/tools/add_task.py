"""Tool to add a new task using AI."""


import os
from typing import Optional, Dict, Any, List
from pathlib import Path

from pydantic import BaseModel, Field

from ...task_manager import TaskManager
from .utils import create_content_response, create_error_response

from loguru import logger

class AddTaskParams(BaseModel):
    """Parameters for the addTask tool."""
    
    prompt: str = Field(
        description="Description of the task to add"
    )
    dependencies: Optional[str] = Field(
        None,
        description="Comma-separated list of task IDs this task depends on"
    )
    priority: Optional[str] = Field(
        None,
        description="Task priority (high, medium, low)"
    )
    file: Optional[str] = Field(
        None,
        description="Path to the tasks file"
    )
    project_root: str = Field(
        description="Root directory of the project (default: current working directory)"
    )

async def execute_add_task(prompt: str,
                         dependencies: Optional[str] = None,
                         priority: Optional[str] = "medium",
                         file: Optional[str] = None,
                         project_root: str = str(Path.cwd())) -> Dict[str, Any]:
    """Execute the addTask tool.
    
    Args:
        prompt: Description of the task to add
        dependencies: Comma-separated list of task IDs this task depends on
        priority: Task priority (high, medium, low)
        file: Optional path to tasks file
        project_root: Project root directory
    
    Returns:
        Tool execution response
    """
    try:
        # Create params object
        params = AddTaskParams(
            prompt=prompt,
            dependencies=dependencies,
            priority=priority,
            file=file,
            project_root=project_root
        )
        logger.info(f"Adding new task: {params.prompt}")
        
        task_root = Path(params.project_root).joinpath("tasks")

        # Initialize TaskManager with custom tasks directory if file is provided
        task_manager = TaskManager(
            params.file if params.file else task_root
        )
        
        # Parse dependencies if provided
        dependencies = []
        if params.dependencies:
            dependencies = [int(id.strip()) for id in params.dependencies.split(',')]
        
        # Add task
        await task_manager.add_task(
            prompt=params.prompt,
            dependencies=dependencies,
            priority=params.priority or "medium"
        )
        
        return create_content_response("Task added successfully")
        
    except Exception as e:
        logger.error(f"Error adding task: {e}")
        return create_error_response(f"Error adding task: {e}")

def register_add_task_tool(server) -> None:
    """Register the addTask tool with the MCP server.
    
    Args:
        server: FastMCP server instance
    """
    # Register using decorator
    server.tool("addTask")(execute_add_task)