"""
Module for converting Process Design Documents (PDDs) to Standard Operating Procedures (SOPs).

This module provides functionality to transform PDDs into SOPs, allowing for
seamless integration between process design and detailed implementation instructions.
"""

import os
from pathlib import Path
from typing import Dict, List, Optional, Union, Any, Tuple

from loguru import logger

from .pdd_document import PDDDocument, PDDDocumentManager, PDDProcess
from .pdd_complexity import PDDComplexityAnalyzer
from .sop_document import SOPDocument, SOPDocumentManager, SOPStep, SOPStatus
from .sop_patterns import get_pattern_for_task, get_all_pattern_types, get_pattern_by_type

class PDDContentAnalyzer:
    """Analyzes PDD content to extract information for SOP generation."""
    
    def __init__(self):
        """Initialize the PDD content analyzer."""
        self.complexity_analyzer = PDDComplexityAnalyzer(use_dspy=False)
    
    def analyze_pdd(self, pdd: PDDDocument) -> Dict[str, Any]:
        """Analyze a PDD document to extract information for SOP generation.
        
        Args:
            pdd: PDD document to analyze
            
        Returns:
            Dictionary containing analysis results
        """
        # Analyze processes
        processes = []
        for process in pdd.processes:
            # Convert complexity string to numeric score
            complexity_score = {
                "simple": 3,
                "medium": 5,
                "complex": 7,
                "very_complex": 9
            }.get(process.complexity, 5)
            
            # Analyze process
            process_info = {
                "process_id": process.process_id,
                "title": process.title,
                "description": process.description,
                "complexity_score": complexity_score,
                "dependencies": process.dependencies,
                "parameters": process.parameters,
                "variations": process.variations
            }
            processes.append(process_info)
        
        # Analyze dependencies
        dependency_graph = {}
        for process in pdd.processes:
            dependency_graph[process.process_id] = process.dependencies
        
        # Return analysis results
        return {
            "processes": processes,
            "dependency_graph": dependency_graph
        }


