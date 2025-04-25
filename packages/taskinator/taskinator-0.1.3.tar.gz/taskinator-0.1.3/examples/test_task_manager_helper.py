#!/usr/bin/env python
"""Test script for the TaskManager helper function."""

import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = str(Path(__file__).parent.parent.absolute())
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# NOTE: This import is commented out because the module doesn't exist in the current codebase.
# This is an example file that needs to be updated to match the current project structure.
# from taskinator.mcp_server.tools.helpers import get_task_manager_for_project
from taskinator.task_manager import TaskManager

def main():
    """Test the TaskManager functionality."""
    print(f"Current working directory: {os.getcwd()}")
    
    try:
        # Create a TaskManager instance directly
        task_manager = TaskManager()
        
        print(f"Tasks file: {task_manager.tasks_file}")
        
        # List all tasks
        tasks = task_manager.list_tasks()
        print(f"Found {len(tasks['tasks'])} tasks")
        
        # Show the next task
        next_task = task_manager.show_next_task()
        if next_task:
            print(f"Next task: {next_task['id']} - {next_task['title']}")
        else:
            print("No next task found")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
