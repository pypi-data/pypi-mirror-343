"""Utility functions for Taskinator."""

import json
import os
import time
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from rich.console import Console
from rich.logging import RichHandler

from .config import config

# Set up logging
from loguru import logger

# Set debug level
logger.remove()
logger.add(lambda msg: print(msg, end=""), level="DEBUG")

console = Console()

class PerformanceTracker:
    """Context manager for tracking performance metrics of operations.
    
    This class is used to track the execution time of operations and log
    performance metrics, which is particularly useful for testing.
    
    Example:
        ```python
        with PerformanceTracker("Loading tasks"):
            tasks = load_tasks()
        ```
    """
    
    def __init__(self, operation_name: str, log_level: str = "INFO"):
        """Initialize the performance tracker.
        
        Args:
            operation_name: Name of the operation being tracked
            log_level: Logging level for performance metrics
        """
        self.operation_name = operation_name
        self.log_level = log_level
        self.start_time = None
        self.end_time = None
    
    def __enter__(self):
        """Start tracking performance."""
        self.start_time = time.time()
        logger.log(self.log_level, f"Starting: {self.operation_name}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Stop tracking performance and log metrics."""
        self.end_time = time.time()
        duration = self.end_time - self.start_time
        
        if exc_type:
            logger.error(f"Error in {self.operation_name}: {exc_val}")
            logger.error(f"Operation failed after {duration:.4f} seconds")
        else:
            logger.log(self.log_level, f"Completed: {self.operation_name} in {duration:.4f} seconds")
        
        # Don't suppress exceptions
        return False

def read_json(path: Union[str, Path]) -> Dict[str, Any]:
    """Read a JSON file and return its contents.
    
    Args:
        path: Path to the JSON file
        
    Returns:
        Dict containing the JSON data
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        json.JSONDecodeError: If the file contains invalid JSON
    """
    path = Path(path)
    try:
        with path.open('r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"File not found: {path}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in {path}: {e}")
        raise

def write_json(path: Union[str, Path], data: Any, indent: int = 2) -> None:
    """Write data to a JSON file.
    
    Args:
        path: Path to the JSON file
        data: Data to write
        indent: Number of spaces for indentation
        
    Raises:
        OSError: If there's an error writing the file
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        with path.open('w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent)
    except OSError as e:
        logger.error(f"Error writing to {path}: {e}")
        raise

def sanitize_prompt(text: str) -> str:
    """Sanitize a prompt string for AI services.
    
    Args:
        text: Text to sanitize
        
    Returns:
        Sanitized text
    """
    # Remove any potentially problematic characters
    return text.strip().replace('\x00', '')

def find_task_by_id(tasks: List[Dict[str, Any]], task_id: Union[str, int]) -> Optional[Dict[str, Any]]:
    """Find a task by its ID.
    
    Args:
        tasks: List of tasks to search
        task_id: ID of the task to find (can be a hierarchical ID like "5.3" or "5.3.2")
        
    Returns:
        Task dict if found, None otherwise
    """
    task_id = str(task_id)
    
    # Handle hierarchical task IDs (e.g., "5.3.2" for subtask 2 of subtask 3 of task 5)
    if '.' in task_id:
        parts = task_id.split('.')
        if all(part.isdigit() for part in parts):
            # Start with the top-level tasks
            current_tasks = tasks
            current_task = None
            
            # Navigate through the hierarchy
            for i, part in enumerate(parts):
                part_id = part
                
                # Find the task at this level
                found = False
                for task in current_tasks:
                    if str(task.get('id')) == part_id:
                        current_task = task
                        found = True
                        break
                
                if not found:
                    return None
                
                # If we're at the last part, return the task
                if i == len(parts) - 1:
                    return current_task
                
                # Otherwise, move to the next level in the hierarchy
                if 'subtasks' not in current_task or not current_task['subtasks']:
                    return None
                
                current_tasks = current_task['subtasks']
            
            return current_task
    
    # Regular task ID lookup
    for task in tasks:
        if str(task.get('id')) == task_id:
            return task
    
    return None

def format_timestamp(timestamp: Optional[float] = None) -> str:
    """Format a timestamp for display.
    
    Args:
        timestamp: Unix timestamp (uses current time if None)
        
    Returns:
        Formatted timestamp string
    """
    if timestamp is None:
        timestamp = datetime.now().timestamp()
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

def truncate(text: str, max_length: int = 50, suffix: str = '...') -> str:
    """Truncate text to a maximum length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: String to append if truncated
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix

def ensure_task_structure(task: Dict[str, Any]) -> Dict[str, Any]:
    """Ensure a task has all required fields with default values.
    
    Args:
        task: Task dictionary to validate
        
    Returns:
        Task dictionary with all required fields
    """
    defaults = {
        'status': 'pending',
        'priority': 'medium',
        'dependencies': [],
        'subtasks': [],
        'description': '',
        'details': '',
        'testStrategy': '',
        'created': datetime.now().timestamp(),
        'updated': datetime.now().timestamp(),
        'external_sync': []
    }
    
    # Create a new task with defaults
    result = {**defaults, **task}
    
    # For backward compatibility, handle the old nextcloud field
    if 'nextcloud' in task and 'external_sync' not in task:
        # This will be migrated by the migration script
        result['nextcloud'] = task['nextcloud']
    
    # Ensure external_sync is a list
    if not isinstance(result.get('external_sync'), list):
        result['external_sync'] = []
    
    return result

def validate_task_id(task_id: Union[str, int]) -> str:
    """Validate and normalize a task ID.
    
    Args:
        task_id: Task ID to validate
        
    Returns:
        Normalized task ID as string
        
    Raises:
        ValueError: If the task ID is invalid
    """
    try:
        # Split into parent and subtask IDs
        parts = str(task_id).split('.')
        
        # Validate parent ID
        parent_id = parts[0]
        parent_id = str(int(parent_id))
        if int(parent_id) <= 0:
            raise ValueError("Parent task ID must be positive")
        
        # Validate subtask IDs
        subtask_ids = parts[1:]
        for subtask_id in subtask_ids:
            subtask_id = str(int(subtask_id))
            if int(subtask_id) <= 0:
                raise ValueError("Subtask ID must be positive")
        
        # Return normalized task ID
        return '.'.join([parent_id] + subtask_ids)
    except (ValueError, TypeError):
        raise ValueError(f"Invalid task ID: {task_id}")

def get_sync_config(system: str) -> Dict[str, Any]:
    """Get configuration for an external system.
    
    Args:
        system: External system name
        
    Returns:
        Configuration dictionary
    """
    import os
    
    # Initialize config
    config = {}
    
    # NextCloud credentials
    if system == "nextcloud":
        nextcloud_host = os.getenv("NEXTCLOUD_HOST")
        nextcloud_username = os.getenv("NEXTCLOUD_USERNAME")
        nextcloud_password = os.getenv("NEXTCLOUD_PASSWORD")
        nextcloud_token = os.getenv("NEXTCLOUD_TOKEN")
        
        # For testing, if no credentials are provided, use dummy values
        if not nextcloud_host:
            logger.warning("No NextCloud credentials found in environment, using dummy values for testing")
            nextcloud_host = "https://nextcloud.example.com"
            nextcloud_username = "testuser"
            nextcloud_password = "testpass"
        
        config["nextcloud"] = {
            "host": nextcloud_host,
            "username": nextcloud_username,
            "password": nextcloud_password,
            "token": nextcloud_token
        }
    
    return config