"""
Unit tests for SOP document parser.
"""

import unittest
import sys
import os
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add the parent directory to the path so we can import the taskinator module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from taskinator.sop_parser import (
    SOPParserBase,
    MarkdownSOPParser,
    YAMLSOPParser,
    TextSOPParser,
    SOPParserFactory
)
from taskinator.sop_document import SOPDocument, SOPStep, SOPStatus, SOPAudienceLevel

class TestMarkdownSOPParser(unittest.TestCase):
    """Test cases for MarkdownSOPParser class."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.parser = MarkdownSOPParser()
        
        # Create a test Markdown file
        self.test_file_path = os.path.join(self.temp_dir, "test_sop.md")
        with open(self.test_file_path, "w") as f:
            f.write("""# Test SOP Document

## Description
This is a test SOP document for unit testing.

## Metadata
- Version: 1.0
- Status: draft
- Author: Test Author
- Department: Test Department
- Audience: intermediate
- Tags: test, markdown, parser

## Steps

### 1. First Step
This is the first step in the procedure.

#### Prerequisites
- Basic knowledge of the system
- Access credentials

#### Required Skills
- Python programming
- Testing knowledge

#### Estimated Time
30 minutes

### 2. Second Step
This is the second step in the procedure.

#### Prerequisites
- Completion of step 1

#### Required Skills
- Debugging skills

#### Estimated Time
15 minutes

## References
- Reference document 1
- Reference document 2

