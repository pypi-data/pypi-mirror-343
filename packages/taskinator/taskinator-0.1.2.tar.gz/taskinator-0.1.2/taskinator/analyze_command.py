"""Analyze command for Taskinator."""

import asyncio
import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Union, Any

import typer
from rich.console import Console
from rich.table import Table

from .config import config
from .utils import (
    display_error,
    display_info,
    display_success,
    display_warning,
    create_loading_indicator
)
from .task_manager import TaskManager, get_task_manager

async def analyze_command(
    task_id: Optional[str] = None,
    threshold: float = 7.0,
    output_file: Optional[str] = None,
    force: bool = False,
    export_training: bool = False,
    use_research: bool = False,
    use_sonnet: bool = False
):
    """Analyze task complexity and generate expansion recommendations."""
    try:
        # Set the model preference before creating the task manager
        if use_sonnet:
            config.use_sonnet_35 = True
            display_info("Using Claude 3.5 Sonnet model for complexity analysis")
            
        task_manager = get_task_manager()
        
        # Convert task_id to int if it's a numeric ID
        if task_id and task_id.isdigit():
            task_id = int(task_id)
        
        result = await task_manager.analyze_tasks(
            task_id=task_id,
            threshold=threshold,
            output_file=output_file,
            force=force,
            use_research=use_research
        )
        
        if export_training and result.get("report_file"):
            # Export training data
            from .complexity_module import ComplexityAnalysisModule
            module = ComplexityAnalysisModule()
            training_file = await module.export_training_data(result["report_file"])
            display_success(f"Exported training data to {training_file}")
            
        return result
    except Exception as e:
        display_error(f"Failed to analyze tasks: {e}")
        raise
