#!/usr/bin/env python
"""Example script to run the Taskinator MCP server."""

import logging
import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = str(Path(__file__).parent.parent.absolute())
if project_root not in sys.path:
    sys.path.insert(0, project_root)
    print(f"Added {project_root} to Python path")

import loguru
from dotenv import load_dotenv

load_dotenv()

# Now import the TaskinatorMCPServer
from taskinator.mcp_server import TaskinatorMCPServer

# Set up logging
LOG_LEVEL = os.getenv('LOG_LEVEL', "INFO").upper()
print(f"LOG_LEVEL: {LOG_LEVEL}")
from loguru import logger
logger.add(sys.stderr, format="{time} {level} {message}", level=LOG_LEVEL)

# Create the TaskinatorMCPServer and expose the server object for FastMCP CLI
taskinator_server = TaskinatorMCPServer()
server = taskinator_server.server

def main():
    """Run the MCP server."""
    # Check for required environment variables
    if not (os.getenv('ANTHROPIC_API_KEY', False) or os.getenv('USE_BEDROCK', False)):
        logger.warning(
            "No Claude AI service configured. Some features will be limited.\n"
            "To enable all features, configure either:\n"
            "1. ANTHROPIC_API_KEY for direct Claude access, or\n"
            "2. USE_BEDROCK=true with AWS credentials for Bedrock access"
        )
    
    try:
        # Start the server with stdio transport
        logger.info("Starting Taskinator MCP server (stdio mode)...")
        taskinator_server.server.run(transport="stdio")
        
    except KeyboardInterrupt:
        # Handle graceful shutdown on Ctrl+C
        logger.info("Shutting down server...")
    except Exception as e:
        logger.error(f"Server error: {e}")
        raise

if __name__ == "__main__":
    main()