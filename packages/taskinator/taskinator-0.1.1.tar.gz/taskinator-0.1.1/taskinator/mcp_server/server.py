"""Main MCP server implementation."""

import logging
import importlib.metadata
import sys
from pathlib import Path
from typing import Dict, Optional

from fastmcp import FastMCP

from .tools import register_taskinator_tools

from loguru import logger

class TaskinatorMCPServer:
    """Main MCP server class that integrates with Taskinator."""
    
    def __init__(self, host: str = "localhost", port: int = 8484, token: Optional[str] = None):
        """Initialize the MCP server.
        
        Args:
            host: The hostname to bind to
            port: The port to bind to
            token: Optional authentication token
        """
        logger.debug(f"Initializing MCP server on {host}:{port}")
        
        # Create FastMCP server
        self.server = FastMCP(
            host=host,
            port=port,
            token=token,
            name="Taskinator MCP",
            description="Model Context Protocol server for Taskinator",
            version=importlib.metadata.version("taskinator"),
            log_level="DEBUG",
            endpoint="/sse"
        )
        
        # Register tools
        self._register_tools()
    
    def _register_tools(self):
        """Register all Taskinator tools with the server."""
        logger.debug("Registering Taskinator tools")
        register_taskinator_tools(self.server)
        logger.debug("Server initialization complete")

    async def list_tools(self):
        """Get all registered tools."""
        return await self.server.list_tools()

    def run(self):
        """Run the server."""
        logger.info("Starting Taskinator MCP server...")
        # Run with SSE transport
        self.server.run(
            transport="sse"
        )

    async def run_async(self):
        """Run the server asynchronously."""
        logger.info("Starting Taskinator MCP server...")
        await self.server.run_async(transport="sse")