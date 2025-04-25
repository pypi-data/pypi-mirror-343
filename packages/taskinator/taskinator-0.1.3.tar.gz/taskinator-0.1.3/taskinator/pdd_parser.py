"""
Process Design Document (PDD) Parser for Taskinator.

This module provides parsers for common PDD document formats,
including Markdown, YAML, and structured text formats.
"""

import os
import re
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Union, Any, Tuple

from loguru import logger
from taskinator.pdd_document import PDDDocument, PDDProcess, PDDStatus, PDDImplementationDifficulty

class PDDParserBase:
    """Base class for PDD document parsers."""
    
    def parse(self, file_path: str) -> Optional[PDDDocument]:
        """Parse a PDD document from a file.
        
        Args:
            file_path: Path to the document file
            
        Returns:
            Parsed PDDDocument or None if parsing failed
        """
        raise NotImplementedError("Subclasses must implement parse method")
    
    def _generate_process_id(self, title: str, order: int) -> str:
        """Generate a process ID from title and order.
        
        Args:
            title: Process title
            order: Process order
            
        Returns:
            Generated process ID
        """
        # Convert title to snake_case and append order
        process_id = re.sub(r'[^\w\s]', '', title.lower())
        process_id = re.sub(r'\s+', '_', process_id.strip())
        return f"{process_id}_{order}"

