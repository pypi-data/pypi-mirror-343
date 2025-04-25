"""Terminal UI components and formatting for Taskinator."""

from typing import Any, Dict, List, Optional, Tuple, Union
import json
import logging
from pathlib import Path

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.text import Text

from .config import TaskPriority, TaskStatus

console = Console()
logger = logging.getLogger(__name__)

# Color schemes
COLORS = {
    'status': {
        TaskStatus.PENDING: 'yellow',
        TaskStatus.IN_PROGRESS: 'blue',
        TaskStatus.DONE: 'green',
        TaskStatus.BLOCKED: 'red'
    },
    'priority': {
        TaskPriority.LOW: 'cyan',
        TaskPriority.MEDIUM: 'yellow',
        TaskPriority.HIGH: 'red'
    }
}

def create_loading_indicator(message: str = "Working...") -> Progress:
    """Create a loading indicator with spinner."""
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True
    )

def display_banner(title: str = "Taskinator") -> None:
    """Display the application banner."""
    console.print()
    console.print(Panel(
        Text(title, style="bold blue", justify="center"),
        box=box.DOUBLE,
        expand=False
    ))
    console.print()

def create_task_table(
    tasks: List[Dict[str, Any]],
    show_subtasks: bool = False,
    show_dependencies: bool = True,
    show_complexity: bool = False
) -> Table:
    """Create a rich table for displaying tasks."""
    table = Table(
        show_header=True,
        header_style="bold blue",
        box=box.ROUNDED,
        expand=True
    )
    
    # Add columns
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Title", style="white")
    table.add_column("Status", style="white", no_wrap=True)
    table.add_column("Priority", style="white", no_wrap=True)
    if show_complexity:
        table.add_column("Complexity", style="white", no_wrap=True)
    if show_dependencies:
        table.add_column("Dependencies", style="white")
    
    # Add rows
    for task in tasks:
        task = _add_conflict_indicators(task)
        row = [
            str(task['id']),
            task['title'],
            Text(task['status'], style=COLORS['status'].get(task['status'], 'white')),
            Text(task['priority'], style=COLORS['priority'].get(task['priority'], 'white')),
        ]
        
        if show_complexity:
            complexity = task.get('complexityScore', task.get('complexity', 'N/A'))
            row.append(str(complexity))
        
        if show_dependencies:
            deps = format_dependencies(task.get('dependencies', []))
            row.append(deps)
        
        table.add_row(*row)
        
        # Add subtasks if requested
        if show_subtasks and task.get('subtasks'):
            for subtask in task['subtasks']:
                subtask = _add_conflict_indicators(subtask)
                sub_row = [
                    f"  {task['id']}.{subtask['id']}",
                    f"└─ {subtask['title']}",
                    Text(subtask['status'], style=COLORS['status'].get(subtask['status'], 'white')),
                    Text(subtask.get('priority', ''), style=COLORS['priority'].get(subtask.get('priority'), 'white')),
                ]
                
                if show_complexity:
                    sub_complexity = subtask.get('complexityScore', subtask.get('complexity', 'N/A'))
                    sub_row.append(str(sub_complexity))
                
                if show_dependencies:
                    sub_deps = format_dependencies(subtask.get('dependencies', []))
                    sub_row.append(sub_deps)
                
                table.add_row(*sub_row)
    
    return table

def format_dependencies(
    dependencies: List[Union[str, int]],
    tasks: Optional[List[Dict[str, Any]]] = None
) -> Text:
    """Format task dependencies with status colors if tasks are provided."""
    if not dependencies:
        return Text("None", style="dim")
    
    result = Text()
    for i, dep in enumerate(dependencies):
        if i > 0:
            result.append(", ")
        
        if tasks:
            # Find the dependency's status
            for task in tasks:
                if str(task['id']) == str(dep):
                    status = task.get('status', TaskStatus.PENDING)
                    result.append(
                        str(dep),
                        style=COLORS['status'].get(status, 'white')
                    )
                    break
            else:
                # Dependency not found
                result.append(str(dep), style="red")
        else:
            # No tasks provided, just show the ID
            result.append(str(dep))
    
    return result

