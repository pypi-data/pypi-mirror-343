"""Taskinator MCP tools."""

from loguru import logger

from .list_tasks import register_list_tasks_tool
from .show_task import register_show_task_tool
from .set_task_status import register_set_task_status_tool
from .expand_task import register_expand_task_tool
from .next_task import register_next_task_tool
from .add_task import register_add_task_tool

from .list_tasks import execute_list_tasks
from .show_task import execute_show_task
from .set_task_status import execute_set_task_status
from .expand_task import execute_expand_task
from .next_task import execute_next_task
from .add_task import execute_add_task

def register_taskinator_tools(server) -> None:
    """Register all Taskinator tools with the MCP server.
    
    Args:
        server: FastMCP server instance
    """
    logger.debug("Registering listTasks tool")
    server.add_tool(execute_list_tasks)
    logger.debug("Registering showTask tool")
    server.add_tool(execute_show_task)
    logger.debug("Registering setTaskStatus tool")
    server.add_tool(execute_set_task_status)
    logger.debug("Registering expandTask tool")
    server.add_tool(execute_expand_task)
    logger.debug("Registering nextTask tool")
    server.add_tool(execute_next_task)
    logger.debug("Registering addTask tool")
    server.add_tool(execute_add_task)

__all__ = [
    'register_taskinator_tools',
    'register_list_tasks_tool',
    'register_show_task_tool',
    'register_set_task_status_tool',
    'register_expand_task_tool',
    'register_next_task_tool',
    'register_add_task_tool'
]