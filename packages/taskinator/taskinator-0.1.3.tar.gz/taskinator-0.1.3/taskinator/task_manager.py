"""Core task management functionality for Taskinator."""

import os
import json
import re
import glob
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union, Any, Set

from rich.console import Console
from rich.prompt import Confirm
from rich.progress import Progress
from rich.table import Table

from . import ai_services
from .config import TaskPriority, TaskStatus, config
from .dependency_manager import (
    get_dependent_tasks,
    update_dependent_tasks_status,
    validate_and_fix_dependencies,
    validate_task_dependencies,
)
from .ui import (
    create_task_table,
    display_error,
    display_info,
    display_success,
    display_table,
    display_task_details,
    create_loading_indicator
)
from .utils import (
    logger,
    read_json,
    write_json,
    validate_task_id,
    ensure_task_structure,
    find_task_by_id,
)
from .similarity_module import TaskSimilarityModule
from .complexity_module import complexity_module  # Import the singleton instance

class TaskManager:
    """Main task management class."""
    
    def __init__(self, tasks_dir: Union[str, Path] = None, display_output: bool = True):
        """Initialize TaskManager.
        
        Args:
            tasks_dir: Directory to store tasks in
            display_output: Whether to display output to console (for CLI usage)
        """
        self.tasks_dir = Path(tasks_dir) if tasks_dir else config.tasks_dir
        self.tasks_file = self.tasks_dir / "tasks.json"
        self.tasks_dir.mkdir(parents=True, exist_ok=True)
        self.display_output = display_output
    
    def _ensure_subtask_structure(self, subtask: Dict) -> Dict:
        """Ensure a subtask has all required fields with defaults."""
        defaults = {
            'status': TaskStatus.PENDING,
            'priority': TaskPriority.MEDIUM,
            'dependencies': [],
            'description': '',
            'details': ''
        }
        return {**defaults, **subtask}
    
    async def parse_prd(
        self,
        prd_path: Union[str, Path],
        num_tasks: int = 10
    ) -> Dict:
        """Parse a PRD file and generate tasks.
        
        Returns:
            Dict containing the generated tasks data
        """
        prd_path = Path(prd_path)
        if not prd_path.exists():
            raise FileNotFoundError(f"PRD file not found: {prd_path}")
        
        try:
            logger.info(f"Parsing PRD file: {prd_path}")
            content = prd_path.read_text(encoding='utf-8')
            
            # Generate tasks using Claude
            tasks_data = await ai_services.call_claude(content, prd_path, num_tasks)
            
            # Ensure tasks directory exists
            self.tasks_dir.mkdir(parents=True, exist_ok=True)
            
            # Ensure task structure
            tasks_data['tasks'] = [
                ensure_task_structure(task) for task in tasks_data['tasks']
            ]
            
            # Write tasks to file
            write_json(self.tasks_file, tasks_data)
            
            logger.info(f"Generated {len(tasks_data['tasks'])} tasks from PRD")
            
            # Generate individual task files
            await self.generate_task_files()
            
            if self.display_output:
                display_success(
                    f"Successfully generated {len(tasks_data['tasks'])} tasks from PRD\n\n"
                    "Next Steps:\n"
                    "1. Run 'taskinator list' to view all tasks\n"
                    "2. Run 'taskinator expand --id=<id>' to break down a task into subtasks"
                )
            
            return tasks_data
            
        except Exception as e:
            logger.error(f"Error parsing PRD: {e}")
            if self.display_output:
                display_error(f"Failed to parse PRD: {e}")
            raise
    
    async def generate_task_files(self) -> List[Path]:
        """Generate individual task files from tasks.json.
        
        Returns:
            List of paths to the generated task files
        """
        try:
            logger.info(f"Reading tasks from {self.tasks_file}")
            data = read_json(self.tasks_file)
            
            if not data or 'tasks' not in data:
                raise ValueError(f"No valid tasks found in {self.tasks_file}")
            
            logger.info("Validating dependencies...")
            _, _, data['tasks'] = validate_and_fix_dependencies(data['tasks'], auto_fix=True)
            
            generated_files = []
            # Generate task files
            for task in data['tasks']:
                task_path = self.tasks_dir / f"task_{str(task['id']).zfill(3)}.txt"
                content = self._format_task_file_content(task, data['tasks'])
                task_path.write_text(content, encoding='utf-8')
                logger.info(f"Generated: {task_path.name}")
                generated_files.append(task_path)
            
            logger.info(f"Generated {len(data['tasks'])} task files")
            return generated_files
            
        except Exception as e:
            logger.error(f"Error generating task files: {e}")
            if self.display_output:
                display_error(f"Failed to generate task files: {e}")
            raise
    
    def _format_task_file_content(self, task: Dict, all_tasks: List[Dict]) -> str:
        """Format task content for file output."""
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
    
    def list_tasks(self, status=None, priority=None):
        """List all tasks."""
        data = read_json(self.tasks_file)
        
        if not data or 'tasks' not in data:
            logger.warning(f"No tasks found in {self.tasks_file}")
            return []
        
        tasks = data['tasks']
        
        # Filter by status if provided
        if status:
            tasks = [task for task in tasks if task.get('status') == status]
        
        # Filter by priority if provided
        if priority:
            tasks = [task for task in tasks if task.get('priority') == priority]
        
        return tasks
    
    async def expand_task(
        self,
        task_id: Union[str, int],
        num_subtasks: int = 5,
        use_research: bool = False,
        additional_context: str = "",
        display_output: Optional[bool] = None
    ) -> Dict:
        """Expand a task into subtasks.
        
        Returns:
            The updated task with subtasks
        """
        try:
            task_id = validate_task_id(task_id)
            
            logger.info(f"Expanding task {task_id} into {num_subtasks} subtasks")
            data = read_json(self.tasks_file)
            
            if not data or 'tasks' not in data:
                raise ValueError(f"No valid tasks found in {self.tasks_file}")
            
            task = find_task_by_id(data['tasks'], task_id)
            if not task:
                raise ValueError(f"Task {task_id} not found")
            
            # Generate subtasks using AI
            with create_loading_indicator("Generating subtasks...") as progress:
                progress_id = progress.add_task("Generating subtasks...", total=None)
                
                subtasks = await ai_services.generate_subtasks(
                    task, num_subtasks, use_research, additional_context, progress
                )
                
                progress.update(progress_id, completed=True)
            
            # Ensure subtask structure
            subtasks = [self._ensure_subtask_structure(st) for st in subtasks]
            
            # Update task with subtasks
            task['subtasks'] = subtasks
            
            # Write updated tasks
            write_json(self.tasks_file, data)
            
            # Regenerate task files
            await self.generate_task_files()
            
            # Determine whether to display output
            should_display = self.display_output if display_output is None else display_output
            
            if should_display:
                display_success(f"Successfully expanded task {task_id} into {len(subtasks)} subtasks")
                display_task_details(task)
            
            return task
            
        except Exception as e:
            logger.error(f"Error expanding task: {e}")
            # Determine whether to display output
            should_display = self.display_output if display_output is None else display_output
            if should_display:
                display_error(f"Failed to expand task: {e}")
            raise
    
    async def set_task_status(
        self,
        task_ids: Union[str, List[str]],
        new_status: str
    ) -> List[Dict]:
        """Set the status of one or more tasks.
        
        Returns:
            List of updated tasks
        """
        try:
            if not TaskStatus.is_valid(new_status):
                raise ValueError(f"Invalid status: {new_status}")
            
            # Convert string of comma-separated IDs to list if needed
            if isinstance(task_ids, str):
                task_ids = [tid.strip() for tid in task_ids.split(',')]
            
            # Validate all task IDs
            task_ids = [validate_task_id(tid) for tid in task_ids]
            
            logger.info(f"Setting status of tasks {task_ids} to {new_status}")
            data = read_json(self.tasks_file)
            
            if not data or 'tasks' not in data:

                raise ValueError(f"No valid tasks found in {self.tasks_file}")

            # Find all tasks to update
            updated_tasks = []
            for task_id in task_ids:
                # Check if it's a subtask ID (format: parent.subtask)
                if '.' in str(task_id):
                    parent_id, subtask_id = str(task_id).split('.')
                    parent_id = int(parent_id)
                    subtask_id = int(subtask_id)
                    
                    parent = find_task_by_id(data['tasks'], parent_id)
                    if not parent or 'subtasks' not in parent:
                        raise ValueError(f"Parent task {parent_id} not found or has no subtasks")
                    
                    for subtask in parent['subtasks']:
                        if subtask['id'] == subtask_id:
                            subtask['status'] = new_status
                            updated_tasks.append(subtask)
                            break
                    else:
                        raise ValueError(f"Subtask {subtask_id} not found in task {parent_id}")
                else:
                    # Regular task
                    task = find_task_by_id(data['tasks'], task_id)
                    if not task:
                        raise ValueError(f"Task {task_id} not found")
                    
                    task['status'] = new_status
                    updated_tasks.append(task)
                    
                    # Update dependent tasks if needed
                    update_dependent_tasks_status(task_id, data['tasks'], new_status)
            
            # Write updated tasks
            write_json(self.tasks_file, data)
            
            # Regenerate task files
            await self.generate_task_files()
            
            if self.display_output:
                display_success(f"Successfully updated status of {len(updated_tasks)} tasks to {new_status}")
            
            return updated_tasks
            
        except Exception as e:
            logger.error(f"Error setting task status: {e}")
            if self.display_output:
                display_error(f"Failed to set task status: {e}")
            raise
    
    async def set_task_priority(
        self,
        task_ids: Union[str, List[str]],
        new_priority: str
    ) -> List[Dict]:
        """Set the priority of one or more tasks.
        
        Returns:
            List of updated tasks
        """
        try:
            # Validate priority
            if not TaskPriority.is_valid(new_priority):
                valid_priorities = TaskPriority.get_valid_priorities()
                raise ValueError(f"Invalid priority: {new_priority}. Valid priorities are: {valid_priorities}")
            
            # Convert single task ID to list
            if isinstance(task_ids, str):
                task_ids = [task_ids]
            
            # Read tasks file
            data = read_json(self.tasks_file)
            tasks = data.get('tasks', [])
            
            # Track updated tasks
            updated_tasks = []
            
            # Update each task
            for task_id in task_ids:
                # Validate task ID
                task_id = validate_task_id(task_id)
                
                # Find task
                task = find_task_by_id(tasks, task_id)
                if not task:
                    logger.warning(f"Task not found: {task_id}")
                    if self.display_output:
                        display_error(f"Task not found: {task_id}")
                    continue
                
                # Update priority
                old_priority = task.get('priority', TaskPriority.MEDIUM)
                task['priority'] = new_priority
                updated_tasks.append(task)
                
                logger.info(f"Changed priority of task {task_id} from {old_priority} to {new_priority}")
                
                # Update subtasks if present
                if 'subtasks' in task and task['subtasks']:
                    for subtask in task['subtasks']:
                        subtask['priority'] = new_priority
                    logger.info(f"Updated priority of all subtasks for task {task_id}")
            
            # Write updated tasks back to file
            write_json(self.tasks_file, data)
            
            # Generate task files
            await self.generate_task_files()
            
            # Display success message
            if self.display_output and updated_tasks:
                display_success(f"Updated priority of {len(updated_tasks)} task(s) to {new_priority}")
                
                # Show updated tasks
                table = create_task_table(updated_tasks)
                display_table(table)
            
            return updated_tasks
            
        except Exception as e:
            logger.error(f"Error setting task priority: {e}")
            if self.display_output:
                display_error(f"Failed to set task priority: {e}")
            raise
    
    async def analyze_task_complexity(
        self,
        output_file: Optional[str] = None,
        task_id: Optional[str] = None,
        use_research: bool = False,
        use_dspy: bool = False,
        analyze_subtasks: bool = True,
        recursive: bool = False
    ) -> Dict:
        """Analyze task complexity and generate a report.
        
        Args:
            output_file: Path to save the complexity report
            task_id: Optional ID of a specific task to analyze
            use_research: Whether to use research for analysis
            use_dspy: Whether to use DSPy for enhanced complexity analysis
            analyze_subtasks: Whether to analyze subtasks instead of parent tasks
            recursive: Whether to recursively analyze all levels of subtasks
            
        Returns:
            Dictionary with complexity analysis results
        """
        try:
            # Load tasks from file
            logger.info(f"Reading tasks from {self.tasks_file}")
            data = read_json(self.tasks_file)
            
            # Filter tasks if task_id is provided
            if task_id:
                # Find the specific task using the hierarchical ID support
                task = find_task_by_id(data['tasks'], task_id)
                if not task:
                    raise ValueError(f"Task with ID {task_id} not found")
                
                # If analyzing a specific task, replace the tasks list with just that task
                data['tasks'] = [task]
            
            # If a task has subtasks, analyze those instead of the parent task
            tasks_to_analyze = []
            parent_task_map = {}  # Maps subtask ID to parent task ID and full hierarchical path
            
            def collect_tasks_to_analyze(tasks, parent_id=None, path_prefix=""):
                for task in tasks:
                    task_id = str(task.get('id'))
                    current_path = f"{path_prefix}{task_id}"
                    
                    if task.get('subtasks') and len(task.get('subtasks', [])) > 0 and analyze_subtasks:
                        # Add all subtasks to the analysis list
                        for subtask in task.get('subtasks', []):
                            # Add a reference to the parent task ID and path
                            subtask_id = str(subtask.get('id'))
                            subtask['parent_id'] = task_id
                            subtask['parent_title'] = task.get('title', '')
                            
                            # Create hierarchical path for this subtask
                            subtask_path = f"{current_path}.{subtask_id}"
                            parent_task_map[subtask_id] = {
                                'parent_id': task_id,
                                'path': subtask_path
                            }
                            
                            tasks_to_analyze.append(subtask)
                            
                            # If recursive and this subtask has its own subtasks, analyze those too
                            if recursive and subtask.get('subtasks') and len(subtask.get('subtasks', [])) > 0:
                                collect_tasks_to_analyze(
                                    [subtask], 
                                    parent_id=subtask_id,
                                    path_prefix=f"{current_path}."
                                )
                    else:
                        # Add the task itself if it has no subtasks or we're not analyzing subtasks
                        if parent_id:
                            task['parent_id'] = parent_id
                            parent_task_map[task_id] = {
                                'parent_id': parent_id,
                                'path': current_path
                            }
                        tasks_to_analyze.append(task)
            
            # Start collecting tasks to analyze
            collect_tasks_to_analyze(data['tasks'])
            
            # If no tasks to analyze, inform the user
            if not tasks_to_analyze:
                console = Console()
                console.print("[yellow]No tasks found to analyze.[/yellow]")
                return {
                    'status': 'no_tasks',
                    'message': 'No tasks found to analyze'
                }
            
            # Use DSPy-based complexity analysis module if requested
            if use_dspy:
                console = Console()
                console.print("[bold blue]Using DSPy-based complexity analysis module[/bold blue]")
                
                # Print debug information about DSPy
                try:
                    import dspy
                    console.print(f"[green]DSPy is available (version: {dspy.__version__})[/green]")
                    console.print(f"[green]DSPy path: {dspy.__file__}[/green]")
                except ImportError:
                    try:
                        import dspy_ai as dspy
                        console.print(f"[green]DSPy-AI is available (version: {dspy.__version__})[/green]")
                        console.print(f"[green]DSPy-AI path: {dspy.__file__}[/green]")
                    except ImportError:
                        console.print("[red]DSPy is not available. Install with 'pip install dspy-ai'[/red]")
                        import sys
                        console.print(f"Python path: {sys.path}")
                
                # Analyze tasks using the complexity_module instance
                complexity_module.use_dspy = True
                results = complexity_module.analyze_tasks(tasks_to_analyze)
            
            else:
                # Generate prompt for complexity analysis
                # Create a new data structure with tasks_to_analyze
                analysis_data = {'tasks': tasks_to_analyze}
                prompt = ai_services.generate_complexity_analysis_prompt(analysis_data)
                
                # Analyze task complexity using AI
                with create_loading_indicator("Analyzing task complexity..."):
                    results = await ai_services.analyze_task_complexity(
                        tasks=tasks_to_analyze,
                        prompt=prompt,
                        use_research=use_research
                    )
            
            # Save results to file
            if output_file:
                os.makedirs(os.path.dirname(output_file), exist_ok=True)
                with open(output_file, 'w') as f:
                    # Wrap results in a dictionary with 'complexityAnalysis' key
                    report = {
                        "complexityAnalysis": results,
                        "generatedAt": datetime.now().isoformat(),
                        "totalTasks": len(tasks_to_analyze)
                    }
                    json.dump(report, f, indent=2)
                
                console = Console()
                console.print(f"[green]Complexity analysis saved to {output_file}[/green]")
            
            # Display results
            console = Console()
            
            # Group results by parent task
            results_by_parent = {}
            standalone_results = []
            
            for result in results:
                task_id = str(result.get('taskId'))
                if task_id in parent_task_map:
                    parent_info = parent_task_map[task_id]
                    parent_id = parent_info['parent_id']
                    if parent_id not in results_by_parent:
                        results_by_parent[parent_id] = []
                    
                    # Add the hierarchical path to the result
                    result['hierarchicalPath'] = parent_info['path']
                    results_by_parent[parent_id].append(result)
                else:
                    standalone_results.append(result)
            
            # Display standalone tasks first
            if standalone_results:
                table = Table(title="Task Complexity Analysis")
                table.add_column("ID", style="cyan")
                table.add_column("Title", style="green")
                table.add_column("Complexity", style="yellow")
                table.add_column("Subtasks", style="magenta")
                
                for result in standalone_results:
                    task_id = result.get('taskId')
                    title = result.get('taskTitle', '')
                    complexity = result.get('complexityScore', 0)
                    subtasks = result.get('recommendedSubtasks', 0)
                    
                    # Color based on complexity
                    complexity_color = "green"
                    if complexity >= 8:
                        complexity_color = "red"
                    elif complexity >= 5:
                        complexity_color = "yellow"
                    
                    table.add_row(
                        str(task_id),
                        title[:50] + ('...' if len(title) > 50 else ''),
                        f"[{complexity_color}]{complexity}[/{complexity_color}]",
                        str(subtasks) if subtasks else "-"
                    )
                
                console.print(table)
            
            # Display subtasks grouped by parent
            for parent_id, subtask_results in results_by_parent.items():
                # Find parent title
                parent_title = "Unknown"
                parent_task = None
                
                # Look for the parent in the original data
                for task in data['tasks']:
                    if str(task.get('id')) == str(parent_id):
                        parent_task = task
                        parent_title = task.get('title', 'Unknown')
                        break
                
                # If not found at top level, it might be a subtask itself
                if not parent_task and task_id:
                    # The parent might be the task we're analyzing
                    task = find_task_by_id(data['tasks'], task_id)
                    if task and str(task.get('id')) == str(parent_id):
                        parent_task = task
                        parent_title = task.get('title', 'Unknown')
                
                table = Table(title=f"Subtask Analysis for Task {parent_id}: {parent_title}")
                table.add_column("ID", style="cyan")
                table.add_column("Subtask", style="green")
                table.add_column("Complexity", style="yellow")
                table.add_column("Further Breakdown", style="magenta")
                
                for result in subtask_results:
                    task_id = result.get('taskId')
                    title = result.get('taskTitle', '')
                    complexity = result.get('complexityScore', 0)
                    subtasks = result.get('recommendedSubtasks', 0)
                    
                    # Color based on complexity
                    complexity_color = "green"
                    if complexity >= 8:
                        complexity_color = "red"
                    elif complexity >= 5:
                        complexity_color = "yellow"
                    
                    # Use hierarchical path if available
                    display_id = result.get('hierarchicalPath', task_id)
                    
                    table.add_row(
                        str(display_id),
                        title[:50] + ('...' if len(title) > 50 else ''),
                        f"[{complexity_color}]{complexity}[/{complexity_color}]",
                        str(subtasks) if subtasks else "-"
                    )
                
                console.print(table)
            
            return results
            
        except Exception as e:
            logger.error(f"Error analyzing task complexity: {e}")
            raise
    
    async def analyze_task_similarities(
        self,
        threshold: float = 0.7,
        output_file: str = "tasks/task-similarity-report.json",
        use_dspy: bool = False
    ) -> Dict[str, Any]:
        """Analyze task similarities using the TaskSimilarityModule.
        
        Args:
            threshold: Similarity threshold (0-1) for considering tasks similar
            output_file: Path to save the similarity report
            use_dspy: Whether to use DSPy for enhanced similarity analysis
            
        Returns:
            Dictionary with similarity analysis results
        """
        try:
            # Load tasks
            logger.info(f"Reading tasks from {self.tasks_file}")
            data = read_json(self.tasks_file)
            tasks = data.get('tasks', [])
            
            if not tasks:
                logger.warning("No tasks found for similarity analysis")
                return {
                    "error": "No tasks found",
                    "totalTasksAnalyzed": 0,
                    "totalPairsCompared": 0
                }
            
            logger.info(f"Found {len(tasks)} tasks for similarity analysis.")
            
            # Initialize similarity module
            similarity_module = TaskSimilarityModule(use_dspy=use_dspy)
            
            # Generate similarity analysis
            analysis_report = similarity_module.analyze_task_similarities(tasks)
            
            # Save report to file
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            with open(output_file, 'w') as f:
                json.dump(analysis_report, f, indent=2)
            
            logger.info(f"Task similarity analysis completed. Report saved to {output_file}")
            
            return analysis_report
            
        except Exception as e:
            error_msg = f"Failed to analyze task similarities: {str(e)}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)
    
    def _collect_dependencies(self, all_tasks: List[Dict], dependency_ids: List[int], result: Set[int]) -> None:
        """Recursively collect all dependencies for a set of task IDs.
        
        Args:
            all_tasks: List of all tasks
            dependency_ids: List of dependency IDs to collect
            result: Set to store collected dependency IDs
        """
        for dep_id in dependency_ids:
            if dep_id not in result:
                result.add(dep_id)
                dep_task = find_task_by_id(all_tasks, dep_id)
                if dep_task and 'dependencies' in dep_task and dep_task['dependencies']:
                    self._collect_dependencies(all_tasks, dep_task['dependencies'], result)
    
    def show_next_task(self) -> Optional[Dict]:
        """Show the next task to work on based on priority and dependencies.
        
        Returns:
            The next task to work on, or None if no eligible tasks
        """
        try:
            data = read_json(self.tasks_file)
            if not data or 'tasks' not in data:
                raise ValueError(f"No valid tasks found in {self.tasks_file}")

            # Get completed task IDs
            completed_task_ids = {
                task['id'] for task in data['tasks']
                if task['status'] == TaskStatus.DONE
            }

            # Filter for eligible tasks (pending/in-progress with satisfied dependencies)
            eligible_tasks = [
                task for task in data['tasks']
                if (task['status'] in (TaskStatus.PENDING, TaskStatus.IN_PROGRESS) and
                    all(dep_id in completed_task_ids for dep_id in task.get('dependencies', [])))
            ]

            if not eligible_tasks:
                if self.display_output:
                    display_info("No eligible tasks found. All tasks are either completed or blocked by dependencies.")
                return None

            # Sort by priority, dependency count, and ID
            priority_values = {
                TaskPriority.HIGH: 3,
                TaskPriority.MEDIUM: 2,
                TaskPriority.LOW: 1
            }

            def task_sort_key(task: Dict) -> Tuple[int, int, int]:
                priority = priority_values.get(task.get('priority', TaskPriority.MEDIUM), 2)
                dep_count = len(task.get('dependencies', []))
                return (-priority, dep_count, task['id'])

            next_task = min(eligible_tasks, key=task_sort_key)
            
            if self.display_output:
                display_info("Next task to work on:")
                display_task_details(next_task)
                
            return next_task

        except Exception as e:
            logger.error(f"Error showing next task: {e}")
            if self.display_output:
                display_error(f"Failed to show next task: {e}")
            raise
    
    def show_task(self, task_id: Union[str, int]) -> Optional[Dict]:
        """Show detailed information about a specific task.
        
        Returns:
            The task details, or None if not found
        """
        try:
            task_id = validate_task_id(task_id)
            
            data = read_json(self.tasks_file)
            if not data or 'tasks' not in data:
                raise ValueError(f"No valid tasks found in {self.tasks_file}")
            
            task = find_task_by_id(data['tasks'], task_id)
            if not task:
                raise ValueError(f"Task {task_id} not found")
            
            if self.display_output:
                display_task_details(task)
            
            return task
            
        except Exception as e:
            logger.error(f"Error showing task: {e}")
            if self.display_output:
                display_error(f"Failed to show task: {e}")
            raise
    
    async def add_task(
        self,
        prompt: str,
        dependencies: List[int] = None,
        priority: str = "medium"
    ) -> Dict:
        """Add a new task using AI.
        
        Args:
            prompt: Description of the task to add
            dependencies: List of task IDs this task depends on
            priority: Task priority (high, medium, low)
            
        Returns:
            The newly created task
        """
        try:
            logger.info(f"Adding new task: {prompt}")
            
            # Read existing tasks
            data = read_json(self.tasks_file)
            if not data:
                data = {"tasks": []}
            
            # Generate task details using AI
            task_details = await ai_services.generate_task_details(prompt)
            
            # Create new task
            new_task = {
                "id": len(data["tasks"]) + 1,
                "title": task_details["title"],
                "description": task_details["description"],
                "details": task_details["details"],
                "testStrategy": task_details["testStrategy"],
                "dependencies": dependencies or [],
                "priority": priority,
                "status": TaskStatus.PENDING
            }
            
            # Add task to list
            data["tasks"].append(new_task)
            
            # Write updated tasks
            write_json(self.tasks_file, data)
            
            # Regenerate task files
            await self.generate_task_files()
            
            if self.display_output:
                display_success(f"Successfully added task {new_task['id']}")
                display_task_details(new_task)
            
            return new_task
            
        except Exception as e:
            logger.error(f"Error adding task: {e}")
            if self.display_output:
                display_error(f"Failed to add task: {e}")
            raise
    
    def review_complexity_recommendations(
        self,
        report_file: str = "tasks/task-complexity-report.json",
        threshold: float = 5.0,
        non_interactive: bool = False
    ) -> List[Dict[str, Any]]:
        """Review task complexity recommendations and approve tasks for expansion.
        
        Args:
            report_file: Path to the complexity report file
            threshold: Complexity score threshold for recommending expansion
            non_interactive: If True, approve all recommendations above threshold
            
        Returns:
            List of approved task expansions
        """
        try:
            # Read the complexity report
            if not os.path.exists(report_file):
                raise ValueError(f"Complexity report file not found: {report_file}")
            
            with open(report_file, "r") as f:
                report = json.load(f)
            
            if "complexityAnalysis" not in report:
                raise ValueError(f"Invalid complexity report format in {report_file}")
            
            # Filter tasks above threshold
            tasks_to_review = [
                task for task in report["complexityAnalysis"]
                if task.get("complexityScore", 0) >= threshold and task.get("recommendedSubtasks", 0) > 0
            ]
            
            if not tasks_to_review:
                if self.display_output:
                    display_info(f"No tasks found with complexity score >= {threshold}")
                return []
            
            approved_tasks = []
            
            # In non-interactive mode, approve all tasks above threshold
            if non_interactive:
                approved_tasks = tasks_to_review
                if self.display_output:
                    display_info(f"Auto-approved {len(approved_tasks)} tasks for expansion")
                return approved_tasks
            
            # Interactive review
            if self.display_output:
                from rich.panel import Panel
                from rich.text import Text
                from rich.columns import Columns
                from rich.padding import Padding
                
                console = Console()
                
                # Display header
                console.print()
                display_info(f"Found {len(tasks_to_review)} tasks with complexity score >= {threshold}")
                console.print(Panel(
                    "[bold]Review each task and approve for expansion[/bold]",
                    border_style="blue",
                    expand=False
                ))
                console.print()
                
                for task in tasks_to_review:
                    task_id = task.get("taskId")
                    title = task.get("taskTitle", "Unknown")
                    score = task.get("complexityScore", 0)
                    subtasks = task.get("recommendedSubtasks", 0)
                    prompt = task.get("expansionPrompt", "")
                    reasoning = task.get("reasoning", "")
                    
                    # Create score indicator with color based on complexity
                    score_color = "green" if score < 6 else "yellow" if score < 8 else "red"
                    score_text = Text(f"{score}/10", style=f"bold {score_color}")
                    
                    # Create task header
                    task_header = Panel(
                        f"[bold cyan]Task {task_id}:[/bold cyan] [bold]{title}[/bold]",
                        border_style="cyan",
                        expand=False
                    )
                    
                    # Create complexity panel
                    complexity_panel = Panel(
                        Columns([
                            f"[bold]Complexity:[/bold] {score_text}",
                            f"[bold]Subtasks:[/bold] {subtasks}"
                        ]),
                        title="Complexity",
                        border_style="blue",
                        expand=False
                    )
                    
                    # Create reasoning panel
                    reasoning_panel = Panel(
                        Text(reasoning, justify="left"),
                        title="Reasoning",
                        border_style="blue",
                        expand=False
                    )
                    
                    # Create expansion prompt panel
                    prompt_panel = Panel(
                        Text(prompt, justify="left"),
                        title="Expansion Prompt",
                        border_style="green",
                        expand=False
                    )
                    
                    # Display all panels
                    console.print(task_header)
                    console.print(complexity_panel)
                    console.print(reasoning_panel)
                    console.print(prompt_panel)
                    
                    # Ask for approval with better formatting
                    console.print()
                    approve = Confirm.ask("[bold]Approve this task for expansion?[/bold]")
                    if approve:
                        approved_tasks.append(task)
                        console.print("[bold green]✓ Task approved for expansion[/bold green]")
                    else:
                        console.print("[bold yellow]✗ Task skipped[/bold yellow]")
                    
                    # Add separator between tasks
                    console.print("\n" + "─" * 80 + "\n")
            
            return approved_tasks
            
        except Exception as e:
            logger.error(f"Error reviewing recommendations: {e}")
            if self.display_output:
                display_error(f"Failed to review recommendations: {e}")
            raise
    
    async def sync_tasks(
        self,
        system: Optional[str] = None,
        task_id: Optional[Union[str, int]] = None,
        direction: str = "bidirectional",
        config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Synchronize tasks with external systems.
        
        Args:
            system: External system to sync with (if None, sync with all configured systems)
            task_id: ID of the task to sync (if None, sync all tasks)
            direction: Synchronization direction ('local_to_remote', 'remote_to_local', 'bidirectional')
            config: Configuration for external systems
            
        Returns:
            Synchronization results
        """
        try:
            from .sync_manager import SyncManager
            from .external_integration import ExternalSystem, SyncDirection
            
            # Validate direction
            if direction not in (SyncDirection.LOCAL_TO_REMOTE, SyncDirection.REMOTE_TO_LOCAL, SyncDirection.BIDIRECTIONAL):
                direction = SyncDirection.BIDIRECTIONAL
            
            # Initialize config if not provided
            if config is None:
                config = {}
            
            # Get credentials from environment if not in config
            import os
            
            # NextCloud credentials
            if "nextcloud" not in config:
                config["nextcloud"] = {
                    "host": os.getenv("NEXTCLOUD_HOST"),
                    "username": os.getenv("NEXTCLOUD_USERNAME"),
                    "password": os.getenv("NEXTCLOUD_PASSWORD"),
                    "token": os.getenv("NEXTCLOUD_TOKEN")
                }
            
            # Initialize sync manager
            sync_manager = SyncManager(
                tasks_file=self.tasks_file,
                nextcloud_host=config.get("nextcloud", {}).get("host"),
                nextcloud_username=config.get("nextcloud", {}).get("username"),
                nextcloud_password=config.get("nextcloud", {}).get("password"),
                nextcloud_token=config.get("nextcloud", {}).get("token")
            )
            
            # Sync tasks
            if task_id:
                # Validate task ID
                from .utils import validate_task_id
                task_id = validate_task_id(task_id)
                
                # Sync specific task
                result = await sync_manager.sync_task(task_id, direction)
            else:
                # Sync all tasks
                result = await sync_manager.sync_all(direction)
            
            # Display results if needed
            if self.display_output:
                from rich.console import Console
                from rich.table import Table
                
                console = Console()
                console.print()
                console.print("[bold]Synchronization Results:[/bold]")
                console.print("------------------------")
                
                if "status" in result:
                    status_color = "green" if result["status"] == "success" else "red"
                    console.print(f"Status: [{status_color}]{result['status']}[/{status_color}]")
                
                if "message" in result:
                    console.print(f"Message: {result['message']}")
                
                if "total" in result:
                    console.print(f"Total tasks: {result['total']}")
                    console.print(f"Synced: {result['synced']}")
                    console.print(f"Errors: {result['errors']}")
                    console.print(f"Conflicts: {result['conflicts']}")
                    console.print(f"Skipped: {result['skipped']}")
                
                if "details" in result and result["details"]:
                    console.print()
                    console.print("[bold]Details:[/bold]")
                    
                    table = Table(show_header=True)
                    table.add_column("Task ID")
                    table.add_column("System")
                    table.add_column("Status")
                    table.add_column("Message")
                    
                    for detail in result["details"]:
                        status = detail.get("status", "")
                        status_color = "green" if status == "success" else "red" if status == "error" else "yellow"
                        
                        table.add_row(
                            str(detail.get("task_id", "")),
                            detail.get("system", ""),
                            f"[{status_color}]{status}[/{status_color}]",
                            detail.get("message", "")
                        )
                    
                    console.print(table)
            
            return result
            
        except Exception as e:
            logger.error(f"Error syncing tasks: {e}")
            if self.display_output:
                display_error(f"Failed to sync tasks: {e}")
            raise
    
    async def resolve_conflict(
        self,
        task_id: Union[str, int],
        system: str,
        resolution: str = "local",
        config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Resolve a synchronization conflict.
        
        Args:
            task_id: ID of the task with conflict
            system: External system identifier
            resolution: Conflict resolution strategy ('local', 'remote', or 'merge')
            config: Configuration for external systems
            
        Returns:
            Resolution results
        """
        try:
            from .sync_manager import SyncManager
            
            # Validate task ID
            from .utils import validate_task_id
            task_id = validate_task_id(task_id)
            
            # Initialize config if not provided
            if config is None:
                config = {}
            
            # Get credentials from environment if not in config
            import os
            
            # NextCloud credentials
            if "nextcloud" not in config:
                config["nextcloud"] = {
                    "host": os.getenv("NEXTCLOUD_HOST"),
                    "username": os.getenv("NEXTCLOUD_USERNAME"),
                    "password": os.getenv("NEXTCLOUD_PASSWORD"),
                    "token": os.getenv("NEXTCLOUD_TOKEN")
                }
            
            # Initialize sync manager
            sync_manager = SyncManager(
                tasks_file=self.tasks_file,
                nextcloud_host=config.get("nextcloud", {}).get("host"),
                nextcloud_username=config.get("nextcloud", {}).get("username"),
                nextcloud_password=config.get("nextcloud", {}).get("password"),
                nextcloud_token=config.get("nextcloud", {}).get("token")
            )
            
            # Resolve conflict
            result = await sync_manager.resolve_conflict(task_id, system, resolution)
            
            # Display results if needed
            if self.display_output:
                from rich.console import Console
                
                console = Console()
                console.print()
                console.print("[bold]Conflict Resolution Results:[/bold]")
                console.print("-----------------------------")
                
                status_color = "green" if result["status"] == "success" else "red"
                console.print(f"Status: [{status_color}]{result['status']}[/{status_color}]")
                
                if "message" in result:
                    console.print(f"Message: {result['message']}")
            
            return result
            
        except Exception as e:
            logger.error(f"Error resolving conflict: {e}")
            if self.display_output:
                display_error(f"Failed to resolve conflict: {e}")
            raise
    
    async def reintegrate_task_files(self, task_dir=None, force_update=True):
        """Reintegrate task files into the tasks.json file.
        
        Args:
            task_dir: Directory containing task files, defaults to self.tasks_dir
            force_update: Force update of research results regardless of content changes
            
        Returns:
            Dictionary with reintegration statistics
        """
        if task_dir is None:
            task_dir = self.tasks_dir
        
        tasks_file = os.path.join(task_dir, 'tasks.json')
        logger.info(f"Reading tasks from {tasks_file}")
        
        try:
            with open(tasks_file, 'r') as f:
                all_tasks = json.load(f)
        except FileNotFoundError:
            logger.error(f"Tasks file not found: {tasks_file}")
            return {
                "success": False,
                "error": f"Tasks file not found: {tasks_file}",
                "files_found": 0,
                "files_processed": 0,
                "tasks_updated": 0,
                "errors": 0
            }
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing tasks file: {e}")
            return {
                "success": False,
                "error": f"Error parsing tasks file: {e}",
                "files_found": 0,
                "files_processed": 0,
                "tasks_updated": 0,
                "errors": 0
            }
        
        # Get all task files
        task_files = glob.glob(os.path.join(task_dir, 'task_*.txt'))
        
        stats = {
            "files_found": len(task_files),
            "files_processed": 0,
            "tasks_updated": 0,
            "errors": 0
        }
        
        # Process each task file
        for task_file in task_files:
            logger.info(f"Processing task file: {os.path.basename(task_file)}")
            
            try:
                with open(task_file, 'r') as f:
                    content = f.read()
                
                # Parse the task file content
                task_data = self._parse_task_file_content(content)
                
                if 'id' not in task_data:
                    logger.error(f"Task ID not found in file: {task_file}")
                    stats["errors"] += 1
                    continue
                
                task_id = task_data['id']
                logger.debug(f"Processing task with ID: {task_id}")
                
                # Find the task in the tasks.json file
                task = next((t for t in all_tasks.get('tasks', []) if t.get('id') == task_id), None)
                
                if task:
                    logger.debug(f"Found task {task_id} in tasks.json")
                    updated = False
                    
                    # Update task fields if they've changed
                    for field in ['title', 'description', 'details', 'status', 'priority', 'dependencies', 'test_strategy']:
                        if field in task_data and task_data[field] != task.get(field, ''):
                            task[field] = task_data[field]
                            updated = True
                    
                    # Handle subtasks
                    if 'subtasks' in task_data:
                        logger.debug(f"Found {len(task_data['subtasks'])} subtasks in task file")
                        
                        # Initialize subtasks if not present
                        if 'subtasks' not in task:
                            task['subtasks'] = []
                        
                        # Process each subtask
                        for subtask_data in task_data['subtasks']:
                            subtask_id = subtask_data.get('id')
                            
                            if not subtask_id:
                                logger.warning(f"Subtask ID not found in task {task_id}")
                                continue
                            
                            logger.debug(f"Processing subtask {subtask_id} for task {task_id}")
                            
                            # Find the subtask in the task
                            subtask = next((s for s in task.get('subtasks', []) if s.get('id') == subtask_id), None)
                            
                            if subtask:
                                logger.debug(f"Found existing subtask {subtask_id} in tasks.json")
                                # Update existing subtask
                                for field in ['details', 'description', 'status', 'priority']:
                                    if field in subtask_data and subtask_data[field] != subtask.get(field, ''):
                                        subtask[field] = subtask_data[field]
                                        updated = True
                                
                                # Handle research results specifically
                                if 'research_results' in subtask_data:
                                    research_content = subtask_data['research_results']
                                    logger.info(f"Found research_results in subtask {subtask_id}, length: {len(research_content)}")
                                    
                                    # Print the first line of the research content for debugging
                                    lines = research_content.split('\n')
                                    if lines:
                                        first_line = lines[0].strip()
                                        logger.info(f"First line of research content: '{first_line}'")
                                    
                                    # Always create research structure if it doesn't exist
                                    if 'research' not in subtask:
                                        subtask['research'] = {}
                                        logger.info(f"Created new research structure for subtask {subtask_id}")
                                        updated = True
                                    
                                    # Only set summary if there's actual content
                                    if lines and lines[0].strip():
                                        # Check if the summary has changed or force update is enabled
                                        current_summary = subtask.get('research', {}).get('summary', '')
                                        if force_update or current_summary != lines[0].strip():
                                            subtask['research']['summary'] = lines[0].strip()
                                            logger.info(f"Set research summary to: '{lines[0].strip()}'")
                                            updated = True
                                    
                                    # Update the key findings with the full research content if force_update or content changed
                                    current_findings = subtask.get('research', {}).get('key_findings', '')
                                    if force_update or current_findings != research_content:
                                        subtask['research']['key_findings'] = research_content
                                        logger.info(f"Updated key_findings with research content")
                                        updated = True
                                        
                                        # Try to extract sections if they exist
                                        if '## Recommendations' in research_content or '**Recommendations' in research_content:
                                            logger.info("Found Recommendations section")
                                            # Split content by recommendations
                                            parts = research_content.split('## Recommendations', 1)
                                            if len(parts) == 1:
                                                parts = research_content.split('**Recommendations', 1)
                                            
                                            if len(parts) > 1:
                                                recommendations = parts[1]
                                                
                                                # Check if there are sources/resources
                                                if '## Sources' in recommendations:
                                                    rec_parts = recommendations.split('## Sources', 1)
                                                    recommendations = rec_parts[0].strip()
                                                    sources = rec_parts[1].strip()
                                                    subtask['research']['sources'] = sources
                                                    logger.info(f"Found Sources section, length: {len(sources)}")
                                                elif '## Resources' in recommendations:
                                                    rec_parts = recommendations.split('## Resources', 1)
                                                    recommendations = rec_parts[0].strip()
                                                    sources = rec_parts[1].strip()
                                                    subtask['research']['resources'] = sources
                                                    logger.info(f"Found Resources section, length: {len(sources)}")
                                                
                                                subtask['research']['implementation_recommendations'] = recommendations.strip()
                                                logger.info(f"Extracted recommendations, length: {len(recommendations.strip())}")
                                            else:
                                                subtask['research']['implementation_recommendations'] = research_content
                                                logger.info(f"No recommendations section found, using full content")
                                    else:
                                        logger.info(f"No changes detected in research content for subtask {subtask_id}")
                            else:
                                # Add new subtask
                                logger.debug(f"Adding new subtask {subtask_id} to task {task_id}")
                                task['subtasks'].append(subtask_data)
                                updated = True
                    
                    if updated:
                        stats["tasks_updated"] += 1
                        logger.info(f"Updated task {task_id} based on file content")
                else:
                    logger.warning(f"Task {task_id} not found in tasks.json")
                
                stats["files_processed"] += 1
                
            except Exception as e:
                logger.error(f"Error processing task file {task_file}: {e}")
                logger.exception(e)
                stats["errors"] += 1
        
        # Write the updated tasks back to the file
        if stats["tasks_updated"] > 0:
            logger.info(f"Writing {stats['tasks_updated']} updated tasks back to {tasks_file}")
            with open(tasks_file, 'w') as f:
                json.dump(all_tasks, f, indent=2)
        else:
            logger.info("No tasks were updated, skipping write to file")
        
        # Return success message with stats
        if self.display_output:
            display_success(
                f"Reintegration complete:\n"
                f"- Found {stats['files_found']} task files\n"
                f"- Processed {stats['files_processed']} files\n"
                f"- Updated {stats['tasks_updated']} tasks\n"
                f"- Encountered {stats['errors']} errors"
            )
        
        stats["success"] = True
        return stats
    
    async def reintegrate_pdd_files(self, pdd_dir="pdds"):
        """Reintegrate PDD files into the processes.json file.
        
        Args:
            pdd_dir: Directory containing PDD files, defaults to 'pdds'
            
        Returns:
            Dictionary with reintegration statistics
        """
        processes_file = os.path.join(pdd_dir, 'processes.json')
        logger.info(f"Reading processes from {processes_file}")
        
        try:
            if not os.path.exists(pdd_dir):
                logger.error(f"PDD directory not found: {pdd_dir}")
                return {
                    "success": False,
                    "error": f"PDD directory not found: {pdd_dir}",
                    "files_found": 0,
                    "files_processed": 0,
                    "processes_updated": 0,
                    "errors": 0
                }
            
            if not os.path.exists(processes_file):
                logger.error(f"Processes file not found: {processes_file}")
                return {
                    "success": False,
                    "error": f"Processes file not found: {processes_file}",
                    "files_found": 0,
                    "files_processed": 0,
                    "processes_updated": 0,
                    "errors": 0
                }
                
            with open(processes_file, 'r') as f:
                all_processes = json.load(f)
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing processes file: {e}")
            return {
                "success": False,
                "error": f"Error parsing processes file: {e}",
                "files_found": 0,
                "files_processed": 0,
                "processes_updated": 0,
                "errors": 0
            }
        
        # Get all PDD files
        pdd_files = glob.glob(os.path.join(pdd_dir, '*_pdd.txt'))
        
        stats = {
            "files_found": len(pdd_files),
            "files_processed": 0,
            "processes_updated": 0,
            "errors": 0
        }
        
        # Process each PDD file
        for pdd_file in pdd_files:
            logger.info(f"Processing PDD file: {os.path.basename(pdd_file)}")
            
            try:
                with open(pdd_file, 'r') as f:
                    content = f.read()
                
                # Parse the PDD file content
                process_data = self._parse_pdd_file_content(content)
                
                if 'process_id' not in process_data:
                    logger.error(f"Process ID not found in file: {pdd_file}")
                    stats["errors"] += 1
                    continue
                
                process_id = process_data['process_id']
                logger.debug(f"Processing process with ID: {process_id}")
                
                # Find the process in the processes.json file
                processes = all_processes.get('processes', [])
                process = next((p for p in processes if p.get('process_id') == process_id or p.get('id') == process_id), None)
                
                if process:
                    logger.debug(f"Found process {process_id} in processes.json")
                    updated = False
                    
                    # Update process fields if they've changed
                    for field in ['title', 'description', 'complexity', 'dependencies', 'resources', 'parameters', 'variations']:
                        if field in process_data and process_data[field] != process.get(field, ''):
                            process[field] = process_data[field]
                            updated = True
                    
                    if updated:
                        stats["processes_updated"] += 1
                else:
                    # Process not found, add it as a new process
                    logger.info(f"Process {process_id} not found in processes.json, adding it")
                    
                    # Ensure process has all required fields
                    new_process = {
                        'process_id': process_id,
                        'title': process_data.get('title', ''),
                        'description': process_data.get('description', ''),
                        'complexity': process_data.get('complexity', ''),
                        'dependencies': process_data.get('dependencies', []),
                        'resources': process_data.get('resources', []),
                        'parameters': process_data.get('parameters', {}),
                        'variations': process_data.get('variations', [])
                    }
                    
                    # Add the new process to the list
                    processes.append(new_process)
                    stats["processes_updated"] += 1
                
                stats["files_processed"] += 1
                
            except Exception as e:
                logger.error(f"Error processing PDD file {pdd_file}: {e}")
                stats["errors"] += 1
        
        # Write updated processes back to file if any were updated
        if stats["processes_updated"] > 0:
            logger.info(f"Writing updated processes to {processes_file}")
            os.makedirs(os.path.dirname(processes_file), exist_ok=True)
            with open(processes_file, 'w') as f:
                json.dump(all_processes, f, indent=2)
        else:
            logger.info("No processes were updated, skipping write to file")
        
        # Return success message with stats
        if self.display_output:
            display_success(
                f"PDD reintegration complete:\n"
                f"- Found {stats['files_found']} PDD files\n"
                f"- Processed {stats['files_processed']} files\n"
                f"- Updated {stats['processes_updated']} processes\n"
                f"- Encountered {stats['errors']} errors"
            )
        
        stats["success"] = True
        return stats
    
    def _parse_pdd_file_content(self, content):
        """Parse PDD file content into a structured dictionary.
        
        Args:
            content: String content of the PDD file
            
        Returns:
            Dictionary with parsed PDD data
        """
        lines = content.split('\n')
        process_data = {}
        
        # Extract metadata from header lines
        current_section = None
        section_content = []
        
        for line in lines:
            # Check for metadata lines at the top (# Key: Value)
            if line.startswith('# '):
                parts = line[2:].split(':', 1)
                if len(parts) == 2:
                    key = parts[0].strip().lower().replace(' ', '_')
                    value = parts[1].strip()
                    
                    # Handle special fields
                    if key == 'dependencies':
                        if value:
                            process_data[key] = [dep.strip() for dep in value.split(',')]
                        else:
                            process_data[key] = []
                    else:
                        process_data[key] = value
            
            # Check for section headers (## Section)
            elif line.startswith('## '):
                # Save previous section if exists
                if current_section:
                    if current_section == 'description':
                        process_data[current_section] = '\n'.join(section_content).strip()
                    elif current_section == 'resources_required':
                        process_data['resources'] = self._parse_list_items(section_content)
                    elif current_section == 'parameters':
                        process_data['parameters'] = self._parse_parameters(section_content)
                    elif current_section == 'variations':
                        process_data['variations'] = self._parse_variations(section_content)
                
                # Start new section
                current_section = line[3:].strip().lower().replace(' ', '_')
                section_content = []
            
            # Add content to current section
            elif current_section:
                section_content.append(line)
        
        # Process the last section
        if current_section:
            if current_section == 'description':
                process_data[current_section] = '\n'.join(section_content).strip()
            elif current_section == 'resources_required':
                process_data['resources'] = self._parse_list_items(section_content)
            elif current_section == 'parameters':
                process_data['parameters'] = self._parse_parameters(section_content)
            elif current_section == 'variations':
                process_data['variations'] = self._parse_variations(section_content)
        
        return process_data
    
    def _parse_list_items(self, lines):
        """Parse list items from content lines.
        
        Args:
            lines: List of content lines
            
        Returns:
            List of items
        """
        items = []
        for line in lines:
            if line.strip().startswith('- '):
                items.append(line.strip()[2:])
        return items
    
    def _parse_parameters(self, lines):
        """Parse parameters from content lines.
        
        Args:
            lines: List of content lines
            
        Returns:
            Dictionary of parameters
        """
        parameters = {}
        for line in lines:
            if line.strip().startswith('- '):
                parts = line.strip()[2:].split(':', 1)
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = parts[1].strip()
                    parameters[key] = value
        return parameters
    
    def _parse_variations(self, lines):
        """Parse variations from content lines.
        
        Args:
            lines: List of content lines
            
        Returns:
            List of variation dictionaries
        """
        variations = []
        current_variation = None
        variation_description = []
        
        for line in lines:
            if line.strip().startswith('### '):
                # Save previous variation if exists
                if current_variation:
                    variations.append({
                        'name': current_variation,
                        'description': '\n'.join(variation_description).strip()
                    })
                
                # Start new variation
                current_variation = line.strip()[4:]
                variation_description = []
            elif current_variation:
                variation_description.append(line)
        
        # Add the last variation
        if current_variation:
            variations.append({
                'name': current_variation,
                'description': '\n'.join(variation_description).strip()
            })
        
        return variations
    
    def _analyze_feedback_ripple_effects(self, feedback_by_task: Dict[int, List[str]], all_tasks: List[Dict[str, Any]]) -> Dict[int, Dict[str, Any]]:
        """Analyze feedback comments to identify tasks affected by ripple effects.
        
        Args:
            feedback_by_task: Dictionary mapping task IDs to their feedback comments
            all_tasks: List of all tasks in the project
            
        Returns:
            Dictionary mapping task IDs to information about how they're affected
        """
        from .ai_services import anthropic_client
        import anthropic
        
        if not anthropic_client:
            logger.warning("Claude service not available for analyzing feedback ripple effects. Skipping.")
            return {task_id: {"task": find_task_by_id(all_tasks, task_id), "feedback": comments, "ripple_source": None} 
                   for task_id, comments in feedback_by_task.items()}
        
        affected_tasks = {}
        
        # First, add all tasks with direct feedback
        for task_id, comments in feedback_by_task.items():
            task = find_task_by_id(all_tasks, task_id)
            if task:
                affected_tasks[task_id] = {
                    "task": task,
                    "feedback": comments,
                    "ripple_source": None  # No ripple source for direct feedback
                }
        
        # For each task with feedback, analyze potential ripple effects
        for task_id, comments in feedback_by_task.items():
            task = find_task_by_id(all_tasks, task_id)
            if not task:
                continue
                
            # Prepare task data for analysis
            task_json = json.dumps(task, indent=2)
            feedback_text = "\n".join([f"- {comment}" for comment in comments])
            
            # Get broader context for the task
            broader_context = self._gather_task_context(task)
            
            # Create the prompt for ripple effect analysis
            system_prompt = """You are a technical lead analyzing how feedback on one task might affect other tasks in a project.
Given a task, feedback comments, and broader project context, identify which other tasks would need to be modified to maintain consistency.

Focus on identifying:
1. Tasks that depend on the current task and would need updates if the current task changes
2. Tasks that share similar structures or concepts that should be updated consistently
3. Tasks that might break if the current task is modified according to the feedback

Return your analysis as a JSON array of affected task IDs with explanations:
[
  {
    "task_id": 5,
    "reason": "This task depends on the data structures defined in the current task"
  },
  {
    "task_id": 8,
    "reason": "This task uses similar List[str] fields that should be updated consistently"
  }
]

Only include tasks that genuinely need updates based on the feedback. Don't include tasks that would be unaffected."""
            
            # Create message parameters
            if hasattr(anthropic, 'AnthropicBedrock') and isinstance(anthropic_client, anthropic.AnthropicBedrock):
                messages = [
                    {
                        "role": "assistant",
                        "content": f"I understand. I'll analyze which other tasks would be affected by this feedback."
                    },
                    {
                        "role": "user",
                        "content": f"""Here is the task that received feedback:

{task_json}

Here is the feedback:
{feedback_text}

Here is the broader context for this task:
{broader_context}

Based on this information, which other tasks in the project would need to be modified to maintain consistency if this feedback is implemented? Return your analysis as a JSON array as specified."""
                    }
                ]
                message_params = {
                    "model": config.claude_model,
                    "max_tokens": config.max_tokens,
                    "temperature": 0.2,
                    "messages": messages
                }
            else:
                message_params = {
                    "model": config.claude_model,
                    "max_tokens": config.max_tokens,
                    "temperature": 0.2,
                    "system": system_prompt,
                    "messages": [{
                        "role": "user",
                        "content": f"""Here is the task that received feedback:

{task_json}

Here is the feedback:
{feedback_text}

Here is the broader context for this task:
{broader_context}

Based on this information, which other tasks in the project would need to be modified to maintain consistency if this feedback is implemented? Return your analysis as a JSON array as specified."""
                    }]
                }
            
            try:
                # Call appropriate client
                if isinstance(anthropic_client, anthropic.AnthropicBedrock):
                    response = anthropic_client.messages.create(**message_params)
                    response_content = response.content[0].text
                else:
                    response = anthropic_client.messages.create(**message_params)
                    response_content = response.content[0].text
                
                # Extract JSON from response
                json_start = response_content.find('[')
                json_end = response_content.rfind(']') + 1
                
                if json_start == -1 or json_end == 0:
                    logger.warning(f"No valid JSON found in ripple effect analysis for task {task_id}")
                    continue
                
                ripple_effects = json.loads(response_content[json_start:json_end])
                
                # Add affected tasks to the result
                for effect in ripple_effects:
                    if 'task_id' in effect and isinstance(effect['task_id'], (int, str)):
                        affected_task_id = int(effect['task_id'])
                        affected_task = find_task_by_id(all_tasks, affected_task_id)
                        
                        if affected_task and affected_task_id not in affected_tasks:
                            affected_tasks[affected_task_id] = {
                                "task": affected_task,
                                "feedback": [],  # No direct feedback
                                "ripple_source": {
                                    "source_task_id": task_id,
                                    "reason": effect.get('reason', "Related to changes in task " + str(task_id))
                                }
                            }
                            logger.info(f"Identified ripple effect from task {task_id} to task {affected_task_id}: {effect.get('reason')}")
                
            except Exception as e:
                logger.error(f"Error analyzing ripple effects for task {task_id}: {e}")
        
        return affected_tasks
    
    def _apply_feedback_changes(self, affected_tasks: Dict[int, Dict[str, Any]], all_tasks: List[Dict[str, Any]]) -> Tuple[Dict[int, Dict[str, Any]], Dict[str, int]]:
        """Apply feedback changes to all affected tasks.
        
        Args:
            affected_tasks: Dictionary mapping task IDs to information about how they're affected
            all_tasks: List of all tasks in the project
            
        Returns:
            Tuple containing updated tasks and statistics
        """
        from .ai_services import anthropic_client
        import anthropic
        
        stats = {
            "tasks_updated": 0,
            "ripple_effects": 0
        }
        
        if not anthropic_client:
            logger.warning("Claude service not available for applying feedback changes. Skipping.")
            return affected_tasks, stats
        
        # Group tasks by ripple source to process them together
        ripple_groups = {}
        direct_feedback_tasks = {}
        
        for task_id, info in affected_tasks.items():
            if info["ripple_source"] is None:
                # Task with direct feedback
                direct_feedback_tasks[task_id] = info
            else:
                # Task affected by ripple effect
                source_id = info["ripple_source"]["source_task_id"]
                if source_id not in ripple_groups:
                    ripple_groups[source_id] = []
                ripple_groups[source_id].append((task_id, info))
        
        # First, process tasks with direct feedback
        for task_id, info in direct_feedback_tasks.items():
            task = info["task"]
            feedback = info["feedback"]
            
            # Process the feedback
            original_task = json.dumps(task)
            updated_task = self._process_task_feedback(task, feedback)
            
            # Check if task was actually modified
            if json.dumps(updated_task) != original_task:
                # Update the task in the affected_tasks dictionary
                affected_tasks[task_id]["task"] = updated_task
                
                # Update the task in the all_tasks list
                task_index = next((i for i, t in enumerate(all_tasks) if t.get('id') == task_id), None)
                if task_index is not None:
                    all_tasks[task_index] = updated_task
                
                stats["tasks_updated"] += 1
                logger.info(f"Updated task {task_id} based on direct feedback")
        
        # Then, process tasks affected by ripple effects
        for source_id, affected_group in ripple_groups.items():
            # Only process ripple effects if the source task was updated
            if source_id in direct_feedback_tasks and source_id in affected_tasks:
                source_task = affected_tasks[source_id]["task"]
                source_feedback = affected_tasks[source_id]["feedback"]
                
                # Process each affected task
                for affected_id, affected_info in affected_group:
                    affected_task = affected_info["task"]
                    ripple_reason = affected_info["ripple_source"]["reason"]
                    
                    # Create a specialized prompt for applying ripple effects
                    affected_task_json = json.dumps(affected_task, indent=2)
                    source_task_json = json.dumps(source_task, indent=2)
                    feedback_text = "\n".join([f"- {comment}" for comment in source_feedback])
                    
                    system_prompt = """You are a technical lead applying consistent changes across multiple tasks in a project.
A source task has been updated based on feedback, and now you need to update a related task to maintain consistency.

You will be given:
1. The original source task that received feedback
2. The updated source task after feedback was applied
3. The feedback that was applied to the source task
4. A related task that needs to be updated for consistency
5. The reason why this related task needs to be updated

Your job is to update the related task to maintain consistency with the changes made to the source task.
Return the updated related task as a valid JSON object.
Do not add any explanation or commentary outside the JSON object."""
                    
                    # Create message parameters
                    if hasattr(anthropic, 'AnthropicBedrock') and isinstance(anthropic_client, anthropic.AnthropicBedrock):
                        messages = [
                            {
                                "role": "assistant",
                                "content": f"I understand. I'll update the related task to maintain consistency with the changes made to the source task."
                            },
                            {
                                "role": "user",
                                "content": f"""Here is the original source task (ID: {source_id}) that received feedback:
{source_task_json}

Here is the feedback that was applied to the source task:
{feedback_text}

Here is the related task (ID: {affected_id}) that needs to be updated for consistency:
{affected_task_json}

Reason why this task needs to be updated:
{ripple_reason}

Please update the related task to maintain consistency with the changes made to the source task. Return the updated task as a valid JSON object."""
                            }
                        ]
                        message_params = {
                            "model": config.claude_model,
                            "max_tokens": config.max_tokens,
                            "temperature": 0.2,
                            "messages": messages
                        }
                    else:
                        message_params = {
                            "model": config.claude_model,
                            "max_tokens": config.max_tokens,
                            "temperature": 0.2,
                            "system": system_prompt,
                            "messages": [{
                                "role": "user",
                                "content": f"""Here is the original source task (ID: {source_id}) that received feedback:
{source_task_json}

Here is the feedback that was applied to the source task:
{feedback_text}

Here is the related task (ID: {affected_id}) that needs to be updated for consistency:
{affected_task_json}

Reason why this task needs to be updated:
{ripple_reason}

Please update the related task to maintain consistency with the changes made to the source task. Return the updated task as a valid JSON object."""
                            }]
                        }
                    
                    try:
                        # Call appropriate client
                        if isinstance(anthropic_client, anthropic.AnthropicBedrock):
                            response = anthropic_client.messages.create(**message_params)
                            response_content = response.content[0].text
                        else:
                            response = anthropic_client.messages.create(**message_params)
                            response_content = response.content[0].text
                        
                        # Extract JSON from response
                        json_start = response_content.find('{')
                        json_end = response_content.rfind('}') + 1
                        
                        if json_start == -1 or json_end == 0:
                            logger.error(f"No valid JSON found in ripple effect update for task {affected_id}")
                            continue
                        
                        updated_affected_task = json.loads(response_content[json_start:json_end])
                        
                        # Validate that we have a valid task structure
                        if not isinstance(updated_affected_task, dict) or 'id' not in updated_affected_task:
                            logger.error(f"Invalid task structure returned for ripple effect update of task {affected_id}")
                            continue
                        
                        # Check if task was actually modified
                        if json.dumps(updated_affected_task) != json.dumps(affected_task):
                            # Update the task in the affected_tasks dictionary
                            affected_tasks[affected_id]["task"] = updated_affected_task
                            
                            # Update the task in the all_tasks list
                            task_index = next((i for i, t in enumerate(all_tasks) if t.get('id') == affected_id), None)
                            if task_index is not None:
                                all_tasks[task_index] = updated_affected_task
                            
                            stats["tasks_updated"] += 1
                            stats["ripple_effects"] += 1
                            logger.info(f"Updated task {affected_id} based on ripple effect from task {source_id}")
                        
                    except Exception as e:
                        logger.error(f"Error applying ripple effect from task {source_id} to task {affected_id}: {e}")
        
        return affected_tasks, stats
    
    def _parse_task_file_content(self, content: str) -> Dict[str, Any]:
        """Parse task file content into a structured dictionary.
        
        Args:
            content: The content of the task file
            
        Returns:
            Dictionary containing the parsed task data
        """
        task_data = {}
        subtasks = []
        current_subtask = None
        section = None
        section_content = []
        feedback_comments = []
        
        # Split the content into lines
        lines = content.split('\n')
        
        # Debug: Log the first few lines to identify the file
        if len(lines) > 2:
            logger.debug(f"Parsing file with ID: {lines[0]}, Title: {lines[1] if len(lines) > 1 else 'Unknown'}")
        
        # Special debug for task 11
        task_id = None
        for i, line in enumerate(lines):
            # Check for feedback comments enclosed in curly braces
            if line.strip().startswith('{') and line.strip().endswith('}'):
                feedback_comment = line.strip()[1:-1].strip()
                feedback_comments.append(feedback_comment)
                continue
            
            # Parse task metadata
            if line.startswith('# Task ID:'):
                task_id = int(line.replace('# Task ID:', '').strip())
                task_data['id'] = task_id
                logger.debug(f"Found Task ID: {task_data['id']}")
                if task_id == 11:
                    logger.info(f"Processing task 11 file, total lines: {len(lines)}")
            
            # Parse task metadata
            elif line.startswith('# Title:'):
                task_data['title'] = line.replace('# Title:', '').strip()
            elif line.startswith('# Status:'):
                task_data['status'] = line.replace('# Status:', '').strip()
            elif line.startswith('# Dependencies:'):
                deps_str = line.replace('# Dependencies:', '').strip()
                if deps_str.lower() != 'none':
                    # Extract numeric IDs from dependency strings like "1 (done)"
                    deps = []
                    for dep in deps_str.split(','):
                        dep = dep.strip()
                        if ' ' in dep:  # Format: "1 (done)"
                            dep_id = dep.split(' ')[0].strip()
                            if dep_id.isdigit():
                                deps.append(int(dep_id))
                        elif dep.isdigit():  # Format: "1"
                            deps.append(int(dep))
                        else:
                            deps.append(dep)
                    task_data['dependencies'] = deps
                else:
                    task_data['dependencies'] = []
            elif line.startswith('# Priority:'):
                task_data['priority'] = line.replace('# Priority:', '').strip()
            elif line.startswith('# Description:'):
                task_data['description'] = line.replace('# Description:', '').strip()
            
            # Handle sections
            elif line.startswith('# Details:'):
                section = 'details'
                section_content = []
            elif line.startswith('# Test Strategy:'):
                if section == 'details':
                    task_data['details'] = '\n'.join(section_content).strip()
                section = 'testStrategy'
                section_content = []
            elif line.startswith('# Subtasks:'):
                if section == 'testStrategy':
                    task_data['testStrategy'] = '\n'.join(section_content).strip()
                section = 'subtasks'
                section_content = []
            
            # Handle subtask metadata
            elif line.startswith('## ') and section == 'subtasks':
                # Save previous subtask if exists
                if current_subtask:
                    # If we were in the research section, save the research results
                    if section == 'subtask_research' and section_content:
                        research_content = '\n'.join(section_content).strip()
                        if research_content:
                            current_subtask['research_results'] = research_content
                            logger.info(f"Added research_results to subtask {current_subtask.get('id')}, length: {len(research_content)}")
                            lines = research_content.split('\n')
                            if lines:
                                logger.info(f"First line of research content: '{lines[0]}'")
                            
                            # Special debug for task 11
                            if task_id == 11:
                                logger.info(f"Task 11: Added research_results to subtask {current_subtask.get('id')}")
                                logger.info(f"Task 11: First 100 chars of research: {research_content[:100]}...")
                    
                    subtasks.append(current_subtask)
                
                # Parse subtask header: "## 1. Subtask Title [status]"
                parts = line.replace('## ', '').split('. ', 1)
                if len(parts) == 2:
                    subtask_id = int(parts[0])
                    title_status = parts[1]
                    
                    # Extract title and status
                    if '[' in title_status and ']' in title_status:
                        title = title_status.split('[')[0].strip()
                        status = title_status.split('[')[1].split(']')[0].strip()
                    else:
                        title = title_status.strip()
                        status = TaskStatus.PENDING
                    
                    current_subtask = {
                        'id': subtask_id,
                        'title': title,
                        'status': status
                    }
                    logger.debug(f"Found subtask: {line}")
                    
                    # Reset section
                    section = 'subtasks'
                    section_content = []
            elif line.startswith('### Dependencies:') and current_subtask:
                deps_str = line.replace('### Dependencies:', '').strip()
                if deps_str.lower() != 'none':
                    # Parse dependencies
                    deps = []
                    for dep in deps_str.split(','):
                        dep = dep.strip()
                        if '.' in dep:  # Format: "task_id.subtask_id"
                            parts = dep.split('.')
                            if len(parts) == 2:
                                deps.append(dep)
                        elif dep.isdigit():  # Format: "subtask_id"
                            deps.append(int(dep))
                        else:
                            deps.append(dep)
                    current_subtask['dependencies'] = deps
                else:
                    current_subtask['dependencies'] = []
            elif line.startswith('### Priority:') and current_subtask:
                current_subtask['priority'] = line.replace('### Priority:', '').strip()
            elif line.startswith('### Description:') and current_subtask:
                current_subtask['description'] = line.replace('### Description:', '').strip()
            elif line.startswith('### Details:') and current_subtask:
                section = 'subtask_details'
                section_content = []
            elif (line.startswith('### Research Results:') or 
                  line.startswith('## Research Results:') or 
                  line.startswith('### Research:') or 
                  line.startswith('## Research:')) and current_subtask:
                # Save subtask details if we were processing them
                if section == 'subtask_details' and current_subtask:
                    current_subtask['details'] = '\n'.join(section_content).strip()
                section = 'subtask_research'
                section_content = []
                logger.info(f"Found research results section for subtask {current_subtask.get('id')} at line {i}")
                
                # Special debug for task 11
                if task_id == 11:
                    logger.info(f"Task 11: Found research section at line {i}: {line}")
                    if i+1 < len(lines):
                        logger.info(f"Task 11: Next line: {lines[i+1]}")
            
            # Check for recommendation sections
            elif (line.startswith('## Recommendations') or 
                  line.startswith('**Recommendations') or
                  line.startswith('## Recommendation')) and section == 'subtask_research':
                logger.info(f"Found Recommendations section at line {i}")
            
            # Collect content for the current section
            elif section:
                if section == 'subtask_details' and current_subtask:
                    # Empty line after subtask details marks the end
                    section_content.append(line)
                else:
                    section_content.append(line)
        
        # Process the last section if any
        if section == 'details':
            task_data['details'] = '\n'.join(section_content).strip()
        elif section == 'testStrategy':
            task_data['testStrategy'] = '\n'.join(section_content).strip()
        elif section == 'subtask_details' and current_subtask:
            current_subtask['details'] = '\n'.join(section_content).strip()
            subtasks.append(current_subtask)
        elif section == 'subtask_research' and current_subtask:
            # Parse research results
            research_content = '\n'.join(section_content).strip()
            if research_content:
                current_subtask['research_results'] = research_content
                logger.info(f"Added research_results to subtask {current_subtask.get('id')}, length: {len(research_content)}")
                lines = research_content.split('\n')
                if lines:
                    logger.info(f"First line of research content: '{lines[0]}'")
                
                # Special debug for task 11
                if task_id == 11:
                    logger.info(f"Task 11: Added research_results to subtask {current_subtask.get('id')}")
                    logger.info(f"Task 11: First 100 chars of research: {research_content[:100]}...")
            subtasks.append(current_subtask)
        # Make sure to add the last subtask if it hasn't been added yet
        elif current_subtask and current_subtask not in subtasks:
            subtasks.append(current_subtask)
        
        # Add subtasks to task data if any
        if subtasks:
            task_data['subtasks'] = subtasks
            logger.debug(f"Total subtasks found: {len(subtasks)}")
        
        # Add feedback comments if any
        if feedback_comments:
            task_data['feedback_comments'] = feedback_comments
        
        return task_data
    
    def _format_research_as_markdown(self, research_results: Dict[str, Any]) -> str:
        """Format research results as markdown.
        
        Args:
            research_results: Research results to format
            
        Returns:
            Formatted markdown string
        """
        markdown_parts = []
        
        # Helper function to handle different types of data
        def format_content(content):
            if isinstance(content, list):
                return "\n".join(str(item) for item in content)
            elif isinstance(content, dict):
                return "\n".join(f"**{k}**: {v}" for k, v in content.items())
            else:
                return str(content)
        
        # Add summary
        if "summary" in research_results and research_results["summary"]:
            markdown_parts.append(f"{format_content(research_results['summary'])}\n")
        
        # Add key findings
        if "key_findings" in research_results and research_results["key_findings"]:
            markdown_parts.append(f"## Key Findings\n{format_content(research_results['key_findings'])}\n")
        
        # Add recommendations
        if "recommendations" in research_results and research_results["recommendations"]:
            markdown_parts.append(f"## Recommendations\n{format_content(research_results['recommendations'])}\n")
        
        # Add resources
        if "resources" in research_results and research_results["resources"]:
            markdown_parts.append(f"## Resources\n{format_content(research_results['resources'])}\n")
        
        # Add sources
        if "sources" in research_results and research_results["sources"]:
            markdown_parts.append(f"## Sources\n{format_content(research_results['sources'])}")
        
        return "\n".join(markdown_parts)
    
    def _gather_task_context(self, task: Dict[str, Any]) -> str:
        """Gather context for a task.
        
        Args:
            task: The task to gather context for
            
        Returns:
            String containing task context
        """
        context_parts = []
        
        # Add task information
        context_parts.append(f"Task {task.get('id')}: {task.get('title', '')}")
        context_parts.append(f"Description: {task.get('description', '')}")
        
        if task.get('details'):
            context_parts.append(f"Details: {task.get('details', '')}")
        
        # Add dependencies
        if task.get('dependencies'):
            # Get dependency tasks
            data = read_json(self.tasks_file)
            if data and 'tasks' in data:
                dependency_info = []
                for dep_id in task.get('dependencies', []):
                    dep_task = find_task_by_id(data['tasks'], dep_id)
                    if dep_task:
                        dependency_info.append(f"- Task {dep_id}: {dep_task.get('title', '')}")
                
                if dependency_info:
                    context_parts.append("\nDependencies:")
                    context_parts.extend(dependency_info)
        
        # Add PRD context if available
        try:
            prd_content = self._find_prd_content()
            if prd_content:
                context_parts.append("\nRelevant PRD Content:")
                context_parts.append(prd_content)
        except Exception as e:
            logger.warning(f"Error finding PRD content: {e}")
        
        return "\n".join(context_parts)
    
    def _gather_research_context(
        self, 
        task: Dict[str, Any], 
        subtask_id: Optional[int] = None,
        additional_context: Optional[str] = None
    ) -> str:
        """Gather context for research.
        
        Args:
            task: The task to research
            subtask_id: Optional ID of the subtask to research
            additional_context: Optional additional context to include
            
        Returns:
            String containing research context
        """
        context_parts = []
        
        # Find the subtask if specified
        subtask = None
        if subtask_id is not None:
            if 'subtasks' in task and task['subtasks']:
                subtask = next((s for s in task['subtasks'] if s.get('id') == subtask_id), None)
        
        # Get the target (task or subtask)
        target = subtask if subtask else task
        
        # Add task information
        context_parts.append(f"Task {task.get('id')}: {task.get('title', '')}")
        
        if subtask:
            context_parts.append(f"Subtask {subtask_id}: {subtask.get('title', '')}")
        
        # Add description
        if target.get('description'):
            context_parts.append(f"Description: {target.get('description', '')}")
        
        # Add details
        if target.get('details'):
            context_parts.append(f"Details: {target.get('details', '')}")
        
        # Add dependencies
        if task.get('dependencies'):
            # Get dependency tasks
            data = read_json(self.tasks_file)
            if data and 'tasks' in data:
                dependency_info = []
                for dep_id in task.get('dependencies', []):
                    dep_task = find_task_by_id(data['tasks'], dep_id)
                    if dep_task:
                        dependency_info.append(f"- Task {dep_id}: {dep_task.get('title', '')}")
                
                if dependency_info:
                    context_parts.append("\nDependencies:")
                    context_parts.extend(dependency_info)
        
        # Add additional context if provided
        if additional_context:
            context_parts.append(f"\nAdditional Context: {additional_context}")
        
        # Add PRD context if available
        try:
            prd_content = self._find_prd_content()
            if prd_content:
                context_parts.append("\nRelevant PRD Content:")
                context_parts.append(prd_content)
        except Exception as e:
            logger.warning(f"Error finding PRD content: {e}")
        
        return "\n".join(context_parts)
    
    def _is_research_task(self, task: Dict[str, Any], subtask_id: Optional[int] = None) -> bool:
        """Determine if a task or subtask is a research task.
        
        Args:
            task: The task to check
            subtask_id: Optional ID of the subtask to check
            
        Returns:
            True if the task or subtask is a research task, False otherwise
        """
        # Find the subtask if specified
        target = None
        if subtask_id is not None:
            if 'subtasks' in task and task['subtasks']:
                target = next((s for s in task['subtasks'] if s.get('id') == subtask_id), None)
        else:
            target = task
        
        if not target:
            return False
        
        # Check if this is a research task
        title = target.get('title', '').lower()
        description = target.get('description', '').lower()
        details = target.get('details', '').lower()
        
        return (
            'research' in title or 
            'evaluate' in title or 
            'compare' in title or
            'analyze' in title or
            'research' in description or
            'evaluate' in description or
            'compare' in description or
            'research' in details or
            'evaluate' in details or
            'compare' in details
        )
    
    def _update_task_with_research(
        self, 
        task_id: int, 
        research_results: Dict[str, str],
        subtask_id: Optional[int] = None
    ) -> None:
        """Update the task file with research results.
        
        Args:
            task_id: ID of the task to update
            research_results: Research results to add to the task
            subtask_id: Optional ID of the subtask to update
        """
        data = read_json(self.tasks_file)
        if not data or 'tasks' not in data:
            raise ValueError(f"No valid tasks found in {self.tasks_file}")

        # Find the task
        task = find_task_by_id(data['tasks'], task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")
        
        # Update the task with research results
        if subtask_id is not None:
            if 'subtasks' not in task:
                task['subtasks'] = []
            
            subtask = next((s for s in task['subtasks'] if s.get('id') == subtask_id), None)
            if not subtask:
                raise ValueError(f"Subtask {subtask_id} not found in task {task_id}")
            
            subtask['research'] = research_results
        else:
            task['research'] = research_results
        
        # Write updated tasks
        write_json(self.tasks_file, data)
    
    def _perform_actual_research(self, research_context: str, depth: int) -> Dict[str, str]:
        """Perform actual research for a research task.
        
        Args:
            research_context: Context for the research
            depth: Research depth (1-3)
            
        Returns:
            Dictionary containing research results
        """
        from .ai_services import perplexity_client
        from .config import config
        
        # Determine research prompt based on depth
        if depth == 1:
            depth_description = "Provide a basic overview of relevant technologies and approaches."
            detail_level = "brief"
        elif depth == 2:
            depth_description = "Provide a comprehensive analysis of relevant technologies, approaches, and best practices."
            detail_level = "moderate"
        else:  # depth == 3
            depth_description = "Provide an in-depth, thorough analysis of all relevant technologies, approaches, best practices, and cutting-edge techniques."
            detail_level = "extensive"
        
        # Check if this is NLP-related research
        is_nlp_research = (
            'nlp' in research_context.lower() or
            'natural language' in research_context.lower() or
            'embedding' in research_context.lower() or
            'semantic' in research_context.lower() or
            'similarity' in research_context.lower() or
            'spacy' in research_context.lower() or
            'nltk' in research_context.lower() or
            'bert' in research_context.lower() or
            'transformer' in research_context.lower()
        )
        
        # Create a specialized prompt for NLP research if needed
        if is_nlp_research:
            system_prompt = f"""You are a technical researcher specializing in NLP technologies.
The developer needs detailed information about NLP libraries, embedding models, and similarity detection approaches.
{depth_description}

Focus your research on:
1. Comparison of NLP libraries (spaCy, NLTK, Hugging Face Transformers, sentence-transformers)
   - Include version information, key features, and performance characteristics
   - Analyze strengths and weaknesses for semantic similarity tasks
   - Discuss ease of integration and community support

2. Analysis of embedding models (BERT, RoBERTa, domain-specific models)
   - Compare pre-trained models suitable for process document similarity
   - Discuss fine-tuning requirements for domain-specific language
   - Analyze performance trade-offs (accuracy vs. computational requirements)

3. Similarity metrics and algorithms (cosine similarity, Jaccard, etc.)
   - Explain how each metric works and when to use it
   - Provide implementation examples for key metrics
   - Discuss hybrid approaches combining multiple metrics

4. Performance considerations and optimizations
   - Techniques for efficient embedding generation and storage
   - Batch processing and caching strategies
   - Hardware requirements and scaling considerations

5. Integration with frameworks like DSPy
   - Explain how DSPy can enhance semantic understanding
   - Provide examples of DSPy integration for similarity tasks
   - Discuss hybrid approaches combining embeddings with LLM capabilities

6. Best practices for semantic similarity detection
   - Preprocessing techniques for process documents
   - Handling edge cases (short text, technical jargon)
   - Evaluation methodologies and benchmarking

Provide {detail_level} details for each section, with concrete code examples where appropriate.
Include specific version information, performance metrics, and implementation considerations.
Cite relevant research papers, documentation, and resources.

Structure your response in these sections:
1. Summary: A concise overview of your findings (2-3 paragraphs)
2. Key Findings: Detailed comparison of libraries and models with pros/cons
3. Implementation Recommendations: Specific recommendations with code examples
4. Resources: Relevant documentation, articles, and other resources
5. Sources: Include all research sources used to compile this information

Return your research as a JSON object with these sections as keys.
IMPORTANT: Always include the sources used for this research in the 'sources' section."""
        else:
            # General research prompt
            system_prompt = f"""You are a technical researcher helping with a software development task.
The developer needs detailed information about implementation approaches, technologies, and best practices.
{depth_description}

Focus your research on:
1. Current best practices and industry standards
2. Available libraries, frameworks, and tools
3. Implementation approaches and design patterns
4. Performance considerations and optimizations
5. Common pitfalls and how to avoid them

Structure your response in these sections:
1. Summary: A concise overview of your findings
2. Key Findings: Detailed information about technologies, approaches, and trade-offs
3. Implementation Recommendations: Specific recommendations for implementation
4. Resources: Relevant documentation, articles, and other resources
5. Sources: Include all research sources used to compile this information

Return your research as a JSON object with these sections as keys.
IMPORTANT: Always include the sources used for this research in the 'sources' section."""
        
        # Create the research query
        research_query = f"""I need to research for this development task:

{research_context}

Please provide detailed information about implementation approaches, technologies, and best practices.
Include all sources used in your research.
IMPORTANT: Include specific code examples and implementation details where appropriate."""
        
        try:
            # Call Perplexity for research (non-async call)
            response = perplexity_client.chat.completions.create(
                model=config.perplexity_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": research_query}
                ],
                temperature=0.2,  # Lower temperature for more factual responses
                max_tokens=config.max_tokens
            )
            
            # Extract JSON from response
            content = response.choices[0].message.content
            logger.info(f"Research response: {content[:100]}...")  # Log the first 100 chars
            
            json_start = content.find('{')
            json_end = content.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                # If no JSON found, try to structure the response
                logger.warning("No valid JSON found in research response, attempting to structure it")
                
                # Try to parse as markdown sections
                sections = {
                    "summary": "Research completed, but results were not properly structured.",
                    "key_findings": content
                }
                
                # Look for markdown headers to extract sections
                headers = {
                    "summary": ["# Summary", "## Summary"],
                    "key_findings": ["# Key Findings", "## Key Findings", "# Findings", "## Findings"],
                    "recommendations": ["# Implementation Recommendations", "## Implementation Recommendations", "# Recommendations", "## Recommendations"],
                    "resources": ["# Resources", "## Resources"],
                    "sources": ["# Sources", "## Sources", "# References", "## References"]
                }
                
                lines = content.split('\n')
                current_section = None
                section_content = []
                
                for line in lines:
                    matched = False
                    for section, section_headers in headers.items():
                        if any(line.strip().startswith(header) for header in section_headers):
                            # Save previous section if any
                            if current_section and section_content:
                                sections[current_section] = '\n'.join(section_content).strip()
                            
                            # Start new section
                            current_section = section
                            section_content = []
                            matched = True
                            break
                    
                    if not matched and current_section:
                        section_content.append(line)
                
                # Save the last section
                if current_section and section_content:
                    sections[current_section] = '\n'.join(section_content).strip()
                
                # Look for sources in the content if not found in sections
                if "sources" not in sections:
                    source_matches = re.findall(r'(https?://[^\s]+)', content)
                    if source_matches:
                        sections["sources"] = "\n".join(source_matches)
                
                research_results = sections
            else:
                # Parse the JSON response
                try:
                    research_results = json.loads(content[json_start:json_end])
                except json.JSONDecodeError:
                    logger.warning(f"Invalid JSON format: {content[json_start:json_end][:100]}...")
                    research_results = {
                        "summary": "Research completed, but JSON results could not be parsed.",
                        "key_findings": content
                    }
                    
                    # Try to extract sources from the content
                    source_matches = re.findall(r'(https?://[^\s]+)', content)
                    if source_matches:
                        research_results["sources"] = "\n".join(source_matches)
            
            # Ensure required fields are present
            if "summary" not in research_results or not research_results["summary"]:
                research_results["summary"] = "Research completed successfully."
            
            # If sources aren't included, add a note
            if "sources" not in research_results or not research_results["sources"]:
                # Try to extract sources from the content
                source_matches = re.findall(r'(https?://[^\s]+)', content)
                if source_matches:
                    research_results["sources"] = "\n".join(source_matches)
                else:
                    research_results["sources"] = "No specific sources were provided by the research service."
            
            # Normalize keys to lowercase for consistency
            normalized_results = {}
            for key, value in research_results.items():
                normalized_key = key.lower()
                if normalized_key == "implementation recommendations":
                    normalized_key = "recommendations"
                normalized_results[normalized_key] = value
            
            return normalized_results
            
        except Exception as e:
            logger.error(f"Error conducting research: {e}")
            raise
    
    def validate_task_id(task_id: Union[str, int]) -> str:
        """Validate and normalize a task ID."""
        if isinstance(task_id, int):
            return str(task_id)
        
        # Handle hierarchical task IDs (e.g., "5.3" for subtask 3 of task 5)
        if '.' in task_id:
            parts = task_id.split('.')
            if len(parts) == 2 and all(part.isdigit() for part in parts):
                return task_id  # Return the hierarchical ID as is
        
        # For regular task IDs, just ensure they're strings
        return str(task_id)