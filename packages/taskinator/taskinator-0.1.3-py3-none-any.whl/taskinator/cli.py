"""Command-line interface for Taskinator."""

import asyncio
import functools
import importlib
import importlib.resources
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List

import typer
import questionary
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown
from rich import box
from loguru import logger
from rich.progress import Progress, SpinnerColumn, TextColumn
from contextlib import contextmanager

from . import __version__, package_data
from .task_manager import TaskManager
from .constants import SyncStatus, ExternalSystem, SyncDirection
from .plugin_registry import registry as plugin_registry
from .background_sync import background_sync_manager, JobStatus, JobPriority
from .sync_manager import SyncManager

from .utils import (
    read_json,
    write_json,
    find_task_by_id,
)
from .ui import (
    display_banner,
    display_info,
    display_success,
    display_warning,
    display_error,
)
from .similarity_module import TaskSimilarityModule, TaskSimilarityResult
from .config import config

# Load environment variables
load_dotenv()

# Create console for rich output
console = Console()

def create_directory_if_not_exists(directory_path: str) -> None:
    """Create a directory if it doesn't exist."""
    Path(directory_path).mkdir(parents=True, exist_ok=True)

@contextmanager
def create_loading_indicator(message: str):
    """Create a loading indicator with a spinner."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task(description=message, total=None)
        try:
            yield
        finally:
            progress.update(task, completed=True)

# Create the main app
app = typer.Typer(
    help="Taskinator: AI-powered task management for developers",
    add_completion=False
)

# Create subcommands
sync_app = typer.Typer()
app.add_typer(sync_app, name="sync", help="Synchronize tasks with external systems")

plugin_app = typer.Typer()
app.add_typer(plugin_app, name="plugin", help="Manage Taskinator plugins")

background_app = typer.Typer()
app.add_typer(background_app, name="background", help="Manage background synchronization")

# Create document management subcommands
pdd_app = typer.Typer()
app.add_typer(pdd_app, name="pdd", help="Manage Process Design Documents (PDDs)")

sop_app = typer.Typer()
app.add_typer(sop_app, name="sop", help="Manage Standard Operating Procedures (SOPs)")

# Wrapper for async commands
def _run_async(func):
    """Decorator to run async functions."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return asyncio.run(func(*args, **kwargs))
    return wrapper

def get_task_manager(display_output: bool = True) -> TaskManager:
    """Get a TaskManager instance."""
    return TaskManager(display_output=display_output)

def get_ai_service():
    """Get the AI service."""
    # We don't have an AIService class, so just return a placeholder
    # The actual AI functions are imported directly where needed
    return None

@app.command()
def version():
    """Show the version of Taskinator."""
    console.print(f"Taskinator v{__version__}")

@app.command()
def init(
    force: bool = typer.Option(
        False, "--force", "-f", help="Force initialization even if files exist"
    )
):
    """Initialize a new Taskinator project."""
    try:
        # Create directories
        Path("tasks").mkdir(exist_ok=True)
        
        # Create cursor and windsurf metadata directories
        cursor_rules_dir = Path(".cursor/rules")
        cursor_rules_dir.mkdir(parents=True, exist_ok=True)
        display_info(f"Created directory: {cursor_rules_dir}")
        
        # Create windsurf directory
        windsurf_dir = Path(".windsurf")
        windsurf_dir.mkdir(parents=True, exist_ok=True)
        display_info(f"Created directory: {windsurf_dir}")
        
        # Copy windsurf rules template
        windsurf_rules_file = Path(".windsurfrules")
        
        if not windsurf_rules_file.exists() or force:
            # Get the template content from package data
            template_path = Path(__file__).parent / "package_data" / "templates" / "windsurf" / ".windsurfrules"
            if template_path.exists():
                with open(template_path, 'r') as src:
                    with open(windsurf_rules_file, 'w') as dst:
                        dst.write(src.read())
                display_info(f"Created file: {windsurf_rules_file}")
            else:
                display_info(f"Template file not found: {template_path}")
        
        # Create tasks.json if it doesn't exist or force is True
        tasks_file = Path("tasks/tasks.json")
        if not tasks_file.exists() or force:
            tasks_data = {
                "tasks": []
            }
            with open(tasks_file, "w") as f:
                json.dump(tasks_data, f, indent=2)
            
            display_success("Initialized Taskinator project")
        else:
            display_error("Taskinator project already initialized. Use --force to reinitialize.")
            raise typer.Exit(1)
    
    except Exception as e:
        logger.error(f"Error initializing project: {e}")
        display_error(f"Failed to initialize project: {e}")
        raise typer.Exit(1)

@app.command()
@_run_async
async def parse_prd(
    prd_file: str = typer.Argument(..., help="Path to the PRD file"),
    num_tasks: int = typer.Option(
        None, "--num-tasks", "-n", help="Number of tasks to generate"
    )
):
    """Parse a PRD file and generate tasks."""
    try:
        task_manager = get_task_manager()
        await task_manager.parse_prd(prd_file, num_tasks)
    except Exception as e:
        display_error(f"Failed to parse PRD: {e}")
        raise typer.Exit(1)

@app.command()
def list(
    status: Optional[str] = typer.Option(
        None, "--status", "-s", help="Filter by status"
    ),
    priority: Optional[str] = typer.Option(
        None, "--priority", "-p", help="Filter by priority"
    )
):
    """List all tasks."""
    try:
        task_manager = get_task_manager()
        tasks = task_manager.list_tasks(status=status, priority=priority)
        display_task_list(tasks)
    except Exception as e:
        display_error(f"Failed to list tasks: {e}")
        raise typer.Exit(1)

@app.command()
@_run_async
async def expand_task(
    task_id: str = typer.Argument(..., help="ID of the task to expand"),
    num_subtasks: int = typer.Option(
        5, "--num-subtasks", "-n", help="Number of subtasks to generate"
    ),
    use_research: bool = typer.Option(
        False, "--research", "-r", help="Use research for generating subtasks"
    ),
    additional_context: str = typer.Option(
        "", "--context", "-c", help="Additional context for generating subtasks"
    )
):
    """Expand a task into subtasks."""
    try:
        display_banner()
        task_manager = get_task_manager()
        await task_manager.expand_task(
            task_id,
            num_subtasks,
            use_research,
            additional_context
        )
    except Exception as e:
        display_error(f"Failed to expand task: {e}")
        raise typer.Exit(1)

@app.command()
@_run_async
async def status(
    task_id: str = typer.Argument(..., help="ID of the task to update"),
    status: str = typer.Argument(..., help="New status for the task")
):
    """Set the status of one or more tasks."""
    try:
        task_manager = get_task_manager()
        await task_manager.set_task_status(task_id, status)
    except Exception as e:
        display_error(f"Failed to update task status: {e}")
        raise typer.Exit(1)

@app.command()
@_run_async
async def priority(
    task_id: str = typer.Argument(..., help="ID of the task to update"),
    priority: str = typer.Argument(..., help="New priority for the task")
):
    """Set the priority of one or more tasks."""
    try:
        task_manager = get_task_manager()
        await task_manager.set_task_priority(task_id, priority)
    except Exception as e:
        display_error(f"Failed to set task priority: {e}")
        raise typer.Exit(1)

@app.command()
@_run_async
async def analyze(
    task_id: Optional[str] = typer.Argument(
        None,
        help="Optional ID of a specific task to analyze. If not provided, all tasks will be analyzed."
    ),
    output_file: str = typer.Option(
        "tasks/task-complexity-report.json", 
        "--output", 
        "-o", 
        help="Path to save the complexity report"
    ),
    use_research: bool = typer.Option(
        False, 
        "--research", 
        "-r", 
        help="Use research for analysis"
    ),
    use_dspy: bool = typer.Option(
        False,
        "--dspy",
        "-d",
        help="Use DSPy-based complexity analysis module instead of Perplexity/Claude"
    ),
    skip_subtasks: bool = typer.Option(
        False,
        "--skip-subtasks",
        "-s",
        help="Skip analyzing subtasks and only analyze parent tasks"
    ),
    export_training: bool = typer.Option(
        False,
        "--export-training",
        "-e",
        help="Export training data from previous analyses for DSPy training"
    )
):
    """Analyze task complexity and generate expansion recommendations."""
    try:
        task_manager = get_task_manager()
        
        if export_training:
            from .complexity_training_logger import complexity_logger
            complexity_logger.export_training_dataset()
            console.print("[green]Training data exported successfully.[/green]")
            return
        
        await task_manager.analyze_task_complexity(
            task_id=task_id,
            output_file=output_file,
            use_research=use_research,
            use_dspy=use_dspy,
            analyze_subtasks=not skip_subtasks
        )
    except Exception as e:
        display_error(f"Failed to analyze tasks: {e}")
        raise typer.Exit(1)

@app.command()
def next():
    """Show the next task to work on."""
    try:
        task_manager = get_task_manager()
        task_manager.show_next_task()
    except Exception as e:
        display_error(f"Failed to show next task: {e}")
        raise typer.Exit(1)

@app.command()
def show(
    task_id: str = typer.Argument(..., help="ID of the task to show")
):
    """Show detailed information about a task."""
    try:
        task_manager = get_task_manager()
        task_manager.show_task(task_id)
    except Exception as e:
        display_error(f"Failed to show task: {e}")
        raise typer.Exit(1)

@app.command()
@_run_async
async def review(
    report_file: str = typer.Option(
        "tasks/task-complexity-report.json", 
        "--report", 
        "-r", 
        help="Path to the complexity report file"
    ),
    threshold: float = typer.Option(
        5.0, 
        "--threshold", 
        "-t", 
        help="Complexity score threshold for recommending expansion"
    ),
    output_file: str = typer.Option(
        "tasks/approved-expansions.json", 
        "--output", 
        "-o", 
        help="Path to save the approved expansions"
    ),
    non_interactive: bool = typer.Option(
        False, 
        "--non-interactive", 
        "-n", 
        help="Run in non-interactive mode, approving all recommendations above threshold"
    )
):
    """Review task complexity recommendations and approve tasks for expansion."""
    try:
        task_manager = get_task_manager()
        approved_tasks = task_manager.review_complexity_recommendations(
            report_file=report_file,
            threshold=threshold,
            non_interactive=non_interactive
        )
        
        # Save approved tasks to file
        if approved_tasks:
            with open(output_file, "w") as f:
                json.dump({"approved_expansions": approved_tasks}, f, indent=2)
            
            if task_manager.display_output:
                display_success(f"Saved {len(approved_tasks)} approved expansions to {output_file}")
                display_info("Run 'taskinator implement' to expand these tasks")
        else:
            if task_manager.display_output:
                display_info("No tasks were approved for expansion")
    
    except Exception as e:
        logger.error(f"Error reviewing recommendations: {e}")
        if task_manager.display_output:
            display_error(f"Failed to review recommendations: {e}")

@app.command()
@_run_async
async def implement(
    approved_file: str = typer.Option(
        "tasks/approved-expansions.json", 
        "--approved", 
        "-a", 
        help="Path to the approved expansions file"
    ),
    num_subtasks: int = typer.Option(
        None, 
        "--num-subtasks", 
        "-n", 
        help="Override the recommended number of subtasks"
    )
):
    """Implement approved task expansions by expanding tasks into subtasks."""
    try:
        task_manager = get_task_manager()
        
        # Read the approved expansions file
        if not Path(approved_file).exists():
            if task_manager.display_output:
                display_error(f"Approved expansions file not found: {approved_file}")
            raise typer.Exit(1)
        
        with open(approved_file, "r") as f:
            approved_data = json.load(f)
        
        if "approved_expansions" not in approved_data or not approved_data["approved_expansions"]:
            if task_manager.display_output:
                display_error("No approved expansions found in the file")
            raise typer.Exit(1)
        
        approved_expansions = approved_data["approved_expansions"]
        
        # Display banner
        display_banner()
        
        # Show summary of what will be implemented
        console = Console()
        console.print()
        
        # Create a table showing tasks to be expanded
        table = Table(title="Tasks to be Expanded", show_header=True, header_style="bold cyan")
        table.add_column("ID", style="cyan", justify="right")
        table.add_column("Task", style="white")
        table.add_column("Subtasks", justify="center")
        
        for expansion in approved_expansions:
            task_id = expansion.get("taskId")
            title = expansion.get("taskTitle", "Unknown")
            subtask_count = num_subtasks if num_subtasks is not None else expansion.get("recommendedSubtasks", 5)
            table.add_row(
                str(task_id),
                title,
                str(subtask_count)
            )
        
        console.print(Panel(table, border_style="blue", expand=False))
        console.print()
        
        # Process each approved expansion
        successful_expansions = 0
        
        for i, expansion in enumerate(approved_expansions):
            task_id = expansion.get("taskId")
            if not task_id:
                continue
                
            # Get the recommended number of subtasks or use the override
            subtask_count = num_subtasks if num_subtasks is not None else expansion.get("recommendedSubtasks", 5)
            
            # Get the expansion prompt
            expansion_prompt = expansion.get("expansionPrompt", "")
            
            # Show progress
            progress_text = f"[{i+1}/{len(approved_expansions)}] "
            console.print(f"{progress_text}[bold cyan]Expanding Task {task_id}[/bold cyan]: {expansion.get('taskTitle', '')}")
            
            try:
                # Expand the task
                expanded_task = await task_manager.expand_task(
                    task_id=task_id,
                    num_subtasks=subtask_count,
                    additional_context=expansion_prompt,
                    display_output=False  # We'll handle our own output
                )
                
                # Show success message
                console.print(f"{' ' * len(progress_text)}[bold green]✓[/bold green] Successfully expanded into {len(expanded_task.get('subtasks', []))} subtasks")
                successful_expansions += 1
                
            except Exception as e:
                # Show error message
                console.print(f"{' ' * len(progress_text)}[bold red]✗[/bold red] Failed: {str(e)}")
            
            # Add separator between tasks
            if i < len(approved_expansions) - 1:
                console.print()
        
        # Show final summary
        console.print()
        if successful_expansions == len(approved_expansions):
            display_success(f"Successfully implemented all {successful_expansions} task expansions")
        else:
            display_info(f"Implemented {successful_expansions} out of {len(approved_expansions)} task expansions")
        
        # Suggest next steps
        console.print(Panel(
            "[bold]Next Steps:[/bold]\n"
            "1. Run [cyan]taskinator list[/cyan] to view all tasks\n"
            "2. Run [cyan]taskinator analyze[/cyan] to analyze the complexity of the new subtasks",
            title="What's Next",
            border_style="green",
            expand=False
        ))
    
    except Exception as e:
        logger.error(f"Error implementing expansions: {e}")
        if task_manager.display_output:
            display_error(f"Failed to implement expansions: {e}")
        raise typer.Exit(1)

