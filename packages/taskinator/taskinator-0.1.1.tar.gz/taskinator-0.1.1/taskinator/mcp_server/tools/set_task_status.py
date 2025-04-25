"""Tool to set the status of a task."""


import os
from typing import Optional, Dict, Any
from pathlib import Path

from pydantic import BaseModel, Field

from ...task_manager import TaskManager
from .utils import create_content_response, create_error_response

from loguru import logger

class SetTaskStatusParams(BaseModel):
    """Parameters for the setTaskStatus tool."""
    
    id: str = Field(
        description="Task ID (can be comma-separated for multiple tasks)"
    )
    status: str = Field(
        description="New status (pending, in_progress, done, blocked)"
    )
    file: Optional[str] = Field(
        None,
        description="Path to the tasks file"
    )
    project_root: str = Field(
        description="Root directory of the project (default: current working directory)"
    )

async def execute_set_task_status(args: Dict[str, Any], context: dict) -> Dict[str, Any]:
    """Execute the setTaskStatus tool.
    
    Args:
        args: Tool parameters
        context: Tool execution context
    
    Returns:
        Tool execution response
    """
    try:
        # Validate parameters
        params = SetTaskStatusParams(**args)
        logger.info(f"Setting status of task(s) {params.id} to: {params.status}")
        
        # Initialize TaskManager with custom tasks directory if file is provided
        
        task_root = Path(params.project_root).joinpath("tasks")

        task_manager = TaskManager(
            params.file if params.file else task_root
        )
        
        # Set task status
        # Note: TaskManager.set_task_status already handles comma-separated IDs
        await task_manager.set_task_status(params.id, params.status)
        
        return create_content_response(f"Successfully set status to {params.status} for task(s): {params.id}")
        
    except Exception as e:
        logger.error(f"Error setting task status: {e}")
        return create_error_response(f"Error setting task status: {e}")

def register_set_task_status_tool(server) -> None:
    """Register the setTaskStatus tool with the MCP server.
    
    Args:
        server: FastMCP server instance
    """
    # Set tool metadata
    execute_set_task_status.__name__ = "setTaskStatus"
    execute_set_task_status.__doc__ = "Set the status of a task"
    
    # Register tool
    server.add_tool(execute_set_task_status)