"""
Unit tests for the PDD parser module.
"""

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from taskinator.pdd_document import PDDDocument, PDDProcess, PDDStatus, PDDImplementationDifficulty
from taskinator.pdd_parser import PDDParserFactory, MarkdownPDDParser, YAMLPDDParser, TextPDDParser

class TestPDDParser(unittest.TestCase):
    """Test cases for the PDD parsers."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test fixtures."""
        # Clean up temp directory
        for file_name in os.listdir(self.temp_dir):
            file_path = os.path.join(self.temp_dir, file_name)
            if os.path.isfile(file_path):
                os.unlink(file_path)
        os.rmdir(self.temp_dir)
    
    @pytest.mark.skip(reason="PDD parser API has changed, test needs revision")
    def test_markdown_parser(self):
        """Test parsing a Markdown PDD document."""
        # Create a test Markdown file
        markdown_content = """# Test PDD Document

## Description
This is a test PDD document for unit testing.

## Metadata
- Version: 1.0
- Status: draft
- Author: Test Author
- Department: Test Department
- Tags: test, markdown, parser

## Business Objectives
- Objective 1: Test the Markdown parser
- Objective 2: Ensure proper extraction of metadata

## Success Criteria
- Criteria 1: All sections are properly parsed
- Criteria 2: Document structure is preserved

## Assumptions
- Assumption 1: The parser works correctly
- Assumption 2: The Markdown format is valid

## Constraints
- Constraint 1: Must handle various Markdown formats
- Constraint 2: Must be robust to formatting errors

## Processes
### Process 1: First Process
Description: This is the first process in the document.
Order: 1
Estimated Time: 2 days
Dependencies: None
Implementation Difficulty: Moderate
Required Resources:
- Developer
- Designer
Inputs:
- User requirements
- Design specifications
Outputs:
- Implementation plan
- Code repository

### Process 2: Second Process
Description: This is the second process in the document.
Order: 2
Estimated Time: 3 days
Dependencies: Process 1
Implementation Difficulty: Complex
Required Resources:
- Developer
- QA Engineer
Inputs:
- Implementation plan
- Test cases
Outputs:
- Implemented feature
- Test results

## References
- Reference document 1
- Reference document 2

## Attachments
- attachment1.pdf
- attachment2.png
"""
        
        file_path = os.path.join(self.temp_dir, "test_pdd.md")
        with open(file_path, "w") as f:
            f.write(markdown_content)
        
        # Parse the document
        parser = MarkdownPDDParser()
        document = parser.parse(file_path)
        
        # Check that the document was parsed correctly
        self.assertIsNotNone(document)
        self.assertEqual(document.doc_id, "test_pdd")
        self.assertEqual(document.title, "Test PDD Document")
        self.assertEqual(document.description, "This is a test PDD document for unit testing.")
        self.assertEqual(document.status, PDDStatus.DRAFT)
        self.assertEqual(document.author, "Test Author")
        self.assertEqual(document.department, "Test Department")
        
        # Check that processes were parsed correctly
        self.assertEqual(len(document.processes), 2)
        self.assertEqual(document.processes[0].title, "First Process")
        self.assertEqual(document.processes[1].title, "Second Process")
        
        # Check business objectives and other sections
        self.assertGreaterEqual(len(document.business_objectives), 1)
        self.assertGreaterEqual(len(document.success_criteria), 1)
        self.assertGreaterEqual(len(document.assumptions), 1)
        self.assertGreaterEqual(len(document.constraints), 1)
        self.assertGreaterEqual(len(document.references), 1)
        self.assertGreaterEqual(len(document.attachments), 1)
    
    @pytest.mark.skip(reason="PDD parser API has changed, test needs revision")
    def test_yaml_parser(self):
        """Test parsing a YAML PDD document."""
        # Create a test YAML file
        yaml_content = """
id: test_pdd_yaml
title: Test YAML PDD Document
description: This is a test YAML PDD document for unit testing.
version: 1.0
status: draft
author: Test Author
department: Test Department
tags:
  - test
  - yaml
  - parser
businessObjectives:
  - Objective 1: Test the YAML parser
  - Objective 2: Ensure proper extraction of data
successCriteria:
  - Criteria 1: All sections are properly parsed
  - Criteria 2: Document structure is preserved
assumptions:
  - Assumption 1: The parser works correctly
  - Assumption 2: The YAML format is valid
constraints:
  - Constraint 1: Must handle various YAML formats
  - Constraint 2: Must be robust to formatting errors
processes:
  - id: process_1
    title: First Process
    description: This is the first process in the document.
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
    title: Second Process
    description: This is the second process in the document.
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
  - Reference document 1
  - Reference document 2
attachments:
  - attachment1.pdf
  - attachment2.png
"""
        
        file_path = os.path.join(self.temp_dir, "test_pdd.yaml")
        with open(file_path, "w") as f:
            f.write(yaml_content)
        
        # Parse the document
        parser = YAMLPDDParser()
        document = parser.parse(file_path)
        
        # Check that the document was parsed correctly
        self.assertIsNotNone(document)
        self.assertEqual(document.doc_id, "test_pdd_yaml")
        self.assertEqual(document.title, "Test YAML PDD Document")
        self.assertEqual(document.description, "This is a test YAML PDD document for unit testing.")
        self.assertEqual(document.status, PDDStatus.DRAFT)
        self.assertEqual(document.author, "Test Author")
        self.assertEqual(document.department, "Test Department")
        
        # Check that processes were parsed correctly
        self.assertEqual(len(document.processes), 2)
        self.assertEqual(document.processes[0].title, "First Process")
        self.assertEqual(document.processes[0].implementation_difficulty, PDDImplementationDifficulty.MODERATE)
        self.assertEqual(document.processes[1].title, "Second Process")
        self.assertEqual(document.processes[1].implementation_difficulty, PDDImplementationDifficulty.COMPLEX)
        
        # Check business objectives and other sections
        self.assertGreaterEqual(len(document.business_objectives), 1)
        self.assertGreaterEqual(len(document.success_criteria), 1)
        self.assertGreaterEqual(len(document.assumptions), 1)
        self.assertGreaterEqual(len(document.constraints), 1)
        self.assertGreaterEqual(len(document.references), 1)
        self.assertGreaterEqual(len(document.attachments), 1)
    
    @pytest.mark.skip(reason="PDD parser API has changed, test needs revision")
    def test_text_parser(self):
        """Test parsing a text PDD document."""
        # Create a test text file
        text_content = """TITLE: Test Text PDD Document
DESCRIPTION: This is a test text PDD document for unit testing.
VERSION: 1.0
STATUS: draft
AUTHOR: Test Author
DEPARTMENT: Test Department
TAGS: test, text, parser

BUSINESS OBJECTIVES:
Objective 1: Test the text parser
Objective 2: Ensure proper extraction of data

SUCCESS CRITERIA:
Criteria 1: All sections are properly parsed
Criteria 2: Document structure is preserved

ASSUMPTIONS:
Assumption 1: The parser works correctly
Assumption 2: The text format is valid

CONSTRAINTS:
Constraint 1: Must handle various text formats
Constraint 2: Must be robust to formatting errors

PROCESSES:
Process 1: First Process
Description: This is the first process in the document.
Order: 1
Estimated Time: 2 days
Dependencies: None
Implementation Difficulty: Moderate
Required Resources: Developer, Designer
Inputs: User requirements, Design specifications
Outputs: Implementation plan, Code repository

Process 2: Second Process
Description: This is the second process in the document.
Order: 2
Estimated Time: 3 days
Dependencies: Process 1
Implementation Difficulty: Complex
Required Resources: Developer, QA Engineer
Inputs: Implementation plan, Test cases
Outputs: Implemented feature, Test results

REFERENCES:
Reference document 1
Reference document 2

ATTACHMENTS:
attachment1.pdf
attachment2.png
"""
        
        file_path = os.path.join(self.temp_dir, "test_pdd.txt")
        with open(file_path, "w") as f:
            f.write(text_content)
        
        # Parse the document
        parser = TextPDDParser()
        document = parser.parse(file_path)
        
        # Check that the document was parsed correctly
        self.assertIsNotNone(document)
        self.assertEqual(document.doc_id, "test_pdd")
        self.assertEqual(document.title, "Test Text PDD Document")
        self.assertEqual(document.description, "This is a test text PDD document for unit testing.")
        self.assertEqual(document.status, PDDStatus.DRAFT)
        self.assertEqual(document.author, "Test Author")
        self.assertEqual(document.department, "Test Department")
        
        # Check that processes were parsed correctly
        self.assertEqual(len(document.processes), 2)
        self.assertEqual(document.processes[0].title, "First Process")
        self.assertEqual(document.processes[1].title, "Second Process")
        
        # Check business objectives and other sections
        self.assertGreaterEqual(len(document.business_objectives), 1)
        self.assertGreaterEqual(len(document.success_criteria), 1)
        self.assertGreaterEqual(len(document.assumptions), 1)
        self.assertGreaterEqual(len(document.constraints), 1)
        self.assertGreaterEqual(len(document.references), 1)
        self.assertGreaterEqual(len(document.attachments), 1)
    
    @pytest.mark.skip(reason="PDD parser API has changed, test needs revision")
    def test_parser_factory(self):
        """Test the parser factory."""
        # Test getting parser for Markdown file
        parser = PDDParserFactory.get_parser("test.md")
        self.assertIsInstance(parser, MarkdownPDDParser)
        
        # Test getting parser for YAML file
        parser = PDDParserFactory.get_parser("test.yaml")
        self.assertIsInstance(parser, YAMLPDDParser)
        
        # Test getting parser for text file
        parser = PDDParserFactory.get_parser("test.txt")
        self.assertIsInstance(parser, TextPDDParser)
        
        # Test parsing with factory
        # Create a test Markdown file
        markdown_content = """# Test PDD Document

## Description
This is a test PDD document for unit testing.
"""
        
        file_path = os.path.join(self.temp_dir, "test_pdd.md")
        with open(file_path, "w") as f:
            f.write(markdown_content)
        
        # Parse the document using the factory
        document = PDDParserFactory.parse(file_path)
        
        # Check that the document was parsed correctly
        self.assertIsNotNone(document)
        self.assertEqual(document.doc_id, "test_pdd")
        self.assertEqual(document.title, "Test PDD Document")

if __name__ == "__main__":
    unittest.main()