@app.command()
@_run_async
async def sync(
    task_id: Optional[str] = typer.Argument(None, help="ID of the task to sync (all tasks if not specified)"),
    system: Optional[str] = typer.Option(None, "--system", "-s", help="External system identifier"),
    direction: str = typer.Option(
        "bidirectional", 
        "--direction", 
        "-d", 
        help="Sync direction (push, pull, bidirectional)"
    ),
    config_file: Path = typer.Option(
        None, 
        "--config", 
        "-c", 
        help="Path to configuration file for external systems"
    ),
    auto_resolve: bool = typer.Option(
        False,
        "--auto-resolve/--no-auto-resolve",
        help="Automatically resolve conflicts"
    ),
    resolution_strategy: str = typer.Option(
        "newest_wins",
        "--strategy",
        "-r",
        help="Conflict resolution strategy (local_wins, remote_wins, newest_wins, manual)"
    ),
    interactive: bool = typer.Option(
        True,
        "--interactive/--non-interactive",
        help="Use interactive conflict resolution for conflicts"
    ),
    background: bool = typer.Option(
        False,
        "--background",
        "-b",
        help="Run in background"
    )
):
    """Synchronize tasks with external systems."""
    try:
        # Initialize sync manager
        sync_manager = SyncManager()
        await sync_manager.initialize()
        
        # Load config if provided
        config = None
        if config_file:
            if not config_file.exists():
                display_error(f"Config file not found: {config_file}")
                raise typer.Exit(1)
            
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
            except json.JSONDecodeError:
                display_error(f"Invalid JSON in config file: {config_file}")
                raise typer.Exit(1)
        
        # Validate resolution strategy
        from .conflict_resolver import ConflictResolutionStrategy
        try:
            strategy = ConflictResolutionStrategy(resolution_strategy)
        except ValueError:
            display_error(f"Invalid resolution strategy: {resolution_strategy}")
            display_info("Valid strategies: local_wins, remote_wins, newest_wins, manual")
            raise typer.Exit(1)
        
        # Sync tasks
        if task_id:
            # Sync specific task
            result = await sync_manager.sync_task(
                task_id, 
                direction=direction,
                system=system,
                config=config,
                auto_resolve=auto_resolve,
                resolution_strategy=strategy,
                interactive=interactive
            )
            
            # Display result
            if result.get("details"):
                detail = result["details"][0]
                status = detail.get("status", "")
                message = detail.get("message", "")
                
                if status == SyncStatus.SYNCED:
                    display_success(f"Task {task_id} synchronized successfully")
                    
                    # Show conflicts if any
                    if any(s["status"] == SyncStatus.CONFLICT for s in result["systems"]):
                        display_info("Conflicts detected during synchronization")
                        
                        if not auto_resolve and not interactive:
                            display_info("Use 'taskinator resolve <task_id>' to resolve conflicts")
                else:
                    display_error(f"Failed to synchronize task {task_id}: {message}")
            else:
                display_info(f"Task {task_id} sync completed")
        else:
            # Sync all tasks
            results = await sync_manager.sync_all(
                direction=direction,
                system=system,
                config=config,
                auto_resolve=auto_resolve,
                resolution_strategy=strategy,
                interactive=interactive
            )
            
            # Display results
            display_success(f"Synchronized {results['total']} tasks")
            
            if results["conflicts"] > 0:
                display_info(f"Detected {results['conflicts']} conflicts during synchronization")
                
                if not auto_resolve and not interactive:
                    display_info("Use 'taskinator conflicts' to view all conflicts")
                    display_info("Use 'taskinator resolve <task_id>' to resolve conflicts")
            
            if results["errors"] > 0:
                display_error(f"Encountered {results['errors']} errors during synchronization")
        
        if background:
            # Start background sync manager if not running
            if not background_sync_manager._running:
                console = Console()
                console.print(Panel("Starting background synchronization service...", title="Info", border_style="blue"))
                background_sync_manager.start()
            
            # Add jobs for each task
            job_ids = []
            if task_id:
                job_id = background_sync_manager.add_job(task_id, system, direction, JobPriority.HIGH)
                job_ids.append(job_id)
            else:
                tasks_file = Path("tasks/tasks.json")
                if not tasks_file.exists():
                    logger.error("Tasks file not found: tasks/tasks.json")
                    return
                
                # Load tasks from file
                try:
                    with open(tasks_file, "r") as f:
                        tasks_data = json.load(f)
                        
                    # Get the tasks list from the JSON object
                    tasks_list = tasks_data.get("tasks", [])
                    
                    # Add jobs for each task
                    for task in tasks_list:
                        task_id = str(task["id"])
                        job_id = background_sync_manager.add_job(task_id, system, direction, JobPriority.HIGH)
                        job_ids.append(job_id)
                    
                    console = Console()
                    console.print(Panel(f"Added {len(job_ids)} jobs to queue", title="Success", border_style="green"))
                    console.print("Run 'taskinator background jobs' to monitor job status")
                except Exception as e:
                    logger.error(f"Error loading tasks: {e}")
                    return
    
    except Exception as e:
        display_error(f"Error: {e}")
        raise typer.Exit(1)

@app.command()
@_run_async
async def init_sync(
    system: str = typer.Option("nextcloud", "--system", "-s", help="External system to sync with (e.g., nextcloud)"),
    calendar: str = typer.Option("Taskinator", "--calendar", "-c", help="Calendar name to use (will be created if it doesn't exist)"),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Show verbose output, including credentials being used"
    ),
):
    """Initialize synchronization with an external system."""
    try:
        # Load environment variables
        load_dotenv()
        
        # Get configuration for the system
        nextcloud_config = get_sync_config(system)
        if verbose:
            display_info(f"Using credentials for {system}:")
            for key, value in nextcloud_config.items():
                if key in ["host", "username"]:
                    display_info(f"  {key}: {value}")
                elif key in ["password", "token"]:
                    if value:
                        display_info(f"  {key}: ***")
                    else:
                        display_info(f"  {key}: <not set>")
            display_info(f"Using calendar: {calendar}")
        

        sync_manager = SyncManager(
            tasks_file=None,  # No need for tasks file for initialization
            nextcloud_host=nextcloud_config.get("host"),
            nextcloud_username=nextcloud_config.get("username"),
            nextcloud_password=nextcloud_config.get("password"),
            nextcloud_token=nextcloud_config.get("token"),
            nextcloud_calendar=calendar,
            verbose=verbose
        )
        
        try:
            # Initialize the sync manager
            display_info(f"Initializing synchronization with {system}...")
            results = await sync_manager.initialize()
            
            # Check if initialization was successful
            if system in results:
                if results[system]["status"] == "success":
                    display_success(f"Synchronization initialized successfully with {system}")
                    display_info(f"Calendar '{calendar}' is ready for use")
                else:
                    display_error(f"Failed to initialize synchronization with {system}: {results[system]['message']}")
                    display_info("However, you may still be able to use existing calendars if they were found.")
            else:
                display_error(f"No initialization results for {system}")
        
        finally:
            # Ensure we close any open sessions
            if hasattr(sync_manager, 'adapters') and system in sync_manager.adapters:
                adapter = sync_manager.adapters[system]
                if hasattr(adapter, 'client') and adapter.client:
                    if hasattr(adapter.client, 'session') and adapter.client.session:
                        await adapter.client.session.close()
                        if verbose:
                            display_info("Closed client session")
    
    except Exception as e:
        display_error(f"Error initializing synchronization: {e}")
        raise typer.Exit(1)

@app.command()
@_run_async
async def push_tasks(
    task_ids: Optional[List[str]] = None,
    system: str = "nextcloud",
    all_tasks: bool = False,
    verbose: bool = False,
    background: bool = typer.Option(False, "--background", "-b", help="Run in background")
):
    """Push tasks to an external system."""
    console = Console()
    
    # If background mode is enabled, use the background sync manager
    if background:
        # Start background sync manager if not running
        if not background_sync_manager._running:
            console.print(Panel("Starting background synchronization service...", title="Info", border_style="blue"))
            background_sync_manager.start()
        
        # Get tasks to push
        tasks = get_tasks_for_sync(task_ids, all_tasks)
        if not tasks:
            console.print(Panel("No tasks to push", title="Info", border_style="blue"))
            return
        
        # Add jobs for each task
        job_ids = []
        for task in tasks:
            task_id = str(task["id"])
            job_id = background_sync_manager.add_job(task_id, system, SyncDirection.PUSH, JobPriority.HIGH)
            job_ids.append(job_id)
        
        console.print(Panel(f"Added {len(job_ids)} jobs to queue", title="Success", border_style="green"))
        console.print("Run 'taskinator background jobs' to monitor job status")
        return
    
    # Otherwise, run synchronously
    try:
        # Load the plugin for the specified system
        plugin_name = f"{system}_adapter"
        if not plugin_registry.load_plugin(plugin_name):
            console.print(Panel(f"Failed to load plugin for system '{system}'", title="Error", border_style="red"))
            raise typer.Exit(1)
        
        # Get the adapter instance
        adapter = await plugin_registry.get_adapter_instance(system, **get_sync_config(system))
        if not adapter:
            console.print(Panel(f"Failed to create adapter for system '{system}'", title="Error", border_style="red"))
            raise typer.Exit(1)
        
        # Get tasks to push
        tasks = get_tasks_for_sync(task_ids, all_tasks)
        if not tasks:
            console.print(Panel("No tasks to push", title="Info", border_style="blue"))
            return
            
        console.print(f"Pushing {len(tasks)} tasks to {system}...")
        
        # Create a table for results
        table = Table(title=f"Push Results ({system})", box=box.ROUNDED)
        table.add_column("Task ID", style="cyan")
        table.add_column("Title", style="green")
        table.add_column("Status", style="yellow")
        table.add_column("Message", style="blue")
        
        # Push each task
        for task in tasks:
            try:
                # Push the task
                updated_task = await adapter.sync_task(task, direction=SyncDirection.PUSH.value)
                
                # Debug log the task structure
                logger.debug(f"Task returned from sync_task: {updated_task}")
                
                # Get metadata
                status = "unknown"
                message = ""
                
                # Try to get metadata from the task
                if isinstance(updated_task, dict):
                    if "sync_status" in updated_task:
                        status = updated_task.get("sync_status", "unknown")
                        message = updated_task.get("message", "")
                    elif "external_sync" in updated_task:
                        if system in updated_task["external_sync"]:
                            metadata = updated_task["external_sync"][system]
                            logger.debug(f"metadata for {system}: {metadata}")
                            status = metadata.get("sync_status", "unknown")
                            message = metadata.get("message", "")
                
                # Add row to table
                table.add_row(
                    str(task["id"]),
                    task["title"],
                    status,
                    message
                )
                
            except SyncError as e:
                # Handle sync error
                table.add_row(
                    str(task["id"]),
                    task["title"],
                    "error",
                    e.get_user_friendly_message()
                )
                
            except Exception as e:
                # Handle other errors
                table.add_row(
                    str(task["id"]),
                    task["title"],
                    "error",
                    str(e)
                )
        
        # Display results
        console.print(table)
        
    except Exception as e:
        console.print(Panel(f"Error: {e}", title="Error", border_style="red"))
        raise typer.Exit(1)
    finally:
        # Close the adapter
        if 'adapter' in locals() and adapter:
            await plugin_registry.close_adapter(system)

@app.command()
@_run_async
async def pull_tasks(
    task_ids: Optional[List[str]] = None,
    system: str = "nextcloud",
    all_tasks: bool = False,
    verbose: bool = False,
    background: bool = typer.Option(False, "--background", "-b", help="Run in background")
):
    """Pull tasks from an external system."""
    console = Console()
    
    # If background mode is enabled, use the background sync manager
    if background:
        # Start background sync manager if not running
        if not background_sync_manager._running:
            console.print(Panel("Starting background synchronization service...", title="Info", border_style="blue"))
            background_sync_manager.start()
        
        # Get tasks to pull
        tasks = get_tasks_for_sync(task_ids, all_tasks)
        if not tasks:
            console.print(Panel("No tasks to pull", title="Info", border_style="blue"))
            return
        
        # Add jobs for each task
        job_ids = []
        for task in tasks:
            task_id = str(task["id"])
            job_id = background_sync_manager.add_job(task_id, system, SyncDirection.PULL, JobPriority.HIGH)
            job_ids.append(job_id)
        
        console.print(Panel(f"Added {len(job_ids)} jobs to queue", title="Success", border_style="green"))
        console.print("Run 'taskinator background jobs' to monitor job status")
        return
    
    # Otherwise, run synchronously
    try:
        # Load the plugin for the specified system
        plugin_name = f"{system}_adapter"
        if not plugin_registry.load_plugin(plugin_name):
            console.print(Panel(f"Failed to load plugin for system '{system}'", title="Error", border_style="red"))
            raise typer.Exit(1)
        
        # Get the adapter instance
        adapter = await plugin_registry.get_adapter_instance(system, **get_sync_config(system))
        if not adapter:
            console.print(Panel(f"Failed to create adapter for system '{system}'", title="Error", border_style="red"))
            raise typer.Exit(1)
        
        # Get tasks to pull
        tasks = get_tasks_for_sync(task_ids, all_tasks)
        if not tasks:
            console.print(Panel("No tasks to pull", title="Info", border_style="blue"))
            return
            
        console.print(f"Pulling {len(tasks)} tasks from {system}...")
        
        # Create a table for results
        table = Table(title=f"Pull Results ({system})", box=box.ROUNDED)
        table.add_column("Task ID", style="cyan")
        table.add_column("Title", style="green")
        table.add_column("Status", style="yellow")
        table.add_column("Message", style="blue")
        
        # Pull each task
        for task in tasks:
            try:
                # Pull the task
                updated_task = await adapter.sync_task(task, direction=SyncDirection.PULL.value)
                
                # Get metadata
                metadata = updated_task.get("metadata", {}).get(system, {})
                status = metadata.get("sync_status", "unknown")
                message = metadata.get("message", "")
                
                # Correctly extract the sync status from the task metadata
                if "external_sync" in updated_task and system in updated_task["external_sync"]:
                    status = updated_task["external_sync"][system].get("sync_status", "unknown")
                
                # Add row to table
                table.add_row(
                    str(task["id"]),
                    task["title"],
                    status,
                    message
                )
                
            except SyncError as e:
                # Handle sync error
                table.add_row(
                    str(task["id"]),
                    task["title"],
                    "error",
                    e.get_user_friendly_message()
                )
                
            except Exception as e:
                # Handle other errors
                table.add_row(
                    str(task["id"]),
                    task["title"],
                    "error",
                    str(e)
                )
        
        # Display results
        console.print(table)
        
    except Exception as e:
        console.print(Panel(f"Error: {e}", title="Error", border_style="red"))
        raise typer.Exit(1)
    finally:
        # Close the adapter
        if 'adapter' in locals() and adapter:
            await plugin_registry.close_adapter(system)

