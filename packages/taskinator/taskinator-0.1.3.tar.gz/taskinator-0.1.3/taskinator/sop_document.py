"""
SOP Document Support for Taskinator.

This module provides support for Standard Operating Procedure (SOP) documents,
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

class SOPStatus(str, Enum):
    """Status of an SOP document."""
    DRAFT = "draft"
    REVIEW = "review"
    APPROVED = "approved"
    DEPRECATED = "deprecated"
    ARCHIVED = "archived"

class SOPAudienceLevel(str, Enum):
    """Target audience skill level for an SOP."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

class SOPStep:
    """Represents a single step in an SOP document."""
    
    def __init__(self, 
                 step_id: str,
                 title: str,
                 description: str,
                 order: int,
                 estimated_time: Optional[str] = None,
                 prerequisites: Optional[List[str]] = None,
                 complexity: Optional[float] = None,
                 required_skills: Optional[List[str]] = None):
        """Initialize a new SOP step.
        
        Args:
            step_id: Unique identifier for the step
            title: Step title
            description: Detailed description of the step
            order: Order of the step in the procedure
            estimated_time: Estimated time to complete the step
            prerequisites: List of prerequisite steps or knowledge
            complexity: Complexity score (1-5)
            required_skills: List of skills required for this step
        """
        self.step_id = step_id
        self.title = title
        self.description = description
        self.order = order
        self.estimated_time = estimated_time
        self.prerequisites = prerequisites or []
        self.complexity = complexity
        self.required_skills = required_skills or []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the step to a dictionary.
        
        Returns:
            Dictionary representation of the step
        """
        return {
            "id": self.step_id,
            "title": self.title,
            "description": self.description,
            "order": self.order,
            "estimatedTime": self.estimated_time,
            "prerequisites": self.prerequisites,
            "complexity": self.complexity,
            "requiredSkills": self.required_skills
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SOPStep':
        """Create a step from a dictionary.
        
        Args:
            data: Dictionary representation of the step
            
        Returns:
            New SOPStep instance
        """
        return cls(
            step_id=data.get("id", ""),
            title=data.get("title", ""),
            description=data.get("description", ""),
            order=data.get("order", 0),
            estimated_time=data.get("estimatedTime"),
            prerequisites=data.get("prerequisites", []),
            complexity=data.get("complexity"),
            required_skills=data.get("requiredSkills", [])
        )

class SOPDocument:
    """Represents a Standard Operating Procedure document."""
    
    def __init__(self,
                 doc_id: str,
                 title: str,
                 description: str,
                 version: str = "1.0",
                 status: SOPStatus = SOPStatus.DRAFT,
                 author: Optional[str] = None,
                 created_date: Optional[str] = None,
                 updated_date: Optional[str] = None,
                 audience_level: SOPAudienceLevel = SOPAudienceLevel.INTERMEDIATE,
                 department: Optional[str] = None,
                 tags: Optional[List[str]] = None,
                 steps: Optional[List[SOPStep]] = None,
                 references: Optional[List[str]] = None,
                 attachments: Optional[List[str]] = None):
        """Initialize a new SOP document.
        
        Args:
            doc_id: Unique identifier for the document
            title: Document title
            description: Document description
            version: Document version
            status: Document status
            author: Document author
            created_date: Creation date (ISO format)
            updated_date: Last update date (ISO format)
            audience_level: Target audience skill level
            department: Department responsible for the SOP
            tags: List of tags for categorization
            steps: List of procedure steps
            references: List of reference documents
            attachments: List of attachment files
        """
        self.doc_id = doc_id
        self.title = title
        self.description = description
        self.version = version
        self.status = status
        self.author = author
        self.created_date = created_date or datetime.now().isoformat()
        self.updated_date = updated_date or self.created_date
        self.audience_level = audience_level
        self.department = department
        self.tags = tags or []
        self.steps = steps or []
        self.references = references or []
        self.attachments = attachments or []
    
    def add_step(self, step: SOPStep) -> None:
        """Add a step to the document.
        
        Args:
            step: Step to add
        """
        self.steps.append(step)
        self.steps.sort(key=lambda s: s.order)
        self.updated_date = datetime.now().isoformat()
    
    def remove_step(self, step_id: str) -> bool:
        """Remove a step from the document.
        
        Args:
            step_id: ID of the step to remove
            
        Returns:
            True if the step was removed, False otherwise
        """
        initial_length = len(self.steps)
        self.steps = [s for s in self.steps if s.step_id != step_id]
        
        if len(self.steps) < initial_length:
            self.updated_date = datetime.now().isoformat()
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
            "audienceLevel": self.audience_level.value,
            "department": self.department,
            "tags": self.tags,
            "steps": [step.to_dict() for step in self.steps],
            "references": self.references,
            "attachments": self.attachments
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SOPDocument':
        """Create a document from a dictionary.
        
        Args:
            data: Dictionary representation of the document
            
        Returns:
            New SOPDocument instance
        """
        steps = [SOPStep.from_dict(step_data) for step_data in data.get("steps", [])]
        
        return cls(
            doc_id=data.get("id", ""),
            title=data.get("title", ""),
            description=data.get("description", ""),
            version=data.get("version", "1.0"),
            status=SOPStatus(data.get("status", SOPStatus.DRAFT.value)),
            author=data.get("author"),
            created_date=data.get("createdDate"),
            updated_date=data.get("updatedDate"),
            audience_level=SOPAudienceLevel(data.get("audienceLevel", SOPAudienceLevel.INTERMEDIATE.value)),
            department=data.get("department"),
            tags=data.get("tags", []),
            steps=steps,
            references=data.get("references", []),
            attachments=data.get("attachments", [])
        )

class SOPDocumentManager:
    """Manages SOP documents, including storage, retrieval, and analysis."""
    
    def __init__(self, sop_dir: str = "sops"):
        """Initialize the SOP document manager.
        
        Args:
            sop_dir: Directory to store SOP documents
        """
        self.sop_dir = sop_dir
        self._ensure_directory_exists()
    
    def _ensure_directory_exists(self) -> None:
        """Ensure the SOP document directory exists."""
        os.makedirs(self.sop_dir, exist_ok=True)
    
    def _get_document_path(self, doc_id: str) -> str:
        """Get the file path for a document.
        
        Args:
            doc_id: Document ID
            
        Returns:
            Path to the document file
        """
        return os.path.join(self.sop_dir, f"{doc_id}.json")
    
    def save_document(self, document: SOPDocument) -> bool:
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
            logger.info(f"Saved SOP document {document.doc_id} to {file_path}")
            return True
        except Exception as e:
            logger.error(f"Error saving SOP document {document.doc_id}: {e}")
            return False
    
    def load_document(self, doc_id: str) -> Optional[SOPDocument]:
        """Load a document from storage.
        
        Args:
            doc_id: Document ID
            
        Returns:
            Loaded document or None if not found
        """
        try:
            file_path = self._get_document_path(doc_id)
            if not os.path.exists(file_path):
                logger.warning(f"SOP document {doc_id} not found at {file_path}")
                return None
            
            data = read_json(file_path)
            document = SOPDocument.from_dict(data)
            logger.info(f"Loaded SOP document {doc_id} from {file_path}")
            return document
        except Exception as e:
            logger.error(f"Error loading SOP document {doc_id}: {e}")
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
                logger.warning(f"SOP document {doc_id} not found at {file_path}")
                return False
            
            os.remove(file_path)
            logger.info(f"Deleted SOP document {doc_id} from {file_path}")
            return True
        except Exception as e:
            logger.error(f"Error deleting SOP document {doc_id}: {e}")
            return False
    
    def list_documents(self) -> List[Dict[str, Any]]:
        """List all available documents.
        
        Returns:
            List of document metadata dictionaries
        """
        try:
            self._ensure_directory_exists()
            documents = []
            
            for file_name in os.listdir(self.sop_dir):
                if file_name.endswith(".json"):
                    file_path = os.path.join(self.sop_dir, file_name)
                    try:
                        data = read_json(file_path)
                        # Include only metadata, not the full document
                        documents.append({
                            "id": data.get("id", ""),
                            "title": data.get("title", ""),
                            "version": data.get("version", ""),
                            "status": data.get("status", ""),
                            "author": data.get("author", ""),
                            "updatedDate": data.get("updatedDate", "")
                        })
                    except Exception as e:
                        logger.error(f"Error reading SOP document {file_name}: {e}")
            
            return documents
        except Exception as e:
            logger.error(f"Error listing SOP documents: {e}")
            return []
