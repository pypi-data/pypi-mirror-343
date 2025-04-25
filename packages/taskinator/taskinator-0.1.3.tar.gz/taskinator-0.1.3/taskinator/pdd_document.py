"""
Process Design Document (PDD) Support for Taskinator.

This module provides support for Process Design Document (PDD) documents,
including data models, parsing, storage, and complexity analysis.
"""

import json
import os
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Union, Any

from loguru import logger
from taskinator.utils import read_json, write_json
import json

class PDDStatus(str, Enum):
    """Status of a PDD document."""
    DRAFT = "draft"
    REVIEW = "review"
    APPROVED = "approved"
    DEPRECATED = "deprecated"
    ARCHIVED = "archived"

class PDDImplementationDifficulty(str, Enum):
    """Implementation difficulty level for a PDD process."""
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    VERY_COMPLEX = "very_complex"
    EXTREME = "extreme"

class PDDProcess:
    """A process in a PDD document."""
    
    def __init__(
        self,
        process_id: str,
        title: str,
        description: str,
        complexity: str = "medium",
        dependencies: List[str] = None,
        resources: List[str] = None,
        parameters: Dict[str, Any] = None,
        variations: List[Dict[str, Any]] = None
    ):
        """Initialize a new PDD process.
        
        Args:
            process_id: Unique identifier for the process
            title: Title of the process
            description: Description of the process
            complexity: Complexity of the process (simple, medium, complex, very_complex)
            dependencies: List of process IDs that this process depends on
            resources: List of resources required for this process
            parameters: Dictionary of parameters for this process
            variations: List of variations of this process
        """
        self.process_id = process_id
        self.title = title
        self.description = description
        self.complexity = complexity
        self.dependencies = dependencies or []
        self.resources = resources or []
        self.parameters = parameters or {}
        self.variations = variations or []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the process to a dictionary.
        
        Returns:
            Dictionary representation of the process
        """
        return {
            "process_id": self.process_id,
            "title": self.title,
            "description": self.description,
            "complexity": self.complexity,
            "dependencies": self.dependencies,
            "resources": self.resources,
            "parameters": self.parameters,
            "variations": self.variations
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PDDProcess":
        """Create a process from a dictionary.
        
        Args:
            data: Dictionary representation of the process
            
        Returns:
            PDDProcess object
        """
        return cls(
            process_id=data.get("process_id", ""),
            title=data.get("title", ""),
            description=data.get("description", ""),
            complexity=data.get("complexity", "medium"),
            dependencies=data.get("dependencies", []),
            resources=data.get("resources", []),
            parameters=data.get("parameters", {}),
            variations=data.get("variations", [])
        )
    
    def add_variation(self, name: str, description: str, parameters: Dict[str, Any] = None) -> None:
        """Add a variation of this process.
        
        Args:
            name: Name of the variation
            description: Description of the variation
            parameters: Parameters specific to this variation
        """
        variation = {
            "name": name,
            "description": description,
            "parameters": parameters or {}
        }
        self.variations.append(variation)

class PDDDocument:
    """Represents a Process Design Document."""
    
    def __init__(self,
                 doc_id: str,
                 title: str,
                 description: str,
                 version: str = "1.0",
                 status: PDDStatus = PDDStatus.DRAFT,
                 author: Optional[str] = None,
                 created_date: Optional[str] = None,
                 updated_date: Optional[str] = None,
                 department: Optional[str] = None,
                 tags: Optional[List[str]] = None,
                 processes: Optional[List[PDDProcess]] = None,
                 references: Optional[List[str]] = None,
                 attachments: Optional[List[str]] = None,
                 business_objectives: Optional[List[str]] = None,
                 success_criteria: Optional[List[str]] = None,
                 assumptions: Optional[List[str]] = None,
                 constraints: Optional[List[str]] = None):
        """Initialize a new PDD document.
        
        Args:
            doc_id: Unique identifier for the document
            title: Document title
            description: Document description
            version: Document version
            status: Document status
            author: Document author
            created_date: Document creation date
            updated_date: Document last update date
            department: Department responsible for the document
            tags: List of tags
            processes: List of processes
            references: List of reference documents
            attachments: List of attachments
            business_objectives: List of business objectives
            success_criteria: List of success criteria
            assumptions: List of assumptions
            constraints: List of constraints
        """
        self.doc_id = doc_id
        self.title = title
        self.description = description
        self.version = version
        self.status = status
        self.author = author
        self.created_date = created_date or datetime.now().isoformat()
        self.updated_date = updated_date or self.created_date
        self.department = department
        self.tags = tags or []
        self.processes = processes or []
        self.references = references or []
        self.attachments = attachments or []
        self.business_objectives = business_objectives or []
        self.success_criteria = success_criteria or []
        self.assumptions = assumptions or []
        self.constraints = constraints or []
    
    def add_process(self, process: PDDProcess) -> None:
        """Add a process to the document.
        
        Args:
            process: Process to add
        """
        self.processes.append(process)
        self.processes.sort(key=lambda p: p.process_id)
    
    def remove_process(self, process_id: str) -> bool:
        """Remove a process from the document.
        
        Args:
            process_id: ID of the process to remove
            
        Returns:
            True if the process was removed, False otherwise
        """
        for i, process in enumerate(self.processes):
            if process.process_id == process_id:
                self.processes.pop(i)
                return True
        return False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the document to a dictionary.
        
        Returns:
            Dictionary representation of the document
        """
        return {
            "id": self.doc_id,
            "title": self.title,
            "description": self.description,
            "version": self.version,
            "status": self.status.value,
            "author": self.author,
            "createdDate": self.created_date,
            "updatedDate": self.updated_date,
            "department": self.department,
            "tags": self.tags,
            "processes": [process.to_dict() for process in self.processes],
            "references": self.references,
            "attachments": self.attachments,
            "businessObjectives": self.business_objectives,
            "successCriteria": self.success_criteria,
            "assumptions": self.assumptions,
            "constraints": self.constraints
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PDDDocument':
        """Create a document from a dictionary.
        
        Args:
            data: Dictionary representation of the document
            
        Returns:
            New PDDDocument instance
        """
        # Parse processes
        processes = []
        for process_data in data.get("processes", []):
            processes.append(PDDProcess.from_dict(process_data))
        
        # Parse status
        status = PDDStatus.DRAFT
        if data.get("status"):
            try:
                status = PDDStatus(data.get("status"))
            except ValueError:
                logger.warning(f"Invalid status: {data.get('status')}")
        
        return cls(
            doc_id=data.get("id", ""),
            title=data.get("title", ""),
            description=data.get("description", ""),
            version=data.get("version", "1.0"),
            status=status,
            author=data.get("author"),
            created_date=data.get("createdDate"),
            updated_date=data.get("updatedDate"),
            department=data.get("department"),
            tags=data.get("tags", []),
            processes=processes,
            references=data.get("references", []),
            attachments=data.get("attachments", []),
            business_objectives=data.get("businessObjectives", []),
            success_criteria=data.get("successCriteria", []),
            assumptions=data.get("assumptions", []),
            constraints=data.get("constraints", [])
        )

    def generate_mermaid_diagram(self) -> str:
        """Generate a Mermaid flowchart diagram representing the document processes.
        
        Returns:
            Mermaid diagram as a string
        """
        # Start building the Mermaid diagram
        mermaid = "```mermaid\nflowchart TD\n"
        
        # Add title as a comment
        mermaid += f"    %% {self.title}\n"
        
        # Add nodes for each process - using only basic rectangular nodes
        for process in self.processes:
            process_id = process.process_id
            complexity = process.complexity
            
            # Add complexity level to the title for all processes
            title = f"{process.title} ({complexity})"
            
            # Use only simple rectangular nodes for all processes
            mermaid += f"    {process_id}[\"{title}\"]\n"
        
        # Add connections based on dependencies
        for process in self.processes:
            for dep in process.dependencies:
                mermaid += f"    {dep} --> {process.process_id}\n"
        
        # Close the diagram
        mermaid += "```"
        
        return mermaid
    
    def to_markdown(self) -> str:
        """Convert the document to a Markdown format.
        
        Returns:
            Markdown representation of the document
        """
        # Generate Markdown content
        md_content = f"# {self.title}\n\n"
        md_content += f"## Description\n{self.description}\n\n"
        
        md_content += "## Metadata\n"
        md_content += f"- Version: {self.version}\n"
        md_content += f"- Status: {self.status.value}\n"
        
        if self.author:
            md_content += f"- Author: {self.author}\n"
        if self.department:
            md_content += f"- Department: {self.department}\n"
        if self.tags:
            md_content += f"- Tags: {', '.join(self.tags)}\n"
        
        md_content += "\n"
        
        # Add process diagram
        md_content += "## Process Flow Diagram\n\n"
        md_content += self.generate_mermaid_diagram() + "\n\n"
        
        # Add business objectives if present
        if self.business_objectives:
            md_content += "## Business Objectives\n"
            for objective in self.business_objectives:
                md_content += f"- {objective}\n"
            md_content += "\n"
        
        # Add success criteria if present
        if self.success_criteria:
            md_content += "## Success Criteria\n"
            for criteria in self.success_criteria:
                md_content += f"- {criteria}\n"
            md_content += "\n"
        
        # Add assumptions if present
        if self.assumptions:
            md_content += "## Assumptions\n"
            for assumption in self.assumptions:
                md_content += f"- {assumption}\n"
            md_content += "\n"
        
        # Add constraints if present
        if self.constraints:
            md_content += "## Constraints\n"
            for constraint in self.constraints:
                md_content += f"- {constraint}\n"
            md_content += "\n"
        
        # Add detailed process descriptions
        md_content += "## Processes\n"
        for process in sorted(self.processes, key=lambda p: p.process_id):
            md_content += f"### Process {process.process_id}: {process.title}\n"
            md_content += f"Description: {process.description}\n"
            md_content += f"Complexity: {process.complexity}\n"
            
            if process.dependencies:
                md_content += f"Dependencies: {', '.join(process.dependencies)}\n"
            
            if process.resources:
                md_content += "Resources:\n"
                for resource in process.resources:
                    md_content += f"- {resource}\n"
            
            if process.parameters:
                md_content += "Parameters:\n"
                for key, value in process.parameters.items():
                    md_content += f"- {key}: {value}\n"
            
            if process.variations:
                md_content += "Variations:\n"
                for variation in process.variations:
                    md_content += f"- {variation['name']}: {variation['description']}\n"
                    if variation['parameters']:
                        md_content += "  Parameters:\n"
                        for key, value in variation['parameters'].items():
                            md_content += f"    - {key}: {value}\n"
            
            md_content += "\n"
        
        # Add references if present
        if self.references:
            md_content += "## References\n"
            for reference in self.references:
                md_content += f"- {reference}\n"
            md_content += "\n"
        
        # Add attachments if present
        if self.attachments:
            md_content += "## Attachments\n"
            for attachment in self.attachments:
                md_content += f"- {attachment}\n"
        
        return md_content

class PDDDocumentManager:
    """Manages PDD documents, including storage, retrieval, and analysis."""
    
    def __init__(self, pdd_dir: str = "pdds"):
        """Initialize the PDD document manager.
        
        Args:
            pdd_dir: Directory to store PDD documents
        """
        self.pdd_dir = pdd_dir
        self._ensure_directory_exists()
    
    def _ensure_directory_exists(self) -> None:
        """Ensure the PDD document directory exists."""
        os.makedirs(self.pdd_dir, exist_ok=True)
    
    def _get_document_path(self, doc_id: str) -> str:
        """Get the file path for a document.
        
        Args:
            doc_id: Document ID
            
        Returns:
            Path to the document file
        """
        return os.path.join(self.pdd_dir, f"{doc_id}.json")
    
    def save_document(self, document: PDDDocument) -> bool:
        """Save a document to storage.
        
        Args:
            document: Document to save
            
        Returns:
            True if successful, False otherwise
        """
        try:
            document.updated_date = datetime.now().isoformat()
            file_path = self._get_document_path(document.doc_id)
            write_json(file_path, document.to_dict())
            logger.info(f"Saved PDD document {document.doc_id} to {file_path}")
            return True
        except Exception as e:
            logger.error(f"Error saving PDD document {document.doc_id}: {e}")
            return False
    
    def load_document(self, doc_id: str) -> Optional[PDDDocument]:
        """Load a document from storage.
        
        Args:
            doc_id: Document ID
            
        Returns:
            Loaded document or None if not found
        """
        try:
            file_path = self._get_document_path(doc_id)
            if not os.path.exists(file_path):
                logger.warning(f"PDD document {doc_id} not found at {file_path}")
                return None
            
            data = json.loads(file_path)
            document = PDDDocument.from_dict(data)
            logger.info(f"Loaded PDD document {doc_id} from {file_path}")
            return document
        except Exception as e:
            logger.error(f"Error loading PDD document {doc_id}: {e}")
            return None
    
    def delete_document(self, doc_id: str) -> bool:
        """Delete a document from storage.
        
        Args:
            doc_id: Document ID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            file_path = self._get_document_path(doc_id)
            if not os.path.exists(file_path):
                logger.warning(f"PDD document {doc_id} not found at {file_path}")
                return False
            
            os.remove(file_path)
            logger.info(f"Deleted PDD document {doc_id} from {file_path}")
            return True
        except Exception as e:
            logger.error(f"Error deleting PDD document {doc_id}: {e}")
            return False
    
    def list_documents(self) -> List[Dict[str, Any]]:
        """List all available documents.
        
        Returns:
            List of document metadata dictionaries
        """
        self._ensure_directory_exists()
        documents = []
        
        for file_name in os.listdir(self.pdd_dir):
            if file_name.endswith(".json"):
                file_path = os.path.join(self.pdd_dir, file_name)
                pdddata = read_json(file_path)
                for data in pdddata['processes']:
                    # Include only metadata, not the full document
                    documents.append({
                        "id": data.get("process_id", ""),
                        "title": data.get("title", ""),
                        "complexity": data.get("complexity", ""),
                        "dependencies": data.get("dependencies", "")
                    })
        
        return documents
