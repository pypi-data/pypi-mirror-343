"""Main MCP server implementation."""

import logging
import importlib.metadata
import sys
from pathlib import Path
from typing import Dict, Optional, List

from fastmcp import FastMCP
from fastmcp.tools.tool import Tool
from pydantic_settings import BaseSettings, SettingsConfigDict

from loguru import logger

# Configure loguru to write to stderr
logger.remove()
logger.add(sys.stderr, level="DEBUG")

class MCPServerConfig(BaseSettings):
    """MCP Server configuration."""
    host: str = "localhost"
    port: int = 8484
    transport: str = "stdio"  # Changed from stdin to stdio
    token: Optional[str] = None
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"  # Ignore extra fields from .env
    )

# Import tool registration function
from .tools import register_taskinator_tools

class TaskinatorMCPServer:
    """Main MCP server class that integrates with Taskinator."""
    
    def __init__(self, config: Optional[MCPServerConfig] = None):
        """Initialize the MCP server.
        
        Args:
            config: Server configuration. If not provided, loads from environment.
        """
        self.config = config or MCPServerConfig()
        logger.debug(f"Initializing MCP server with {self.config.transport} transport")
        
        # Create FastMCP server
        self.server = FastMCP(
            host=self.config.host,  # Always provide host
            port=self.config.port,  # Always provide port
            token=self.config.token,
            name="Taskinator MCP",
            description="Model Context Protocol server for Taskinator",
            version=importlib.metadata.version("taskinator"),
            log_level="DEBUG"
        )
        
        # Register Taskinator tools
        self._register_tools()
    
    def _register_tools(self):
        """Register Taskinator tools with the server."""
        logger.debug("Registering Taskinator tools")
        register_taskinator_tools(self.server)
        logger.debug("Server initialization complete")

    async def list_tools(self) -> List[Tool]:
        """Get all registered tools."""
        return await self.server.list_tools()

    def run(self):
        """Run the server."""
        logger.info(f"Starting Taskinator MCP server with {self.config.transport} transport...")
        try:
            self.server.run(transport=self.config.transport)
        except Exception as e:
            logger.error(f"Server failed: {e}")
            raise

    async def run_async(self):
        """Run the server asynchronously."""
        logger.info(f"Starting Taskinator MCP server with {self.config.transport} transport...")
        try:
            await self.server.run_async(transport=self.config.transport)
        except Exception as e:
            logger.error(f"Server failed: {e}")
            raise

def main():
    """Main entry point for the MCP server."""
    try:
        # Load config from environment
        config = MCPServerConfig()
        
        # Force stdio transport for CLI usage
        config.transport = "stdio"
        
        # Initialize and run server
        server = TaskinatorMCPServer(config=config)
        server.run()
    except Exception as e:
        logger.error(f"Failed to start MCP server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()