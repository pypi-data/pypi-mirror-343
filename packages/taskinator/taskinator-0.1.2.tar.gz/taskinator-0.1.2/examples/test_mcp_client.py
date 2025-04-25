#!/usr/bin/env python
"""Simple test client for the Taskinator MCP server."""

import asyncio
import json
import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = str(Path(__file__).parent.parent.absolute())
if project_root not in sys.path:
    sys.path.insert(0, project_root)
    print(f"Added {project_root} to Python path")

from loguru import logger

# Set up logging
LOG_LEVEL = os.getenv('LOG_LEVEL', "INFO").upper()
logger.add(sys.stderr, format="{time} {level} {message}", level=LOG_LEVEL)

async def send_command(command):
    """Send a command to the MCP server and get the response."""
    logger.debug(f"Sending command: {command}")
    
    # Format the message according to MCP protocol
    message = {
        "type": "tool",
        "name": command["tool"],
        "parameters": command["parameters"]
    }
    
    # Send HTTP POST request to the server
    import aiohttp
    async with aiohttp.ClientSession() as session:
        async with session.post('http://localhost:8484/api/mcp', json=message) as resp:
            response = await resp.json()
            logger.debug(f"Received response: {response}")
            return response

async def main():
    """Run test commands."""
    try:
        # Example 1: List all tasks
        print("\nListing all tasks...")
        response = await send_command({
            "tool": "listTasks",
            "parameters": {
                "project_root": ".",
                "status": None,
                "with_subtasks": False
            }
        })
        print(json.dumps(response, indent=2))
        
        # Example 2: Find next task
        print("\nFinding next task...")
        response = await send_command({
            "tool": "nextTask",
            "parameters": {
                "project_root": "."
            }
        })
        print(json.dumps(response, indent=2))

        # Example 3: Show task details
        print("\nShowing task details...")
        response = await send_command({
            "tool": "showTask",
            "parameters": {
                "project_root": ".",
                "id": "1"
            }
        })
        print(json.dumps(response, indent=2))
        
    except Exception as e:
        logger.error(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())