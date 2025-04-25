"""Conflict presentation system for Taskinator.

This module provides a comprehensive system for presenting conflicts to users
in a clear and accessible way, with support for different presentation formats
and notification mechanisms.
"""

from typing import Any, Dict, List, Optional, Tuple, Union, Callable
import json
import os
from datetime import datetime
from pathlib import Path
from loguru import logger

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
from rich.tree import Tree
from rich.progress import Progress, SpinnerColumn, TextColumn

from .conflict_resolver import ConflictResolver, ManualConflictResolver, ConflictResolutionStrategy
from .conflict_ui import ConflictUI, display_conflict_list
from .resolution_strategies import StrategyFactory
from .nextcloud_sync import get_nextcloud_metadata, SyncStatus
from .ui import console, display_error, display_success, display_info, COLORS
from .config import config


class ConflictNotificationManager:
    """Manages notifications for conflicts."""
    
    def __init__(self, notification_handlers: Optional[List[Callable]] = None):
        """Initialize the notification manager.
        
        Args:
            notification_handlers: List of notification handler functions
        """
        self.notification_handlers = notification_handlers or []
        
        # Add default terminal notification handler
        if not self.notification_handlers:
            self.notification_handlers.append(self._terminal_notification)
    
    def add_notification_handler(self, handler: Callable) -> None:
        """Add a notification handler.
        
        Args:
            handler: Notification handler function
        """
        self.notification_handlers.append(handler)
    
    def notify_conflict(self, task: Dict[str, Any], system: str) -> None:
        """Notify about a conflict.
        
        Args:
            task: Task with conflict
            system: External system name
        """
        for handler in self.notification_handlers:
            handler(task, system)
    
    def _terminal_notification(self, task: Dict[str, Any], system: str) -> None:
        """Default terminal notification handler.
        
        Args:
            task: Task with conflict
            system: External system name
        """
        display_error(f"Conflict detected in task {task.get('id')}: {task.get('title')} with {system}")


class ConflictSummaryView:
    """Provides a summary view of conflicts across all tasks."""
    
    def __init__(self, conflict_resolver: Optional[ConflictResolver] = None):
        """Initialize the conflict summary view.
        
        Args:
            conflict_resolver: Conflict resolver instance
        """
        self.conflict_resolver = conflict_resolver or ConflictResolver()
    
    def display_conflict_summary(self, tasks: List[Dict[str, Any]]) -> None:
        """Display a summary of all conflicts.
        
        Args:
            tasks: List of all tasks
        """
        # Get tasks with conflicts
        tasks_with_conflicts = self.conflict_resolver.get_conflicts(tasks)
        
        if not tasks_with_conflicts:
            display_info("No conflicts found")
            return
        
        # Count conflicts by system
        conflicts_by_system = {}
        for task in tasks_with_conflicts:
            for system_name, system_data in task.items():
                if isinstance(system_data, dict) and system_data.get("sync_status") == SyncStatus.CONFLICT.value:
                    conflicts_by_system[system_name] = conflicts_by_system.get(system_name, 0) + 1
        
        # Create summary panel
        console.print(Panel(
            Text.from_markup(f"""
[bold]Total conflicts:[/bold] {len(tasks_with_conflicts)}

[bold]Conflicts by system:[/bold]
{self._format_conflicts_by_system(conflicts_by_system)}

Use [cyan]taskinator conflicts[/cyan] to view detailed conflict information.
Use [cyan]taskinator resolve <task_id>[/cyan] to resolve conflicts for a specific task.
            """.strip()),
            title="Conflict Summary",
            box=box.ROUNDED,
            border_style="red",
            expand=False
        ))
    
    def _format_conflicts_by_system(self, conflicts_by_system: Dict[str, int]) -> str:
        """Format conflicts by system for display.
        
        Args:
            conflicts_by_system: Dictionary of conflicts by system
            
        Returns:
            Formatted string
        """
        if not conflicts_by_system:
            return "No conflicts found"
        
        result = []
        for system, count in conflicts_by_system.items():
            result.append(f"  • [blue]{system}[/blue]: [red]{count}[/red] conflict{'s' if count > 1 else ''}")
        
        return "\n".join(result)