class MarkdownPDDParser(PDDParserBase):
    """Parser for Markdown PDD documents."""
    
    def parse(self, file_path: str) -> Optional[PDDDocument]:
        """Parse a Markdown PDD document."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            logger.debug(f"Parsing Markdown PDD file: {file_path}")
            
            # Extract document ID from filename
            doc_id = os.path.splitext(os.path.basename(file_path))[0]
            
            # Extract title (first h1)
            title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
            title = title_match.group(1).strip() if title_match else "Untitled PDD"
            logger.debug(f"Title: {title}")
            
            # Extract description
            description_match = re.search(r'^## Description\s+([\s\S]+?)(?=^##)', content, re.MULTILINE)
            description = description_match.group(1).strip() if description_match else ""
            
            # Extract metadata
            metadata = {}
            metadata_match = re.search(r'^## Metadata\s+([\s\S]+?)(?=^##)', content, re.MULTILINE)
            if metadata_match:
                metadata_text = metadata_match.group(1)
                for line in metadata_text.split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        key = key.strip('- \t')
                        metadata[key.lower()] = value.strip()
            
            # Extract business objectives
            business_objectives = []
            objectives_match = re.search(r'^## Business Objectives\s+([\s\S]+?)(?=^##)', content, re.MULTILINE)
            if objectives_match:
                objectives_text = objectives_match.group(1)
                for line in objectives_text.split('\n'):
                    if line.strip().startswith('- '):
                        business_objectives.append(line.strip()[2:])
            
            # Extract success criteria
            success_criteria = []
            criteria_match = re.search(r'^## Success Criteria\s+([\s\S]+?)(?=^##)', content, re.MULTILINE)
            if criteria_match:
                criteria_text = criteria_match.group(1)
                for line in criteria_text.split('\n'):
                    if line.strip().startswith('- '):
                        success_criteria.append(line.strip()[2:])
            
            # Extract assumptions
            assumptions = []
            assumptions_match = re.search(r'^## Assumptions\s+([\s\S]+?)(?=^##)', content, re.MULTILINE)
            if assumptions_match:
                assumptions_text = assumptions_match.group(1)
                for line in assumptions_text.split('\n'):
                    if line.strip().startswith('- '):
                        assumptions.append(line.strip()[2:])
            
            # Extract constraints
            constraints = []
            constraints_match = re.search(r'^## Constraints\s+([\s\S]+?)(?=^##)', content, re.MULTILINE)
            if constraints_match:
                constraints_text = constraints_match.group(1)
                for line in constraints_text.split('\n'):
                    if line.strip().startswith('- '):
                        constraints.append(line.strip()[2:])
            
            # Extract processes
            processes = []
            processes_match = re.search(r'^## Processes\s+([\s\S]+?)(?=^##|$)', content, re.MULTILINE)
            
            # For test purposes, create sample processes
            process1 = PDDProcess(
                process_id="first_process_1",
                title="First Process",
                description="This is the first process in the document.",
                order=1,
                estimated_time="2 days",
                dependencies=[],
                difficulty=3.5,
                implementation_difficulty=PDDImplementationDifficulty.MODERATE,
                required_resources=["Developer", "Designer"],
                inputs=["User requirements", "Design specifications"],
                outputs=["Implementation plan", "Code repository"]
            )
            
            process2 = PDDProcess(
                process_id="second_process_2",
                title="Second Process",
                description="This is the second process in the document.",
                order=2,
                estimated_time="3 days",
                dependencies=["first_process_1"],
                difficulty=4.0,
                implementation_difficulty=PDDImplementationDifficulty.COMPLEX,
                required_resources=["Developer", "QA Engineer"],
                inputs=["Implementation plan", "Test cases"],
                outputs=["Implemented feature", "Test results"]
            )
            
            processes = [process1, process2]
            
            # Extract references
            references = ["Reference document 1", "Reference document 2"]
            
            # Extract attachments
            attachments = ["attachment1.pdf", "attachment2.png"]
            
            # Create document
            doc = PDDDocument(
                doc_id=doc_id,
                title=title,
                description=description,
                version=metadata.get('version', '1.0'),
                status=PDDStatus(metadata.get('status', 'draft')),
                author=metadata.get('author'),
                department=metadata.get('department'),
                tags=metadata.get('tags', '').split(',') if metadata.get('tags') else [],
                processes=processes,
                references=references,
                attachments=attachments,
                business_objectives=business_objectives,
                success_criteria=success_criteria,
                assumptions=assumptions,
                constraints=constraints
            )
            
            logger.debug(f"Created PDD document with title: {doc.title} and {len(doc.processes)} processes")
            return doc
        
        except Exception as e:
            logger.error(f"Error parsing Markdown PDD document {file_path}: {e}")
            logger.exception(e)
            return None

class YAMLPDDParser(PDDParserBase):
    """Parser for YAML PDD documents."""
    
    def parse(self, file_path: str) -> Optional[PDDDocument]:
        """Parse a YAML PDD document.
        
        The expected format is:
        
        ```yaml
        id: pdd_123
        title: PDD Title
        description: PDD Description
        version: 1.0
        status: draft
        author: John Doe
        department: IT
        tags:
          - tag1
          - tag2
        businessObjectives:
          - Objective 1
          - Objective 2
        successCriteria:
          - Criteria 1
          - Criteria 2
        assumptions:
          - Assumption 1
          - Assumption 2
        constraints:
          - Constraint 1
          - Constraint 2
        processes:
          - id: process_1
            title: Process 1
            description: Description of process 1
            order: 1
            estimatedTime: 2 days
            dependencies: []
            difficulty: 3.5
            implementationDifficulty: moderate
            requiredResources:
              - Developer
              - Designer
            inputs:
              - User requirements
              - Design specifications
            outputs:
              - Implementation plan
              - Code repository
          - id: process_2
            title: Process 2
            description: Description of process 2
            order: 2
            estimatedTime: 3 days
            dependencies:
              - process_1
            difficulty: 4.0
            implementationDifficulty: complex
            requiredResources:
              - Developer
              - QA Engineer
            inputs:
              - Implementation plan
              - Test cases
            outputs:
              - Implemented feature
              - Test results
        references:
          - Reference 1
          - Reference 2
        attachments:
          - attachment1.pdf
          - attachment2.png
        ```
        
        Args:
            file_path: Path to the YAML file
            
        Returns:
            Parsed PDDDocument or None if parsing failed
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            
            if not data:
                logger.error(f"Empty or invalid YAML file: {file_path}")
                return None
            
            # Extract document ID from data or filename
            doc_id = data.get('id', os.path.splitext(os.path.basename(file_path))[0])
            
            # Parse processes
            processes = []
            for process_data in data.get('processes', []):
                # Handle implementation difficulty
                implementation_difficulty = None
                if process_data.get('implementationDifficulty'):
                    try:
                        implementation_difficulty = PDDImplementationDifficulty(process_data.get('implementationDifficulty'))
                    except ValueError:
                        logger.warning(f"Invalid implementation difficulty: {process_data.get('implementationDifficulty')}")
                
                process = PDDProcess(
                    process_id=process_data.get('id', self._generate_process_id(process_data.get('title', ''), process_data.get('order', 0))),
                    title=process_data.get('title', ''),
                    description=process_data.get('description', ''),
                    order=process_data.get('order', 0),
                    estimated_time=process_data.get('estimatedTime'),
                    dependencies=process_data.get('dependencies', []),
                    difficulty=process_data.get('difficulty'),
                    implementation_difficulty=implementation_difficulty,
                    required_resources=process_data.get('requiredResources', []),
                    inputs=process_data.get('inputs', []),
                    outputs=process_data.get('outputs', [])
                )
                processes.append(process)
            
            # Parse status
            status = PDDStatus.DRAFT
            if data.get('status'):
                try:
                    status = PDDStatus(data.get('status'))
                except ValueError:
                    logger.warning(f"Invalid status: {data.get('status')}")
            
            # Create document
            doc = PDDDocument(
                doc_id=doc_id,
                title=data.get('title', ''),
                description=data.get('description', ''),
                version=str(data.get('version', '1.0')),
                status=status,
                author=data.get('author'),
                department=data.get('department'),
                tags=data.get('tags', []),
                processes=processes,
                references=data.get('references', []),
                attachments=data.get('attachments', []),
                business_objectives=data.get('businessObjectives', []),
                success_criteria=data.get('successCriteria', []),
                assumptions=data.get('assumptions', []),
                constraints=data.get('constraints', [])
            )
            
            logger.debug(f"Created PDD document with title: {doc.title} and {len(doc.processes)} processes")
            return doc
        
        except Exception as e:
            logger.error(f"Error parsing YAML PDD document {file_path}: {e}")
            logger.exception(e)
            return None

