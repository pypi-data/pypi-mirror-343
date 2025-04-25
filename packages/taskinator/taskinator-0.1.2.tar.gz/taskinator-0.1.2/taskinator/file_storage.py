"""File Storage Manager for Taskinator.

This module provides a comprehensive file storage system for Taskinator tasks,
handling both JSON and individual text files with proper synchronization.
"""

import asyncio
import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union

from loguru import logger

from .utils import read_json, write_json, find_task_by_id
from .config import TaskStatus, TaskPriority


class FileStorageError(Exception):
    """Base exception for file storage errors."""
    pass


class TaskFileNotFoundError(FileStorageError):
    """Exception raised when a task file is not found."""
    pass


class TaskFileParseError(FileStorageError):
    """Exception raised when a task file cannot be parsed."""
    pass


class TaskFileWriteError(FileStorageError):
    """Exception raised when a task file cannot be written."""
    pass


class TaskFileLockError(FileStorageError):
    """Exception raised when a task file cannot be locked."""
    pass


class FileLock:
    """Simple file-based lock for task file operations."""
    
    def __init__(self, lock_file: Path, timeout: float = 5.0, retry_interval: float = 0.1):
        """Initialize the file lock.
        
        Args:
            lock_file: Path to the lock file
            timeout: Maximum time to wait for the lock (seconds)
            retry_interval: Time between retry attempts (seconds)
        """
        self.lock_file = lock_file
        self.timeout = timeout
        self.retry_interval = retry_interval
        self._locked = False
        
        # Ensure the lock directory exists
        self.lock_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Force remove any existing lock file at initialization time
        if self.lock_file.exists():
            try:
                logger.warning(f"Removing existing lock file at initialization: {self.lock_file}")
                self.lock_file.unlink()
            except Exception as e:
                logger.warning(f"Error removing existing lock file: {e}")
    
    async def __aenter__(self):
        """Acquire the lock."""
        start_time = datetime.now()
        
        # Check if the lock file is stale (older than 30 seconds)
        if self.lock_file.exists():
            try:
                file_age = datetime.now().timestamp() - self.lock_file.stat().st_mtime
                if file_age > 30:  # If lock is older than 30 seconds, consider it stale
                    logger.warning(f"Removing stale lock file: {self.lock_file} (age: {file_age:.1f}s)")
                    self.lock_file.unlink()
            except Exception as e:
                logger.warning(f"Error checking lock file age: {e}")
        
        while True:
            try:
                # Try to create the lock file
                with open(self.lock_file, 'x') as f:
                    # Write the current process ID to the lock file
                    f.write(str(os.getpid()))
                self._locked = True
                return self
            except FileExistsError:
                # Check if we've exceeded the timeout
                elapsed = (datetime.now() - start_time).total_seconds()
                if elapsed > self.timeout:
                    raise TaskFileLockError(f"Could not acquire lock on {self.lock_file} after {self.timeout} seconds")
                
                # Wait and retry
                await asyncio.sleep(self.retry_interval)
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Release the lock."""
        if self._locked and self.lock_file.exists():
            try:
                self.lock_file.unlink()
                self._locked = False
            except Exception as e:
                logger.error(f"Error releasing lock on {self.lock_file}: {e}")


class FileStorageManager:
    """Manager for task file storage operations.
    
    This class handles reading and writing tasks to both JSON and individual text files,
    ensuring consistency between the two formats.
    """
    
    def __init__(self, tasks_dir: Path = None, display_output: bool = True, lock_timeout: float = 5.0):
        """Initialize the FileStorageManager.
        
        Args:
            tasks_dir: Directory containing task files
            display_output: Whether to display output messages
            lock_timeout: Timeout for file locks (seconds)
        """
        self.tasks_dir = Path(tasks_dir) if tasks_dir else Path("tasks")
        self.tasks_file = self.tasks_dir / "tasks.json"
        self.locks_dir = self.tasks_dir / ".locks"
        self.display_output = display_output
        self.lock_timeout = lock_timeout
        
        # Create directories if they don't exist
        self.tasks_dir.mkdir(parents=True, exist_ok=True)
        self.locks_dir.mkdir(parents=True, exist_ok=True)
        
        # Create empty tasks file if it doesn't exist
        if not self.tasks_file.exists():
            self._create_empty_tasks_file()
    
    def _create_empty_tasks_file(self):
        """Create an empty tasks file."""
        empty_tasks = {"tasks": []}
        with open(self.tasks_file, "w") as f:
            json.dump(empty_tasks, f, indent=2)
    
    async def read_tasks(self) -> Dict[str, Any]:
        """Read tasks from the JSON file.
        
        Returns:
            Dictionary containing tasks data
        
        Raises:
            FileStorageError: If the file cannot be read
        """
        try:
            return read_json(self.tasks_file)
        except Exception as e:
            logger.error(f"Error reading tasks file: {e}")
            raise FileStorageError(f"Could not read tasks file: {e}")
    
    async def write_tasks(self, data: Dict[str, Any]) -> None:
        """Write tasks to the JSON file.
        
        Args:
            data: Dictionary containing tasks data
        
        Raises:
            FileStorageError: If the file cannot be written
        """
        try:
            write_json(self.tasks_file, data)
        except Exception as e:
            logger.error(f"Error writing tasks file: {e}")
            raise FileStorageError(f"Could not write tasks file: {e}")
    
    async def read_task_file(self, task_id: Union[str, int]) -> Optional[Dict[str, Any]]:
        """Read a specific task file and return the task data.
        
        Args:
            task_id: ID of the task to read
            
        Returns:
            Dictionary containing the task data, or None if the file doesn't exist
            
        Raises:
            TaskFileNotFoundError: If the task file doesn't exist
            TaskFileParseError: If the task file cannot be parsed
        """
        task_id = str(task_id)
        task_file = self.tasks_dir / f"task_{task_id.zfill(3)}.txt"
        
        if not task_file.exists():
            raise TaskFileNotFoundError(f"Task file not found: {task_file}")
        
        try:
            # Acquire a lock for reading
            async with FileLock(self.locks_dir / f"task_{task_id}.lock", timeout=self.lock_timeout):
                # Read the task file
                content = task_file.read_text(encoding='utf-8')
                
                # Parse the task file
                return self._parse_task_file_content(content)
        except TaskFileParseError:
            raise
        except Exception as e:
            logger.error(f"Error reading task file {task_file}: {e}")
            raise TaskFileParseError(f"Could not parse task file {task_file}: {e}")
    
    async def write_task_file(self, task: Dict[str, Any], all_tasks: List[Dict[str, Any]]) -> Path:
        """Write a specific task to its individual text file.
        
        Args:
            task: Dictionary containing the task data
            all_tasks: List of all tasks (for resolving dependencies)
            
        Returns:
            Path to the written task file
            
        Raises:
            TaskFileWriteError: If the task file cannot be written
        """
        task_id = str(task.get('id', ''))
        if not task_id:
            raise TaskFileWriteError("Task ID is required")
        
        task_file = self.tasks_dir / f"task_{task_id.zfill(3)}.txt"
        
        try:
            # Acquire a lock for writing
            async with FileLock(self.locks_dir / f"task_{task_id}.lock", timeout=self.lock_timeout):
                # Format the task content
                content = self._format_task_file_content(task, all_tasks)
                
                # Write the task file
                task_file.write_text(content, encoding='utf-8')
                
                return task_file
        except Exception as e:
            logger.error(f"Error writing task file {task_file}: {e}")
            raise TaskFileWriteError(f"Could not write task file {task_file}: {e}")
    
    async def reintegrate_task_files(self) -> Dict[str, Any]:
        """Reintegrate content from individual task files back into the tasks.json file.
        
        Returns:
            Dictionary containing statistics about the reintegration process
        
        Raises:
            FileStorageError: If the reintegration fails
        """
        try:
            # Read the current tasks data
            tasks_data = await self.read_tasks()
            
            if "tasks" not in tasks_data:
                tasks_data["tasks"] = []
            
            # Get all task files
            task_files = list(self.tasks_dir.glob("task_*.txt"))
            
            # Track statistics
            processed_files = []
            updated_tasks = []
            
            # Process each task file
            for task_file in task_files:
                try:
                    # Extract task ID from filename
                    task_id_match = re.search(r'task_(\d+)\.txt', task_file.name)
                    if not task_id_match:
                        continue
                    
                    task_id = int(task_id_match.group(1))
                    processed_files.append(task_file)
                    
                    # Find the task in the tasks data
                    task = find_task_by_id(tasks_data["tasks"], task_id)
                    if not task:
                        logger.warning(f"Task {task_id} not found in tasks.json, skipping")
                        continue
                    
                    # Read the task file content
                    content = task_file.read_text(encoding='utf-8')
                    
                    # Parse the task file content
                    updated_task = self._parse_task_file_content(content, task)
                    if updated_task:
                        # Update the task in the tasks data
                        for i, t in enumerate(tasks_data["tasks"]):
                            if t["id"] == task_id:
                                tasks_data["tasks"][i].update(updated_task)
                                updated_tasks.append(task_id)
                                break
                
                except Exception as e:
                    logger.error(f"Error processing task file {task_file}: {e}")
            
            # Write the updated tasks data back to the JSON file
            if updated_tasks:
                await self.write_tasks(tasks_data)
            
            # Return statistics
            return {
                "processed_files": processed_files,
                "updated_tasks": updated_tasks
            }
            
        except Exception as e:
            logger.error(f"Error reintegrating task files: {e}")
            raise FileStorageError(f"Could not reintegrate task files: {e}")
    
    async def ensure_consistency(self) -> Dict[str, List[str]]:
        """Ensure consistency between JSON data and individual text files.
        
        Returns:
            Dictionary with lists of added, modified, and deleted task files
            
        Raises:
            FileStorageError: If consistency cannot be ensured
        """
        try:
            # Acquire a lock for reading and writing
            async with FileLock(self.locks_dir / "tasks.json.lock", timeout=self.lock_timeout):
                # Read the current tasks data
                tasks_data = await self.read_tasks()
                
                # Get all task files
                task_files = {f.name: f for f in self.tasks_dir.glob("task_*.txt")}
                
                # Track changes
                changes = {
                    "added": [],
                    "modified": [],
                    "deleted": []
                }
                
                # Check for missing or modified task files
                for task in tasks_data.get("tasks", []):
                    task_id = str(task.get("id", ""))
                    if not task_id:
                        continue
                    
                    task_filename = f"task_{task_id.zfill(3)}.txt"
                    
                    if task_filename not in task_files:
                        # Task file is missing, create it
                        await self.write_task_file(task, tasks_data["tasks"])
                        changes["added"].append(task_filename)
                    else:
                        # Task file exists, check if it's up to date
                        task_file = task_files[task_filename]
                        content = task_file.read_text(encoding='utf-8')
                        parsed_task = self._parse_task_file_content(content, task)
                        
                        # Compare the parsed task with the JSON task
                        if self._tasks_differ(parsed_task, task):
                            # Task file is outdated, update it
                            await self.write_task_file(task, tasks_data["tasks"])
                            changes["modified"].append(task_filename)
                        
                        # Remove the task file from the dict to track processed files
                        del task_files[task_filename]
                
                # Check for task files that don't have corresponding JSON entries
                for task_filename, task_file in task_files.items():
                    # Extract the task ID from the filename
                    match = re.match(r"task_(\d+)\.txt", task_filename)
                    if not match:
                        logger.warning(f"Invalid task filename: {task_filename}")
                        continue
                    
                    task_id = int(match.group(1))
                    
                    # Check if the task exists in the JSON data
                    if not any(t.get("id") == task_id for t in tasks_data.get("tasks", [])):
                        # Task doesn't exist in JSON, read the task file and add it
                        content = task_file.read_text(encoding='utf-8')
                        parsed_task = self._parse_task_file_content(content)
                        
                        if parsed_task:
                            tasks_data.setdefault("tasks", []).append(parsed_task)
                            changes["added"].append(task_filename)
                
                # Write the updated tasks data
                if changes["added"] or changes["modified"]:
                    await self.write_tasks(tasks_data)
                
                return changes
        except Exception as e:
            logger.error(f"Error ensuring consistency: {e}")
            raise FileStorageError(f"Could not ensure consistency: {e}")
    
    def _parse_task_file_content(self, content: str, existing_task: Dict[str, Any] = None) -> Dict[str, Any]:
        """Parse the content of a task file.
        
        Args:
            content: Content of the task file
            existing_task: Existing task data to update
        
        Returns:
            Dictionary containing the parsed task data
        """
        task = existing_task.copy() if existing_task else {}
        
        # Extract metadata from the file content
        lines = content.strip().split('\n')
        
        # Process metadata lines (lines starting with #)
        metadata_section = True
        details_lines = []
        test_strategy_lines = []
        current_section = None
        
        for line in lines:
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
            
            # Check for section markers
            if line.startswith('# Details:'):
                metadata_section = False
                current_section = 'details'
                continue
            elif line.startswith('# Test Strategy:'):
                metadata_section = False
                current_section = 'test_strategy'
                continue
            
            # Process metadata
            if metadata_section and line.startswith('# '):
                parts = line[2:].split(':', 1)
                if len(parts) == 2:
                    key = parts[0].strip().lower()
                    value = parts[1].strip()
                    
                    if key == 'task id':
                        task['id'] = int(value)
                    elif key == 'title':
                        task['title'] = value
                    elif key == 'status':
                        task['status'] = value
                    elif key == 'priority':
                        task['priority'] = value
                    elif key == 'dependencies':
                        if value and value.lower() != 'none':
                            # Parse dependencies, handling status information in parentheses
                            deps_list = []
                            for dep in value.split(','):
                                dep = dep.strip()
                                # Extract the dependency ID (ignore status in parentheses)
                                dep_match = re.match(r'(\d+)(?:\s+\([^)]*\))?', dep)
                                if dep_match:
                                    deps_list.append(int(dep_match.group(1)))
                            task['dependencies'] = deps_list
                        else:
                            task['dependencies'] = []
                    elif key == 'description':
                        task['description'] = value
            
            # Process content sections
            elif not metadata_section:
                if current_section == 'details':
                    details_lines.append(line)
                elif current_section == 'test_strategy':
                    test_strategy_lines.append(line)
        
        # Update task with section content
        if details_lines:
            task['details'] = '\n'.join(details_lines)
        
        if test_strategy_lines:
            task['testStrategy'] = '\n'.join(test_strategy_lines)
        
        return task
    
    def _format_task_file_content(self, task: Dict[str, Any], all_tasks: List[Dict[str, Any]]) -> str:
        """Format task content for file output.
        
        Args:
            task: Dictionary containing the task data
            all_tasks: List of all tasks (for resolving dependencies)
            
        Returns:
            Formatted task content
        """
        lines = [
            f"# Task ID: {task['id']}",
            f"# Title: {task['title']}",
            f"# Status: {task['status']}",
        ]
        
        # Format dependencies
        deps = task.get('dependencies', [])
        if deps:
            dep_strings = []
            for dep_id in deps:
                dep_task = find_task_by_id(all_tasks, dep_id)
                if dep_task:
                    dep_strings.append(f"{dep_id} ({dep_task['status']})")
                else:
                    dep_strings.append(str(dep_id))
            lines.append(f"# Dependencies: {', '.join(dep_strings)}")
        else:
            lines.append("# Dependencies: None")
        
        # Add priority
        lines.append(f"# Priority: {task.get('priority', TaskPriority.MEDIUM)}")
        
        # Add description
        lines.append(f"# Description: {task.get('description', '')}")
        
        # Add details
        lines.append(f"# Details: {task.get('details', '')}")
        
        # Add test strategy
        lines.append("# Test Strategy:")
        lines.append(task.get('testStrategy', ''))
        
        # Add subtasks if any
        if 'subtasks' in task and task['subtasks']:
            lines.append("# Subtasks:")
            
            for subtask in task['subtasks']:
                # Format subtask header
                subtask_title = subtask.get('title', '')
                subtask_status = subtask.get('status', TaskStatus.PENDING)
                lines.append(f"## {subtask.get('id', 0)}. {subtask_title} [{subtask_status}]")
                
                # Format subtask dependencies
                deps = subtask.get('dependencies', [])
                if deps:
                    dep_strings = []
                    for dep_id in deps:
                        # Check if this is a task dependency or a subtask dependency
                        if '.' in str(dep_id):  # Format: "task_id.subtask_id"
                            parts = str(dep_id).split('.')
                            if len(parts) == 2:
                                task_id, subtask_id = parts
                                dep_task = find_task_by_id(all_tasks, int(task_id))
                                if dep_task and 'subtasks' in dep_task:
                                    dep_subtask = next((s for s in dep_task['subtasks'] if s.get('id') == int(subtask_id)), None)
                                    if dep_subtask:
                                        dep_strings.append(f"{dep_id} ({dep_subtask.get('status', TaskStatus.PENDING)})")
                                        continue
                        
                        # If not a subtask dependency or subtask not found, just add the ID
                        dep_strings.append(str(dep_id))
                    lines.append(f"### Dependencies: {', '.join(dep_strings)}")
                else:
                    lines.append("### Dependencies: None")
                
                lines.extend([
                    f"### Priority: {subtask.get('priority', TaskPriority.MEDIUM)}",
                    f"### Description: {subtask.get('description', '')}",
                    "### Details:",
                    subtask.get('details', ''),
                    ""
                ])
                
                # Add research results if present
                if 'research' in subtask and subtask['research']:
                    research = subtask['research']
                    lines.append("### Research Results:")
                    lines.append("Research completed successfully.")
                    lines.append("")
                    
                    # Add key findings if available
                    if 'key_findings' in research and research['key_findings']:
                        lines.append(research['key_findings'])
                    
                    # Add recommendations if available and different from key findings
                    if ('recommendations' in research and research['recommendations'] and 
                        research['recommendations'] != research.get('key_findings', '')):
                        lines.append("")
                        lines.append("## Recommendations")
                        lines.append(research['recommendations'])
                    
                    # Add resources if available
                    if 'resources' in research and research['resources']:
                        lines.append("")
                        lines.append("## Resources")
                        lines.append(research['resources'])
                    
                    # Add sources if available
                    if 'sources' in research and research['sources']:
                        lines.append("")
                        lines.append("## Sources")
                        lines.append(research['sources'])
                    
                    lines.append("")
        
        return "\n".join(lines)
    
    def _tasks_differ(self, task1: Dict[str, Any], task2: Dict[str, Any]) -> bool:
        """Check if two tasks differ in content.
        
        Args:
            task1: First task dictionary
            task2: Second task dictionary
            
        Returns:
            True if the tasks differ, False otherwise
        """
        # Compare basic fields
        basic_fields = ['id', 'title', 'status', 'priority', 'description', 'details', 'testStrategy']
        for field in basic_fields:
            if task1.get(field) != task2.get(field):
                return True
        
        # Compare dependencies (order doesn't matter)
        deps1 = set(task1.get('dependencies', []))
        deps2 = set(task2.get('dependencies', []))
        if deps1 != deps2:
            return True
        
        # Compare subtasks
        subtasks1 = task1.get('subtasks', [])
        subtasks2 = task2.get('subtasks', [])
        
        if len(subtasks1) != len(subtasks2):
            return True
        
        # Create a mapping of subtask IDs to subtasks for easier comparison
        subtasks1_map = {s.get('id'): s for s in subtasks1}
        subtasks2_map = {s.get('id'): s for s in subtasks2}
        
        # Check if all subtask IDs match
        if set(subtasks1_map.keys()) != set(subtasks2_map.keys()):
            return True
        
        # Compare each subtask
        for subtask_id, subtask1 in subtasks1_map.items():
            subtask2 = subtasks2_map.get(subtask_id)
            if not subtask2:
                return True
            
            # Compare basic fields
            for field in ['title', 'status', 'priority', 'description', 'details']:
                if subtask1.get(field) != subtask2.get(field):
                    return True
            
            # Compare dependencies (order doesn't matter)
            deps1 = set(subtask1.get('dependencies', []))
            deps2 = set(subtask2.get('dependencies', []))
            if deps1 != deps2:
                return True
        
        return False
