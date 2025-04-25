"""Dependency management and validation for Taskinator."""

from typing import Dict, List, Set, Tuple, Union

from .config import TaskStatus
from .ui import display_error
from .utils import find_task_by_id, logger

def validate_task_dependencies(
    tasks: List[Dict],
    task_id: Union[str, int, None] = None
) -> Tuple[bool, List[str]]:
    """Validate dependencies for a single task or all tasks.
    
    Args:
        tasks: List of all tasks
        task_id: Optional specific task ID to validate
        
    Returns:
        Tuple of (is_valid, list of error messages)
    """
    errors = []
    
    if task_id is not None:
        # Validate single task
        task = find_task_by_id(tasks, task_id)
        if not task:
            return False, [f"Task {task_id} not found"]
        
        task_errors = _validate_single_task_dependencies(task, tasks)
        errors.extend(task_errors)
    else:
        # Validate all tasks
        for task in tasks:
            task_errors = _validate_single_task_dependencies(task, tasks)
            errors.extend(task_errors)
    
    return len(errors) == 0, errors

def _validate_single_task_dependencies(
    task: Dict,
    all_tasks: List[Dict]
) -> List[str]:
    """Validate dependencies for a single task.
    
    Args:
        task: Task to validate
        all_tasks: List of all tasks
        
    Returns:
        List of error messages
    """
    errors = []
    task_id = str(task['id'])
    dependencies = task.get('dependencies', [])
    
    # Check each dependency
    for dep_id in dependencies:
        dep_id = str(dep_id)
        
        # Skip self-reference check for subtasks
        if '.' in dep_id and dep_id.startswith(f"{task_id}."):
            continue
            
        # Validate dependency exists
        dep_task = find_task_by_id(all_tasks, dep_id)
        if not dep_task:
            errors.append(f"Task {task_id} depends on non-existent task {dep_id}")
            continue
        
        # Check for circular dependencies
        if _has_circular_dependency(task_id, dep_id, all_tasks, set()):
            errors.append(f"Circular dependency detected: {task_id} -> {dep_id}")
        
        # Validate status consistency
        if task['status'] == TaskStatus.DONE and dep_task['status'] != TaskStatus.DONE:
            errors.append(
                f"Task {task_id} is marked as done but depends on "
                f"unfinished task {dep_id}"
            )
    
    return errors

def _has_circular_dependency(
    start_id: str,
    current_id: str,
    tasks: List[Dict],
    visited: Set[str]
) -> bool:
    """Check for circular dependencies recursively.
    
    Args:
        start_id: ID of the starting task
        current_id: ID of the current task being checked
        tasks: List of all tasks
        visited: Set of already visited task IDs
        
    Returns:
        True if a circular dependency is found
    """
    if current_id in visited:
        return current_id == start_id
    
    visited.add(current_id)
    current_task = find_task_by_id(tasks, current_id)
    
    if not current_task:
        return False
    
    for dep_id in current_task.get('dependencies', []):
        if _has_circular_dependency(start_id, str(dep_id), tasks, { *visited }):
            return True
    
    return False

def validate_and_fix_dependencies(
    tasks: List[Dict],
    auto_fix: bool = False
) -> Tuple[bool, List[str], List[Dict]]:
    """Validate and optionally fix dependency issues.
    
    Args:
        tasks: List of all tasks
        auto_fix: Whether to automatically fix issues
        
    Returns:
        Tuple of (is_valid, list of error messages, updated tasks)
    """
    is_valid, errors = validate_task_dependencies(tasks)
    
    if not is_valid and auto_fix:
        fixed_tasks = tasks.copy()
        fixed = False
        
        # Try to fix status inconsistencies
        for task in fixed_tasks:
            if task['status'] == TaskStatus.DONE:
                deps_done = True
                for dep_id in task.get('dependencies', []):
                    dep_task = find_task_by_id(fixed_tasks, dep_id)
                    if dep_task and dep_task['status'] != TaskStatus.DONE:
                        deps_done = False
                        break
                
                if not deps_done:
                    task['status'] = TaskStatus.BLOCKED
                    fixed = True
                    logger.info(
                        f"Auto-fixed: Task {task['id']} marked as blocked due to "
                        "unfinished dependencies"
                    )
        
        # Remove invalid dependencies
        for task in fixed_tasks:
            valid_deps = []
            for dep_id in task.get('dependencies', []):
                if find_task_by_id(fixed_tasks, dep_id):
                    valid_deps.append(dep_id)
                else:
                    fixed = True
                    logger.info(
                        f"Auto-fixed: Removed invalid dependency {dep_id} from "
                        f"task {task['id']}"
                    )
            task['dependencies'] = valid_deps
        
        if fixed:
            # Revalidate after fixes
            is_valid, new_errors = validate_task_dependencies(fixed_tasks)
            if is_valid:
                logger.info("Successfully fixed dependency issues")
                return True, [], fixed_tasks
            else:
                logger.warning("Some dependency issues could not be auto-fixed")
                return False, new_errors, fixed_tasks
    
    return is_valid, errors, tasks

def get_dependent_tasks(
    task_id: Union[str, int],
    tasks: List[Dict]
) -> List[Dict]:
    """Get all tasks that depend on the given task.
    
    Args:
        task_id: ID of the task
        tasks: List of all tasks
        
    Returns:
        List of dependent tasks
    """
    task_id = str(task_id)
    dependent_tasks = []
    
    for task in tasks:
        if str(task_id) in [str(dep) for dep in task.get('dependencies', [])]:
            dependent_tasks.append(task)
    
    return dependent_tasks

def update_dependent_tasks_status(
    task_id: Union[str, int],
    tasks: List[Dict],
    new_status: str
) -> List[Dict]:
    """Update the status of tasks that depend on the given task.
    
    Args:
        task_id: ID of the task
        tasks: List of all tasks
        new_status: New status to set
        
    Returns:
        Updated list of tasks
    """
    if not TaskStatus.is_valid(new_status):
        raise ValueError(f"Invalid status: {new_status}")
    
    updated_tasks = tasks.copy()
    dependent_tasks = get_dependent_tasks(task_id, tasks)
    
    for task in dependent_tasks:
        if new_status == TaskStatus.DONE:
            # Check if all dependencies are done
            all_deps_done = True
            for dep_id in task.get('dependencies', []):
                dep_task = find_task_by_id(updated_tasks, dep_id)
                if dep_task and dep_task['status'] != TaskStatus.DONE:
                    all_deps_done = False
                    break
            
            if all_deps_done:
                task['status'] = TaskStatus.PENDING
            else:
                task['status'] = TaskStatus.BLOCKED
        elif new_status != TaskStatus.DONE and task['status'] == TaskStatus.DONE:
            # If a dependency is no longer done, mark dependent task as blocked
            task['status'] = TaskStatus.BLOCKED
    
    return updated_tasks