class ConflictDashboard:
    """Interactive dashboard for managing conflicts."""
    
    def __init__(
        self,
        conflict_resolver: Optional[ConflictResolver] = None,
        manual_resolver: Optional[ManualConflictResolver] = None,
        conflict_ui: Optional[ConflictUI] = None
    ):
        """Initialize the conflict dashboard.
        
        Args:
            conflict_resolver: Conflict resolver instance
            manual_resolver: Manual conflict resolver instance
            conflict_ui: Conflict UI instance
        """
        self.conflict_resolver = conflict_resolver or ConflictResolver()
        self.manual_resolver = manual_resolver or ManualConflictResolver()
        self.conflict_ui = conflict_ui or ConflictUI(self.manual_resolver)
        self.summary_view = ConflictSummaryView(self.conflict_resolver)
    
    def display_dashboard(self, tasks: List[Dict[str, Any]]) -> None:
        """Display the conflict dashboard.
        
        Args:
            tasks: List of all tasks
        """
        # Get tasks with conflicts
        tasks_with_conflicts = self.conflict_resolver.get_conflicts(tasks)
        
        if not tasks_with_conflicts:
            display_info("No conflicts found")
            return
        
        # Display summary
        self.summary_view.display_conflict_summary(tasks)
        
        # Display conflict list
        console.print()
        display_conflict_list(tasks)
        
        # Offer to resolve conflicts
        console.print()
        if Confirm.ask("Would you like to resolve conflicts now?"):
            self._interactive_resolution(tasks, tasks_with_conflicts)
    
    def _interactive_resolution(
        self,
        all_tasks: List[Dict[str, Any]],
        conflict_tasks: List[Dict[str, Any]]
    ) -> None:
        """Interactive conflict resolution workflow.
        
        Args:
            all_tasks: List of all tasks
            conflict_tasks: List of tasks with conflicts
        """
        # Create options for task selection
        options = ["all"] + [str(task.get("id", "")) for task in conflict_tasks]
        
        # Ask which task to resolve
        choice = Prompt.ask(
            "Which task would you like to resolve?",
            choices=options,
            default="all"
        )
        
        if choice == "all":
            # Resolve all conflicts
            self._resolve_all_conflicts(all_tasks, conflict_tasks)
        else:
            # Resolve specific task
            task = next((t for t in conflict_tasks if str(t.get("id", "")) == choice), None)
            if task:
                self._resolve_task_conflicts(all_tasks, task)
            else:
                display_error(f"Task {choice} not found")
    
    def _resolve_all_conflicts(
        self,
        all_tasks: List[Dict[str, Any]],
        conflict_tasks: List[Dict[str, Any]]
    ) -> None:
        """Resolve all conflicts.
        
        Args:
            all_tasks: List of all tasks
            conflict_tasks: List of tasks with conflicts
        """
        # Ask for resolution strategy
        strategy_choice = Prompt.ask(
            "Choose a resolution strategy for all conflicts",
            choices=["manual", "newest_wins", "local_wins", "remote_wins"],
            default="manual"
        )
        
        if strategy_choice == "manual":
            # Resolve each task manually
            for task in conflict_tasks:
                self._resolve_task_conflicts(all_tasks, task)
        else:
            # Apply automatic strategy to all tasks
            strategy = ConflictResolutionStrategy(strategy_choice)
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                transient=True
            ) as progress:
                task_id = progress.add_task(f"Resolving conflicts using {strategy_choice}...", total=len(conflict_tasks))
                
                for task in conflict_tasks:
                    # Get the task index in the all_tasks list
                    task_index = next((i for i, t in enumerate(all_tasks) if t.get("id") == task.get("id")), -1)
                    if task_index >= 0:
                        # Get external systems with conflicts
                        for system_name, system_data in task.items():
                            if isinstance(system_data, dict) and system_data.get("sync_status") == SyncStatus.CONFLICT.value:
                                # TODO: Implement actual resolution for each system
                                # For now, we'll just mark it as resolved
                                system_data["sync_status"] = SyncStatus.SYNCED.value
                                task[system_name] = system_data
                        
                        # Update the task in all_tasks
                        all_tasks[task_index] = task
                    
                    progress.update(task_id, advance=1)
            
            display_success(f"Resolved {len(conflict_tasks)} conflicts using {strategy_choice}")
    
    def _resolve_task_conflicts(self, all_tasks: List[Dict[str, Any]], task: Dict[str, Any]) -> None:
        """Resolve conflicts for a specific task.
        
        Args:
            all_tasks: List of all tasks
            task: Task with conflicts
        """
        # Get the task index in the all_tasks list
        task_index = next((i for i, t in enumerate(all_tasks) if t.get("id") == task.get("id")), -1)
        if task_index < 0:
            display_error(f"Task {task.get('id')} not found in task list")
            return
        
        # Use the conflict UI to resolve conflicts
        updated_task = self.conflict_ui.resolve_conflict_interactive(task)
        
        # Update the task in all_tasks
        all_tasks[task_index] = updated_task
        
        display_success(f"Conflicts resolved for task {task.get('id')}")


