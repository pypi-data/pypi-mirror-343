"""Tool to list all tasks from Taskinator."""

import logging
import os
from typing import Optional, Dict, Any
from pathlib import Path

from pydantic import BaseModel, Field

from ...task_manager import TaskManager
from .utils import create_content_response, create_error_response

logger = logging.getLogger(__name__)

class ListTasksParams(BaseModel):
    """Parameters for the listTasks tool."""
    
    status: Optional[str] = Field(
        None,
        description="Filter tasks by status"
    )
    with_subtasks: Optional[bool] = Field(
        False,
        description="Include subtasks in the response"
    )
    file: Optional[str] = Field(
        None,
        description="Path to the tasks file"
    )
    project_root: str = Field(
        description="Root directory of the project (default: current working directory)"
    )

async def execute_list_tasks(args: Dict[str, Any], context: dict) -> Dict[str, Any]:
    """Execute the listTasks tool.
    
    Args:
        args: Tool parameters
        context: Tool execution context
    
    Returns:
        Tool execution response
    """
    try:
        # Extract args from the wrapper
        if isinstance(args, dict) and "args" in args:
            args = args["args"]
            
        # Validate parameters
        params = ListTasksParams(**args)
        logger.info(f"Listing tasks with filters: {params.model_dump_json()}")
        
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
        
        # List tasks with provided filters - use correct parameter names
        tasks = task_manager.list_tasks(
            status=params.status
        )
        
        # Return the tasks as a structured response
        return create_content_response({
            "message": "Tasks listed successfully",
            "tasks": tasks
        })
        
    except Exception as e:
        # Include the current working directory in the error message
        current_cwd = os.getcwd()
        error_message = f"Error listing tasks: {str(e)} (CWD: {current_cwd})"
        logger.error(error_message)
        return create_error_response({
            "message": error_message,
            "error": str(e)
        })

def register_list_tasks_tool(server) -> None:
    """Register the listTasks tool with the MCP server.
    
    Args:
        server: FastMCP server instance
    """
    # Set tool metadata
    execute_list_tasks.__name__ = "listTasks"
    execute_list_tasks.__doc__ = "List all tasks from Taskinator"
    
    # Register tool
    server.add_tool(execute_list_tasks)