#!/usr/bin/env python3
"""
Demo script for creating, saving, and analyzing a Process Design Document (PDD).
"""

import os
import sys
from pathlib import Path

from taskinator.pdd_document import (
    PDDDocument, 
    PDDProcess, 
    PDDStatus, 
    PDDImplementationDifficulty,
    PDDDocumentManager
)
from taskinator.pdd_parser import PDDParserFactory
from taskinator.pdd_complexity import PDDComplexityAnalyzer

def create_sample_pdd():
    """Create a sample PDD document for the Taskinator project."""
    # Create processes
    process1 = PDDProcess(
        process_id="parse_prd",
        title="Parse PRD Document",
        description="Parse a Product Requirements Document (PRD) and extract tasks.",
        order=1,
        estimated_time="2 days",
        dependencies=[],
        difficulty=2.5,
        implementation_difficulty=PDDImplementationDifficulty.MODERATE,
        required_resources=["Developer", "Product Manager"],
        inputs=["PRD document"],
        outputs=["Initial task list", "Task dependencies"]
    )
    
    process2 = PDDProcess(
        process_id="analyze_complexity",
        title="Analyze Task Complexity",
        description="Analyze the complexity of each task and identify which ones need to be broken down.",
        order=2,
        estimated_time="1 day",
        dependencies=["parse_prd"],
        difficulty=3.0,
        implementation_difficulty=PDDImplementationDifficulty.MODERATE,
        required_resources=["Developer", "AI Engineer"],
        inputs=["Initial task list"],
        outputs=["Complexity scores", "Breakdown recommendations"]
    )
    
    process3 = PDDProcess(
        process_id="expand_tasks",
        title="Expand Complex Tasks",
        description="Break down complex tasks into smaller, more manageable subtasks.",
        order=3,
        estimated_time="3 days",
        dependencies=["analyze_complexity"],
        difficulty=4.0,
        implementation_difficulty=PDDImplementationDifficulty.COMPLEX,
        required_resources=["Developer", "AI Engineer", "Product Manager"],
        inputs=["Complexity scores", "Breakdown recommendations"],
        outputs=["Expanded task list", "Updated dependencies"]
    )
    
    process4 = PDDProcess(
        process_id="generate_task_files",
        title="Generate Task Files",
        description="Generate individual task files for each task and subtask.",
        order=4,
        estimated_time="1 day",
        dependencies=["expand_tasks"],
        difficulty=2.0,
        implementation_difficulty=PDDImplementationDifficulty.SIMPLE,
        required_resources=["Developer"],
        inputs=["Expanded task list"],
        outputs=["Task files"]
    )
    
    # Create the PDD document
    pdd = PDDDocument(
        doc_id="taskinator_workflow",
        title="Taskinator Workflow Process Design",
        description="Process design for the Taskinator workflow, which breaks down PRDs into tasks and subtasks.",
        version="1.0",
        status=PDDStatus.DRAFT,
        author="Taskinator Team",
        department="Engineering",
        tags=["taskinator", "workflow", "process"],
        processes=[process1, process2, process3, process4],
        business_objectives=[
            "Automate the process of breaking down PRDs into manageable tasks",
            "Ensure consistent task complexity across the project",
            "Reduce the time spent on task planning"
        ],
        success_criteria=[
            "All tasks have complexity scores below the threshold",
            "Task dependencies are correctly identified",
            "Task files are generated with all required information"
        ],
        assumptions=[
            "PRD documents follow a consistent format",
            "Complexity analysis can be automated with AI"
        ],
        constraints=[
            "Must work with existing Taskinator infrastructure",
            "Must support both interactive and scripted workflows"
        ]
    )
    
    return pdd

def save_pdd_as_yaml(pdd, output_dir):
    """Save the PDD as a YAML file for demonstration purposes."""
    import yaml
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Convert PDD to dictionary
    pdd_dict = pdd.to_dict()
    
    # Save as YAML
    yaml_path = os.path.join(output_dir, f"{pdd.doc_id}.yaml")
    with open(yaml_path, "w") as f:
        yaml.dump(pdd_dict, f, default_flow_style=False, sort_keys=False)
    
    print(f"Saved PDD as YAML: {yaml_path}")
    return yaml_path

def save_pdd_as_markdown(pdd, output_dir):
    """Save the PDD as a Markdown file for demonstration purposes."""
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate Markdown content with the integrated Mermaid diagram
    md_content = pdd.to_markdown()
    
    # Save as Markdown
    md_path = os.path.join(output_dir, f"{pdd.doc_id}.md")
    with open(md_path, "w") as f:
        f.write(md_content)
    
    print(f"Saved PDD as Markdown with Mermaid diagram: {md_path}")
    return md_path

def analyze_pdd(pdd):
    """Analyze the PDD document for complexity."""
    analyzer = PDDComplexityAnalyzer(use_dspy=False)
    analysis = analyzer.analyze_document(pdd)
    
    print("\n=== PDD Complexity Analysis ===")
    print(f"Document: {analysis['documentTitle']}")
    print(f"Average Complexity: {analysis['averageComplexity']:.2f}")
    print(f"Maximum Complexity: {analysis['maxComplexity']:.2f}")
    print(f"Overall Difficulty: {analysis['overallDifficulty']}")
    print(f"Explanation: {analysis['explanation']}")
    
    print("\nProcess Analyses:")
    for process_analysis in analysis['processAnalyses']:
        print(f"  - {process_analysis['processTitle']}: {process_analysis['complexityScore']:.2f} " +
              f"({process_analysis['implementationDifficulty']})")
    
    return analysis

def main():
    """Main function to demonstrate PDD functionality."""
    print("=== Taskinator PDD Demo ===")
    
    # Create a sample PDD
    print("\nCreating sample PDD document...")
    pdd = create_sample_pdd()
    
    # Create a temporary directory for output files
    output_dir = "pdd_demo_output"
    
    # Save the PDD using the document manager
    print("\nSaving PDD using PDDDocumentManager...")
    manager = PDDDocumentManager(output_dir)
    manager.save_document(pdd)
    
    # Save as YAML and Markdown for demonstration
    yaml_path = save_pdd_as_yaml(pdd, output_dir)
    md_path = save_pdd_as_markdown(pdd, output_dir)
    
    # Parse the YAML file using the parser
    print("\nParsing PDD from YAML file...")
    parsed_pdd = PDDParserFactory.parse(yaml_path)
    print(f"Parsed PDD: {parsed_pdd.title} with {len(parsed_pdd.processes)} processes")
    
    # Analyze the PDD
    print("\nAnalyzing PDD complexity...")
    analysis = analyze_pdd(pdd)
    
    print("\nDemo completed successfully!")
    print(f"Output files are in the '{output_dir}' directory.")

if __name__ == "__main__":
    main()
