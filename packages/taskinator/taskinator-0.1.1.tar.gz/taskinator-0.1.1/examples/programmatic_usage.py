#!/usr/bin/env python3
"""
Example of using Taskinator as a library with programmatic access.
This demonstrates how to use the TaskManager class directly in your code.
"""

import asyncio
import json
from pathlib import Path

from taskinator.task_manager import TaskManager
from taskinator.config import TaskStatus


async def example_workflow():
    """Demonstrate a complete workflow using Taskinator programmatically."""
    # Create a TaskManager instance with display_output=False to suppress console output
    # This makes it suitable for programmatic use
    task_manager = TaskManager(display_output=False)
    
    # Example 1: Parse a PRD file
    print("Example 1: Parsing a PRD file")
    prd_path = Path("examples/sample_prd.txt")
    if prd_path.exists():
        tasks_data = await task_manager.parse_prd(prd_path, num_tasks=3)
        print(f"Generated {len(tasks_data['tasks'])} tasks")
        
        # Access the tasks data directly
        for task in tasks_data['tasks']:
            print(f"Task {task['id']}: {task['title']} ({task['status']})")
    else:
        print(f"PRD file not found: {prd_path}")
        print("Run 'taskinator init' first to create sample files")
    
    print("\n" + "-" * 50 + "\n")
    
    # Example 2: List tasks and filter by status
    print("Example 2: Listing tasks")
    tasks = task_manager.list_tasks()
    print(f"Total tasks: {len(tasks)}")
    
    # Filter tasks programmatically
    pending_tasks = [t for t in tasks if t['status'] == TaskStatus.PENDING]
    print(f"Pending tasks: {len(pending_tasks)}")
    
    # Or use the built-in filter
    pending_tasks_alt = task_manager.list_tasks(status_filter=TaskStatus.PENDING)
    print(f"Pending tasks (using filter): {len(pending_tasks_alt)}")
    
    print("\n" + "-" * 50 + "\n")
    
    # Example 3: Get task details
    print("Example 3: Getting task details")
    if tasks:
        first_task_id = tasks[0]['id']
        task = task_manager.show_task(first_task_id)
        print(f"Task {task['id']} details:")
        print(f"  Title: {task['title']}")
        print(f"  Status: {task['status']}")
        print(f"  Priority: {task['priority']}")
        print(f"  Dependencies: {task['dependencies']}")
    
    print("\n" + "-" * 50 + "\n")
    
    # Example 4: Update task status
    print("Example 4: Updating task status")
    if tasks:
        first_task_id = tasks[0]['id']
        updated_tasks = await task_manager.set_task_status(first_task_id, TaskStatus.IN_PROGRESS)
        print(f"Updated task {updated_tasks[0]['id']} status to {updated_tasks[0]['status']}")
        
        # Verify the change
        task = task_manager.show_task(first_task_id)
        print(f"Verified status: {task['status']}")
    
    print("\n" + "-" * 50 + "\n")
    
    # Example 5: Expand a task into subtasks
    print("Example 5: Expanding a task into subtasks")
    if tasks:
        first_task_id = tasks[0]['id']
        expanded_task = await task_manager.expand_task(
            first_task_id, 
            num_subtasks=2,
            additional_context="Keep the subtasks simple for this example"
        )
        
        print(f"Expanded task {expanded_task['id']} into {len(expanded_task.get('subtasks', []))} subtasks")
        for subtask in expanded_task.get('subtasks', []):
            print(f"  Subtask {subtask['id']}: {subtask['title']}")
    
    print("\n" + "-" * 50 + "\n")
    
    # Example 6: Finding the next task to work on
    print("\nExample 6: Finding the next task to work on")
    next_task = task_manager.show_next_task()
    if next_task:
        print(f"Next task to work on: {next_task['id']} - {next_task['title']}")
    else:
        print("No eligible tasks found")
    
    print("\n" + "-" * 50 + "\n")
    
    # Example 7: Add a new task
    print("Example 7: Adding a new task")
    new_task = await task_manager.add_task(
        prompt="Create a user authentication system with login and registration",
        dependencies=[],
        priority="high"
    )
    print(f"Added new task {new_task['id']}: {new_task['title']}")
    
    print("\n" + "-" * 50 + "\n")
    
    # Example 8: Custom data processing
    print("Example 8: Custom data processing with task data")
    all_tasks = task_manager.list_tasks()
    
    # Calculate statistics
    status_counts = {}
    priority_counts = {}
    
    for task in all_tasks:
        # Count by status
        status = task['status']
        status_counts[status] = status_counts.get(status, 0) + 1
        
        # Count by priority
        priority = task['priority']
        priority_counts[priority] = priority_counts.get(priority, 0) + 1
    
    print("Task Statistics:")
    print(f"  Status distribution: {json.dumps(status_counts, indent=2)}")
    print(f"  Priority distribution: {json.dumps(priority_counts, indent=2)}")
    
    # Example of more advanced processing
    tasks_with_subtasks = [t for t in all_tasks if t.get('subtasks')]
    avg_subtasks = sum(len(t.get('subtasks', [])) for t in tasks_with_subtasks) / len(tasks_with_subtasks) if tasks_with_subtasks else 0
    
    print(f"  Tasks with subtasks: {len(tasks_with_subtasks)}")
    print(f"  Average subtasks per task: {avg_subtasks:.2f}")


if __name__ == "__main__":
    asyncio.run(example_workflow())