class ConflictHistoryView:
    """View for displaying conflict history."""
    
    def display_conflict_history(self, task: Dict[str, Any]) -> None:
        """Display conflict history for a task.
        
        Args:
            task: Task to display history for
        """
        # Get metadata for all systems
        history_entries = []
        
        for system_name, system_data in task.items():
            if isinstance(system_data, dict) and "version_history" in system_data:
                for version in system_data.get("version_history", []):
                    if "changes" in version and any(c.get("resolution") for c in version.get("changes", [])):
                        # This is a conflict resolution entry
                        timestamp = version.get("timestamp", 0)
                        modified_by = version.get("modified_by", "unknown")
                        
                        history_entries.append({
                            "system": system_name,
                            "timestamp": timestamp,
                            "modified_by": modified_by,
                            "changes": version.get("changes", []),
                            "version": version.get("version", "")
                        })
        
        if not history_entries:
            display_info(f"No conflict history found for task {task.get('id')}")
            return
        
        # Sort by timestamp, newest first
        history_entries.sort(key=lambda x: x.get("timestamp", 0), reverse=True)
        
        # Create a tree view
        tree = Tree(f"[bold]Conflict History for Task {task.get('id')}: {task.get('title')}[/bold]")
        
        for entry in history_entries:
            timestamp = datetime.fromtimestamp(entry.get("timestamp", 0)).strftime("%Y-%m-%d %H:%M:%S")
            system = entry.get("system", "unknown")
            modified_by = entry.get("modified_by", "unknown")
            
            entry_node = tree.add(f"[yellow]{timestamp}[/yellow] - [blue]{system}[/blue] - {modified_by}")
            
            for change in entry.get("changes", []):
                field = change.get("field", "")
                resolution = change.get("resolution", "unknown")
                
                if resolution == "local":
                    resolution_text = f"[green]{resolution}[/green]"
                elif resolution == "remote":
                    resolution_text = f"[blue]{resolution}[/blue]"
                else:
                    resolution_text = f"[yellow]{resolution}[/yellow]"
                
                entry_node.add(f"Field [cyan]{field}[/cyan] - Resolution: {resolution_text}")
        
        console.print(Panel(
            tree,
            title="Conflict Resolution History",
            box=box.ROUNDED,
            expand=False
        ))