@app.command()
@_run_async
async def link_task(
    task_id: str = typer.Argument(..., help="ID of the task to link"),
    system: str = typer.Option("nextcloud", "--system", "-s", help="External system to link with (e.g., nextcloud)"),
    external_id: str = typer.Option(..., "--external-id", "-e", help="External task ID to link with"),
    calendar: str = typer.Option("Taskinator", "--calendar", "-c", help="Calendar name to use (will be created if it doesn't exist)"),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Show verbose output, including credentials being used"
    ),
):
    """Link a local task with an external task."""
    try:
        # Load environment variables
        load_dotenv()
        
        # Get task manager
        task_manager = TaskManager()
        
        # Get configuration for the system
        config = get_sync_config(system)
        
        if verbose:
            display_info(f"Using credentials for {system}:")
            for key, value in config.items():
                if key in ["host", "username"]:
                    display_info(f"  {key}: {value}")
                elif key in ["password", "token"]:
                    if value:
                        display_info(f"  {key}: ***")
                    else:
                        display_info(f"  {key}: <not set>")
            display_info(f"Using calendar: {calendar}")
        
        # Create sync manager
        nextcloud_config = config.get("nextcloud", {})
        sync_manager = SyncManager(
            tasks_file=task_manager.tasks_file,
            nextcloud_host=nextcloud_config.get("host"),
            nextcloud_username=nextcloud_config.get("username"),
            nextcloud_password=nextcloud_config.get("password"),
            nextcloud_token=nextcloud_config.get("token"),
            nextcloud_calendar=calendar,
            verbose=verbose
        )
        
        try:
            # Initialize the sync manager
            await sync_manager.initialize()
            
            # Get task
            task_id = int(task_id)
            task = task_manager.get_task(task_id)
            
            if not task:
                display_error(f"Task {task_id} not found")
                raise typer.Exit(1)
            
            # Link task
            display_info(f"Linking task {task_id} with external task {external_id}...")
            result = await sync_manager.link_task(task, system, external_id)
            
            if result:
                display_success(f"Task {task_id} linked successfully")
                
                # Update task in task manager
                task_manager.update_task(result)
                task_manager.save_tasks()
            else:
                display_error(f"Failed to link task {task_id}")
        finally:
            # Ensure we close any open sessions
            if hasattr(sync_manager, 'adapters') and system in sync_manager.adapters:
                adapter = sync_manager.adapters[system]
                if hasattr(adapter, 'client') and adapter.client:
                    if hasattr(adapter.client, 'session') and adapter.client.session:
                        await adapter.client.session.close()
                        if verbose:
                            display_info("Closed client session")
    
    except Exception as e:
        display_error(f"Error: {e}")
        raise typer.Exit(1)

@app.command()
@_run_async
async def resolve(
    task_id: str = typer.Argument(..., help="ID of the task with conflicts to resolve"),
    field: Optional[str] = typer.Option(None, "--field", "-f", help="Specific field to resolve"),
    resolution: Optional[str] = typer.Option(None, "--resolution", "-r", help="Resolution strategy (local, remote)"),
    interactive: bool = typer.Option(True, "--interactive/--non-interactive", help="Use interactive conflict resolution for conflicts")
):
    """Resolve conflicts for a task interactively."""
    try:
        # Read tasks file
        tasks_file = config.tasks_dir / "tasks.json"
        data = read_json(tasks_file)
        tasks = data.get("tasks", [])
        
        # Find task by ID
        task = None
        task_index = -1
        for i, t in enumerate(tasks):
            if str(t.get("id")) == str(task_id):
                task = t
                task_index = i
                break
        
        if not task:
            display_error(f"Task not found: {task_id}")
            raise typer.Exit(1)
        
        # Create conflict UI
        conflict_ui = ConflictUI()
        
        if field and resolution:
            # Resolve specific field
            from .conflict_resolver import ManualConflictResolver
            resolver = ManualConflictResolver()
            
            if resolution not in ["local", "remote"]:
                display_error(f"Invalid resolution: {resolution}. Must be 'local' or 'remote'")
                raise typer.Exit(1)
            
            updated_task = resolver.resolve_field_conflict(task, field, resolution)
            
            # Update task in data
            data["tasks"][task_index] = updated_task
            
            # Write updated tasks back to file
            write_json(tasks_file, data)
            
            display_success(f"Resolved conflict for field '{field}' in task {task_id} using {resolution} value")
            
        elif interactive:
            # Interactive resolution
            if field:
                # Show details for specific field
                conflict_ui.display_conflict_details(task, field)
            else:
                # Resolve all conflicts interactively
                updated_task = conflict_ui.resolve_conflict_interactive(task)
                
                # Update task in data
                data["tasks"][task_index] = updated_task
                
                # Write updated tasks back to file
                write_json(tasks_file, data)
        else:
            # Just show conflict summary
            conflict_ui.display_conflict_summary(task)
            
    except Exception as e:
        display_error(f"Failed to resolve conflicts: {e}")
        raise typer.Exit(1)

@app.command()
@_run_async
async def conflicts():
    """List all tasks with conflicts."""
    try:
        # Read tasks file
        tasks_file = config.tasks_dir / "tasks.json"
        data = read_json(tasks_file)
        tasks = data.get("tasks", [])
        
        # Display conflicts using the presentation system
        conflict_presentation_system.display_dashboard(tasks)
        
    except Exception as e:
        display_error(f"Failed to list conflicts: {e}")
        raise typer.Exit(1)

@app.command()
@_run_async
async def conflict_history(
    task_id: str = typer.Argument(..., help="ID of the task to show conflict history for")
):
    """Show conflict resolution history for a task."""
    try:
        # Read tasks file
        tasks_file = config.tasks_dir / "tasks.json"
        data = read_json(tasks_file)
        tasks = data.get("tasks", [])
        
        # Find task by ID
        task = None
        for t in tasks:
            if str(t.get("id")) == str(task_id):
                task = t
                break
        
        if not task:
            display_error(f"Task not found: {task_id}")
            raise typer.Exit(1)
        
        # Display conflict history
        conflict_presentation_system.display_conflict_history(task)
        
    except Exception as e:
        display_error(f"Failed to show conflict history: {e}")
        raise typer.Exit(1)

@app.command()
@_run_async
async def conflict_preferences(
    default_strategy: Optional[str] = typer.Option(None, "--default", "-d", help="Set default resolution strategy"),
    field: Optional[str] = typer.Option(None, "--field", "-f", help="Field name for preference"),
    system: Optional[str] = typer.Option(None, "--system", "-s", help="System name for preference"),
    strategy: Optional[str] = typer.Option(None, "--strategy", "-r", help="Resolution strategy")
):
    """Manage conflict resolution preferences."""
    try:
        if default_strategy:
            # Set default strategy
            conflict_presentation_system.set_default_strategy(default_strategy)
            display_success(f"Default strategy set to: {default_strategy}")
        
        elif field and strategy:
            # Set field preference
            conflict_presentation_system.set_field_preference(field, strategy)
            display_success(f"Field preference set for {field}: {strategy}")
        
        elif system and strategy:
            # Set system preference
            conflict_presentation_system.set_system_preference(system, strategy)
            display_success(f"System preference set for {system}: {strategy}")
        
        else:
            # Display current preferences
            conflict_presentation_system.display_preferences()
        
    except Exception as e:
        display_error(f"Failed to manage conflict preferences: {e}")
        raise typer.Exit(1)

@app.command()
@_run_async
async def migrate(
    migration: str = typer.Argument(..., help="Migration to run"),
    tasks_file: Path = typer.Option(None, "--file", "-f", help="Path to tasks.json file")
):
    """Run a database migration."""
    try:
        # Determine tasks file path
        if not tasks_file:
            task_manager = TaskManager(display_output=True)
            tasks_file = task_manager.tasks_file
        
        # Check if migration exists
        try:
            migration_module = importlib.import_module(f"taskinator.migrations.{migration}")
        except ImportError:
            display_error(f"Migration not found: {migration}")
            raise typer.Exit(1)
        
        # Run migration
        display_info(f"Running migration: {migration}")
        migration_module.run_migration(tasks_file)
        display_success(f"Migration completed successfully: {migration}")
        
    except Exception as e:
        display_error(f"Error: {e}")
        raise typer.Exit(1)

@app.command()
@_run_async
async def reintegrate(
    pdd_dir: str = typer.Option(
        "pdds",
        "--pdd-dir",
        "-d",
        help="Directory containing PDD files"
    ),
    include_pdds: bool = typer.Option(
        True,
        "--include-pdds/--skip-pdds",
        help="Whether to include PDD files in reintegration"
    )
):
    """Reintegrate content from individual files back into their respective JSON files.
    
    This command reads all individual task files and updates the corresponding entries
    in the tasks.json file with any additional content found in those files. This is
    particularly useful for preserving notes and design constraints added to individual
    task files.
    
    It also reintegrates PDD files back into the processes.json file, preserving any
    modifications made to the individual PDD files.
    
    Feedback comments enclosed in curly braces {} will be processed and incorporated
    into the tasks. For example, adding a comment like:
    { The List[] definitions for the fields should be classes, not str }
    will be processed and the task will be updated accordingly.
    """
    try:
        task_manager = get_task_manager()
        
        # Reintegrate task files
        task_stats = await task_manager.reintegrate_task_files()
        
        # Generate task files again to ensure consistency
        if task_stats["tasks_updated"] > 0:
            await task_manager.generate_task_files()
            
            # Display feedback processing information if available
            if "feedback_processed" in task_stats and task_stats["feedback_processed"] > 0:
                display_success(
                    f"\nFeedback processed for {task_stats['feedback_processed']} tasks. "
                    f"Task files have been regenerated with the incorporated feedback."
                )
        
        # Reintegrate PDD files if requested
        if include_pdds:
            display_info("\nReintegrating PDD files...")
            pdd_stats = await task_manager.reintegrate_pdd_files(pdd_dir=pdd_dir)
            
            # Display combined statistics
            if task_stats["tasks_updated"] > 0 or pdd_stats["processes_updated"] > 0:
                display_success(
                    f"\nReintegration complete:\n"
                    f"- Updated {task_stats['tasks_updated']} tasks\n"
                    f"- Updated {pdd_stats['processes_updated']} processes"
                )
            
    except Exception as e:
        display_error(f"Failed to reintegrate files: {e}")
        raise typer.Exit(1)

@app.command()
@_run_async
async def research(
    task_id: int = typer.Argument(..., help="ID of the task to research"),
    subtask_id: Optional[int] = typer.Option(
        None, "--subtask", "-s", help="ID of the subtask to research"
    ),
    output: Optional[str] = typer.Option(
        None, "--output", "-o", help="Path to save the research report"
    ),
    context: Optional[str] = typer.Option(
        None, "--context", "-c", help="Additional context for the research"
    ),
    depth: int = typer.Option(
        2, "--depth", "-d", help="Research depth (1-3, where 3 is most thorough)"
    ),
    runtime_research: bool = typer.Option(
        False, "--runtime-research", "-r", help="Enable runtime research"
    )
):
    """
    Conduct targeted research on a specific task or subtask.
    
    This command uses AI to research implementation details, best practices,
    and relevant technologies for a given task or subtask. The research
    results are displayed and can optionally be saved to a file.
    """
    try:
        task_manager = get_task_manager()
        
        # Validate depth
        if depth < 1 or depth > 3:
            display_error("Depth must be between 1 and 3")
            raise typer.Exit(1)
        
        # Conduct research
        progress = create_loading_indicator(
            f"Conducting research on task {task_id}" + 
            (f", subtask {subtask_id}" if subtask_id else "") +
            f" (depth: {depth})..."
        )
        progress.start()
        
        try:
            research_results = task_manager.conduct_research(
                task_id=task_id,
                subtask_id=subtask_id,
                additional_context=context,
                depth=depth,
                runtime_research=runtime_research
            )
        finally:
            progress.stop()
        
        # Display research results
        console = Console()
        
        # Create a panel for the research summary
        summary_panel = Panel(
            str(research_results.get("summary", "Research completed successfully.")),
            title="Research Summary",
            border_style="cyan",
            expand=False
        )
        console.print(summary_panel)
        
        # Create a panel for key findings
        if "key_findings" in research_results:
            findings_md = Markdown(str(research_results["key_findings"]))
            findings_panel = Panel(
                findings_md,
                title="Key Findings",
                border_style="green",
                expand=False
            )
            console.print(findings_panel)
        
        # Create a panel for implementation recommendations
        if "recommendations" in research_results:
            recommendations_md = Markdown(str(research_results["recommendations"]))
            recommendations_panel = Panel(
                recommendations_md,
                title="Implementation Recommendations",
                border_style="magenta",
                expand=False
            )
            console.print(recommendations_panel)
        
        # Create a panel for resources
        if "resources" in research_results:
            resources_md = Markdown(str(research_results["resources"]))
            resources_panel = Panel(
                resources_md,
                title="Resources",
                border_style="yellow",
                expand=False
            )
            console.print(resources_panel)
        
        # Save to file if requested
        if output:
            output_path = Path(output)
            
            # Create directory if it doesn't exist
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Format as markdown
            markdown_content = f"# Research Report: Task {task_id}"
            if subtask_id:
                markdown_content += f", Subtask {subtask_id}"
            markdown_content += f"\n\n*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n"
            
            markdown_content += f"## Summary\n\n{research_results.get('summary', 'Research completed successfully.')}\n\n"
            
            if "key_findings" in research_results:
                markdown_content += f"## Key Findings\n\n{research_results['key_findings']}\n\n"
            
            if "recommendations" in research_results:
                markdown_content += f"## Implementation Recommendations\n\n{research_results['recommendations']}\n\n"
            
            if "resources" in research_results:
                markdown_content += f"## Resources\n\n{research_results['resources']}\n\n"
            
            # Write to file
            with open(output_path, "w") as f:
                f.write(markdown_content)
            
            display_success(f"Research report saved to {output_path}")
        
    except Exception as e:
        display_error(f"Failed to conduct research: {e}")
        raise typer.Exit(1)

