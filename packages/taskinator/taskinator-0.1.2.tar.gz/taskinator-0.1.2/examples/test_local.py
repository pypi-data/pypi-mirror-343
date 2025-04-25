#!/usr/bin/env python
"""Test script that runs both the MCP client and server in a single process."""

import asyncio
import json
import os
import sys
from pathlib import Path
import threading
import queue
import time

# Add the project root to the Python path
project_root = str(Path(__file__).parent.parent.absolute())
if project_root not in sys.path:
    sys.path.insert(0, project_root)
    print(f"Added {project_root} to Python path")

from loguru import logger
from dotenv import load_dotenv

load_dotenv()

from taskinator.mcp_server import TaskinatorMCPServer

# Set up logging
LOG_LEVEL = os.getenv('LOG_LEVEL', "INFO").upper()
logger.add(sys.stderr, format="{time} {level} {message}", level=LOG_LEVEL)

# Create queues for communication between client and server
client_to_server = queue.Queue()
server_to_client = queue.Queue()

# Flag to control server shutdown
server_running = True

def run_server():
    """Run the MCP server in a separate thread."""
    # Create server
    server = TaskinatorMCPServer()
    
    # Override the server's input/output methods to use our queues
    def custom_read():
        try:
            message = client_to_server.get(timeout=0.1)
            if message:
                logger.debug(f"Server received: {message}")
            return message
        except queue.Empty:
            return None

    def custom_write(message):
        logger.debug(f"Server sending: {message}")
        server_to_client.put(message)
    
    # Create event loop for this thread
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    # Patch the server's read/write methods
    server.server._read_message = custom_read
    server.server._write_message = custom_write
    
    # Run the server with message processing loop
    try:
        logger.info("Starting Taskinator MCP server...")
        while server_running:
            try:
                # Process any pending messages
                message = custom_read()
                if message:
                    try:
                        # Parse the message
                        data = json.loads(message)
                        tool_name = data.get('tool')
                        params = data.get('parameters', {})
                        
                        # Get all tools from the server
                        tools = loop.run_until_complete(server.get_tools())
                        
                        # Execute the tool if found
                        if tool_name in tools:
                            tool_func = tools[tool_name]
                            result = loop.run_until_complete(tool_func(params, {}))
                            custom_write(json.dumps(result))
                        else:
                            custom_write(json.dumps({
                                "error": f"Tool not found: {tool_name}"
                            }))
                        if result:
                            custom_write(json.dumps(result))
                    except Exception as e:
                        logger.error(f"Error processing message: {e}")
                        custom_write(json.dumps({
                            "error": f"Error processing message: {str(e)}"
                        }))
                
                # Small delay to prevent busy waiting
                time.sleep(0.01)
            except Exception as e:
                logger.error(f"Error in message processing loop: {e}")
                if server_running:  # Only log error if we're not shutting down
                    logger.error(f"Error in message processing loop: {e}")
                break
    except Exception as e:
        logger.error(f"Server error: {e}")

def send_command(command):
    """Send a command to the MCP server and get the response."""
    logger.debug(f"Client sending: {command}")
    client_to_server.put(json.dumps(command))
    
    # Wait for response with timeout
    start_time = time.time()
    while time.time() - start_time < 5:  # 5 second timeout
        try:
            response = server_to_client.get(timeout=0.1)
            logger.debug(f"Client received: {response}")
            return json.loads(response)
        except queue.Empty:
            continue
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding response: {e}")
            return {"error": f"Invalid JSON response: {response}"}
    
    return {"error": "Timeout waiting for server response"}

def main():
    """Run example MCP commands."""
    global server_running
    
    try:
        # Start the server in a separate thread
        server_thread = threading.Thread(target=run_server)
        server_thread.start()
        
        # Give the server a moment to initialize and set up message processing
        time.sleep(2)
        
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
        
        # Example 2: Find next task
        print("\nFinding next task...")
        response = send_command({
            "tool": "nextTask",
            "parameters": {
                "project_root": "."
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
    finally:
        server_running = False


def cleanup():
    """Clean up resources and shutdown server."""
    global server_running
    server_running = False
    
    # Clear the queues
    while not client_to_server.empty():
        client_to_server.get()
    while not server_to_client.empty():
        server_to_client.get()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nTest client stopped.")
    except Exception as e:
        print(f"\nError: {e}")
    finally:
        cleanup()
