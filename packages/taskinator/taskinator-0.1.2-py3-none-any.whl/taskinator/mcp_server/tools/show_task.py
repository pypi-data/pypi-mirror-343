"""Tool to show detailed information about a specific task."""


from typing import Optional, Dict, Any
from pathlib import Path

from pydantic import BaseModel, Field

from ...task_manager import TaskManager
from .utils import create_content_response, create_error_response

from loguru import logger

class ShowTaskParams(BaseModel):
    """Parameters for the showTask tool."""
    
    id: str = Field(
        description="Task ID to show"
    )
    file: Optional[str] = Field(
        None,
        description="Path to the tasks file"
    )
    project_root: str = Field(
        description="Root directory of the project (default: current working directory)"
    )

async def execute_show_task(args: Dict[str, Any], context: dict) -> Dict[str, Any]:
    """Execute the showTask tool.
    
    Args:
        args: Tool parameters
        context: Tool execution context
    
    Returns:
        Tool execution response
    """

    # Validate parameters
    params = ShowTaskParams(**args)
    logger.info(f"Showing task details for ID: {params.id}")
    
    task_root = Path(params.project_root).joinpath("tasks")
    
    # Initialize TaskManager with custom tasks directory if file is provided
    task_manager = TaskManager(
        params.file if params.file else task_root
    )
    
    try:
        # Get task details
        task = task_manager.show_task(params.id)
        if task:
            return create_content_response({
                "message": "Task details retrieved successfully",
                "task": task
            })
        else:
            return create_error_response({
                "message": f"Task not found with ID: {params.id}"
            })
    except Exception as e:
        return create_error_response({
            "message": f"Error showing task: {str(e)}"
        })
        


def register_show_task_tool(server) -> None:
    """Register the showTask tool with the MCP server.
    
    Args:
        server: FastMCP server instance
    """
    # Set tool metadata
    execute_show_task.__name__ = "showTask"
    execute_show_task.__doc__ = "Show detailed information about a specific task"
    
    # Register tool
    server.add_tool(execute_show_task)