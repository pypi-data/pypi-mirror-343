"""Taskinator API for programmatic usage.

This module provides a high-level API for using Taskinator as a library,
allowing for scripted workflows and automation.
"""

import asyncio
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from .task_manager import TaskManager
from .utils import logger


class TaskinatorAPI:
    """API for programmatic usage of Taskinator.
    
    This class provides a programmatic interface to Taskinator functionality,
    allowing for automated workflows and integration with other systems.
    """
    
    def __init__(
        self, 
        project_root: str = ".",
        tasks_file: str = "tasks.json",
        display_output: bool = True
    ):
        """Initialize the TaskinatorAPI.
        
        Args:
            project_root: Root directory of the project
            tasks_file: Path to the tasks file
            display_output: Whether to display output to the console
        """
        self.task_manager = TaskManager(
            project_root=project_root,
            tasks_file=tasks_file,
            display_output=display_output
        )
    
    async def parse_prd(
        self, 
        prd_file: str,
        output_file: Optional[str] = None
    ) -> Dict[str, Any]:
        """Parse a PRD file and generate tasks.
        
        Args:
            prd_file: Path to the PRD file
            output_file: Optional path to save the generated tasks
            
        Returns:
            Dictionary containing the generated tasks
        """
        return await self.task_manager.parse_prd(prd_file, output_file)
    
    def list_tasks(self) -> List[Dict[str, Any]]:
        """List all tasks.
        
        Returns:
            List of tasks
        """
        data = self.task_manager.read_tasks()
        return data.get('tasks', []) if data else []
    
    async def expand_task(
        self,
        task_id: Union[str, int],
        num_subtasks: int = 5,
        use_research: bool = False,
        additional_context: str = ""
    ) -> Dict[str, Any]:
        """Expand a task into subtasks.
        
        Args:
            task_id: ID of the task to expand
            num_subtasks: Number of subtasks to generate
            use_research: Whether to use research for generating subtasks
            additional_context: Additional context for generating subtasks
            
        Returns:
            The updated task with subtasks
        """
        return await self.task_manager.expand_task(
            task_id=task_id,
            num_subtasks=num_subtasks,
            use_research=use_research,
            additional_context=additional_context
        )
    
    async def analyze_task_similarities(
        self, 
        threshold: float = 0.7, 
        output_file: Optional[str] = None
    ) -> Dict[str, Any]:
        """Analyze task similarities using the TaskSimilarityModule.
        
        Args:
            threshold: Similarity threshold (0.0-1.0)
            output_file: Path to save the similarity report
            
        Returns:
            Dictionary with similarity analysis results
        """
        task_manager = TaskManager(
            tasks_file=self.tasks_file,
            tasks_dir=self.tasks_dir,
            display_output=False
        )
        
        return await task_manager.analyze_task_similarities(
            threshold=threshold,
            output_file=output_file
        )
    
    async def analyze_task_complexity(
        self,
        task_id: Optional[str] = None,
        output_file: Optional[str] = None,
        use_research: bool = False,
        use_dspy: bool = False
    ) -> Dict[str, Any]:
        """Analyze task complexity using AI or DSPy.
        
        Args:
            task_id: Optional ID of a specific task to analyze
            output_file: Path to save the complexity report
            use_research: Whether to use research for analysis
            use_dspy: Whether to use the DSPy-based complexity analysis module
            
        Returns:
            Dictionary with complexity analysis results
        """
        task_manager = TaskManager(
            tasks_file=self.tasks_file,
            tasks_dir=self.tasks_dir,
            display_output=False
        )
        
        return await task_manager.analyze_task_complexity(
            task_id=task_id,
            output_file=output_file,
            use_research=use_research,
            use_dspy=use_dspy
        )
    
    def export_complexity_training_data(
        self,
        output_file: str = "training_data/complexity_dataset.json"
    ) -> None:
        """Export training data from previous complexity analyses.
        
        Args:
            output_file: Path to save the training dataset
        """
        from .complexity_training_logger import complexity_logger
        complexity_logger.export_training_dataset(output_file=output_file)
    
    async def review_recommendations(
        self,
        report_file: str = "tasks/task-complexity-report.json",
        threshold: float = 5.0,
        non_interactive: bool = True,
        output_file: Optional[str] = "tasks/approved-expansions.json"
    ) -> List[Dict[str, Any]]:
        """Review task complexity recommendations and approve tasks for expansion.
        
        Args:
            report_file: Path to the complexity report file
            threshold: Complexity score threshold for recommending expansion
            non_interactive: If True, approve all recommendations above threshold
            output_file: Optional path to save the approved expansions
            
        Returns:
            List of approved task expansions
        """
        approved_tasks = self.task_manager.review_complexity_recommendations(
            report_file=report_file,
            threshold=threshold,
            non_interactive=non_interactive
        )
        
        # Save approved tasks to file if output_file is provided
        if output_file and approved_tasks:
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            with open(output_file, "w") as f:
                json.dump({"approved_expansions": approved_tasks}, f, indent=2)
        
        return approved_tasks
    
    async def implement_expansions(
        self,
        approved_expansions: Optional[List[Dict[str, Any]]] = None,
        approved_file: Optional[str] = None,
        num_subtasks: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Implement approved task expansions by expanding tasks into subtasks.
        
        Args:
            approved_expansions: List of approved expansions
            approved_file: Path to the approved expansions file
            num_subtasks: Override the recommended number of subtasks
            
        Returns:
            List of expanded tasks
        """
        if not approved_expansions and not approved_file:
            raise ValueError("Either approved_expansions or approved_file must be provided")
        
        # Read from file if approved_expansions is not provided
        if not approved_expansions:
            if not os.path.exists(approved_file):
                raise ValueError(f"Approved expansions file not found: {approved_file}")
            
            with open(approved_file, "r") as f:
                approved_data = json.load(f)
            
            if "approved_expansions" not in approved_data or not approved_data["approved_expansions"]:
                raise ValueError("No approved expansions found in the file")
            
            approved_expansions = approved_data["approved_expansions"]
        
        expanded_tasks = []
        
        # Process each approved expansion
        for expansion in approved_expansions:
            task_id = expansion.get("taskId")
            if not task_id:
                continue
                
            # Get the recommended number of subtasks or use the override
            subtask_count = num_subtasks if num_subtasks is not None else expansion.get("recommendedSubtasks", 5)
            
            # Get the expansion prompt
            expansion_prompt = expansion.get("expansionPrompt", "")
            
            # Expand the task
            expanded_task = await self.task_manager.expand_task(
                task_id=task_id,
                num_subtasks=subtask_count,
                additional_context=expansion_prompt
            )
            
            expanded_tasks.append(expanded_task)
        
        return expanded_tasks
    
    async def recursive_expand_tasks(
        self,
        complexity_threshold: float = 5.0,
        max_depth: int = 3,
        current_depth: int = 0
    ) -> Dict[str, Any]:
        """Recursively expand tasks until all are below the complexity threshold.
        
        Args:
            complexity_threshold: Complexity score threshold for expansion
            max_depth: Maximum recursion depth
            current_depth: Current recursion depth
            
        Returns:
            Dictionary containing statistics about the expansion process
        """
        if current_depth >= max_depth:
            return {
                "status": "max_depth_reached",
                "max_depth": max_depth,
                "current_depth": current_depth
            }
        
        # Analyze task complexity
        analysis = await self.analyze_task_complexity()
        
        # Get tasks above threshold
        tasks_above_threshold = [
            task for task in analysis.get("complexityAnalysis", [])
            if task.get("complexityScore", 0) >= complexity_threshold 
            and task.get("recommendedSubtasks", 0) > 0
        ]
        
        if not tasks_above_threshold:
            return {
                "status": "complete",
                "message": "All tasks are below complexity threshold",
                "depth_reached": current_depth
            }
        
        # Review recommendations (non-interactive)
        approved_tasks = self.review_recommendations(
            threshold=complexity_threshold,
            non_interactive=True
        )
        
        if not approved_tasks:
            return {
                "status": "no_approved_tasks",
                "message": "No tasks were approved for expansion",
                "depth_reached": current_depth
            }
        
        # Implement expansions
        await self.implement_expansions(approved_expansions=approved_tasks)
        
        # Recursively expand tasks
        return await self.recursive_expand_tasks(
            complexity_threshold=complexity_threshold,
            max_depth=max_depth,
            current_depth=current_depth + 1
        )


# Example usage
async def example_workflow():
    """Example workflow using the Taskinator API."""
    api = TaskinatorAPI(display_output=True)
    
    # Parse PRD
    await api.parse_prd("enhancement_1_prd.txt")
    
    # Analyze complexity
    await api.analyze_task_complexity()
    
    # Review recommendations (non-interactive)
    approved_tasks = api.review_recommendations(non_interactive=True)
    
    # Implement expansions
    await api.implement_expansions(approved_expansions=approved_tasks)
    
    # Or do it all recursively
    # await api.recursive_expand_tasks(complexity_threshold=5.0, max_depth=3)


if __name__ == "__main__":
    # Run the example workflow
    asyncio.run(example_workflow())
