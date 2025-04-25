#!/usr/bin/env python3
"""Test script for reintegrating a single task file."""

import asyncio
import json
import os
import shutil
import sys
from pathlib import Path

from taskinator.task_manager import TaskManager
from loguru import logger

async def main():
    """Main function to test task reintegration."""
    # Setup test environment
    test_dir = Path("test_tasks")
    test_dir.mkdir(exist_ok=True)
    
    # Copy the test task file to the test directory
    test_task_file = Path("test_task.txt")
    if not test_task_file.exists():
        logger.error(f"Test task file not found: {test_task_file}")
        return
    
    shutil.copy(test_task_file, test_dir / "task_011.txt")
    
    # Create a minimal tasks.json file
    tasks_json = {
        "tasks": [
            {
                "id": 11,
                "title": "Develop NLP similarity detection for Process Intelligence Engine",
                "status": "in_progress",
                "priority": "high",
                "dependencies": [],
                "description": "Implement NLP-based similarity detection for comparing process steps",
                "details": "Develop a system that can detect semantic similarity between process steps in different SOPs and PDDs. This will be used to identify redundant or similar processes across the organization.",
                "subtasks": [
                    {
                        "id": 1,
                        "title": "Research and select NLP libraries and embedding models",
                        "status": "pending",
                        "priority": "high",
                        "description": "Evaluate and select appropriate NLP libraries and embedding models for semantic similarity detection",
                        "details": "Research and evaluate different NLP libraries and embedding models for semantic similarity detection. Consider factors such as accuracy, performance, ease of integration, and licensing.",
                        "research": {
                            "summary": "Research completed successfully.",
                            "key_findings": "Original research findings",
                            "implementation_recommendations": "Original recommendations",
                            "resources": "Original resources",
                            "sources": "Original sources"
                        }
                    },
                    {
                        "id": 2,
                        "title": "Define similarity metrics and thresholds for process steps",
                        "status": "pending",
                        "priority": "medium",
                        "dependencies": [1],
                        "description": "Define appropriate similarity metrics and thresholds for determining when process steps are similar"
                    }
                ]
            }
        ]
    }
    
    with open(test_dir / "tasks.json", "w") as f:
        json.dump(tasks_json, f, indent=2)
    
    # Create a task manager for the test directory
    task_manager = TaskManager(tasks_dir=str(test_dir))
    
    # Reintegrate the task file
    logger.info("Reintegrating test task file")
    result = await task_manager.reintegrate_task_files(task_dir=str(test_dir))
    
    logger.info(f"Reintegration result: {result}")
    
    # Check if the tasks.json file was updated
    with open(test_dir / "tasks.json", "r") as f:
        updated_tasks = json.load(f)
    
    # Print the updated research data
    task = next((t for t in updated_tasks.get("tasks", []) if t.get("id") == 11), None)
    if task:
        subtask = next((s for s in task.get("subtasks", []) if s.get("id") == 1), None)
        if subtask and "research" in subtask:
            logger.info("Updated research data:")
            logger.info(f"Summary: {subtask['research'].get('summary', '')}")
            logger.info(f"Key findings first 100 chars: {subtask['research'].get('key_findings', '')[:100]}...")
        else:
            logger.error("No research data found in subtask")
    else:
        logger.error("Task not found in updated tasks.json")

if __name__ == "__main__":
    asyncio.run(main())