class PDDToSOPConverter:
    """Converts PDD documents to SOP documents."""
    
    def __init__(self, pdd_dir: str = "pdds", sop_dir: str = "sops"):
        """Initialize the PDD to SOP converter.
        
        Args:
            pdd_dir: Directory containing PDD documents
            sop_dir: Directory to store SOP documents
        """
        self.pdd_dir = pdd_dir
        self.sop_dir = sop_dir
        self.pdd_manager = PDDDocumentManager(pdd_dir)
        self.sop_manager = SOPDocumentManager(sop_dir)
        self.content_analyzer = PDDContentAnalyzer()
    
    def convert_pdd_to_sop(self, pdd_id: str, process_id: str, variation_name: str = None) -> Optional[SOPDocument]:
        """Convert a specific process in a PDD to an SOP document.
        
        Args:
            pdd_id: ID of the PDD document
            process_id: ID of the process to convert
            variation_name: Optional name of a specific variation to convert
            
        Returns:
            Generated SOP document
        """
        # Load the PDD document
        pdd = self.pdd_manager.load_document(pdd_id)
        if not pdd:
            logger.error(f"PDD document not found: {pdd_id}")
            return None
        
        # Analyze the PDD document
        logger.info(f"Analyzing PDD document: {pdd_id}")
        pdd_analysis = self.content_analyzer.analyze_pdd(pdd)
        
        # Find the process
        process = next((p for p in pdd.processes if p.process_id == process_id), None)
        if not process:
            logger.error(f"Process not found in PDD: {process_id}")
            return None
        
        # Generate SOP structure
        logger.info(f"Generating SOP structure for process: {process_id}")
        
        # Get process details
        process_title = process.title
        process_description = process.description
        complexity = process.complexity
        
        # Check if we're generating for a specific variation
        variation = None
        if variation_name:
            variation = next((v for v in process.variations if v["name"] == variation_name), None)
            if variation:
                # Update process details with variation specifics
                process_title = f"{process_title} - {variation['name']}"
                process_description = variation["description"]
                # Complexity might be adjusted based on variation parameters
                if "complexity" in variation["parameters"]:
                    complexity = variation["parameters"]["complexity"]
        
        # Convert complexity string to numeric score for pattern selection
        complexity_score = {
            "simple": 3,
            "medium": 5,
            "complex": 7,
            "very_complex": 9
        }.get(complexity, 5)
        
        # Get the appropriate SOP pattern based on the process characteristics
        pattern = get_pattern_for_task(process_title, process_description, complexity_score)
        
        # Determine the pattern type from the pattern
        pattern_type = None
        if "design" in pattern["title"].lower() or any(keyword in (process_title + " " + process_description).lower() for keyword in ["design", "architect", "structure", "model"]) or complexity_score >= 7:
            pattern_type = "design"
        elif "implement" in pattern["title"].lower() or any(keyword in (process_title + " " + process_description).lower() for keyword in ["implement", "build", "develop", "code", "create"]):
            pattern_type = "implementation"
        elif "test" in pattern["title"].lower() or any(keyword in (process_title + " " + process_description).lower() for keyword in ["test", "verify", "validate", "quality"]):
            pattern_type = "testing"
        elif "analy" in pattern["title"].lower() or any(keyword in (process_title + " " + process_description).lower() for keyword in ["analyze", "assess", "evaluate", "research"]):
            pattern_type = "analysis"
        elif "integrat" in pattern["title"].lower() or any(keyword in (process_title + " " + process_description).lower() for keyword in ["integrate", "connect", "interface", "plugin"]):
            pattern_type = "integration"
        else:
            pattern_type = "implementation"  # Default
        
        # Create a specific SOP ID
        sop_id = f"{pdd_id}_{process_id}_sop"
        if variation_name:
            sop_id = f"{pdd_id}_{process_id}_{variation_name}_sop"
        
        # Create a specific SOP title that references both the pattern and the specific process
        sop_title = f"SOP for {process_title}"
        
        # Create a description that explains this is a specific implementation of a pattern
        sop_description = f"Standard Operating Procedure for implementing '{process_title}' based on the {pattern_type} pattern.\n\n"
        sop_description += f"This SOP provides specific instructions for: {process_description}\n\n"
        sop_description += f"Based on pattern: {pattern['title']}"
        
        # Create a new SOP document
        sop = SOPDocument(
            doc_id=sop_id,
            title=sop_title,
            description=sop_description,
            author=pdd.author,
            department=pdd.department,
            tags=[*pdd.tags, pattern_type, "sop"],
            steps=[]
        )
        
        # Add steps from the pattern but customize them for this specific process
        for i, step_info in enumerate(pattern["steps"]):
            # Customize step description for this specific process
            customized_description = step_info["description"]
            
            # Add process-specific details to the step description
            if "Requirements Analysis" in step_info["title"]:
                customized_description += f"\n\nFor {process_title}, focus on: {process_description}"
            elif "Core Implementation" in step_info["title"]:
                customized_description += f"\n\nImplement the specific functionality described in: {process_description}"
            elif "Component Design" in step_info["title"]:
                customized_description += f"\n\nDesign the components needed for: {process_description}"
            elif "Testing" in step_info["title"]:
                customized_description += f"\n\nTest the specific functionality of: {process_description}"
            
            # Add variation-specific details if applicable
            if variation:
                customized_description += f"\n\nThis is a variation of the base process: {variation['name']}"
                for param_key, param_value in variation["parameters"].items():
                    if param_key != "complexity":  # Skip complexity as it's used for pattern selection
                        customized_description += f"\n- {param_key}: {param_value}"
            
            step = SOPStep(
                step_id=f"step{i+1}",
                title=step_info["title"],
                description=customized_description,
                order=i+1,
                estimated_time=step_info["estimated_time"],
                prerequisites=step_info["prerequisites"],
                required_skills=step_info["required_skills"]
            )
            sop.add_step(step)
        
        # Add context information to the description
        sop.description += "\n\n## Context\n"
        sop.description += f"This SOP is derived from PDD: {pdd_id}, Process: {process_id}\n"
        sop.description += f"Complexity: {complexity}\n"
        
        if variation:
            sop.description += f"Variation: {variation['name']}\n"
        
        # Save the SOP document
        logger.info(f"Saving SOP document: {sop_id}")
        self.sop_manager.save_document(sop)
        
        return sop
    
    def convert_all_processes(self, pdd_id: str) -> List[SOPDocument]:
        """Convert all processes in a PDD to SOP documents.
        
        Args:
            pdd_id: ID of the PDD document
            
        Returns:
            List of generated SOP documents
        """
        # Load the PDD document
        pdd = self.pdd_manager.load_document(pdd_id)
        if not pdd:
            logger.error(f"PDD document not found: {pdd_id}")
            return []
        
        # Generate SOPs for all processes and their variations
        sops = []
        
        for process in pdd.processes:
            # Generate SOP for the base process
            sop = self.convert_pdd_to_sop(pdd_id, process.process_id)
            if sop:
                sops.append(sop)
            
            # Generate SOPs for each variation if any
            if process.variations:
                for variation_info in process.variations:
                    variation_name = variation_info["name"]
                    variation_sop = self.convert_pdd_to_sop(pdd_id, process.process_id, variation_name)
                    if variation_sop:
                        sops.append(variation_sop)
                        logger.info(f"Generated variation SOP: {variation_sop.doc_id}")
        
        return sops