@app.command()
@_run_async
async def similarity(
    threshold: float = typer.Option(
        0.7, 
        "--threshold", 
        "-t", 
        help="Similarity threshold (0-1) for considering tasks similar"
    ),
    output_file: str = typer.Option(
        "tasks/task-similarity-report.json", 
        "--output", 
        "-o", 
        help="Path to save the similarity report"
    ),
    optimize: bool = typer.Option(
        False,
        "--optimize",
        help="Use DSPy for enhanced similarity analysis"
    ),
):
    """Find similar tasks based on semantic similarity."""
    try:
        # Get task manager
        task_manager = get_task_manager()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task("Analyzing task similarities...", total=None)
            
            # Use the task manager to analyze similarities
            analysis_report = await task_manager.analyze_task_similarities(
                threshold=threshold,
                output_file=output_file,
                use_dspy=optimize
            )
        
        # Get tasks from the tasks file
        tasks_file = task_manager.tasks_file
        if os.path.exists(tasks_file):
            with open(tasks_file, 'r') as f:
                data = json.load(f)
                tasks = data.get('tasks', [])
        else:
            console.print("[yellow]No tasks file found.[/yellow]")
            return
        
        # Extract similar pairs for display
        similar_pairs = []
        if "potentialDuplicates" in analysis_report:
            similar_pairs.extend([TaskSimilarityResult(**item) for item in analysis_report["potentialDuplicates"]])
        if "highSimilarity" in analysis_report:
            similar_pairs.extend([TaskSimilarityResult(**item) for item in analysis_report["highSimilarity"]])
        
        # Filter by threshold
        similar_pairs = [p for p in similar_pairs if p.similarity_score >= threshold]
        
        # Display results
        if similar_pairs:
            console.print(f"\n[bold green]Found {len(similar_pairs)} similar task pairs:[/bold green]\n")
            
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Task 1")
            table.add_column("Task 2")
            table.add_column("Similarity")
            table.add_column("Explanation")
            
            for result in similar_pairs:
                # Find tasks by ID using a different approach
                task1 = {}
                task2 = {}
                
                for task in tasks:
                    if task.get('id') == result.task_id1:
                        task1 = task
                    if task.get('id') == result.task_id2:
                        task2 = task
                
                table.add_row(
                    f"#{result.task_id1}: {task1.get('title', 'Unknown')}",
                    f"#{result.task_id2}: {task2.get('title', 'Unknown')}",
                    f"{result.similarity_score:.2f}",
                    result.explanation
                )
            
            console.print(table)
            console.print(f"\n[bold]Full report saved to:[/bold] {output_file}")
        else:
            console.print(f"\n[yellow]No similar tasks found with threshold {threshold}.[/yellow]")
            console.print(f"[bold]Full report saved to:[/bold] {output_file}")
    
    except Exception as e:
        display_error(f"Failed to analyze task similarities: {e}")
        raise typer.Exit(1)

@app.command(name="analyze-subtasks")
@_run_async
async def analyze_subtasks(
    task_id: str = typer.Argument(
        ...,
        help="ID of the parent task whose subtasks should be analyzed"
    ),
    output_file: str = typer.Option(
        "tasks/subtask-complexity-report.json", 
        "--output", 
        "-o", 
        help="Path to save the complexity report"
    ),
    use_research: bool = typer.Option(
        False, 
        "--research", 
        "-r", 
        help="Use research for analysis"
    ),
    use_dspy: bool = typer.Option(
        False,
        "--dspy",
        "-d",
        help="Use DSPy-based complexity analysis module instead of Perplexity/Claude"
    ),
    recursive: bool = typer.Option(
        False,
        "--recursive",
        "-R",
        help="Recursively analyze all levels of subtasks"
    )
):
    """Analyze complexity of all subtasks for a specific parent task."""
    try:
        task_manager = get_task_manager()
        
        # Load tasks
        data = read_json(task_manager.tasks_file)
        
        # Find the parent task
        parent_task = None
        for t in data['tasks']:
            if str(t.get("id")) == str(task_id):
                parent_task = t
                break
        
        if not parent_task:
            display_error(f"Task {task_id} not found")
            raise typer.Exit(1)
        
        # Check if the task has subtasks
        if not parent_task.get('subtasks') or len(parent_task.get('subtasks', [])) == 0:
            display_error(f"Task {task_id} has no subtasks to analyze")
            raise typer.Exit(1)
        
        console.print(f"[bold blue]Analyzing subtasks of task {task_id}: {parent_task['title']}[/bold blue]")
        
        # Analyze the subtasks
        await task_manager.analyze_task_complexity(
            task_id=task_id,
            output_file=output_file,
            use_research=use_research,
            use_dspy=use_dspy,
            analyze_subtasks=True,
            recursive=recursive
        )
        
    except Exception as e:
        display_error(f"Failed to analyze subtasks: {e}")
        raise typer.Exit(1)

@plugin_app.command("list")
def list_plugins():
    """List all available plugins."""
    console = Console()
    
    # Discover plugins
    plugins = plugin_registry.discover_plugins()
    
    if not plugins:
        console.print(Panel("No plugins found", title="Plugins", border_style="yellow"))
        return
    
    # Create a table for plugins
    table = Table(title="Available Plugins", box=box.ROUNDED)
    table.add_column("Plugin Name", style="cyan")
    table.add_column("Status", style="green")
    
    # Get loaded plugins
    loaded_plugins = set(plugin_registry.plugin_manager.loaded_plugins)
    
    # Add rows for each plugin
    for plugin in plugins:
        status = "Loaded" if plugin in loaded_plugins else "Not Loaded"
        table.add_row(plugin, status)
    
    console.print(table)
    
    # Show available systems
    systems = plugin_registry.get_available_systems()
    if systems:
        system_table = Table(title="Available External Systems", box=box.ROUNDED)
        system_table.add_column("System ID", style="cyan")
        
        for system_id in systems:
            system_table.add_row(system_id)
        
        console.print(system_table)

@plugin_app.command("load")
def load_plugin(plugin_name: str):
    """Load a plugin by name.
    
    Args:
        plugin_name: Name of the plugin to load
    """
    console = Console()
    
    # Load the plugin
    success = plugin_registry.load_plugin(plugin_name)
    
    if success:
        console.print(Panel(f"Plugin '{plugin_name}' loaded successfully", title="Success", border_style="green"))
    else:
        console.print(Panel(f"Failed to load plugin '{plugin_name}'", title="Error", border_style="red"))

@plugin_app.command("unload")
def unload_plugin(plugin_name: str):
    """Unload a plugin by name.
    
    Args:
        plugin_name: Name of the plugin to unload
    """
    console = Console()
    
    # Unload the plugin
    success = plugin_registry.unload_plugin(plugin_name)
    
    if success:
        console.print(Panel(f"Plugin '{plugin_name}' unloaded successfully", title="Success", border_style="green"))
    else:
        console.print(Panel(f"Failed to unload plugin '{plugin_name}'", title="Error", border_style="red"))

@plugin_app.command("load-all")
def load_all_plugins():
    """Load all available plugins."""
    console = Console()
    
    # Load all plugins
    success = plugin_registry.load_all_plugins()
    
    if success:
        console.print(Panel("All plugins loaded successfully", title="Success", border_style="green"))
    else:
        console.print(Panel("Some plugins failed to load", title="Warning", border_style="yellow"))
    
    # Show loaded plugins
    list_plugins()

@plugin_app.command("info")
def plugin_info(plugin_name: str):
    """Show information about a plugin.
    
    Args:
        plugin_name: Name of the plugin
    """
    console = Console()
    
    # Get plugin info
    plugin_info = plugin_registry.get_plugin_info(plugin_name)
    
    if not plugin_info:
        console.print(Panel(f"Plugin '{plugin_name}' not found", title="Error", border_style="red"))
        raise typer.Exit(1)
    
    # Create a panel with plugin info
    info_text = f"Name: {plugin_info.name}\n"
    info_text += f"Version: {plugin_info.version}\n"
    
    if plugin_info.description:
        info_text += f"Description: {plugin_info.description}\n"
    
    if plugin_info.author:
        info_text += f"Author: {plugin_info.author}\n"
    
    # Add dependencies
    if plugin_info.dependencies:
        info_text += "\nDependencies:\n"
        for dependency in plugin_info.dependencies:
            optional_text = " (optional)" if dependency.optional else ""
            version_text = f" {dependency.version}" if dependency.version else ""
            info_text += f"  - {dependency.name}{version_text}{optional_text}\n"
    
    # Add dependent plugins
    dependents = plugin_registry.get_dependent_plugins(plugin_name)
    if dependents:
        info_text += "\nRequired by:\n"
        for dependent in dependents:
            info_text += f"  - {dependent}\n"
    
    console.print(Panel(info_text, title=f"Plugin: {plugin_info.name}", border_style="green"))

@plugin_app.command("dependencies")
def plugin_dependencies(plugin_name: str):
    """Show dependencies for a plugin.
    
    Args:
        plugin_name: Name of the plugin
    """
    console = Console()
    
    # Get plugin info
    plugin_info = plugin_registry.get_plugin_info(plugin_name)
    
    if not plugin_info:
        console.print(Panel(f"Plugin '{plugin_name}' not found", title="Error", border_style="red"))
        raise typer.Exit(1)
    
    # Create a table for dependencies
    table = Table(title=f"Dependencies for {plugin_info.name}", box=box.ROUNDED)
    table.add_column("Dependency", style="cyan")
    table.add_column("Version", style="green")
    table.add_column("Optional", style="yellow")
    table.add_column("Status", style="blue")
    
    # Add rows for each dependency
    if not plugin_info.dependencies:
        console.print(Panel(f"Plugin '{plugin_name}' has no dependencies", title="Info", border_style="blue"))
        return
    
    for dependency in plugin_info.dependencies:
        optional = "Yes" if dependency.optional else "No"
        version = dependency.version if dependency.version else ""
        status = "Loaded" if dependency.name in plugin_registry.plugin_manager.loaded_plugins else "Not Loaded"
        
        table.add_row(dependency.name, version, optional, status)
    
    console.print(table)

@plugin_app.command("dependents")
def plugin_dependents(plugin_name: str):
    """Show plugins that depend on the specified plugin.
    
    Args:
        plugin_name: Name of the plugin
    """
    console = Console()
    
    # Get dependent plugins
    dependents = plugin_registry.get_dependent_plugins(plugin_name)
    
    if not dependents:
        console.print(Panel(f"No plugins depend on '{plugin_name}'", title="Info", border_style="blue"))
        return
    
    # Create a table for dependents
    table = Table(title=f"Plugins that depend on {plugin_name}", box=box.ROUNDED)
    table.add_column("Plugin", style="cyan")
    table.add_column("Status", style="green")
    
    # Add rows for each dependent
    for dependent in dependents:
        status = "Loaded" if dependent in plugin_registry.plugin_manager.loaded_plugins else "Not Loaded"
        table.add_row(dependent, status)
    
    console.print(table)

def get_sync_config(system: str) -> Dict[str, Any]:
    """Get configuration for external system synchronization.
    
    Args:
        system: External system name
        
    Returns:
        Configuration dictionary
    """
    
    # Initialize config
    config = {}
    
    # NextCloud credentials
    # Load environment variables from the project root
    dotenv_path = Path(os.getcwd()) / '.env'
    load_dotenv(dotenv_path=dotenv_path)
    
    if system == "nextcloud":
        nextcloud_host = os.getenv("NEXTCLOUD_HOST")
        nextcloud_username = os.getenv("NEXTCLOUD_USERNAME")
        nextcloud_password = os.getenv("NEXTCLOUD_PASSWORD")
        nextcloud_token = os.getenv("NEXTCLOUD_TOKEN")
                
        config = {
            "host": nextcloud_host,
            "username": nextcloud_username,
            "password": nextcloud_password,
            "token": nextcloud_token
        }
    
    return config

def display_sync_results(result):
    """Display synchronization results."""
    from rich.console import Console
    from rich.table import Table
    
    console = Console()
    console.print()
    console.print("[bold]Synchronization Results:[/bold]")
    console.print("------------------------")
    
    status_color = "green" if result.get("status") == "success" else "red"
    console.print(f"Status: [{status_color}]{result.get('status', 'unknown')}[/{status_color}]")
    
    # Display summary
    console.print(f"Total tasks: {result.get('total', 0)}")
    console.print(f"Synced: {result.get('synced', 0)}")
    console.print(f"Errors: {result.get('errors', 0)}")
    console.print(f"Conflicts: {result.get('conflicts', 0)}")
    console.print(f"Skipped: {result.get('skipped', 0)}")
    
    # Display details if available
    if "details" in result and result["details"]:
        console.print()
        console.print("Details:")
        
        table = Table(show_header=True)
        table.add_column("Task ID")
        table.add_column("System")
        table.add_column("Status")
        table.add_column("Message")
        
        for detail in result["details"]:
            status = detail.get("status", "")
            status_color = "green" if status == "synced" else "red" if status == "error" else "yellow" if status == "conflict" else "dim"
            
            table.add_row(
                str(detail.get("task_id", "")),
                detail.get("system", ""),
                f"[{status_color}]{status}[/{status_color}]",
                detail.get("message", "")
            )
        
        console.print(table)

