"""Taskinator MCP tools."""

from loguru import logger

def register_taskinator_tools(server) -> None:
    """Register all Taskinator tools with the MCP server.
    
    Args:
        server: FastMCP server instance
    """
    @server.tool("echo")
    async def echo_tool(text: str) -> str:
        """Simple echo tool for testing."""
        logger.debug(f"Echo tool called with: {text}")
        return f"Echo: {text}"

    logger.debug("Registered echo tool")