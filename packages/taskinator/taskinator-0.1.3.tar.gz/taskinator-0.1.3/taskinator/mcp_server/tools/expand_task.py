"""Tool to break down a task into detailed subtasks."""


import os
from typing import Optional, Dict, Any
from pathlib import Path

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

async def execute_expand_task(id: str,
                            num: Optional[int] = 5,
                            research: Optional[bool] = False,
                            prompt: Optional[str] = None,
                            force: Optional[bool] = False,
                            file: Optional[str] = None,
                            project_root: str = str(Path.cwd())) -> Dict[str, Any]:
    """Execute the expandTask tool.
    
    Args:
        id: Task ID to expand
        num: Number of subtasks to generate (default: 5)
        research: Enable Perplexity AI for research-backed subtask generation
        prompt: Additional context to guide subtask generation
        force: Force expansion even if subtasks already exist
        file: Optional path to tasks file
        project_root: Project root directory
    
    Returns:
        Tool execution response
    """
    try:
        # Create params object
        params = ExpandTaskParams(
            id=id,
            num=num,
            research=research,
            prompt=prompt,
            force=force,
            file=file,
            project_root=project_root
        )
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
    # Register using decorator
    server.tool("expandTask")(execute_expand_task)