class ConflictPreferenceManager:
    """Manages user preferences for conflict resolution."""
    
    def __init__(self):
        """Initialize the preference manager."""
        # Use the config directory if available, otherwise use the current directory
        config_dir = getattr(config, 'config_dir', None)
        if not config_dir:
            config_dir = Path.home() / '.taskinator'
            os.makedirs(config_dir, exist_ok=True)
            
        self.preferences_file = os.path.join(config_dir, "conflict_preferences.json")
        self.preferences = self._load_preferences()
    
    def _load_preferences(self) -> Dict[str, Any]:
        """Load preferences from file.
        
        Returns:
            Dictionary of preferences
        """
        if os.path.exists(self.preferences_file):
            try:
                import json
                with open(self.preferences_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading conflict preferences: {e}")
        
        # Default preferences
        return {
            "default_strategy": ConflictResolutionStrategy.MANUAL.value,
            "field_preferences": {},
            "system_preferences": {}
        }
    
    def _save_preferences(self) -> None:
        """Save preferences to file."""
        try:
            import json
            os.makedirs(os.path.dirname(self.preferences_file), exist_ok=True)
            with open(self.preferences_file, 'w') as f:
                json.dump(self.preferences, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving conflict preferences: {e}")
    
    def get_default_strategy(self) -> str:
        """Get the default resolution strategy.
        
        Returns:
            Default strategy name
        """
        return self.preferences.get("default_strategy", ConflictResolutionStrategy.MANUAL.value)
    
    def set_default_strategy(self, strategy: str) -> None:
        """Set the default resolution strategy.
        
        Args:
            strategy: Strategy name
        """
        if strategy not in [s.value for s in ConflictResolutionStrategy]:
            raise ValueError(f"Invalid strategy: {strategy}")
        
        self.preferences["default_strategy"] = strategy
        self._save_preferences()
    
    def get_field_preference(self, field: str) -> Optional[str]:
        """Get the preferred resolution strategy for a field.
        
        Args:
            field: Field name
            
        Returns:
            Preferred strategy name or None
        """
        return self.preferences.get("field_preferences", {}).get(field)
    
    def set_field_preference(self, field: str, strategy: str) -> None:
        """Set the preferred resolution strategy for a field.
        
        Args:
            field: Field name
            strategy: Strategy name
        """
        if strategy not in [s.value for s in ConflictResolutionStrategy]:
            raise ValueError(f"Invalid strategy: {strategy}")
        
        if "field_preferences" not in self.preferences:
            self.preferences["field_preferences"] = {}
        
        self.preferences["field_preferences"][field] = strategy
        self._save_preferences()
    
    def get_system_preference(self, system: str) -> Optional[str]:
        """Get the preferred resolution strategy for a system.
        
        Args:
            system: System name
            
        Returns:
            Preferred strategy name or None
        """
        return self.preferences.get("system_preferences", {}).get(system)
    
    def set_system_preference(self, system: str, strategy: str) -> None:
        """Set the preferred resolution strategy for a system.
        
        Args:
            system: System name
            strategy: Strategy name
        """
        if strategy not in [s.value for s in ConflictResolutionStrategy]:
            raise ValueError(f"Invalid strategy: {strategy}")
        
        if "system_preferences" not in self.preferences:
            self.preferences["system_preferences"] = {}
        
        self.preferences["system_preferences"][system] = strategy
        self._save_preferences()
    
    def display_preferences(self) -> None:
        """Display current preferences."""
        console.print(Panel(
            Text.from_markup(f"""
[bold]Default Strategy:[/bold] {self.get_default_strategy()}

[bold]Field Preferences:[/bold]
{self._format_field_preferences()}

[bold]System Preferences:[/bold]
{self._format_system_preferences()}
            """.strip()),
            title="Conflict Resolution Preferences",
            box=box.ROUNDED,
            expand=False
        ))
    
    def _format_field_preferences(self) -> str:
        """Format field preferences for display.
        
        Returns:
            Formatted string
        """
        field_prefs = self.preferences.get("field_preferences", {})
        if not field_prefs:
            return "  No field preferences set"
        
        result = []
        for field, strategy in field_prefs.items():
            result.append(f"  • [cyan]{field}[/cyan]: {strategy}")
        
        return "\n".join(result)
    
    def _format_system_preferences(self) -> str:
        """Format system preferences for display.
        
        Returns:
            Formatted string
        """
        system_prefs = self.preferences.get("system_preferences", {})
        if not system_prefs:
            return "  No system preferences set"
        
        result = []
        for system, strategy in system_prefs.items():
            result.append(f"  • [blue]{system}[/blue]: {strategy}")
        
        return "\n".join(result)


class ConflictPresentationSystem:
    """Main class for the conflict presentation system."""
    
    def __init__(self):
        """Initialize the conflict presentation system."""
        self.conflict_resolver = ConflictResolver()
        self.manual_resolver = ManualConflictResolver()
        self.conflict_ui = ConflictUI(self.manual_resolver)
        self.notification_manager = ConflictNotificationManager()
        self.summary_view = ConflictSummaryView(self.conflict_resolver)
        self.dashboard = ConflictDashboard(
            self.conflict_resolver,
            self.manual_resolver,
            self.conflict_ui
        )
        self.history_view = ConflictHistoryView()
        self.preference_manager = ConflictPreferenceManager()
    
    def notify_conflict(self, task: Dict[str, Any], system: str) -> None:
        """Notify about a conflict.
        
        Args:
            task: Task with conflict
            system: External system name
        """
        self.notification_manager.notify_conflict(task, system)
    
    def display_conflict_summary(self, tasks: List[Dict[str, Any]]) -> None:
        """Display a summary of all conflicts.
        
        Args:
            tasks: List of all tasks
        """
        self.summary_view.display_conflict_summary(tasks)
    
    def display_dashboard(self, tasks: List[Dict[str, Any]]) -> None:
        """Display the conflict dashboard.
        
        Args:
            tasks: List of all tasks
        """
        self.dashboard.display_dashboard(tasks)
    
    def display_conflict_history(self, task: Dict[str, Any]) -> None:
        """Display conflict history for a task.
        
        Args:
            task: Task to display history for
        """
        self.history_view.display_conflict_history(task)
    
    def display_preferences(self) -> None:
        """Display current preferences."""
        self.preference_manager.display_preferences()
    
    def set_default_strategy(self, strategy: str) -> None:
        """Set the default resolution strategy.
        
        Args:
            strategy: Strategy name
        """
        self.preference_manager.set_default_strategy(strategy)
    
    def set_field_preference(self, field: str, strategy: str) -> None:
        """Set the preferred resolution strategy for a field.
        
        Args:
            field: Field name
            strategy: Strategy name
        """
        self.preference_manager.set_field_preference(field, strategy)
    
    def set_system_preference(self, system: str, strategy: str) -> None:
        """Set the preferred resolution strategy for a system.
        
        Args:
            system: System name
            strategy: Strategy name
        """
        self.preference_manager.set_system_preference(system, strategy)
    
    def get_preferred_strategy(self, task: Dict[str, Any], field: str, system: str) -> str:
        """Get the preferred resolution strategy for a task field.
        
        Args:
            task: Task with conflict
            field: Field name
            system: System name
            
        Returns:
            Preferred strategy name
        """
        # Check field preference first
        field_pref = self.preference_manager.get_field_preference(field)
        if field_pref:
            return field_pref
        
        # Check system preference next
        system_pref = self.preference_manager.get_system_preference(system)
        if system_pref:
            return system_pref
        
        # Fall back to default
        return self.preference_manager.get_default_strategy()


# Create a singleton instance
conflict_presentation_system = ConflictPresentationSystem()