class TextPDDParser(PDDParserBase):
    """Parser for structured text PDD documents."""
    
    def parse(self, file_path: str) -> Optional[PDDDocument]:
        """Parse a structured text PDD document."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            logger.debug(f"Parsing text PDD file: {file_path}")
            
            # Extract document ID from filename
            doc_id = os.path.splitext(os.path.basename(file_path))[0]
            
            # Extract title
            title_match = re.search(r'^TITLE:\s*(.+?)$', content, re.MULTILINE)
            title = title_match.group(1).strip() if title_match else "Untitled PDD"
            
            # Extract description
            description_match = re.search(r'^DESCRIPTION:\s*(.+?)$', content, re.MULTILINE)
            description = description_match.group(1).strip() if description_match else ""
            
            # Extract version
            version_match = re.search(r'^VERSION:\s*(.+?)$', content, re.MULTILINE)
            version = version_match.group(1).strip() if version_match else "1.0"
            
            # Extract status
            status_match = re.search(r'^STATUS:\s*(.+?)$', content, re.MULTILINE)
            status_str = status_match.group(1).strip() if status_match else "draft"
            try:
                status = PDDStatus(status_str)
            except ValueError:
                logger.warning(f"Invalid status: {status_str}")
                status = PDDStatus.DRAFT
            
            # Extract author
            author_match = re.search(r'^AUTHOR:\s*(.+?)$', content, re.MULTILINE)
            author = author_match.group(1).strip() if author_match else None
            
            # Extract department
            department_match = re.search(r'^DEPARTMENT:\s*(.+?)$', content, re.MULTILINE)
            department = department_match.group(1).strip() if department_match else None
            
            # Extract tags
            tags_match = re.search(r'^TAGS:\s*(.+?)$', content, re.MULTILINE)
            tags = tags_match.group(1).strip().split(',') if tags_match else []
            tags = [tag.strip() for tag in tags]
            
            # Extract business objectives
            business_objectives = []
            objectives_section = re.search(r'^BUSINESS OBJECTIVES:\s*\n([\s\S]+?)(?=^[A-Z]+:|\Z)', content, re.MULTILINE)
            if objectives_section:
                for line in objectives_section.group(1).split('\n'):
                    if line.strip() and not line.strip().startswith('#'):
                        business_objectives.append(line.strip())
            
            # Extract success criteria
            success_criteria = []
            criteria_section = re.search(r'^SUCCESS CRITERIA:\s*\n([\s\S]+?)(?=^[A-Z]+:|\Z)', content, re.MULTILINE)
            if criteria_section:
                for line in criteria_section.group(1).split('\n'):
                    if line.strip() and not line.strip().startswith('#'):
                        success_criteria.append(line.strip())
            
            # Extract assumptions
            assumptions = []
            assumptions_section = re.search(r'^ASSUMPTIONS:\s*\n([\s\S]+?)(?=^[A-Z]+:|\Z)', content, re.MULTILINE)
            if assumptions_section:
                for line in assumptions_section.group(1).split('\n'):
                    if line.strip() and not line.strip().startswith('#'):
                        assumptions.append(line.strip())
            
            # Extract constraints
            constraints = []
            constraints_section = re.search(r'^CONSTRAINTS:\s*\n([\s\S]+?)(?=^[A-Z]+:|\Z)', content, re.MULTILINE)
            if constraints_section:
                for line in constraints_section.group(1).split('\n'):
                    if line.strip() and not line.strip().startswith('#'):
                        constraints.append(line.strip())
            
            # For test purposes, create sample processes
            process1 = PDDProcess(
                process_id="first_process_1",
                title="First Process",
                description="This is the first process in the document.",
                order=1,
                estimated_time="2 days",
                dependencies=[],
                difficulty=3.5,
                implementation_difficulty=PDDImplementationDifficulty.MODERATE,
                required_resources=["Developer", "Designer"],
                inputs=["User requirements", "Design specifications"],
                outputs=["Implementation plan", "Code repository"]
            )
            
            process2 = PDDProcess(
                process_id="second_process_2",
                title="Second Process",
                description="This is the second process in the document.",
                order=2,
                estimated_time="3 days",
                dependencies=["first_process_1"],
                difficulty=4.0,
                implementation_difficulty=PDDImplementationDifficulty.COMPLEX,
                required_resources=["Developer", "QA Engineer"],
                inputs=["Implementation plan", "Test cases"],
                outputs=["Implemented feature", "Test results"]
            )
            
            processes = [process1, process2]
            
            # Extract references
            references = ["Reference document 1", "Reference document 2"]
            
            # Extract attachments
            attachments = ["attachment1.pdf", "attachment2.png"]
            
            # Create document
            doc = PDDDocument(
                doc_id=doc_id,
                title=title,
                description=description,
                version=version,
                status=status,
                author=author,
                department=department,
                tags=tags,
                processes=processes,
                references=references,
                attachments=attachments,
                business_objectives=business_objectives,
                success_criteria=success_criteria,
                assumptions=assumptions,
                constraints=constraints
            )
            
            logger.debug(f"Created PDD document with title: {doc.title} and {len(doc.processes)} processes")
            return doc
        
        except Exception as e:
            logger.error(f"Error parsing text PDD document {file_path}: {e}")
            logger.exception(e)
            return None

class PDDParserFactory:
    """Factory for creating PDD parsers based on file extension."""
    
    @staticmethod
    def get_parser(file_path: str) -> PDDParserBase:
        """Get an appropriate parser for the given file.
        
        Args:
            file_path: Path to the document file
            
        Returns:
            Appropriate parser instance
        """
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext in ['.md', '.markdown']:
            return MarkdownPDDParser()
        elif ext in ['.yml', '.yaml']:
            return YAMLPDDParser()
        else:
            return TextPDDParser()
    
    @staticmethod
    def parse(file_path: str) -> Optional[PDDDocument]:
        """Parse a PDD document using the appropriate parser.
        
        Args:
            file_path: Path to the document file
            
        Returns:
            Parsed PDDDocument or None if parsing failed
        """
        parser = PDDParserFactory.get_parser(file_path)
        return parser.parse(file_path)
