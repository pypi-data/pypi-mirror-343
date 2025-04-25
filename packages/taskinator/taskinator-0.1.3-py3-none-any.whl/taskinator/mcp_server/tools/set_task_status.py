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

async def execute_set_task_status(id: str,
                                status: str,
                                file: Optional[str] = None,
                                project_root: str = str(Path.cwd())) -> Dict[str, Any]:
    """Execute the setTaskStatus tool.
    
    Args:
        id: Task ID (can be comma-separated for multiple tasks)
        status: New status (pending, in_progress, done, blocked)
        file: Optional path to tasks file
        project_root: Project root directory
    
    Returns:
        Tool execution response
    """
    try:
        # Create params object
        params = SetTaskStatusParams(
            id=id,
            status=status,
            file=file,
            project_root=project_root
        )
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
    # Register using decorator
    server.tool("setTaskStatus")(execute_set_task_status)