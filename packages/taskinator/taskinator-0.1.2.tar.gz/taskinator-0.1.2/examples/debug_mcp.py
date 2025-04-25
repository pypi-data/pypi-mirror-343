#!/usr/bin/env python
"""Debug script for the MCP server."""

import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = str(Path(__file__).parent.parent.absolute())
if project_root not in sys.path:
    sys.path.insert(0, project_root)
    print(f"Added {project_root} to Python path")

from taskinator.task_manager import TaskManager
from taskinator.config import config

def main():
    """Debug the TaskManager and MCP server."""
    print(f"Current working directory: {os.getcwd()}")
    print(f"Default tasks directory from config: {config.tasks_dir}")
    
    # Try to initialize the TaskManager with different paths
    try:
        # Default initialization
        print("\nTrying default initialization...")
        task_manager = TaskManager(display_output=False)
        print(f"TaskManager tasks_dir: {task_manager.tasks_dir}")
        print(f"TaskManager tasks_file: {task_manager.tasks_file}")
        print(f"tasks_file exists: {os.path.exists(task_manager.tasks_file)}")
    except Exception as e:
        print(f"Error with default initialization: {e}")
    
    try:
        # Absolute path to tasks directory
        tasks_dir = os.path.join(project_root, "tasks")
        print(f"\nTrying with absolute path to tasks directory: {tasks_dir}")
        task_manager = TaskManager(tasks_dir=tasks_dir, display_output=False)
        print(f"TaskManager tasks_dir: {task_manager.tasks_dir}")
        print(f"TaskManager tasks_file: {task_manager.tasks_file}")
        print(f"tasks_file exists: {os.path.exists(task_manager.tasks_file)}")
    except Exception as e:
        print(f"Error with absolute path: {e}")
    
    try:
        # Change working directory to project root
        print("\nTrying with changed working directory...")
        original_cwd = os.getcwd()
        os.chdir(project_root)
        print(f"New working directory: {os.getcwd()}")
        task_manager = TaskManager(display_output=False)
        print(f"TaskManager tasks_dir: {task_manager.tasks_dir}")
        print(f"TaskManager tasks_file: {task_manager.tasks_file}")
        print(f"tasks_file exists: {os.path.exists(task_manager.tasks_file)}")
        os.chdir(original_cwd)
    except Exception as e:
        print(f"Error with changed working directory: {e}")
        os.chdir(original_cwd)
    
    # Try to list tasks from the CLI
    print("\nTrying to run CLI command...")
    try:
        import subprocess
        result = subprocess.run(["taskinator", "list"],
                               cwd=project_root,
                               capture_output=True, 
                               text=True)
        print(f"CLI command exit code: {result.returncode}")
        print(f"CLI command output:\n{result.stdout}")
        if result.stderr:
            print(f"CLI command error:\n{result.stderr}")
    except Exception as e:
        print(f"Error running CLI command: {e}")

if __name__ == "__main__":
    main()