## Attachments
- attachment1.pdf
- attachment2.png
""")
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir)
    
    def test_parse(self):
        """Test parsing a Markdown SOP document."""
        document = self.parser.parse(self.test_file_path)
        
        self.assertIsNotNone(document)
        self.assertEqual(document.title, "Test SOP Document")
        self.assertEqual(document.description.strip(), "This is a test SOP document for unit testing.")
        self.assertEqual(document.version, "1.0")
        self.assertEqual(document.status, SOPStatus.DRAFT)
        self.assertEqual(document.author, "Test Author")
        self.assertEqual(document.department, "Test Department")
        self.assertEqual(document.audience_level, SOPAudienceLevel.INTERMEDIATE)
        self.assertEqual(document.tags, ["test", "markdown", "parser"])
        
        # Check steps
        self.assertEqual(len(document.steps), 2)
        
        # First step
        self.assertEqual(document.steps[0].title, "First Step")
        self.assertEqual(document.steps[0].order, 1)
        self.assertEqual(document.steps[0].description.strip(), "This is the first step in the procedure.")
        self.assertEqual(document.steps[0].prerequisites, ["Basic knowledge of the system", "Access credentials"])
        self.assertEqual(document.steps[0].required_skills, ["Python programming", "Testing knowledge"])
        self.assertEqual(document.steps[0].estimated_time, "30 minutes")
        
        # Second step
        self.assertEqual(document.steps[1].title, "Second Step")
        self.assertEqual(document.steps[1].order, 2)
        self.assertEqual(document.steps[1].description.strip(), "This is the second step in the procedure.")
        self.assertEqual(document.steps[1].prerequisites, ["Completion of step 1"])
        self.assertEqual(document.steps[1].required_skills, ["Debugging skills"])
        self.assertEqual(document.steps[1].estimated_time, "15 minutes")
        
        # References and attachments
        self.assertEqual(document.references, ["Reference document 1", "Reference document 2"])
        self.assertEqual(document.attachments, ["attachment1.pdf", "attachment2.png"])

class TestYAMLSOPParser(unittest.TestCase):
    """Test cases for YAMLSOPParser class."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.parser = YAMLSOPParser()
        
        # Create a test YAML file
        self.test_file_path = os.path.join(self.temp_dir, "test_sop.yaml")
        with open(self.test_file_path, "w") as f:
            f.write("""id: test_yaml_sop
title: Test YAML SOP Document
description: This is a test YAML SOP document for unit testing.
version: 1.0
status: draft
author: Test Author
department: Test Department
audienceLevel: intermediate
tags:
  - test
  - yaml
  - parser
steps:
  - id: step_1
    title: First Step
    description: This is the first step in the procedure.
    order: 1
    estimatedTime: 30 minutes
    prerequisites:
      - Basic knowledge of the system
      - Access credentials
    requiredSkills:
      - Python programming
      - Testing knowledge
    complexity: 3.5
  - id: step_2
    title: Second Step
    description: This is the second step in the procedure.
    order: 2
    estimatedTime: 15 minutes
    prerequisites:
      - Completion of step 1
    requiredSkills:
      - Debugging skills
    complexity: 2.0
references:
  - Reference document 1
  - Reference document 2
attachments:
  - attachment1.pdf
  - attachment2.png
""")
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir)
    
    def test_parse(self):
        """Test parsing a YAML SOP document."""
        document = self.parser.parse(self.test_file_path)
        
        self.assertIsNotNone(document)
        self.assertEqual(document.doc_id, "test_yaml_sop")
        self.assertEqual(document.title, "Test YAML SOP Document")
        self.assertEqual(document.description, "This is a test YAML SOP document for unit testing.")
        self.assertEqual(document.version, "1.0")
        self.assertEqual(document.status, SOPStatus.DRAFT)
        self.assertEqual(document.author, "Test Author")
        self.assertEqual(document.department, "Test Department")
        self.assertEqual(document.audience_level, SOPAudienceLevel.INTERMEDIATE)
        self.assertEqual(document.tags, ["test", "yaml", "parser"])
        
        # Check steps
        self.assertEqual(len(document.steps), 2)
        
        # First step
        self.assertEqual(document.steps[0].step_id, "step_1")
        self.assertEqual(document.steps[0].title, "First Step")
        self.assertEqual(document.steps[0].order, 1)
        self.assertEqual(document.steps[0].description, "This is the first step in the procedure.")
        self.assertEqual(document.steps[0].prerequisites, ["Basic knowledge of the system", "Access credentials"])
        self.assertEqual(document.steps[0].required_skills, ["Python programming", "Testing knowledge"])
        self.assertEqual(document.steps[0].estimated_time, "30 minutes")
        self.assertEqual(document.steps[0].complexity, 3.5)
        
        # Second step
        self.assertEqual(document.steps[1].step_id, "step_2")
        self.assertEqual(document.steps[1].title, "Second Step")
        self.assertEqual(document.steps[1].order, 2)
        self.assertEqual(document.steps[1].description, "This is the second step in the procedure.")
        self.assertEqual(document.steps[1].prerequisites, ["Completion of step 1"])
        self.assertEqual(document.steps[1].required_skills, ["Debugging skills"])
        self.assertEqual(document.steps[1].estimated_time, "15 minutes")
        self.assertEqual(document.steps[1].complexity, 2.0)
        
        # References and attachments
        self.assertEqual(document.references, ["Reference document 1", "Reference document 2"])
        self.assertEqual(document.attachments, ["attachment1.pdf", "attachment2.png"])

class TestTextSOPParser(unittest.TestCase):
    """Test cases for TextSOPParser class."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.parser = TextSOPParser()
        
        # Create a test text file
        self.test_file_path = os.path.join(self.temp_dir, "test_sop.txt")
        with open(self.test_file_path, "w") as f:
            f.write("""TITLE: Test Text SOP Document
DESCRIPTION: This is a test text SOP document for unit testing.
VERSION: 1.0
STATUS: draft
AUTHOR: Test Author
DEPARTMENT: Test Department
AUDIENCE: intermediate
TAGS: test, text, parser

STEP 1: First Step
This is the first step in the procedure.

PREREQUISITES:
- Basic knowledge of the system
- Access credentials

REQUIRED SKILLS:
- Python programming
- Testing knowledge

ESTIMATED TIME: 30 minutes

STEP 2: Second Step
This is the second step in the procedure.

PREREQUISITES:
- Completion of step 1

