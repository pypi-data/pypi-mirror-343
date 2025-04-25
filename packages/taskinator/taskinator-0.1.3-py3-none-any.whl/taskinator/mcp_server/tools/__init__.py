"""Taskinator MCP tools."""

from loguru import logger

from .list_tasks import register_list_tasks_tool
from .show_task import register_show_task_tool
from .set_task_status import register_set_task_status_tool
from .expand_task import register_expand_task_tool
from .next_task import register_next_task_tool
from .add_task import register_add_task_tool

def register_taskinator_tools(server) -> None:
    """Register all Taskinator tools with the MCP server.
    
    Args:
        server: FastMCP server instance
    """
    logger.debug("Registering Taskinator tools")
    register_list_tasks_tool(server)
    register_show_task_tool(server)
    register_set_task_status_tool(server)
    register_expand_task_tool(server)
    register_next_task_tool(server)
    register_add_task_tool(server)
    logger.debug("All tools registered")