"""UI components for conflict resolution in Taskinator."""

from typing import Any, Dict, List, Optional, Tuple, Union
import difflib
from datetime import datetime
from loguru import logger

from .conflict_resolver import ConflictResolver, ManualConflictResolver, ConflictResolutionStrategy
from .nextcloud_sync import get_nextcloud_metadata, SyncStatus
from .ui import console, display_error, display_success, display_info, COLORS

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.columns import Columns
from rich.prompt import Prompt, Confirm
from rich.syntax import Syntax
from rich.layout import Layout
from rich.live import Live


class ConflictUI:
    """UI components for conflict resolution."""

    def __init__(self, conflict_resolver: Optional[ManualConflictResolver] = None):
        """Initialize conflict UI.

        Args:
            conflict_resolver: Manual conflict resolver instance
        """
        self.conflict_resolver = conflict_resolver or ManualConflictResolver()

    def display_conflict_summary(self, task: Dict[str, Any]) -> None:
        """Display a summary of conflicts for a task.

        Args:
            task: Task with conflicts
        """
        # Get metadata
        metadata = get_nextcloud_metadata(task)

        if metadata.sync_status != SyncStatus.CONFLICT:
            display_info(f"Task {task.get('id')} has no conflicts")
            return

        # Get field conflicts
        conflicts = self.conflict_resolver.get_field_conflicts(task)

        if not conflicts:
            display_info(f"Task {task.get('id')} has no field conflicts")
            return

        # Create table for conflicts
        table = Table(
            title=f"Conflicts for Task {task.get('id')}: {task.get('title')}",
            box=box.ROUNDED,
            show_header=True,
            header_style="bold magenta",
            expand=True
        )

        table.add_column("Field", style="cyan")
        table.add_column("Local Value", style="green")
        table.add_column("Remote Value", style="blue")

        for conflict in conflicts:
            field = conflict.get("field", "")
            local_value = str(conflict.get("local_value", ""))
            remote_value = str(conflict.get("remote_value", ""))

            table.add_row(field, local_value, remote_value)

        console.print(table)
        console.print()
        display_info(f"Use 'resolve-conflict {task.get('id')} <field> <local|remote>' to resolve a specific field conflict")

    def display_conflict_details(self, task: Dict[str, Any], field: str) -> None:
        """Display detailed comparison for a specific field conflict.

        Args:
            task: Task with conflicts
            field: Field name to display
        """
        # Get field conflicts
        conflicts = self.conflict_resolver.get_field_conflicts(task)

        # Find the conflict for this field
        conflict = None
        for c in conflicts:
            if c.get("field") == field:
                conflict = c
                break

        if not conflict:
            display_error(f"No conflict found for field '{field}' in task {task.get('id')}")
            return

        local_value = str(conflict.get("local_value", ""))
        remote_value = str(conflict.get("remote_value", ""))

        # For text fields, show a diff
        if isinstance(local_value, str) and isinstance(remote_value, str) and len(local_value) > 20:
            self._display_text_diff(field, local_value, remote_value)
        else:
            # For simple values, show side by side
            layout = Layout()
            layout.split_column(
                Layout(Panel(
                    Text(local_value, style="green"),
                    title="Local Value",
                    box=box.ROUNDED,
                    border_style="green"
                )),
                Layout(Panel(
                    Text(remote_value, style="blue"),
                    title="Remote Value",
                    box=box.ROUNDED,
                    border_style="blue"
                ))
            )

            console.print(Panel(
                layout,
                title=f"Conflict in '{field}' for Task {task.get('id')}",
                box=box.ROUNDED,
                expand=False
            ))

    def _display_text_diff(self, field: str, local_text: str, remote_text: str) -> None:
        """Display a diff between two text values.

        Args:
            field: Field name
            local_text: Local text value
            remote_text: Remote text value
        """
        # Generate diff
        diff = list(difflib.unified_diff(
            local_text.splitlines(),
            remote_text.splitlines(),
            lineterm="",
            fromfile="Local",
            tofile="Remote"
        ))

        # Create syntax highlighted diff
        diff_text = "\n".join(diff)
        syntax = Syntax(diff_text, "diff", theme="monokai", line_numbers=True)

        console.print(Panel(
            syntax,
            title=f"Diff for '{field}' in Task {field}",
            box=box.ROUNDED,
            expand=False
        ))

    def resolve_conflict_interactive(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Interactively resolve conflicts for a task.

        Args:
            task: Task with conflicts

        Returns:
            Updated task with resolved conflicts
        """
        # Get field conflicts
        conflicts = self.conflict_resolver.get_field_conflicts(task)

        if not conflicts:
            display_info(f"Task {task.get('id')} has no field conflicts")
            return task

        # Display summary
        self.display_conflict_summary(task)

        # Resolve each conflict
        updated_task = task.copy()
        for conflict in conflicts:
            field = conflict.get("field", "")
            local_value = conflict.get("local_value", "")
            remote_value = conflict.get("remote_value", "")

            # Display conflict details
            self.display_conflict_details(updated_task, field)

            # Prompt for resolution
            console.print()
            resolution = Prompt.ask(
                f"Resolve conflict for '{field}'",
                choices=["local", "remote", "skip"],
                default="skip"
            )

            if resolution != "skip":
                updated_task = self.conflict_resolver.resolve_field_conflict(
                    updated_task, field, resolution
                )

                display_success(f"Resolved conflict for '{field}' using {resolution} value")

        return updated_task

    def display_conflict_resolution_form(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Display a form for resolving all conflicts in a task at once.

        Args:
            task: Task with conflicts

        Returns:
            Updated task with resolved conflicts
        """
        # Get field conflicts
        conflicts = self.conflict_resolver.get_field_conflicts(task)

        if not conflicts:
            display_info(f"Task {task.get('id')} has no field conflicts")
            return task

        # Create a layout for the form
        layout = Layout()

        # Add header
        header = Panel(
            Text(f"Conflict Resolution for Task {task.get('id')}: {task.get('title')}", style="bold cyan"),
            box=box.ROUNDED,
            border_style="cyan"
        )

        # Create table for conflicts
        table = Table(
            box=box.ROUNDED,
            show_header=True,
            header_style="bold magenta",
            expand=True
        )

        table.add_column("Field", style="cyan")
        table.add_column("Local Value", style="green")
        table.add_column("Remote Value", style="blue")
        table.add_column("Resolution", style="yellow")

        # Track resolutions
        resolutions = {}

        # Add rows for each conflict
        for conflict in conflicts:
            field = conflict.get("field", "")
            local_value = str(conflict.get("local_value", ""))
            remote_value = str(conflict.get("remote_value", ""))

            # Initialize resolution to None
            resolutions[field] = None

            table.add_row(field, local_value, remote_value, "?")

        # Add table to layout
        layout.split_column(
            Layout(header, size=3),
            Layout(table)
        )

        # Display the form
        with Live(layout, refresh_per_second=4) as live:
            # Process each conflict
            updated_task = task.copy()
            for conflict in conflicts:
                field = conflict.get("field", "")

                # Prompt for resolution
                console.print()
                resolution = Prompt.ask(
                    f"Resolve conflict for '{field}'",
                    choices=["local", "remote", "skip"],
                    default="skip"
                )

                if resolution != "skip":
                    resolutions[field] = resolution
                    updated_task = self.conflict_resolver.resolve_field_conflict(
                        updated_task, field, resolution
                    )

                    # Update the table
                    for i, row in enumerate(table.rows):
                        if row[0].plain == field:
                            table.rows[i] = (
                                row[0],
                                row[1],
                                row[2],
                                Text(resolution, style="yellow")
                            )
                            break

                    # Update the live display
                    live.update(layout)

        # Show summary
        resolved_count = sum(1 for r in resolutions.values() if r is not None)
        display_success(f"Resolved {resolved_count} out of {len(conflicts)} conflicts")

        return updated_task


def display_conflict_list(tasks: List[Dict[str, Any]]) -> None:
    """Display a list of tasks with conflicts.

    Args:
        tasks: List of all tasks
    """
    # Find tasks with conflicts
    conflict_resolver = ConflictResolver()
    tasks_with_conflicts = conflict_resolver.get_conflicts(tasks)

    if not tasks_with_conflicts:
        display_info("No tasks with conflicts found")
        return

    # Create table for conflicts
    table = Table(
        title="Tasks with Conflicts",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold red",
        expand=True
    )

    table.add_column("ID", style="cyan")
    table.add_column("Title", style="white")
    table.add_column("Status", style="white")
    table.add_column("Priority", style="white")
    table.add_column("Conflict Fields", style="red")

    # Add rows for each task with conflicts
    for task in tasks_with_conflicts:
        # Get conflict fields
        manual_resolver = ManualConflictResolver()
        conflicts = manual_resolver.get_field_conflicts(task)
        conflict_fields = ", ".join(c.get("field", "") for c in conflicts)

        table.add_row(
            str(task.get("id", "")),
            task.get("title", ""),
            task.get("status", ""),
            task.get("priority", ""),
            conflict_fields
        )

    console.print(table)
    console.print()
    display_info("Use 'resolve-conflict <task_id>' to resolve conflicts for a specific task")
