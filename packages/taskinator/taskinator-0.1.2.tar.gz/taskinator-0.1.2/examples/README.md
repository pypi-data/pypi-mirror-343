# Taskinator MCP Server Examples

This directory contains examples showing how to use the Taskinator MCP server.

## Prerequisites

1. Install Taskinator:
```bash
pip install taskinator
```

2. Configure AI Services:
The Taskinator MCP server requires access to Claude AI for certain operations. You can configure this in one of two ways:

a. Direct Claude API access:
```bash
export ANTHROPIC_API_KEY=your_api_key_here
```

b. AWS Bedrock access:
```bash
export USE_BEDROCK=true
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_REGION=your_region  # default: us-east-1
```

You can also create a `.env` file with these settings.

## Running the MCP Server

Run the server:
```bash
python run_mcp_server.py
```

The server will start in stdio mode, ready to accept MCP commands.

## Testing with MCP Tools

You can test the MCP server using any MCP client. Here are some example commands you can send:

### List Tasks
```json
{
    "tool": "listTasks",
    "parameters": {
        "project_root": ".",
        "status": null,
        "with_subtasks": false
    }
}
```

### Show Task Details
```json
{
    "tool": "showTask",
    "parameters": {
        "project_root": ".",
        "id": "1"
    }
}
```

### Set Task Status
```json
{
    "tool": "setTaskStatus",
    "parameters": {
        "project_root": ".",
        "id": "1",
        "status": "in_progress"
    }
}
```

### Expand Task
```json
{
    "tool": "expandTask",
    "parameters": {
        "project_root": ".",
        "id": "1",
        "num": 5,
        "research": false,
        "prompt": "Additional context for subtask generation"
    }
}
```

### Find Next Task
```json
{
    "tool": "nextTask",
    "parameters": {
        "project_root": "."
    }
}
```

### Add New Task
```json
{
    "tool": "addTask",
    "parameters": {
        "project_root": ".",
        "prompt": "Implement user authentication system",
        "dependencies": "1,2",
        "priority": "high"
    }
}
```

## Response Format

The server will respond with JSON messages in this format:

### Success Response
```json
{
    "success": true,
    "content": "Operation result or message"
}
```

### Error Response
```json
{
    "success": false,
    "error": {
        "message": "Error description",
        "details": {} // Optional additional error details
    }
}
```

## Testing Tips

1. Each command should be sent as a single line of JSON
2. The server expects stdio communication, so each command should end with a newline
3. You can use tools like `netcat` or write a simple Python script to send commands
4. All paths are relative to the project_root parameter
5. The server will maintain state between commands
6. Use Ctrl+C to gracefully shut down the server

## Example Python Client

Here's a simple Python script to test the MCP server:

```python
import json
import sys

def send_command(command):
    """Send a command to the MCP server."""
    print(json.dumps(command))
    sys.stdout.flush()
    response = input()
    return json.loads(response)

# Example: List all tasks
command = {
    "tool": "listTasks",
    "parameters": {
        "project_root": ".",
        "status": None,
        "with_subtasks": False
    }
}

response = send_command(command)
print(json.dumps(response, indent=2))
```

Save this as `test_mcp.py` and run it in a separate terminal while the MCP server is running.

## Troubleshooting

1. If you see a warning about "No Claude AI service is available", make sure you've set up either:
   - ANTHROPIC_API_KEY for direct Claude access, or
   - USE_BEDROCK=true with AWS credentials for Bedrock access

2. If tools fail with "Invalid parameters", check that your JSON command matches the expected format and parameter types

3. For detailed error messages, check the server's log output