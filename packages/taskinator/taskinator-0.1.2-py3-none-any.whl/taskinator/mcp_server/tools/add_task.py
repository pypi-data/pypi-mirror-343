"""Tool to add a new task using AI."""


import os
from typing import Optional, Dict, Any

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

async def execute_add_task(args: Dict[str, Any], context: dict) -> Dict[str, Any]:
    """Execute the addTask tool.
    
    Args:
        args: Tool parameters
        context: Tool execution context
    
    Returns:
        Tool execution response
    """
    try:
        # Validate parameters
        params = AddTaskParams(**args)
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
    # Set tool metadata
    execute_add_task.__name__ = "addTask"
    execute_add_task.__doc__ = "Add a new task using AI"
    
    # Register tool
    server.add_tool(execute_add_task)