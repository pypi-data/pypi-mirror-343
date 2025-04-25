"""
Module for converting PDD documents to Taskinator tasks.

This module provides functionality to convert Process Design Documents (PDDs)
into Taskinator tasks, allowing for seamless integration between process design
and task implementation.
"""

import os
from pathlib import Path
from typing import Dict, List, Optional, Union, Any

from loguru import logger

from .pdd_document import PDDDocument, PDDDocumentManager, PDDProcess
from .pdd_complexity import PDDComplexityAnalyzer
from .task_manager import TaskManager
from .config import TaskPriority, TaskStatus


class PDDTaskConverter:
    """Converts PDD documents to Taskinator tasks."""
    
    def __init__(self, task_manager: Optional[TaskManager] = None):
        """Initialize the PDD to Task converter.
        
        Args:
            task_manager: TaskManager instance to use for task creation
        """
        self.task_manager = task_manager or TaskManager()
        self.pdd_manager = PDDDocumentManager()
        self.complexity_analyzer = PDDComplexityAnalyzer(use_dspy=False)
    
    def convert_pdd_to_tasks(
        self, 
        pdd_id: str, 
        priority: str = "medium",
        generate_files: bool = True,
        auto_analyze: bool = False,
        auto_expand_threshold: Optional[float] = None
    ) -> Dict[str, Any]:
        """Convert a PDD document to Taskinator tasks.
        
        Args:
            pdd_id: ID of the PDD document to convert
            priority: Default priority for the generated tasks
            generate_files: Whether to generate task files
            auto_analyze: Whether to automatically analyze task complexity after conversion
            auto_expand_threshold: If set, automatically expand tasks with complexity above this threshold
            
        Returns:
            Dictionary containing the generated tasks data
        """
        # Load the PDD document
        pdd = self.pdd_manager.load_document(pdd_id)
        if not pdd:
            logger.error(f"PDD document not found: {pdd_id}")
            raise ValueError(f"PDD document not found: {pdd_id}")
        
        # Analyze the PDD document for complexity
        complexity_analysis = self.complexity_analyzer.analyze_document(pdd)
        
        # Create tasks from the PDD processes
        tasks = []
        
        # First, create a task for the overall PDD
        main_task = {
            "id": len(tasks) + 1,
            "title": f"Implement {pdd.title}",
            "description": pdd.description,
            "status": TaskStatus.PENDING,
            "priority": priority,
            "dependencies": [],
            "details": self._generate_main_task_details(pdd, complexity_analysis),
            "test_strategy": "Verify all processes are implemented according to the PDD specifications.",
            "complexity": complexity_analysis.get("averageComplexity", 5.0)
        }
        tasks.append(main_task)
        
        # Then create tasks for each process
        process_tasks = []
        for process in sorted(pdd.processes, key=lambda p: p.order):
            # Find the process complexity analysis
            process_analysis = next(
                (pa for pa in complexity_analysis.get("processAnalyses", []) 
                 if pa.get("processTitle") == process.title),
                None
            )
            
            # Determine dependencies based on process dependencies
            dependencies = []
            if process.dependencies:
                for dep_id in process.dependencies:
                    # Find the task ID for the dependent process
                    dep_task_idx = next(
                        (i for i, t in enumerate(process_tasks) 
                         if t.get("process_id") == dep_id),
                        None
                    )
                    if dep_task_idx is not None:
                        # Add 2 to account for the main task (id=1) and 0-based indexing
                        dependencies.append(dep_task_idx + 2)
            
            # Always depend on the main task
            dependencies.append(1)
            
            # Create the task
            task = {
                "id": len(tasks) + 1,
                "title": process.title,
                "description": process.description,
                "status": TaskStatus.PENDING,
                "priority": priority,
                "dependencies": dependencies,
                "details": self._generate_process_task_details(process, process_analysis),
                "test_strategy": f"Verify the process outputs: {', '.join(process.outputs)}",
                "complexity": process_analysis.get("complexityScore", 5.0) if process_analysis else 5.0,
                "process_id": process.process_id,  # Store the process ID for reference
                "source_pdd": pdd_id,  # Store the source PDD ID for reference
                "source_type": "pdd_process"  # Indicate this task came from a PDD process
            }
            tasks.append(task)
            process_tasks.append(task)
        
        # Create the tasks data structure
        tasks_data = {
            "tasks": tasks,
            "metadata": {
                "source": f"PDD: {pdd.title}",
                "created_date": pdd.created_date,
                "version": pdd.version,
                "pdd_id": pdd_id
            }
        }
        
        # Write tasks to the tasks.json file
        tasks_file = Path(self.task_manager.tasks_file)
        tasks_file.parent.mkdir(parents=True, exist_ok=True)
        
        from .utils import write_json
        write_json(tasks_file, tasks_data)
        
        logger.info(f"Generated {len(tasks)} tasks from PDD: {pdd.title}")
        
        # Generate individual task files if requested
        if generate_files:
            import asyncio
            asyncio.run(self.task_manager.generate_task_files())
        
        # Automatically analyze task complexity if requested
        if auto_analyze:
            logger.info(f"Automatically analyzing task complexity for PDD: {pdd.title}")
            import asyncio
            analysis_results = asyncio.run(self.task_manager.analyze_task_complexity(
                output_file=f"tasks/pdd-{pdd_id}-complexity-report.json",
                analyze_subtasks=True
            ))
            
            # Automatically expand tasks above the threshold if requested
            if auto_expand_threshold is not None:
                logger.info(f"Automatically expanding tasks with complexity above {auto_expand_threshold}")
                expanded_tasks = []
                
                for result in analysis_results:
                    task_id = result.get('taskId')
                    complexity = result.get('complexityScore', 0)
                    
                    if complexity >= auto_expand_threshold:
                        logger.info(f"Expanding task {task_id} with complexity {complexity}")
                        try:
                            expanded_task = asyncio.run(self.task_manager.expand_task(
                                task_id=task_id,
                                num_subtasks=result.get('recommendedSubtasks', 5),
                                use_research=True
                            ))
                            expanded_tasks.append(expanded_task)
                        except Exception as e:
                            logger.error(f"Error expanding task {task_id}: {e}")
                
                if expanded_tasks:
                    logger.info(f"Automatically expanded {len(expanded_tasks)} tasks")
        
        return tasks_data
    
    def _generate_main_task_details(self, pdd: PDDDocument, analysis: Dict[str, Any]) -> str:
        """Generate details for the main task.
        
        Args:
            pdd: PDD document
            analysis: Complexity analysis results
            
        Returns:
            Task details as a string
        """
        details = f"# Implementation of {pdd.title}\n\n"
        
        # Add description
        details += f"## Description\n{pdd.description}\n\n"
        
        # Add business objectives
        if pdd.business_objectives:
            details += "## Business Objectives\n"
            for objective in pdd.business_objectives:
                details += f"- {objective}\n"
            details += "\n"
        
        # Add success criteria
        if pdd.success_criteria:
            details += "## Success Criteria\n"
            for criteria in pdd.success_criteria:
                details += f"- {criteria}\n"
            details += "\n"
        
        # Add complexity analysis
        details += "## Complexity Analysis\n"
        details += f"Average Complexity: {analysis.get('averageComplexity', 'N/A')}\n"
        details += f"Maximum Complexity: {analysis.get('maxComplexity', 'N/A')}\n"
        details += f"Overall Difficulty: {analysis.get('overallDifficulty', 'N/A')}\n\n"
        
        # Add implementation notes
        details += "## Implementation Notes\n"
        details += "This task involves implementing all processes defined in the PDD document.\n"
        details += "Each process has been broken down into a separate task with its own details.\n\n"
        
        # Add process overview
        details += "## Process Overview\n"
        for process in sorted(pdd.processes, key=lambda p: p.order):
            details += f"### {process.order}. {process.title}\n"
            details += f"{process.description}\n"
            if process.dependencies:
                details += f"Dependencies: {', '.join(process.dependencies)}\n"
            details += "\n"
        
        return details
    
    def _generate_process_task_details(self, process: PDDProcess, analysis: Optional[Dict[str, Any]]) -> str:
        """Generate details for a process task.
        
        Args:
            process: PDD process
            analysis: Process complexity analysis results
            
        Returns:
            Task details as a string
        """
        details = f"# Implementation of Process: {process.title}\n\n"
        
        # Add description
        details += f"## Description\n{process.description}\n\n"
        
        # Add implementation details
        details += "## Implementation Details\n"
        
        # Add estimated time
        if process.estimated_time:
            details += f"Estimated Time: {process.estimated_time}\n"
        
        # Add implementation difficulty
        if process.implementation_difficulty:
            details += f"Implementation Difficulty: {process.implementation_difficulty.value}\n"
        
        # Add complexity analysis
        if analysis:
            details += f"Complexity Score: {analysis.get('complexityScore', 'N/A')}\n"
            if analysis.get('explanation'):
                details += f"Analysis: {analysis.get('explanation')}\n"
        
        details += "\n"
        
        # Add required resources
        if process.required_resources:
            details += "## Required Resources\n"
            for resource in process.required_resources:
                details += f"- {resource}\n"
            details += "\n"
        
        # Add inputs and outputs
        details += "## Process Interface\n"
        
        if process.inputs:
            details += "### Inputs\n"
            for input_item in process.inputs:
                details += f"- {input_item}\n"
            details += "\n"
        
        if process.outputs:
            details += "### Outputs\n"
            for output_item in process.outputs:
                details += f"- {output_item}\n"
            details += "\n"
        
        # Add implementation guidance
        details += "## Implementation Guidance\n"
        details += "1. Review the process description and requirements carefully\n"
        details += "2. Ensure all required resources are available\n"
        details += "3. Implement the process to handle all specified inputs\n"
        details += "4. Verify that the process produces the expected outputs\n"
        details += "5. Document any assumptions or decisions made during implementation\n"
        
        return details