class SOPStructureGenerator:
    """Generates SOP structure based on PDD analysis."""
    
    def generate_sop_structure(self, pdd_analysis: Dict[str, Any], process_id: str) -> Dict[str, Any]:
        """Generate SOP structure for a specific process in a PDD.
        
        Args:
            pdd_analysis: Analysis results from PDDContentAnalyzer
            process_id: ID of the process to generate SOP for
            
        Returns:
            Dictionary containing SOP structure
        """
        # Find the process in the analysis
        process_info = next(
            (p for p in pdd_analysis["processes"] if p["process_id"] == process_id),
            None
        )
        
        if not process_info:
            raise ValueError(f"Process not found in PDD analysis: {process_id}")
        
        # Create SOP structure
        sop_structure = {
            "doc_id": f"{pdd_analysis['document_id']}_{process_id}_sop",
            "title": f"SOP for {process_info['title']}",
            "description": f"Standard Operating Procedure for {process_info['title']} process from {pdd_analysis['title']}.",
            "version": "1.0",
            "status": "draft",
            "author": pdd_analysis["author"],
            "department": pdd_analysis["department"],
            "tags": pdd_analysis["tags"] + [process_id, "sop"],
            "steps": process_info["step_suggestions"],
            "related_documents": [{
                "doc_id": pdd_analysis["document_id"],
                "title": pdd_analysis["title"],
                "relationship": "derived_from"
            }]
        }
        
        return sop_structure


def generate_sop_markdown(sop: SOPDocument) -> str:
    """Generate Markdown content for an SOP document.
    
    Args:
        sop: The SOP document to generate Markdown for
        
    Returns:
        Markdown content
    """
    # Generate Markdown content
    md_content = f"# {sop.title}\n\n"
    md_content += f"## Description\n{sop.description}\n\n"
    
    md_content += "## Metadata\n"
    md_content += f"- Version: {sop.version}\n"
    md_content += f"- Status: {sop.status.value}\n"
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
            # Convert prerequisites like "step1" to the correct format
            prereq_id = prereq
            md_content += f"    {prereq_id} --> step{step.order}\n"
    
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

def save_sop_as_markdown(sop: SOPDocument, output_dir: str) -> str:
    """Save an SOP document as Markdown.
    
    Args:
        sop: The SOP document to save
        output_dir: Directory to save the Markdown file
        
    Returns:
        Path to the saved Markdown file
    """
    # Create the output directory if it doesn't exist
    Path(output_dir).mkdir(exist_ok=True)
    
    # Generate Markdown content
    md_content = generate_sop_markdown(sop)
    
    # Save to file
    md_path = os.path.join(output_dir, f"{sop.doc_id}.md")
    with open(md_path, "w") as f:
        f.write(md_content)
    
    return md_path

