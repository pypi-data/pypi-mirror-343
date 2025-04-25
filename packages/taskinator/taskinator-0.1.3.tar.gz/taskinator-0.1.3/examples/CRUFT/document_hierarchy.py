#!/usr/bin/env python3
"""
Script to demonstrate the document hierarchy in Taskinator.
This script creates a simple example of each document type and shows how they relate.
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
from taskinator.sop_document import (
    SOPDocument,
    SOPStep,
    SOPStatus,
    SOPDocumentManager
)
from taskinator.task_manager import TaskManager


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
        processes=[process1, process2],
        business_objectives=[
            "Automate the process of breaking down PRDs into manageable tasks",
            "Ensure consistent task complexity across the project"
        ],
        success_criteria=[
            "All tasks have complexity scores below the threshold",
            "Task dependencies are correctly identified"
        ]
    )
    
    return pdd


def create_sample_sop_for_process(process_id):
    """Create a sample SOP document for a specific PDD process."""
    if process_id == "analyze_complexity":
        # Create steps for the "Analyze Task Complexity" process
        step1 = SOPStep(
            step_id="step1",
            title="Extract task descriptions",
            description="Extract the title, description, and details from each task.",
            order=1,
            estimated_time="15 minutes",
            prerequisites=[],
            required_skills=["Python", "Data Extraction"]
        )
        
        step2 = SOPStep(
            step_id="step2",
            title="Apply complexity heuristics",
            description="Apply complexity heuristics to each task based on its description.",
            order=2,
            estimated_time="30 minutes",
            prerequisites=["step1"],
            required_skills=["Python", "AI", "Complexity Analysis"]
        )
        
        step3 = SOPStep(
            step_id="step3",
            title="Calculate complexity scores",
            description="Calculate complexity scores for each task using the heuristics.",
            order=3,
            estimated_time="15 minutes",
            prerequisites=["step2"],
            required_skills=["Python", "Math"]
        )
        
        step4 = SOPStep(
            step_id="step4",
            title="Generate recommendations",
            description="Generate recommendations for tasks that need to be broken down.",
            order=4,
            estimated_time="30 minutes",
            prerequisites=["step3"],
            required_skills=["Python", "AI", "Task Management"]
        )
        
        # Create the SOP document
        sop = SOPDocument(
            doc_id="analyze_complexity_sop",
            title="SOP for Analyzing Task Complexity",
            description="Standard Operating Procedure for analyzing task complexity and generating breakdown recommendations.",
            version="1.0",
            status=SOPStatus.DRAFT,
            author="Taskinator Team",
            department="Engineering",
            tags=["taskinator", "complexity", "analysis"],
            steps=[step1, step2, step3, step4]
        )
        
        return sop
    else:
        raise ValueError(f"No SOP template available for process: {process_id}")


def demonstrate_document_hierarchy():
    """Demonstrate the document hierarchy in Taskinator."""
    print("=== Taskinator Document Hierarchy Demonstration ===")
    
    # Create output directory
    output_dir = "document_hierarchy_demo"
    os.makedirs(output_dir, exist_ok=True)
    
    # Initialize document managers
    pdd_manager = PDDDocumentManager(output_dir)
    sop_manager = SOPDocumentManager(output_dir)
    
    # 1. Create and save a PDD
    print("\n1. Creating Process Design Document (PDD)...")
    pdd = create_sample_pdd()
    pdd_manager.save_document(pdd)
    print(f"   - Created PDD: {pdd.title} with {len(pdd.processes)} processes")
    
    # 2. Create and save an SOP for a specific process
    print("\n2. Creating Standard Operating Procedure (SOP) for a process...")
    process_id = "analyze_complexity"
    process = next((p for p in pdd.processes if p.process_id == process_id), None)
    if process:
        print(f"   - Selected process: {process.title}")
        sop = create_sample_sop_for_process(process_id)
        sop_manager.save_document(sop)
        print(f"   - Created SOP: {sop.title} with {len(sop.steps)} steps")
    else:
        print(f"   - Process not found: {process_id}")
    
    # 3. Generate Markdown versions for visualization
    print("\n3. Generating Markdown versions for visualization...")
    
    # Generate PDD Markdown
    pdd_md_path = os.path.join(output_dir, f"{pdd.doc_id}.md")
    with open(pdd_md_path, "w") as f:
        f.write(pdd.to_markdown())
    print(f"   - Generated PDD Markdown: {pdd_md_path}")
    
    # Generate SOP Markdown (simplified version)
    if 'sop' in locals():
        sop_md_path = os.path.join(output_dir, f"{sop.doc_id}.md")
        with open(sop_md_path, "w") as f:
            # Simple Markdown representation
            md_content = f"# {sop.title}\n\n"
            md_content += f"## Description\n{sop.description}\n\n"
            
            md_content += "## Steps\n"
            for step in sorted(sop.steps, key=lambda s: s.order):
                md_content += f"### Step {step.order}: {step.title}\n"
                md_content += f"Description: {step.description}\n"
                md_content += f"Estimated Time: {step.estimated_time}\n"
                md_content += f"Prerequisites: {', '.join(step.prerequisites) if step.prerequisites else 'None'}\n"
                md_content += f"Required Skills: {', '.join(step.required_skills) if step.required_skills else 'None'}\n\n"
            
            f.write(md_content)
        print(f"   - Generated SOP Markdown: {sop_md_path}")
    
    # 4. Generate a relationship diagram
    print("\n4. Generating relationship diagram...")
    diagram_path = os.path.join(output_dir, "document_relationship.md")
    
    with open(diagram_path, "w") as f:
        f.write("# Document Relationship Diagram\n\n")
        f.write("```mermaid\nflowchart TD\n")
        
        # Add nodes
        f.write("    PRD[\"Product Requirements Document\"]\n")
        f.write(f"    PDD[\"{pdd.title}\"]\n")
        if 'sop' in locals():
            f.write(f"    SOP[\"{sop.title}\"]\n")
        
        # Add PDD processes
        for i, process in enumerate(sorted(pdd.processes, key=lambda p: p.order)):
            f.write(f"    Process{i+1}[\"{process.title}\"]\n")
        
        # Add SOP steps if available
        if 'sop' in locals():
            for i, step in enumerate(sorted(sop.steps, key=lambda s: s.order)):
                f.write(f"    Step{i+1}[\"{step.title}\"]\n")
        
        # Add relationships
        f.write("    PRD --> PDD\n")
        if 'sop' in locals():
            f.write("    PDD --> SOP\n")
        
        # Connect PDD to processes
        for i in range(len(pdd.processes)):
            f.write(f"    PDD --- Process{i+1}\n")
        
        # Connect processes based on dependencies
        for i, process in enumerate(sorted(pdd.processes, key=lambda p: p.order)):
            for dep in process.dependencies:
                dep_idx = next((j for j, p in enumerate(sorted(pdd.processes, key=lambda p: p.order)) if p.process_id == dep), None)
                if dep_idx is not None:
                    f.write(f"    Process{dep_idx+1} --> Process{i+1}\n")
        
        # Connect SOP to steps if available
        if 'sop' in locals():
            for i in range(len(sop.steps)):
                f.write(f"    SOP --- Step{i+1}\n")
            
            # Connect steps based on prerequisites
            for i, step in enumerate(sorted(sop.steps, key=lambda s: s.order)):
                for prereq in step.prerequisites:
                    prereq_idx = next((j for j, s in enumerate(sorted(sop.steps, key=lambda s: s.order)) if s.step_id == prereq), None)
                    if prereq_idx is not None:
                        f.write(f"    Step{prereq_idx+1} --> Step{i+1}\n")
            
            # Connect process to SOP
            process_idx = next((i for i, p in enumerate(sorted(pdd.processes, key=lambda p: p.order)) if p.process_id == process_id), None)
            if process_idx is not None:
                f.write(f"    Process{process_idx+1} --> SOP\n")
        
        f.write("```\n")
    
    print(f"   - Generated relationship diagram: {diagram_path}")
    
    print("\nDemonstration completed successfully!")
    print(f"Output files are in the '{output_dir}' directory.")


if __name__ == "__main__":
    demonstrate_document_hierarchy()
