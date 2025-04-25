#!/usr/bin/env python
"""Interactive REPL for testing MCP client."""

import asyncio
import json
from pathlib import Path
import sys

# Add the project root to the Python path
project_root = str(Path(__file__).parent.parent.absolute())
if project_root not in sys.path:
    sys.path.insert(0, project_root)
    print(f"Added {project_root} to Python path")

from fastmcp import Client, SSETransport

async def main():
    """Run the interactive REPL."""
    print("MCP Client REPL")
    print("Type 'exit' to quit")
    print()
    
    async with Client(SSETransport("http://localhost:8484/api/mcp")) as client:
        while True:
            try:
                # Get command from user
                command = input("> ")
                if command.lower() == 'exit':
                    break
                    
                # Handle special commands
                if command == 'list_tools':
                    tools = await client.list_tools()
                    print(json.dumps(tools, indent=2))
                    continue
                    
                # Try to evaluate the command as Python code
                result = await eval(command)
                print(json.dumps(result, indent=2))
                
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())