# CLI command implementation
async def convert_pdd_to_sop_command(
    pdd_id: str,
    process_id: Optional[str] = None,
    pdd_dir: str = "pdds",
    sop_dir: str = "sops",
    pattern_type: Optional[str] = None,
    variation: Optional[str] = None
) -> None:
    """CLI command to convert a PDD document to SOP documents.
    
    Args:
        pdd_id: ID of the PDD document to convert
        process_id: Optional ID of a specific process to convert
        pdd_dir: Directory containing PDD documents
        sop_dir: Directory to store SOP documents
        pattern_type: Optional specific pattern type to use for all SOPs
        variation: Optional name of a specific variation to convert
    """
    from .ui import display_success, display_error, display_info, display_warning, create_loading_indicator
    import asyncio
    
    try:
        # Create directories if they don't exist
        Path(pdd_dir).mkdir(exist_ok=True)
        Path(sop_dir).mkdir(exist_ok=True)
        
        # Create converter
        converter = PDDToSOPConverter(pdd_dir, sop_dir)
        
        # If pattern_type is provided, modify the converter to use it
        if pattern_type:
            original_get_pattern = get_pattern_for_task
            
            # Override the pattern selection function to always return the specified pattern
            def forced_pattern(*args, **kwargs):
                return get_pattern_by_type(pattern_type)
            
            # Monkey patch the function temporarily
            import taskinator.sop_patterns
            taskinator.sop_patterns.get_pattern_for_task = forced_pattern
        
        # Create a loading indicator
        with create_loading_indicator("Converting PDD to SOP...") as progress:
            if process_id:
                # Convert a specific process
                if variation:
                    display_info(f"Converting process '{process_id}' variation '{variation}' in PDD '{pdd_id}' to SOP...")
                    sop = converter.convert_pdd_to_sop(pdd_id, process_id, variation)
                else:
                    display_info(f"Converting process '{process_id}' in PDD '{pdd_id}' to SOP...")
                    sop = converter.convert_pdd_to_sop(pdd_id, process_id)
                
                if sop:
                    display_success(f"Successfully generated SOP document: {sop.doc_id}")
                    display_info(f"Title: {sop.title}")
                    display_info(f"Steps: {len(sop.steps)}")
                    
                    # Generate step flow diagram
                    display_info("Step flow:")
                    for step in sorted(sop.steps, key=lambda s: s.order):
                        prereqs = f" (prereqs: {', '.join(step.prerequisites)})" if step.prerequisites else ""
                        display_info(f"  - Step {step.order}: {step.title}{prereqs}")
                else:
                    display_error(f"Failed to generate SOP for process '{process_id}'")
            else:
                # Convert all processes
                display_info(f"Converting all processes in PDD '{pdd_id}' to SOPs...")
                
                # Load the PDD to get all processes
                from .pdd_document import PDDDocumentManager
                pdd_manager = PDDDocumentManager(pdd_dir)
                pdd = pdd_manager.load_document(pdd_id)
                
                if not pdd:
                    display_error(f"PDD document not found: {pdd_id}")
                    return
                
                # Generate SOPs for all processes and their variations
                sops = []
                
                for process in pdd.processes:
                    # Generate SOP for the base process
                    sop = converter.convert_pdd_to_sop(pdd_id, process.process_id)
                    if sop:
                        sops.append(sop)
                    
                    # Generate SOPs for each variation if any
                    if process.variations:
                        for variation_info in process.variations:
                            variation_name = variation_info["name"]
                            variation_sop = converter.convert_pdd_to_sop(pdd_id, process.process_id, variation_name)
                            if variation_sop:
                                sops.append(variation_sop)
                                display_info(f"Generated variation SOP: {variation_sop.doc_id}")
                
                display_success(f"Successfully generated {len(sops)} SOP documents")
                
                # Display generated SOPs
                for sop in sops:
                    display_info(f"- {sop.doc_id}: {sop.title} ({len(sop.steps)} steps)")
                    
                    # Generate step flow for each SOP
                    for step in sorted(sop.steps, key=lambda s: s.order):
                        prereqs = f" (prereqs: {', '.join(step.prerequisites)})" if step.prerequisites else ""
                        display_info(f"  - Step {step.order}: {step.title}{prereqs}")
        
        # Restore the original pattern function if it was patched
        if pattern_type:
            taskinator.sop_patterns.get_pattern_for_task = original_get_pattern
        
    except Exception as e:
        # Restore the original pattern function if it was patched
        if pattern_type:
            import taskinator.sop_patterns
            taskinator.sop_patterns.get_pattern_for_task = original_get_pattern
            
        logger.error(f"Error converting PDD to SOP: {e}")
        display_error(f"Failed to convert PDD to SOP: {e}")
