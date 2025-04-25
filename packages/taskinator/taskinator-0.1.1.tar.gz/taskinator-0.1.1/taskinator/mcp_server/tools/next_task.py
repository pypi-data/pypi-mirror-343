"""Tool to show the next task to work on based on dependencies and status."""

import logging
import os
from typing import Optional, Dict, Any
from pathlib import Path

from pydantic import BaseModel, Field

from ...task_manager import TaskManager
from .utils import create_content_response, create_error_response

logger = logging.getLogger(__name__)

class NextTaskParams(BaseModel):
    """Parameters for the nextTask tool."""
    
    file: Optional[str] = Field(
        None,
        description="Path to the tasks file"
    )
    project_root: str = Field(
        description="Root directory of the project (default: current working directory)"
    )

async def execute_next_task(args: Dict[str, Any], context: dict) -> Dict[str, Any]:
    """Execute the nextTask tool.
    
    Args:
        args: Tool parameters
        context: Tool execution context
    
    Returns:
        Tool execution response
    """
    try:
        # Validate parameters
        params = NextTaskParams(**args)
        logger.info("Finding next task to work on")
        
        # Log the current working directory for debugging
        current_cwd = os.getcwd()
        logger.info(f"Current working directory: {current_cwd}")
        
        # Determine the tasks file path
        if params.file:
            # If a specific file is provided, use it
            tasks_file = params.file
            logger.info(f"Using specified tasks file: {tasks_file}")
            task_manager = TaskManager(
                tasks_file=tasks_file,
                display_output=False
            )
        else:
            # Check if tasks.json exists directly in the project root
            project_tasks_file = os.path.join(params.project_root, "tasks.json")
            if os.path.exists(project_tasks_file):
                logger.info(f"Using tasks file in project root: {project_tasks_file}")
                task_manager = TaskManager(
                    tasks_file=project_tasks_file,
                    display_output=False
                )
            else:
                # Use the tasks directory from environment or default
                tasks_dir = os.getenv("TASKINATOR_TASKS_DIR", os.path.join(params.project_root, "tasks"))
                
                # Make sure tasks_dir is an absolute path
                if not os.path.isabs(tasks_dir):
                    tasks_dir = os.path.abspath(tasks_dir)
                    
                logger.info(f"Using tasks directory: {tasks_dir}")
                task_manager = TaskManager(
                    tasks_dir=tasks_dir,
                    display_output=False
                )
        
        # Find the next task
        next_task = task_manager.show_next_task()
        
        if next_task:
            # Return the task details in a structured format
            return create_content_response({
                "message": f"Found next task: {next_task['id']}",
                "task": next_task
            })
        else:
            return create_content_response({
                "message": "No eligible tasks found. All tasks may be completed or blocked by dependencies.",
                "task": None
            })
        
    except Exception as e:
        # Include the current working directory in the error message
        current_cwd = os.getcwd()
        error_message = f"Error finding next task: {str(e)} (CWD: {current_cwd})"
        logger.error(error_message)
        return create_error_response({
            "message": error_message,
            "error": str(e)
        })

def register_next_task_tool(server) -> None:
    """Register the nextTask tool with the MCP server.
    
    Args:
        server: FastMCP server instance
    """
    # Set tool metadata
    execute_next_task.__name__ = "nextTask"
    execute_next_task.__doc__ = "Show the next task to work on based on dependencies and status"
    
    # Register tool
    server.add_tool(execute_next_task)