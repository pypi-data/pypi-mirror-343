"""Tool to break down a task into detailed subtasks."""


import os
from typing import Optional, Dict, Any

from pydantic import BaseModel, Field

from ...task_manager import TaskManager
from .utils import create_content_response, create_error_response

from loguru import logger

class ExpandTaskParams(BaseModel):
    """Parameters for the expandTask tool."""
    
    id: str = Field(
        description="Task ID to expand"
    )
    num: Optional[int] = Field(
        None,
        description="Number of subtasks to generate"
    )
    research: Optional[bool] = Field(
        False,
        description="Enable Perplexity AI for research-backed subtask generation"
    )
    prompt: Optional[str] = Field(
        None,
        description="Additional context to guide subtask generation"
    )
    force: Optional[bool] = Field(
        False,
        description="Force expansion even if subtasks already exist"
    )
    file: Optional[str] = Field(
        None,
        description="Path to the tasks file"
    )
    project_root: str = Field(
        description="Root directory of the project (default: current working directory)"
    )

async def execute_expand_task(args: Dict[str, Any], context: dict) -> Dict[str, Any]:
    """Execute the expandTask tool.
    
    Args:
        args: Tool parameters
        context: Tool execution context
    
    Returns:
        Tool execution response
    """
    try:
        # Validate parameters
        params = ExpandTaskParams(**args)
        logger.info(f"Expanding task {params.id}")
        
        task_root = Path(params.project_root).joinpath("tasks")
        # Initialize TaskManager with custom tasks directory if file is provided
        task_manager = TaskManager(
            params.file if params.file else task_root
        )
        
        # Expand task with provided options
        await task_manager.expand_task(
            task_id=params.id,
            num_subtasks=params.num or 5,  # Default to 5 subtasks
            use_research=params.research,
            additional_context=params.prompt or ""
        )
        
        return create_content_response(f"Successfully expanded task {params.id}")
        
    except Exception as e:
        logger.error(f"Error expanding task: {e}")
        return create_error_response(f"Error expanding task: {e}")

def register_expand_task_tool(server) -> None:
    """Register the expandTask tool with the MCP server.
    
    Args:
        server: FastMCP server instance
    """
    # Set tool metadata
    execute_expand_task.__name__ = "expandTask"
    execute_expand_task.__doc__ = "Break down a task into detailed subtasks"
    
    # Register tool
    server.add_tool(execute_expand_task)