def display_task_list(tasks, show_details=False):
    """Display a list of tasks in a rich table."""
    # Load complexity data if available
    complexity_data = {}
    try:
        complexity_report_path = Path("tasks/task-complexity-report.json")
        if complexity_report_path.exists():
            with open(complexity_report_path, "r") as f:
                complexity_report = json.load(f)
                for task_analysis in complexity_report.get("complexityAnalysis", []):
                    task_id = task_analysis.get("taskId")
                    if task_id:
                        complexity_data[task_id] = {
                            "score": task_analysis.get("complexityScore", "-"),
                            "subtask_complexity": "-"  # Will be populated if subtasks exist
                        }
    except Exception as e:
        logger.warning(f"Failed to load complexity data: {e}")
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim", width=6)
    table.add_column("Title", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Priority", style="yellow")
    table.add_column("Complexity", style="red")
    table.add_column("Highest Sub", style="red")
    table.add_column("Dependencies", style="blue")
    table.add_column("Sync", style="magenta")
    
    for task in tasks:
        # Format dependencies
        dependencies = ", ".join([str(dep) for dep in task.get("dependencies", [])])
        
        # Get sync status indicators
        sync_status = get_sync_status_indicator(task)
        
        # Get complexity information
        task_id = task.get("id")
        complexity_score = "-"
        highest_subtask_complexity = "-"
        
        if task_id in complexity_data:
            complexity_score = complexity_data[task_id]["score"]
        
        # Check if task has subtasks in the task data
        has_subtasks = "subtasks" in task and task["subtasks"]
        
        # Calculate highest subtask complexity if subtasks exist in the task data
        if has_subtasks:
            # First, try to get complexity scores for subtasks from the complexity report
            subtask_scores = []
            
            # Look for subtask complexity in the complexity report
            for subtask in task["subtasks"]:
                subtask_id = subtask.get("id")
                if subtask_id:
                    # Try different formats for subtask IDs in the complexity report
                    possible_ids = [
                        f"{task_id}.{subtask_id}",  # Format: parent.child
                        subtask_id                  # Direct ID
                    ]
                    
                    for possible_id in possible_ids:
                        if possible_id in complexity_data:
                            subtask_score = complexity_data[possible_id]["score"]
                            if isinstance(subtask_score, (int, float)):
                                subtask_scores.append(subtask_score)
                                break
            
            # If we found subtask scores, use the maximum
            if subtask_scores:
                highest_subtask_complexity = max(subtask_scores)
            # If no subtask scores were found but subtasks exist, show a placeholder
            elif has_subtasks:
                highest_subtask_complexity = "?"
        
        # Format complexity scores with color based on value
        complexity_style = "green"
        if isinstance(complexity_score, (int, float)):
            if complexity_score >= 8:
                complexity_style = "bold red"
            elif complexity_score >= 5:
                complexity_style = "yellow"
        
        subtask_complexity_style = "green"
        if isinstance(highest_subtask_complexity, (int, float)):
            if highest_subtask_complexity >= 8:
                subtask_complexity_style = "bold red"
            elif highest_subtask_complexity >= 5:
                subtask_complexity_style = "yellow"
        elif highest_subtask_complexity == "?":
            subtask_complexity_style = "dim"
        
        # Add row to table
        table.add_row(
            str(task.get("id", "")),
            task.get("title", ""),
            task.get("status", ""),
            task.get("priority", ""),
            f"[{complexity_style}]{complexity_score}[/{complexity_style}]",
            f"[{subtask_complexity_style}]{highest_subtask_complexity}[/{subtask_complexity_style}]",
            dependencies,
            sync_status
        )
        
        # Show subtasks if requested
        if show_details and has_subtasks:
            for subtask in task["subtasks"]:
                # Format subtask dependencies
                subtask_deps = ", ".join([str(dep) for dep in subtask.get("dependencies", [])])
                
                # Get sync status for subtask
                subtask_sync = get_sync_status_indicator(subtask)
                
                # Get subtask complexity
                subtask_id = subtask.get("id")
                subtask_complexity = "-"
                
                if subtask_id:
                    # Try different formats for subtask IDs
                    possible_ids = [
                        f"{task_id}.{subtask_id}",  # Format: parent.child
                        subtask_id                  # Direct ID
                    ]
                    
                    for possible_id in possible_ids:
                        if possible_id in complexity_data:
                            subtask_complexity = complexity_data[possible_id]["score"]
                            break
                
                # Format subtask complexity with color
                subtask_complexity_style = "green"
                if isinstance(subtask_complexity, (int, float)):
                    if subtask_complexity >= 8:
                        subtask_complexity_style = "bold red"
                    elif subtask_complexity >= 5:
                        subtask_complexity_style = "yellow"
                
                # Add subtask row
                table.add_row(
                    f"└─ {subtask.get('id', '')}",
                    f"  {subtask.get('title', '') or subtask.get('description', '')}",
                    subtask.get("status", ""),
                    subtask.get("priority", ""),
                    f"[{subtask_complexity_style}]{subtask_complexity}[/{subtask_complexity_style}]",
                    "",  # No highest subtask complexity for subtasks
                    subtask_deps,
                    subtask_sync
                )
    
    console = Console()
    console.print(table)

def get_sync_status_indicator(task):
    """Get a visual indicator for the sync status of a task."""
    if "external_sync" not in task or not task["external_sync"]:
        return ""
    
    indicators = []
    for sync_data in task["external_sync"]:
        system = sync_data.get("system", "")
        status = sync_data.get("sync_status", "")
        
        # Create indicator based on system and status
        if system == "nextcloud":
            prefix = "NC"
        elif system == "gitlab":
            prefix = "GL"
        elif system == "azure":
            prefix = "AZ"
        else:
            prefix = system[:2].upper()
        
        if status == SyncStatus.SYNCED:
            indicator = f"[green]{prefix}✓[/green]"
        elif status == SyncStatus.CONFLICT:
            indicator = f"[red]{prefix}![/red]"
        elif status == SyncStatus.PENDING:
            indicator = f"[yellow]{prefix}⟳[/yellow]"
        elif status == SyncStatus.ERROR:
            indicator = f"[red]{prefix}✗[/red]"
        else:
            indicator = f"[dim]{prefix}?[/dim]"
        
        indicators.append(indicator)
    
    return " ".join(indicators)

def get_tasks_for_sync(task_ids: Optional[List[str]], all_tasks: bool) -> List[Dict[str, Any]]:
    """Get tasks to sync based on the provided task IDs and all_tasks flag."""
    # Get all tasks if no task IDs are provided or all_tasks is True
    tasks_file = Path("tasks/tasks.json")
    if not tasks_file.exists():
        logger.error("Tasks file not found: tasks/tasks.json")
        return []
        
    # Load tasks from file
    try:
        with open(tasks_file, "r") as f:
            tasks_data = json.load(f)
            
        # Get the tasks list from the JSON object
        tasks_list = tasks_data.get("tasks", [])
        
        # Return all tasks if requested
        if not task_ids or all_tasks:
            return tasks_list
            
        # Filter tasks by ID
        filtered_tasks = []
        for task in tasks_list:
            if str(task.get("id")) in task_ids:
                filtered_tasks.append(task)
                
        return filtered_tasks
        
    except Exception as e:
        logger.error(f"Error loading tasks: {e}")
        return []

@background_app.command("jobs")
def list_background_jobs(
    status: str = typer.Option(None, "--status", "-s", help="Filter jobs by status"),
    task_id: str = typer.Option(None, "--task", "-t", help="Filter jobs by task ID"),
    system: str = typer.Option(None, "--system", "-y", help="Filter jobs by system ID")
):
    """List background synchronization jobs."""
    console = Console()
    
    # Get jobs based on filters
    if status:
        try:
            status_enum = JobStatus(status)
            jobs = background_sync_manager.get_jobs_by_status(status_enum)
        except ValueError:
            console.print(Panel(f"Invalid status: {status}", title="Error", border_style="red"))
            return
    elif task_id:
        jobs = background_sync_manager.get_jobs_by_task(task_id)
    elif system:
        jobs = background_sync_manager.get_jobs_by_system(system)
    else:
        jobs = background_sync_manager.get_all_jobs()
    
    # Create table
    table = Table(title="Background Sync Jobs")
    table.add_column("ID", style="cyan")
    table.add_column("Task ID", style="green")
    table.add_column("System", style="blue")
    table.add_column("Direction", style="magenta")
    table.add_column("Priority", style="yellow")
    table.add_column("Status", style="red")
    table.add_column("Created", style="dim")
    table.add_column("Started", style="dim")
    table.add_column("Completed", style="dim")
    
    # Add rows
    for job in jobs:
        table.add_row(
            job.id,
            job.task_id,
            job.system_id,
            job.direction,
            str(job.priority.value),
            job.status,
            job.created_at.strftime("%Y-%m-%d %H:%M:%S") if job.created_at else "",
            job.started_at.strftime("%Y-%m-%d %H:%M:%S") if job.started_at else "",
            job.completed_at.strftime("%Y-%m-%d %H:%M:%S") if job.completed_at else ""
        )
    
    # Print table
    console.print(table)
    console.print(f"Total jobs: {len(jobs)}")

@background_app.command("add")
def add_background_job(
    task_id: str = typer.Argument(..., help="Task ID to synchronize"),
    system: str = typer.Argument(..., help="System ID to synchronize with"),
    direction: str = typer.Option(SyncDirection.BIDIRECTIONAL, "--direction", "-d", help="Sync direction"),
    priority: int = typer.Option(2, "--priority", "-p", help="Job priority (1=high, 2=medium, 3=low)")
):
    """Add a background synchronization job."""
    console = Console()
    
    # Validate priority
    try:
        priority_enum = JobPriority(priority)
    except ValueError:
        console.print(Panel(f"Invalid priority: {priority}. Must be 1 (high), 2 (medium), or 3 (low).", title="Error", border_style="red"))
        return
    
    # Add job
    job_id = background_sync_manager.add_job(task_id, system, direction, priority_enum)
    
    console.print(Panel(f"Added job {job_id} to queue", title="Success", border_style="green"))

@background_app.command("cancel")
def cancel_background_job(
    job_id: str = typer.Argument(..., help="Job ID to cancel")
):
    """Cancel a background synchronization job."""
    console = Console()
    
    # Cancel job
    success = background_sync_manager.cancel_job(job_id)
    
    if success:
        console.print(Panel(f"Cancelled job {job_id}", title="Success", border_style="green"))
    else:
        console.print(Panel(f"Failed to cancel job {job_id}. Job may not exist or is already running/completed.", title="Error", border_style="red"))

@background_app.command("show")
def show_background_job(
    job_id: str = typer.Argument(..., help="Job ID to show")
):
    """Show details of a background synchronization job."""
    console = Console()
    
    # Get job
    job = background_sync_manager.get_job(job_id)
    
    if not job:
        console.print(Panel(f"Job {job_id} not found", title="Error", border_style="red"))
        return
    
    # Create table
    table = Table(title=f"Job {job_id} Details", box=box.ROUNDED)
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")
    
    # Add rows
    job_dict = job.to_dict()
    for key, value in job_dict.items():
        table.add_row(key, str(value))
    
    # Print table
    console.print(table)

@background_app.command("sync")
def sync_task_background(
    task_id: str = typer.Argument(..., help="Task ID to synchronize"),
    system: str = typer.Argument(..., help="System ID to synchronize with"),
    direction: str = typer.Option(SyncDirection.BIDIRECTIONAL, "--direction", "-d", help="Sync direction"),
    priority: int = typer.Option(1, "--priority", "-p", help="Job priority (1=high, 2=medium, 3=low)")
):
    """Synchronize a task in the background."""
    console = Console()
    
    # Start background sync manager if not running
    if not background_sync_manager._running:
        console.print(Panel("Starting background synchronization service...", title="Info", border_style="blue"))
        background_sync_manager.start()
    
    # Validate priority
    try:
        priority_enum = JobPriority(priority)
    except ValueError:
        console.print(Panel(f"Invalid priority: {priority}. Must be 1 (high), 2 (medium), or 3 (low).", title="Error", border_style="red"))
        return
    
    # Add job
    job_id = background_sync_manager.add_job(task_id, system, direction, priority_enum)
    
    console.print(Panel(f"Added job {job_id} to queue", title="Success", border_style="green"))
    console.print("Run 'taskinator background jobs' to monitor job status")

@background_app.command("sync-all")
def sync_all_tasks_background(
    system: str = typer.Argument(..., help="System ID to synchronize with"),
    direction: str = typer.Option(SyncDirection.BIDIRECTIONAL, "--direction", "-d", help="Sync direction"),
    priority: int = typer.Option(2, "--priority", "-p", help="Job priority (1=high, 2=medium, 3=low)")
):
    """Synchronize all tasks in the background."""
    console = Console()
    
    # Start background sync manager if not running
    if not background_sync_manager._running:
        console.print(Panel("Starting background synchronization service...", title="Info", border_style="blue"))
        background_sync_manager.start()
    
    # Validate priority
    try:
        priority_enum = JobPriority(priority)
    except ValueError:
        console.print(Panel(f"Invalid priority: {priority}. Must be 1 (high), 2 (medium), or 3 (low).", title="Error", border_style="red"))
        return
    
    # Get all tasks
    import json
    from pathlib import Path
    
    # Read tasks from the tasks.json file
    tasks_file = Path("tasks/tasks.json")
    if not tasks_file.exists():
        console.print(Panel(f"Tasks file not found: {tasks_file}", title="Error", border_style="red"))
        return
    
    try:
        with open(tasks_file, "r") as f:
            tasks_data = json.load(f)
        
        # Get the tasks list
        tasks_list = tasks_data.get("tasks", [])
        
        # Add jobs for each task
        job_ids = []
        for task in tasks_list:
            task_id = str(task.get("id"))
            job_id = background_sync_manager.add_job(task_id, system, direction, priority_enum)
            job_ids.append(job_id)
        
        console.print(Panel(f"Added {len(job_ids)} jobs to queue", title="Success", border_style="green"))
        console.print("Run 'taskinator background jobs' to monitor job status")
    
    except Exception as e:
        console.print(Panel(f"Error: {e}", title="Error", border_style="red"))

@background_app.command("start")
def start_background_sync():
    """Start the background synchronization service."""
    console = Console()
    console.print(Panel("Starting background synchronization service...", title="Info", border_style="blue"))
    background_sync_manager.start()

@background_app.command("stop")
def stop_background_sync():
    """Stop the background synchronization service."""
    console = Console()
    console.print(Panel("Stopping background synchronization service...", title="Info", border_style="blue"))
    background_sync_manager.stop()

@background_app.command("status")
def get_background_sync_status():
    """Get the status of the background synchronization service."""
    console = Console()
    status = background_sync_manager.get_status()
    console.print(Panel(f"Background synchronization service is {status}", title="Info", border_style="blue"))

@background_app.command("schedule")
def schedule_background_sync(
    interval: int = typer.Option(60, "--interval", "-i", help="Interval in minutes between syncs")
):
    """Schedule the background synchronization service to run at regular intervals."""
    console = Console()
    console.print(Panel(f"Scheduling background synchronization service to run every {interval} minutes...", title="Info", border_style="blue"))
    background_sync_manager.schedule(interval)

@background_app.command("unschedule")
def unschedule_background_sync():
    """Unschedule the background synchronization service."""
    console = Console()
    console.print(Panel("Unscheduling background synchronization service...", title="Info", border_style="blue"))
    background_sync_manager.unschedule()

# SOP Document Commands
sop_app = typer.Typer(help="Manage Standard Operating Procedure (SOP) documents")
app.add_typer(sop_app, name="sop")

@sop_app.command("create")
def sop_create(
    title: str = typer.Option(..., "--title", "-t", help="SOP document title"),
    description: str = typer.Option("", "--description", "-d", help="SOP document description"),
    author: str = typer.Option("", "--author", "-a", help="SOP document author"),
    department: str = typer.Option("", "--department", "-dep", help="Department responsible for the SOP"),
    audience: str = typer.Option("intermediate", "--audience", "-aud", 
                                help="Target audience level (beginner, intermediate, advanced, expert)"),
    tags: str = typer.Option("", "--tags", help="Comma-separated list of tags"),
    output: str = typer.Option("", "--output", "-o", help="Output file path (default: sops/<id>.json)")
):
    """Create a new SOP document."""
    try:
        from taskinator.sop_document import SOPDocument, SOPDocumentManager, SOPAudienceLevel
        import uuid
        
        # Generate a unique ID if not specified in output
        if output:
            doc_id = Path(output).stem
        else:
            doc_id = f"sop_{uuid.uuid4().hex[:8]}"
        
        # Parse tags
        tag_list = [tag.strip() for tag in tags.split(",")] if tags else []
        
        # Create the document
        document = SOPDocument(
            doc_id=doc_id,
            title=title,
            description=description,
            author=author,
            department=department,
            audience_level=SOPAudienceLevel(audience),
            tags=tag_list
        )
        
        # Save the document
        manager = SOPDocumentManager()
        if manager.save_document(document):
            display_success(f"Created SOP document: {doc_id}")
            
            # Show document details
            display_info(f"Title: {title}")
            display_info(f"ID: {doc_id}")
            display_info(f"Saved to: {manager._get_document_path(doc_id)}")
        else:
            display_error("Failed to create SOP document")
            raise typer.Exit(1)
    
    except Exception as e:
        display_error(f"Error creating SOP document: {e}")
        raise typer.Exit(1)

@sop_app.command("list")
def sop_list():
    """List all available SOP documents."""
    try:
        from taskinator.sop_document import SOPDocumentManager
        from rich.table import Table
        
        manager = SOPDocumentManager()
        documents = manager.list_documents()
        
        if not documents:
            display_info("No SOP documents found")
            return
        
        # Create a table for display
        table = Table(title="SOP Documents")
        table.add_column("ID", style="cyan")
        table.add_column("Title")
        table.add_column("Version")
        table.add_column("Status", style="green")
        table.add_column("Author")
        table.add_column("Updated")
        
        for doc in documents:
            table.add_row(
                doc.get("id", ""),
                doc.get("title", ""),
                doc.get("version", ""),
                doc.get("status", ""),
                doc.get("author", ""),
                doc.get("updatedDate", "")
            )
        
        console.print(table)
    
    except Exception as e:
        display_error(f"Error listing SOP documents: {e}")
        raise typer.Exit(1)

@sop_app.command("show")
def sop_show(
    doc_id: str = typer.Argument(..., help="SOP document ID"),
    format: str = typer.Option("rich", "--format", "-f", help="Output format (rich, json, yaml)")
):
    """Show details of an SOP document."""
    try:
        from taskinator.sop_document import SOPDocumentManager
        import json
        import yaml
        
        manager = SOPDocumentManager()
        document = manager.load_document(doc_id)
        
        if not document:
            display_error(f"SOP document not found: {doc_id}")
            raise typer.Exit(1)
        
        if format.lower() == "json":
            # Output as JSON
            print(json.dumps(document.to_dict(), indent=2))
        
        elif format.lower() == "yaml":
            # Output as YAML
            print(yaml.dump(document.to_dict(), default_flow_style=False))
        
        else:
            # Output as rich text
            from rich.panel import Panel
            from rich.text import Text
            
            # Document metadata
            metadata_panel = Panel(
                Text.from_markup(f"""
[bold cyan]Title:[/bold cyan] {document.title}
[bold cyan]ID:[/bold cyan] {document.doc_id}
[bold cyan]Version:[/bold cyan] {document.version}
[bold cyan]Status:[/bold cyan] {document.status.value}
[bold cyan]Author:[/bold cyan] {document.author or 'N/A'}
[bold cyan]Department:[/bold cyan] {document.department or 'N/A'}
[bold cyan]Audience Level:[/bold cyan] {document.audience_level.value}
[bold cyan]Created:[/bold cyan] {document.created_date}
[bold cyan]Updated:[/bold cyan] {document.updated_date}
[bold cyan]Tags:[/bold cyan] {', '.join(document.tags) if document.tags else 'N/A'}
                """.strip()),
                title="SOP Document",
                expand=False
            )
            console.print(metadata_panel)
            
            # Document description
            if document.description:
                description_panel = Panel(
                    document.description,
                    title="Description",
                    expand=False
                )
                console.print(description_panel)
            
            # Steps
            if document.steps:
                from rich.table import Table
                
                steps_table = Table(title="Steps")
                steps_table.add_column("Order", style="cyan")
                steps_table.add_column("Title")
                steps_table.add_column("Est. Time")
                steps_table.add_column("Complexity", style="green")
                
                for step in document.steps:
                    steps_table.add_row(
                        str(step.order),
                        step.title,
                        step.estimated_time or "N/A",
                        str(step.complexity) if step.complexity is not None else "N/A"
                    )
                
                console.print(steps_table)
                
                # Step details
                for step in document.steps:
                    step_panel = Panel(
                        Text.from_markup(f"""
[bold]Description:[/bold]
{step.description}

[bold]Prerequisites:[/bold]
{chr(10).join([f"- {prereq}" for prereq in step.prerequisites]) if step.prerequisites else "None"}

[bold]Required Skills:[/bold]
{chr(10).join([f"- {skill}" for skill in step.required_skills]) if step.required_skills else "None"}
                        """.strip()),
                        title=f"Step {step.order}: {step.title}",
                        expand=False
                    )
                    console.print(step_panel)
            else:
                display_info("No steps defined in this document")
            
            # References and attachments
            if document.references:
                references_panel = Panel(
                    Text.from_markup(chr(10).join([f"- {ref}" for ref in document.references])),
                    title="References",
                    expand=False
                )
                console.print(references_panel)
            
            if document.attachments:
                attachments_panel = Panel(
                    Text.from_markup(chr(10).join([f"- {att}" for att in document.attachments])),
                    title="Attachments",
                    expand=False
                )
                console.print(attachments_panel)
    
    except Exception as e:
        display_error(f"Error showing SOP document: {e}")
        raise typer.Exit(1)

@sop_app.command("parse")
def sop_parse(
    file_path: str = typer.Argument(..., help="Path to the SOP document file to parse"),
    save: bool = typer.Option(True, "--save/--no-save", help="Save the parsed document")
):
    """Parse an SOP document from a file (Markdown, YAML, or text)."""
    try:
        from taskinator.sop_parser import SOPParserFactory
        from taskinator.sop_document import SOPDocumentManager
        
        # Parse the document
        document = SOPParserFactory.parse(file_path)
        
        if not document:
            display_error(f"Failed to parse SOP document: {file_path}")
            raise typer.Exit(1)
        
        display_success(f"Successfully parsed SOP document: {document.title}")
        
        # Save the document if requested
        if save:
            manager = SOPDocumentManager()
            if manager.save_document(document):
                display_success(f"Saved SOP document: {document.doc_id}")
                display_info(f"Saved to: {manager._get_document_path(document.doc_id)}")
            else:
                display_error("Failed to save SOP document")
                raise typer.Exit(1)
        
        # Show document summary
        display_info(f"Title: {document.title}")
        display_info(f"ID: {document.doc_id}")
        display_info(f"Steps: {len(document.steps)}")
    
    except Exception as e:
        display_error(f"Error parsing SOP document: {e}")
        raise typer.Exit(1)

@sop_app.command("analyze")
def sop_analyze(
    doc_id: str = typer.Argument(..., help="SOP document ID to analyze"),
    output: str = typer.Option("", "--output", "-o", help="Output file path for analysis report"),
    dspy: bool = typer.Option(False, "--dspy", help="Use DSPy for analysis (if available)"),
    update: bool = typer.Option(False, "--update", help="Update the document with complexity scores")
):
    """Analyze the complexity of an SOP document."""
    try:
        from taskinator.sop_document import SOPDocumentManager
        from taskinator.sop_complexity import SOPComplexityAnalyzer
        import json
        from pathlib import Path
        
        # Load the document
        manager = SOPDocumentManager()
        document = manager.load_document(doc_id)
        
        if not document:
            display_error(f"SOP document not found: {doc_id}")
            raise typer.Exit(1)
        
        # Analyze the document
        analyzer = SOPComplexityAnalyzer(use_dspy=dspy)
        analysis = analyzer.analyze_document(document)
        
        # Display analysis results
        display_success(f"Analyzed SOP document: {document.title}")
        display_info(f"Average Complexity: {analysis['averageComplexity']:.1f}")
        display_info(f"Max Complexity: {analysis['maxComplexity']:.1f}")
        display_info(f"Target Audience: {analysis['targetAudience']}")
        
        # Create a table for step complexities
        from rich.table import Table
        
        steps_table = Table(title="Step Complexity Analysis")
        steps_table.add_column("Order", style="cyan")
        steps_table.add_column("Title")
        steps_table.add_column("Complexity", style="green")
        steps_table.add_column("Required Skills")
        
        for step_analysis in analysis["stepAnalyses"]:
            # Find the corresponding step to get its order
            step = next((s for s in document.steps if s.step_id == step_analysis["stepId"]), None)
            order = step.order if step else "N/A"
            
            steps_table.add_row(
                str(order),
                step_analysis["stepTitle"],
                f"{step_analysis['complexityScore']:.1f}",
                ", ".join(step_analysis["requiredSkills"]) if step_analysis["requiredSkills"] else "None"
            )
        
        console.print(steps_table)
        
        # Save analysis to file if requested
        if output:
            output_path = Path(output)
            with open(output_path, "w") as f:
                json.dump(analysis, f, indent=2)
            display_success(f"Saved analysis to: {output_path}")
        
        # Update document with complexity scores if requested
        if update:
            updated = False
            for step_analysis in analysis["stepAnalyses"]:
                step = next((s for s in document.steps if s.step_id == step_analysis["stepId"]), None)
                if step:
                    step.complexity = step_analysis["complexityScore"]
                    updated = True
            
            if updated and manager.save_document(document):
                display_success(f"Updated document with complexity scores: {doc_id}")
            elif updated:
                display_error("Failed to update document with complexity scores")
    
    except Exception as e:
        display_error(f"Error analyzing SOP document: {e}")
        raise typer.Exit(1)

@sop_app.command("add-step")
def sop_add_step(
    doc_id: str = typer.Argument(..., help="SOP document ID"),
    title: str = typer.Option(..., "--title", "-t", help="Step title"),
    description: str = typer.Option("", "--description", "-d", help="Step description"),
    order: int = typer.Option(None, "--order", "-o", help="Step order (auto-increment if not specified)"),
    estimated_time: str = typer.Option("", "--time", help="Estimated time to complete the step"),
    prerequisites: str = typer.Option("", "--prerequisites", "-p", help="Comma-separated list of prerequisites"),
    required_skills: str = typer.Option("", "--skills", "-s", help="Comma-separated list of required skills")
):
    """Add a step to an SOP document."""
    try:
        from taskinator.sop_document import SOPDocumentManager, SOPStep
        import uuid
        
        # Load the document
        manager = SOPDocumentManager()
        document = manager.load_document(doc_id)
        
        if not document:
            display_error(f"SOP document not found: {doc_id}")
            raise typer.Exit(1)
        
        # Determine step order if not specified
        if order is None:
            order = max([step.order for step in document.steps], default=0) + 1
        
        # Parse prerequisites and required skills
        prereq_list = [p.strip() for p in prerequisites.split(",")] if prerequisites else []
        skills_list = [s.strip() for s in required_skills.split(",")] if required_skills else []
        
        # Create the step
        step_id = f"step_{uuid.uuid4().hex[:8]}"
        step = SOPStep(
            step_id=step_id,
            title=title,
            description=description,
            order=order,
            estimated_time=estimated_time if estimated_time else None,
            prerequisites=prereq_list,
            required_skills=skills_list
        )
        
        # Add the step to the document
        document.add_step(step)
        
        # Save the document
        if manager.save_document(document):
            display_success(f"Added step to SOP document: {doc_id}")
            display_info(f"Step ID: {step_id}")
            display_info(f"Order: {order}")
        else:
            display_error("Failed to save SOP document")
            raise typer.Exit(1)
    
    except Exception as e:
        display_error(f"Error adding step to SOP document: {e}")
        raise typer.Exit(1)

@pdd_app.command("list")
def pdd_list(
    pdd_dir: str = typer.Option(
        "pdds",
        "--pdd-dir",
        "-d",
        help="Directory containing PDD files"
    ),
    show_processes: bool = typer.Option(
        False,
        "--processes",
        "-p",
        help="Show processes within each PDD"
    )
):
    """List all PDD documents in a table format.
    
    This command displays all Process Design Documents (PDDs) in a tabular format,
    showing their ID, title, number of processes, and other metadata.
    
    Use the --processes flag to also display the processes within each PDD.
    """
    try:
        from taskinator.pdd_document import PDDDocumentManager
        import os
        import json
        
        # Display banner
        display_banner("Process Design Documents")
        
        # Check if processes.json exists
        processes_file = os.path.join(pdd_dir, "processes.json")
        if not os.path.exists(processes_file):
            display_error(f"No processes.json file found in {pdd_dir}")
            display_info("You can create PDDs using the 'taskinator pdd identify-processes' command")
            raise typer.Exit(1)
            
        # Load processes.json
        with open(processes_file, 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                display_error(f"Invalid JSON in {processes_file}")
                raise typer.Exit(1)
                
        processes = data.get("processes", [])
        if not processes:
            display_warning("No processes found in processes.json")
            raise typer.Exit(0)
            
        # Create a table for PDDs
        table = Table(title="Process Design Documents")
        table.add_column("ID", style="cyan")
        table.add_column("Title", style="green")
        table.add_column("Complexity", style="yellow")
        table.add_column("Dependencies", style="magenta")
        table.add_column("Variations", style="blue")
        
        # Add rows for each process
        for process in processes:
            process_id = process.get("process_id") or process.get("id", "")
            title = process.get("title", "")
            complexity = process.get("complexity", "")
            dependencies = ", ".join(str(dep) for dep in process.get("dependencies", []))
            variation_count = len(process.get("variations", []))
            
            table.add_row(
                str(process_id),
                title,
                complexity,
                dependencies,
                str(variation_count) if variation_count > 0 else "-"
            )
        
        console.print(table)
        
        # If show_processes is True, display processes for each PDD
        if show_processes and processes:
            console.print()
            display_info("Process Details:")
            
            for process in processes:
                process_id = process.get("process_id") or process.get("id", "")
                title = process.get("title", "")
                description = process.get("description", "")
                
                console.print(f"[bold cyan]{process_id}[/bold cyan]: [bold]{title}[/bold]")
                console.print(f"  Description: {description}")
                
                # Show variations if any
                variations = process.get("variations", [])
                if variations:
                    console.print("  [bold]Variations:[/bold]")
                    for i, variation in enumerate(variations, 1):
                        var_name = variation.get("name", f"Variation {i}")
                        console.print(f"    - {var_name}")
                
                console.print()
        
        # Display next steps
        console.print()
        display_info("Next steps:")
        display_info("1. Convert PDDs to SOPs: taskinator pdd convert")
        display_info("2. Convert PDDs to tasks: taskinator pdd to-tasks")
        
    except Exception as e:
        display_error(f"Error listing PDDs: {e}")
        raise typer.Exit(1)

@pdd_app.command("to-tasks")
@_run_async
async def pdd_to_tasks(
    pdd_id: str = typer.Argument(
        ...,
        help="ID of the PDD document to convert"
    ),
    priority: str = typer.Option(
        "medium", 
        "--priority", 
        "-p", 
        help="Default priority for the generated tasks"
    ),
    pdd_dir: str = typer.Option(
        "pdds",
        "--pdd-dir",
        help="Directory containing PDD documents"
    ),
    generate_files: bool = typer.Option(
        True,
        "--generate-files/--no-generate-files",
        "-g/-G",
        help="Whether to generate individual task files"
    ),
    auto_analyze: bool = typer.Option(
        False, 
        "--analyze/--no-analyze", 
        "-a/-A", 
        help="Automatically analyze task complexity after conversion"
    ),
    auto_expand: bool = typer.Option(
        False, 
        "--expand/--no-expand", 
        "-e/-E", 
        help="Automatically expand complex tasks after analysis"
    ),
    complexity_threshold: float = typer.Option(
        7.0, 
        "--threshold", 
        "-t", 
        help="Complexity threshold for automatic task expansion"
    )
):
    """Convert a PDD document to Taskinator tasks.
    
    This command analyzes a Process Design Document (PDD) and generates
    Taskinator tasks for each process in the PDD.
    """
    try:
        from taskinator.pdd_to_task import PDDTaskConverter
        
        # Create a PDD to task converter
        converter = PDDTaskConverter()
        
        # Determine whether to auto-expand based on auto_analyze and auto_expand
        auto_expand_threshold = complexity_threshold if auto_analyze and auto_expand else None
        
        # Convert the PDD to tasks
        tasks_data = converter.convert_pdd_to_tasks(
            pdd_id=pdd_id,
            priority=priority,
            generate_files=generate_files,
            auto_analyze=auto_analyze,
            auto_expand_threshold=auto_expand_threshold
        )
        
        # Display success message
        console.print(f"[green]Successfully converted PDD {pdd_id} to {len(tasks_data['tasks'])} tasks[/green]")
        
        # Display next steps
        console.print("\n[bold]Next Steps:[/bold]")
        console.print("1. Review the generated tasks with: [cyan]taskinator list[/cyan]")
        
        if auto_analyze:
            console.print(f"2. View the complexity analysis report: [cyan]tasks/pdd-{pdd_id}-complexity-report.json[/cyan]")
            
            if auto_expand:
                console.print("3. Check the expanded tasks with: [cyan]taskinator list[/cyan]")
            else:
                console.print("3. Expand complex tasks with: [cyan]taskinator expand-task <task_id>[/cyan]")
        else:
            console.print("2. Analyze task complexity with: [cyan]taskinator analyze[/cyan]")
            console.print("3. Expand complex tasks with: [cyan]taskinator expand-task <task_id>[/cyan]")
        
        console.print("4. Start implementing tasks with: [cyan]taskinator next[/cyan]")
        
    except Exception as e:
        display_error(f"Failed to convert PDD to tasks: {e}")
        raise typer.Exit(1)

@pdd_app.command("convert")
@_run_async
async def pdd_convert(
    pdd_id: str = typer.Argument(
        ...,
        help="ID of the PDD document to convert"
    ),
    process_id: str = typer.Option(
        None,
        "--process",
        "-p",
        help="ID of a specific process to convert (converts all processes if not specified)"
    ),
    variation: str = typer.Option(
        None,
        "--variation",
        "-v",
        help="Name of a specific variation to convert (only used with --process)"
    ),
    pdd_dir: str = typer.Option(
        "pdds",
        "--pdd-dir",
        help="Directory containing PDD documents"
    ),
    sop_dir: str = typer.Option(
        "sops",
        "--sop-dir",
        help="Directory to store SOP documents"
    ),
    format: str = typer.Option(
        "markdown",
        "--format",
        "-f",
        help="Output format (markdown, text)"
    )
):
    """Convert a PDD document to SOP documents.
    
    This command converts a PDD document to Standard Operating Procedure (SOP) documents.
    You can convert all processes in a PDD or a specific process.
    """
    try:
        import os
        import json
        from taskinator.pdd_to_sop import SOPDocument, SOPStep
        
        # Display banner
        display_banner("Taskinator PDD Converter")
        
        # Check if we're converting a specific process
        if process_id:
            console.print(f"Converting process '{process_id}' in PDD '{pdd_id}' to SOP...")
        else:
            console.print(f"Converting all processes in PDD '{pdd_id}' to SOP...")
        
        # Check if processes.json exists
        processes_file = os.path.join(pdd_dir, "processes.json")
        if not os.path.exists(processes_file):
            display_error(f"No processes.json file found in {pdd_dir}")
            display_info("You can create PDDs using the 'taskinator pdd identify-processes' command")
            raise typer.Exit(1)
            
        # Load processes.json
        with open(processes_file, 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                display_error(f"Invalid JSON in {processes_file}")
                raise typer.Exit(1)
                
        processes = data.get("processes", [])
        if not processes:
            display_warning("No processes found in processes.json")
            raise typer.Exit(0)
            
        # Find the process(es) to convert
        processes_to_convert = []
        if process_id:
            # Find the specific process
            for p in processes:
                p_id = p.get("process_id") or p.get("id", "")
                if p_id == process_id:
                    processes_to_convert.append(p)
                    break
            
            if not processes_to_convert:
                display_error(f"Process with ID '{process_id}' not found")
                display_info(f"Use 'taskinator pdd list' to see available processes")
                raise typer.Exit(1)
        else:
            # Convert all processes
            processes_to_convert = processes
        
        # Create SOP directory if it doesn't exist
        os.makedirs(sop_dir, exist_ok=True)
        
        # Convert each process to an SOP
        for process in processes_to_convert:
            p_id = process.get("process_id") or process.get("id", "")
            title = process.get("title", "")
            description = process.get("description", "")
            
            # Check if we're converting a specific variation
            variations = process.get("variations", [])
            if variation and variations:
                # Find the specified variation
                variation_data = None
                for var in variations:
                    if var.get("name") == variation:
                        variation_data = var
                        break
                
                if not variation_data:
                    display_warning(f"Variation '{variation}' not found for process '{p_id}'")
                    display_info(f"Available variations: {', '.join([v.get('name', '') for v in variations])}")
                    continue
                
                # Use variation data
                var_title = f"{title} - {variation_data.get('name')}"
                var_description = variation_data.get("description", description)
                
                # Create SOP for the variation
                sop = SOPDocument(
                    doc_id=f"{p_id}_{variation}",
                    title=var_title,
                    description=var_description,
                    version="1.0",
                    author="Taskinator",
                    department="Engineering",
                    tags=["auto-generated", "variation"]
                )
            else:
                # Create SOP for the main process
                sop = SOPDocument(
                    doc_id=p_id,
                    title=title,
                    description=description,
                    version="1.0",
                    author="Taskinator",
                    department="Engineering",
                    tags=["auto-generated"]
                )
            
            # Generate steps based on process complexity and description
            steps = []
            complexity = process.get("complexity", "medium")
            
            # Define step count based on complexity
            step_count = 3  # Default for simple
            if complexity == "medium":
                step_count = 5
            elif complexity == "complex":
                step_count = 7
            
            # Generate steps
            for i in range(1, step_count + 1):
                # Create step with appropriate title based on position in sequence
                if i == 1:
                    step_title = "Preparation and Planning"
                    step_desc = f"Prepare resources and plan the execution of the {title} process."
                    prereqs = []
                elif i == step_count:
                    step_title = "Finalization and Documentation"
                    step_desc = f"Finalize the {title} process and document the results."
                    prereqs = [f"step{i-1}"]
                else:
                    step_title = f"Execute Phase {i-1}"
                    step_desc = f"Perform the activities required for phase {i-1} of the {title} process."
                    prereqs = [f"step{i-1}"]
                
                # Create the step
                step = SOPStep(
                    step_id=f"step{i}",
                    order=i,
                    title=step_title,
                    description=step_desc,
                    prerequisites=prereqs,
                    estimated_time="1 hour",
                    required_skills=["Domain knowledge"]
                )
                
                # Add the step to the SOP
                sop.add_step(step)
            
            # Save the SOP
            sop_filename = f"{p_id}_sop"
            if variation:
                sop_filename += f"_{variation}"
            
            if format.lower() == "markdown":
                sop_filename += ".md"
                sop_content = generate_sop_markdown(sop)
            else:  # text format
                sop_filename += ".txt"
                sop_content = str(sop)
            
            sop_path = os.path.join(sop_dir, sop_filename)
            with open(sop_path, "w") as f:
                f.write(sop_content)
            
            display_success(f"Generated SOP: {sop_path}")
        
        # Display next steps
        console.print()
        display_info("Next steps:")
        display_info("1. Review the generated SOP documents")
        display_info("2. Customize the steps as needed")
        display_info("3. Share the SOPs with your team")
        
    except Exception as e:
        display_error(f"Error converting PDD to SOP: {e}")
        raise typer.Exit(1)

def generate_sop_markdown(sop):
    """Generate Markdown content for an SOP document."""
    # Generate Markdown content
    md_content = f"# {sop.title}\n\n"
    md_content += f"## Description\n{sop.description}\n\n"
    
    md_content += "## Metadata\n"
    md_content += f"- Version: {sop.version}\n"
    
    if sop.author:
        md_content += f"- Author: {sop.author}\n"
    
    if sop.department:
        md_content += f"- Department: {sop.department}\n"
    
    if sop.tags:
        md_content += f"- Tags: {', '.join(sop.tags)}\n"
    
    md_content += "\n"
    
    # Add step flow diagram
    md_content += "## Step Flow Diagram\n\n"
    md_content += "```mermaid\nflowchart TD\n"
    
    # Add nodes for each step
    for step in sorted(sop.steps, key=lambda s: s.order):
        md_content += f"    step{step.order}[\"{step.title}\"]\n"
    
    # Add connections based on prerequisites
    for step in sorted(sop.steps, key=lambda s: s.order):
        for prereq in step.prerequisites:
            md_content += f"    {prereq} --> step{step.order}\n"
    
    md_content += "```\n\n"
    
    # Add steps
    md_content += "## Steps\n"
    for step in sorted(sop.steps, key=lambda s: s.order):
        md_content += f"### Step {step.order}: {step.title}\n"
        md_content += f"Description: {step.description}\n"
        if step.estimated_time:
            md_content += f"Estimated Time: {step.estimated_time}\n"
        md_content += f"Prerequisites: {', '.join(step.prerequisites) if step.prerequisites else 'None'}\n"
        if step.required_skills:
            md_content += "Required Skills:\n"
            for skill in step.required_skills:
                md_content += f"- {skill}\n"
        md_content += "\n"
    
    return md_content

@pdd_app.command("show")
def pdd_show(
    process_id: str = typer.Argument(
        ...,
        help="ID of the process to show"
    ),
    pdd_dir: str = typer.Option(
        "pdds",
        "--pdd-dir",
        "-d",
        help="Directory containing PDD files"
    ),
    format: str = typer.Option(
        "rich",
        "--format",
        "-f",
        help="Output format (rich, json, markdown)"
    )
):
    """Display detailed information about a specific process.
    
    This command shows detailed information about a specific process from a PDD,
    including its description, complexity, dependencies, resources, parameters,
    and variations.
    
    You can specify different output formats:
    - rich: Formatted console output with colors (default)
    - json: Raw JSON output
    - markdown: Markdown formatted output
    """
    try:
        import os
        import json
        from rich.panel import Panel
        from rich.markdown import Markdown
        
        # Display banner
        display_banner(f"Process Details: {process_id}")
        
        # Check if processes.json exists
        processes_file = os.path.join(pdd_dir, "processes.json")
        if not os.path.exists(processes_file):
            display_error(f"No processes.json file found in {pdd_dir}")
            display_info("You can create PDDs using the 'taskinator pdd identify-processes' command")
            raise typer.Exit(1)
            
        # Load processes.json
        with open(processes_file, 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                display_error(f"Invalid JSON in {processes_file}")
                raise typer.Exit(1)
                
        processes = data.get("processes", [])
        if not processes:
            display_warning("No processes found in processes.json")
            raise typer.Exit(0)
            
        # Find the process with the specified ID
        process = None
        for p in processes:
            p_id = p.get("process_id") or p.get("id", "")
            if p_id == process_id:
                process = p
                break
                
        if not process:
            display_error(f"Process with ID '{process_id}' not found")
            display_info(f"Use 'taskinator pdd list' to see available processes")
            raise typer.Exit(1)
            
        # Output in the specified format
        if format.lower() == "json":
            # Output raw JSON
            import json
            console.print(json.dumps(process, indent=2))
            
        elif format.lower() == "markdown":
            # Generate markdown content
            md_content = f"# Process: {process.get('title', '')}\n\n"
            md_content += f"**ID:** {process_id}\n\n"
            md_content += f"**Complexity:** {process.get('complexity', '')}\n\n"
            
            dependencies = process.get("dependencies", [])
            if dependencies:
                md_content += "**Dependencies:**\n"
                for dep in dependencies:
                    md_content += f"- {dep}\n"
                md_content += "\n"
                
            md_content += f"## Description\n\n{process.get('description', '')}\n\n"
            
            resources = process.get("resources", []) or process.get("resources_required", [])
            if resources:
                md_content += "## Resources\n\n"
                for resource in resources:
                    md_content += f"- {resource}\n"
                md_content += "\n"
                
            parameters = process.get("parameters", {}) or process.get("domain_parameters", {})
            if parameters:
                md_content += "## Parameters\n\n"
                for key, value in parameters.items():
                    md_content += f"- **{key}:** {value}\n"
                md_content += "\n"
                
            # Include research insights if available
            if "research_insights" in data:
                md_content += f"## Research Insights\n\n{data.get('research_insights', '')}\n\n"
                
            # Include variations if available
            variations = process.get("variations", [])
            if variations:
                md_content += "## Variations\n\n"
                for i, variation in enumerate(variations, 1):
                    var_name = variation.get("name", f"Variation {i}")
                    var_desc = variation.get("description", "")
                    
                    md_content += f"### {var_name}\n\n{var_desc}\n\n"
                    
                    var_advantages = variation.get("advantages", [])
                    if var_advantages:
                        md_content += "**Advantages:**\n"
                        for adv in var_advantages:
                            md_content += f"- {adv}\n"
                        md_content += "\n"
                        
                    var_disadvantages = variation.get("disadvantages", [])
                    if var_disadvantages:
                        md_content += "**Disadvantages:**\n"
                        for dis in var_disadvantages:
                            md_content += f"- {dis}\n"
                        md_content += "\n"
                        
                    var_scenarios = variation.get("scenarios", [])
                    if var_scenarios:
                        md_content += "**When to use:**\n"
                        for scn in var_scenarios:
                            md_content += f"- {scn}\n"
                        md_content += "\n"
            
            # Output markdown
            console.print(Markdown(md_content))
            
            # Optionally save to file
            md_file = os.path.join(pdd_dir, f"{process_id}_details.md")
            with open(md_file, "w") as f:
                f.write(md_content)
            display_info(f"Markdown saved to: {md_file}")
            
        else:  # rich format (default)
            # Display process details in rich format
            title = process.get("title", "")
            description = process.get("description", "")
            complexity = process.get("complexity", "")
            
            # Display basic info
            console.print(f"[bold cyan]ID:[/bold cyan] {process_id}")
            console.print(f"[bold cyan]Title:[/bold cyan] {title}")
            console.print(f"[bold cyan]Complexity:[/bold cyan] {complexity}")
            
            # Display dependencies
            dependencies = process.get("dependencies", [])
            if dependencies:
                console.print("[bold cyan]Dependencies:[/bold cyan]")
                for dep in dependencies:
                    console.print(f"  - {dep}")
            
            # Display description
            console.print(Panel(description, title="Description", border_style="green"))
            
            # Display resources
            resources = process.get("resources", []) or process.get("resources_required", [])
            if resources:
                console.print("[bold cyan]Resources:[/bold cyan]")
                for resource in resources:
                    console.print(f"  - {resource}")
            
            # Display parameters
            parameters = process.get("parameters", {}) or process.get("domain_parameters", {})
            if parameters:
                console.print("[bold cyan]Parameters:[/bold cyan]")
                for key, value in parameters.items():
                    console.print(f"  - [bold]{key}:[/bold] {value}")
            
            # Display research insights if available
            if "research_insights" in data:
                console.print(Panel(data.get("research_insights", ""), title="Research Insights", border_style="blue"))
            
            # Display variations if available
            variations = process.get("variations", [])
            if variations:
                console.print("[bold cyan]Variations:[/bold cyan]")
                
                for i, variation in enumerate(variations, 1):
                    var_name = variation.get("name", f"Variation {i}")
                    var_desc = variation.get("description", "")
                    
                    console.print(f"  [bold]{var_name}[/bold]")
                    console.print(f"  {var_desc}")
                    
                    var_advantages = variation.get("advantages", [])
                    if var_advantages:
                        console.print("  [bold]Advantages:[/bold]")
                        for adv in var_advantages:
                            console.print(f"    - {adv}")
                    
                    var_disadvantages = variation.get("disadvantages", [])
                    if var_disadvantages:
                        console.print("  [bold]Disadvantages:[/bold]")
                        for dis in var_disadvantages:
                            console.print(f"    - {dis}")
                    
                    var_scenarios = variation.get("scenarios", [])
                    if var_scenarios:
                        console.print("  [bold]When to use:[/bold]")
                        for scn in var_scenarios:
                            console.print(f"    - {scn}")
                    
                    console.print()
        
        # Display next steps
        console.print()
        display_info("Next steps:")
        display_info(f"1. Convert process to SOP: taskinator pdd convert {process_id} --process {process_id}")
        display_info(f"2. Convert process to tasks: taskinator pdd to-tasks {process_id} --process {process_id}")
        
    except Exception as e:
        display_error(f"Error showing process: {e}")
        raise typer.Exit(1)

def generate_sop_markdown(sop):
    """Generate Markdown content for an SOP document."""
    # Generate Markdown content
    md_content = f"# {sop.title}\n\n"
    md_content += f"## Description\n{sop.description}\n\n"
    
    md_content += "## Metadata\n"
    md_content += f"- Version: {sop.version}\n"
    
    if sop.author:
        md_content += f"- Author: {sop.author}\n"
    
    if sop.department:
        md_content += f"- Department: {sop.department}\n"
    
    if sop.tags:
        md_content += f"- Tags: {', '.join(sop.tags)}\n"
    
    md_content += "\n"
    
    # Add step flow diagram
    md_content += "## Step Flow Diagram\n\n"
    md_content += "```mermaid\nflowchart TD\n"
    
    # Add nodes for each step
    for step in sorted(sop.steps, key=lambda s: s.order):
        md_content += f"    step{step.order}[\"{step.title}\"]\n"
    
    # Add connections based on prerequisites
    for step in sorted(sop.steps, key=lambda s: s.order):
        for prereq in step.prerequisites:
            md_content += f"    {prereq} --> step{step.order}\n"
    
    md_content += "```\n\n"
    
    # Add steps
    md_content += "## Steps\n"
    for step in sorted(sop.steps, key=lambda s: s.order):
        md_content += f"### Step {step.order}: {step.title}\n"
        md_content += f"Description: {step.description}\n"
        if step.estimated_time:
            md_content += f"Estimated Time: {step.estimated_time}\n"
        md_content += f"Prerequisites: {', '.join(step.prerequisites) if step.prerequisites else 'None'}\n"
        if step.required_skills:
            md_content += "Required Skills:\n"
            for skill in step.required_skills:
                md_content += f"- {skill}\n"
        md_content += "\n"
    
    return md_content

@pdd_app.command("identify-processes")
@_run_async
async def identify_processes(
    output_dir: str = typer.Option(
        "pdds", 
        "--output-dir", 
        "-o", 
        help="Directory to store identified processes"
    ),
    task_id: Optional[str] = typer.Option(
        None,
        "--task-id",
        "-t",
        help="Optional ID of a specific task to analyze. If not provided, all tasks will be analyzed."
    ),
    research: bool = typer.Option(
        False,
        "--research",
        help="Enable research mode to provide more in-depth analysis and domain-specific insights"
    ),
    variations: int = typer.Option(
        0,
        "--variations",
        "-v",
        help="Number of process variations to generate for each identified process (0-5)"
    )
):
    """Identify processes from tasks using AI.
    
    This command analyzes existing tasks to identify domain-specific processes
    and creates a structured processes.json file and individual PDD text files.
    
    When --research is enabled, the AI will perform more in-depth analysis of the domain
    and provide research-backed recommendations for process design. This includes:
    - Industry standards and established methodologies
    - Best practices for the specific domain
    - References to relevant frameworks
    - Consideration of edge cases and potential challenges
    
    The --variations option allows generating alternative approaches for each process,
    which can be useful for comparing different implementation strategies. Each variation includes:
    - A descriptive name
    - Key differences from the main approach
    - Advantages and disadvantages
    - Scenarios where the variation would be preferred
    
    Example usage:
      taskinator pdd identify-processes --research
      taskinator pdd identify-processes --variations 3
      taskinator pdd identify-processes --research --variations 2 --task-id 5
    """
    try:
        # Validate variations input
        if variations < 0 or variations > 5:
            display_error("Variations must be between 0 and 5")
            raise typer.Exit(1)
            
        # Get task manager
        task_manager = get_task_manager()
        
        # Load tasks
        data = read_json(task_manager.tasks_file)
        tasks = data.get('tasks', [])
        
        if not tasks:
            display_error("No tasks found for process identification")
            raise typer.Exit(1)
        
        # Filter tasks if task_id is provided
        if task_id:
            found = False
            for t in tasks:
                if str(t.get("id")) == str(task_id):
                    tasks = [t]
                    found = True
                    break
            
            if not found:
                display_error(f"Task with ID {task_id} not found")
                raise typer.Exit(1)
        
        display_banner("Process Identification")
        
        # Show mode information
        mode_info = []
        if research:
            mode_info.append("Research Mode: Enabled")
        if variations > 0:
            mode_info.append(f"Process Variations: {variations}")
            
        if mode_info:
            console.print(Panel("\n".join(mode_info), title="Analysis Configuration", border_style="blue"))
            
        display_info(f"Analyzing {len(tasks)} tasks to identify processes...")
        
        # Call AI service to identify processes
        with create_loading_indicator("Identifying processes..."):
            from .ai_services import identify_processes_from_tasks
            result = await identify_processes_from_tasks(
                tasks, 
                output_dir, 
                research_mode=research,
                variations_count=variations
            )
        
        # Display results
        processes = result.get("processes", [])
        display_success(f"Identified {len(processes)} processes")
        
        # Display processes in a table
        table = Table(title="Identified Processes")
        table.add_column("ID", style="cyan")
        table.add_column("Title", style="green")
        table.add_column("Complexity", style="yellow")
        table.add_column("Dependencies", style="magenta")
        table.add_column("Variations", style="blue")
        
        for process in processes:
            process_id = process.get("process_id") or process.get("id", "")
            title = process.get("title", "")
            complexity = process.get("complexity", "")
            dependencies = ", ".join(str(dep) for dep in process.get("dependencies", []))
            variation_count = len(process.get("variations", []))
            
            table.add_row(
                str(process_id),
                title,
                complexity,
                dependencies,
                str(variation_count) if variation_count > 0 else "-"
            )
        
        console.print(table)
        
        # Display analysis approach
        if "analysis_approach" in result:
            console.print(Panel(
                result.get("analysis_approach", ""),
                title="Analysis Approach",
                border_style="blue"
            ))
            
        # Display research insights if available
        if research and "research_insights" in result:
            console.print(Panel(
                result.get("research_insights", ""),
                title="Research Insights",
                border_style="green"
            ))
            
        # Display variations summary if present
        if variations > 0:
            variation_summary = []
            for process in processes:
                process_id = process.get("process_id") or process.get("id", "")
                title = process.get("title", "")
                process_variations = process.get("variations", [])
                
                if process_variations:
                    variation_summary.append(f"[bold cyan]{process_id}[/bold cyan]: [bold]{title}[/bold]")
                    for i, var in enumerate(process_variations, 1):
                        var_name = var.get("name", f"Variation {i}")
                        variation_summary.append(f"  {i}. [italic]{var_name}[/italic]")
                        
            if variation_summary:
                console.print(Panel(
                    "\n".join(variation_summary),
                    title="Process Variations Summary",
                    border_style="yellow"
                ))
        
        # Display next steps
        console.print()
        display_info("Process identification complete. The following files were created:")
        display_info(f"- {output_dir}/processes.json")
        for process in processes:
            process_id = process.get("process_id") or process.get("id", "")
            title = process.get("title", "")
            if process_id and title:
                filename = f"{process_id}_{title.lower().replace(' ', '_')}_pdd.txt"
                display_info(f"- {output_dir}/{filename}")
        
        console.print()
        display_info("Next steps:")
        display_info("1. Review the identified processes in the generated files")
        display_info("2. Convert PDDs to SOPs: taskinator pdd convert")
        display_info("3. Convert PDDs to tasks: taskinator pdd to-tasks")
        
    except Exception as e:
        display_error(f"Error identifying processes: {e}")
        raise typer.Exit(1)

@pdd_app.command("reintegrate")
@_run_async
async def pdd_reintegrate(
    pdd_dir: str = typer.Option(
        "pdds",
        "--pdd-dir",
        "-d",
        help="Directory containing PDD files"
    )
):
    """Reintegrate content from individual PDD files back into processes.json.
    
    This command reads all individual PDD files and updates the corresponding entries
    in the processes.json file with any additional content found in those files. This is
    particularly useful for preserving notes and design constraints added to individual
    PDD files.
    """
    try:
        task_manager = get_task_manager()
        stats = await task_manager.reintegrate_pdd_files(pdd_dir=pdd_dir)
        
    except Exception as e:
        display_error(f"Failed to reintegrate PDD files: {e}")
        raise typer.Exit(1)

def run():
    """Entry point for the CLI."""
    try:
        app()
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        display_error(f"An unexpected error occurred: {e}")
        raise typer.Exit(1)

if __name__ == "__main__":
    run()