REQUIRED SKILLS:
- Debugging skills

ESTIMATED TIME: 15 minutes

REFERENCES:
- Reference document 1
- Reference document 2

ATTACHMENTS:
- attachment1.pdf
- attachment2.png
""")
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir)
    
    def test_parse(self):
        """Test parsing a text SOP document."""
        document = self.parser.parse(self.test_file_path)
        
        self.assertIsNotNone(document)
        self.assertEqual(document.title, "Test Text SOP Document")
        self.assertEqual(document.description, "This is a test text SOP document for unit testing.")
        self.assertEqual(document.version, "1.0")
        self.assertEqual(document.status, SOPStatus.DRAFT)
        self.assertEqual(document.author, "Test Author")
        self.assertEqual(document.department, "Test Department")
        self.assertEqual(document.audience_level, SOPAudienceLevel.INTERMEDIATE)
        self.assertEqual(document.tags, ["test", "text", "parser"])
        
        # Check steps
        self.assertEqual(len(document.steps), 2)
        
        # First step
        self.assertEqual(document.steps[0].title, "First Step")
        self.assertEqual(document.steps[0].order, 1)
        self.assertEqual(document.steps[0].description.strip(), "This is the first step in the procedure.")
        self.assertEqual(document.steps[0].prerequisites, ["Basic knowledge of the system", "Access credentials"])
        self.assertEqual(document.steps[0].required_skills, ["Python programming", "Testing knowledge"])
        self.assertEqual(document.steps[0].estimated_time, "30 minutes")
        
        # Second step
        self.assertEqual(document.steps[1].title, "Second Step")
        self.assertEqual(document.steps[1].order, 2)
        self.assertEqual(document.steps[1].description.strip(), "This is the second step in the procedure.")
        self.assertEqual(document.steps[1].prerequisites, ["Completion of step 1"])
        self.assertEqual(document.steps[1].required_skills, ["Debugging skills"])
        self.assertEqual(document.steps[1].estimated_time, "15 minutes")
        
        # References and attachments
        self.assertEqual(document.references, ["Reference document 1", "Reference document 2"])
        self.assertEqual(document.attachments, ["attachment1.pdf", "attachment2.png"])

class TestSOPParserFactory(unittest.TestCase):
    """Test cases for SOPParserFactory class."""
    
    def test_get_parser(self):
        """Test getting the appropriate parser for different file types."""
        # Markdown files
        parser = SOPParserFactory.get_parser("test.md")
        self.assertIsInstance(parser, MarkdownSOPParser)
        
        parser = SOPParserFactory.get_parser("test.markdown")
        self.assertIsInstance(parser, MarkdownSOPParser)
        
        # YAML files
        parser = SOPParserFactory.get_parser("test.yml")
        self.assertIsInstance(parser, YAMLSOPParser)
        
        parser = SOPParserFactory.get_parser("test.yaml")
        self.assertIsInstance(parser, YAMLSOPParser)
        
        # Text files (default)
        parser = SOPParserFactory.get_parser("test.txt")
        self.assertIsInstance(parser, TextSOPParser)
        
        parser = SOPParserFactory.get_parser("test.unknown")
        self.assertIsInstance(parser, TextSOPParser)
    
    def test_parse(self):
        """Test parsing with the factory method."""
        with tempfile.NamedTemporaryFile(suffix=".md") as temp_file:
            # Write a simple Markdown SOP
            temp_file.write(b"# Test Document\n\n## Description\nTest description.\n")
            temp_file.flush()
            
            # Mock the MarkdownSOPParser.parse method
            with patch.object(MarkdownSOPParser, 'parse') as mock_parse:
                mock_doc = MagicMock()
                mock_parse.return_value = mock_doc
                
                # Call the factory parse method
                result = SOPParserFactory.parse(temp_file.name)
                
                # Verify that the correct parser was used
                mock_parse.assert_called_once_with(temp_file.name)
                self.assertEqual(result, mock_doc)

if __name__ == '__main__':
    unittest.main()
