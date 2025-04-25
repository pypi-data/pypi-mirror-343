#!/usr/bin/env python
"""Example script to test the Taskinator MCP server."""

import json
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = str(Path(__file__).parent.parent.absolute())
if project_root not in sys.path:
    sys.path.insert(0, project_root)
    print(f"Added {project_root} to Python path")

from typing import Any, Dict
from loguru import logger

def send_command(command: Dict[str, Any]) -> Dict[str, Any]:
    """Send a command to the MCP server.
    
    Args:
        command: Command to send
        
    Returns:
        Server response
    """
    # Send command as JSON
    #print(json.dumps(command))
    logger.debug(f"Sent command: {command}")
    print(json.dumps(command))
    sys.stdout.flush()
    
    # Read response
    response = input()
    return json.loads(response)

def main():
    """Run example MCP commands."""
    # Example 1: List all tasks
    print("\nListing all tasks...")
    response = send_command({
        "tool": "listTasks",
        "parameters": {
            "project_root": ".",
            "status": None,
            "with_subtasks": False
        }
    })
    print(json.dumps(response, indent=2))
    
    # Example 2: Add a new task
    print("\nAdding a new task...")
    response = send_command({
        "tool": "addTask",
        "parameters": {
            "project_root": ".",
            "prompt": "Implement user authentication system",
            "priority": "high"
        }
    })
    print(json.dumps(response, indent=2))
    
    # Example 3: Show task details
    print("\nShowing task details...")
    response = send_command({
        "tool": "showTask",
        "parameters": {
            "project_root": ".",
            "id": "1"
        }
    })
    print(json.dumps(response, indent=2))
    
    # Example 4: Find next task
    print("\nFinding next task...")
    response = send_command({
        "tool": "nextTask",
        "parameters": {
            "project_root": "."
        }
    })
    print(json.dumps(response, indent=2))

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nTest client stopped.")
    except Exception as e:
        print(f"\nError: {e}")