# CLI command implementation
async def convert_pdd_to_tasks_command(pdd_id: str, priority: str = "medium") -> None:
    """CLI command to convert a PDD document to tasks.
    
    Args:
        pdd_id: ID of the PDD document to convert
        priority: Default priority for the generated tasks
    """
    from .ui import display_success, display_error, display_info, create_loading_indicator
    
    try:
        # Ensure PDD directory exists
        pdd_dir = "pdds"
        Path(pdd_dir).mkdir(exist_ok=True)
        
        # Create converter and task manager
        task_manager = TaskManager(display_output=True)
        converter = PDDTaskConverter(task_manager)
        
        # Display banner info
        display_info(f"Converting PDD document '{pdd_id}' to tasks...")
        display_info(f"Using priority: {priority}")
        
        # Create a loading indicator
        with create_loading_indicator("Converting PDD to tasks...") as progress:
            # Load the PDD document to verify it exists
            pdd = converter.pdd_manager.load_document(pdd_id)
            if not pdd:
                display_error(f"PDD document not found: {pdd_id}")
                return
                
            display_info(f"Found PDD: {pdd.title} with {len(pdd.processes)} processes")
            
            # Convert PDD to tasks
            tasks_data = converter.convert_pdd_to_tasks(pdd_id, priority, generate_files=False)
            
            # Generate task files manually (to avoid asyncio issues)
            await task_manager.generate_task_files()
            
            # Display task information
            display_info("\nGenerated Tasks:")
            for task in tasks_data["tasks"]:
                dependencies = ", ".join([str(dep) for dep in task.get("dependencies", [])])
                display_info(f"  - Task {task['id']}: {task['title']} (Priority: {task['priority']}, Dependencies: {dependencies or 'None'})")
        
        # Display success and next steps
        display_success(
            f"Successfully generated {len(tasks_data['tasks'])} tasks from PDD '{pdd_id}'\n\n"
            "Next Steps:\n"
            "1. Run 'taskinator list' to view all tasks\n"
            "2. Run 'taskinator analyze' to analyze task complexity\n"
            "3. Run 'taskinator expand --id=<id>' to break down complex tasks into subtasks"
        )
        
    except Exception as e:
        logger.error(f"Error converting PDD to tasks: {e}")
        display_error(f"Failed to convert PDD to tasks: {e}")