def display_task_details(task: Dict[str, Any]) -> None:
    """Display detailed information about a task."""
    console.print(Panel(
        Text.from_markup(f"""
[bold cyan]Task {task['id']}[/bold cyan]: {task['title']}
[bold]Status:[/bold] {Text(task['status'], style=COLORS['status'].get(task['status'], 'white'))}
[bold]Priority:[/bold] {Text(task['priority'], style=COLORS['priority'].get(task['priority'], 'white'))}
[bold]Dependencies:[/bold] {format_dependencies(task.get('dependencies', []))}

[bold]Description:[/bold]
{task.get('description', 'No description provided.')}

[bold]Details:[/bold]
{task.get('details', 'No details provided.')}

[bold]Test Strategy:[/bold]
{task.get('testStrategy', 'No test strategy provided.')}
        """.strip()),
        title=f"Task Details",
        box=box.ROUNDED,
        expand=False
    ))
    
    if task.get('subtasks'):
        console.print()
        
        # Load complexity data from the report if available
        complexity_data = {}
        try:
            complexity_report_path = Path("tasks/task-complexity-report.json")
            if complexity_report_path.exists():
                with open(complexity_report_path, "r") as f:
                    complexity_report = json.load(f)
                    
                    # Handle both old format (dict with complexityAnalysis key) and new format (direct list)
                    if isinstance(complexity_report, dict) and "complexityAnalysis" in complexity_report:
                        # Old format
                        task_analyses = complexity_report.get("complexityAnalysis", [])
                    elif isinstance(complexity_report, list):
                        # New format - direct list of task analyses
                        task_analyses = complexity_report
                    else:
                        # Unknown format
                        task_analyses = []
                    
                    for task_analysis in task_analyses:
                        task_id = task_analysis.get("taskId")
                        if task_id:
                            complexity_data[str(task_id)] = task_analysis.get("complexityScore", "N/A")
        except Exception as e:
            logger.warning(f"Failed to load complexity data: {e}")
        
        # Add complexity scores to subtasks
        subtasks_with_complexity = []
        for subtask in task['subtasks']:
            subtask_copy = subtask.copy()
            
            # Try different formats for subtask IDs
            subtask_id = subtask.get('id')
            possible_ids = [
                f"{task['id']}.{subtask_id}",  # Format: parent.child
                str(subtask_id)                # Direct ID
            ]
            
            # Look for complexity in the data
            for possible_id in possible_ids:
                if possible_id in complexity_data:
                    subtask_copy['complexity'] = complexity_data[possible_id]
                    break
            
            subtasks_with_complexity.append(subtask_copy)
        
        console.print(Panel(
            create_task_table(subtasks_with_complexity, show_subtasks=False, show_complexity=True),
            title="Subtasks",
            box=box.ROUNDED,
            expand=False
        ))

def display_error(message: str) -> None:
    """Display an error message."""
    console.print(Panel(
        Text(message, style="red"),
        title="Error",
        box=box.ROUNDED,
        border_style="red",
        expand=False
    ))

def display_success(message: str) -> None:
    """Display a success message."""
    console.print(Panel(
        Text(message, style="green"),
        title="Success",
        box=box.ROUNDED,
        border_style="green",
        expand=False
    ))

def display_info(message: str) -> None:
    """Display an informational message."""
    console.print(f"[blue]{message}[/blue]")

def display_warning(message: str) -> None:
    """Display a warning message."""
    console.print(Panel(
        Text(message, style="yellow"),
        title="Warning",
        box=box.ROUNDED,
        border_style="yellow",
        expand=False
    ))

def display_table(table: Table) -> None:
    """Display a Rich table."""
    console.print(table)

def _add_conflict_indicators(task):
    """Add visual indicators for conflicts to a task.
    
    Args:
        task: Task to add indicators to
        
    Returns:
        Task with conflict indicators
    """
    # Check if task has conflicts
    if "nextcloud" in task and task["nextcloud"].get("sync_status") == "conflict":
        # Add conflict indicator to title
        if "title" in task:
            task["title"] = f"{task['title']} [red]⚠[/red]"
    
    return task