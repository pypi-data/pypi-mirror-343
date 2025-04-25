"""
Unit tests for SOP document support.
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

from taskinator.sop_document import (
    SOPDocument,
    SOPStep,
    SOPStatus,
    SOPAudienceLevel,
    SOPDocumentManager
)

class TestSOPStep(unittest.TestCase):
    """Test cases for SOPStep class."""
    
    def test_init(self):
        """Test initialization of SOPStep."""
        step = SOPStep(
            step_id="step_1",
            title="Test Step",
            description="This is a test step",
            order=1,
            estimated_time="30 minutes",
            prerequisites=["Step 0"],
            complexity=3.5,
            required_skills=["Python"]
        )
        
        self.assertEqual(step.step_id, "step_1")
        self.assertEqual(step.title, "Test Step")
        self.assertEqual(step.description, "This is a test step")
        self.assertEqual(step.order, 1)
        self.assertEqual(step.estimated_time, "30 minutes")
        self.assertEqual(step.prerequisites, ["Step 0"])
        self.assertEqual(step.complexity, 3.5)
        self.assertEqual(step.required_skills, ["Python"])
    
    def test_to_dict(self):
        """Test converting a step to a dictionary."""
        step = SOPStep(
            step_id="step_1",
            title="Test Step",
            description="This is a test step",
            order=1,
            estimated_time="30 minutes",
            prerequisites=["Step 0"],
            complexity=3.5,
            required_skills=["Python"]
        )
        
        step_dict = step.to_dict()
        
        self.assertEqual(step_dict["id"], "step_1")
        self.assertEqual(step_dict["title"], "Test Step")
        self.assertEqual(step_dict["description"], "This is a test step")
        self.assertEqual(step_dict["order"], 1)
        self.assertEqual(step_dict["estimatedTime"], "30 minutes")
        self.assertEqual(step_dict["prerequisites"], ["Step 0"])
        self.assertEqual(step_dict["complexity"], 3.5)
        self.assertEqual(step_dict["requiredSkills"], ["Python"])
    
    def test_from_dict(self):
        """Test creating a step from a dictionary."""
        step_dict = {
            "id": "step_1",
            "title": "Test Step",
            "description": "This is a test step",
            "order": 1,
            "estimatedTime": "30 minutes",
            "prerequisites": ["Step 0"],
            "complexity": 3.5,
            "requiredSkills": ["Python"]
        }
        
        step = SOPStep.from_dict(step_dict)
        
        self.assertEqual(step.step_id, "step_1")
        self.assertEqual(step.title, "Test Step")
        self.assertEqual(step.description, "This is a test step")
        self.assertEqual(step.order, 1)
        self.assertEqual(step.estimated_time, "30 minutes")
        self.assertEqual(step.prerequisites, ["Step 0"])
        self.assertEqual(step.complexity, 3.5)
        self.assertEqual(step.required_skills, ["Python"])

class TestSOPDocument(unittest.TestCase):
    """Test cases for SOPDocument class."""
    
    def test_init(self):
        """Test initialization of SOPDocument."""
        doc = SOPDocument(
            doc_id="doc_1",
            title="Test Document",
            description="This is a test document",
            version="1.0",
            status=SOPStatus.DRAFT,
            author="Test Author",
            department="Test Department",
            audience_level=SOPAudienceLevel.INTERMEDIATE,
            tags=["test", "document"]
        )
        
        self.assertEqual(doc.doc_id, "doc_1")
        self.assertEqual(doc.title, "Test Document")
        self.assertEqual(doc.description, "This is a test document")
        self.assertEqual(doc.version, "1.0")
        self.assertEqual(doc.status, SOPStatus.DRAFT)
        self.assertEqual(doc.author, "Test Author")
        self.assertEqual(doc.department, "Test Department")
        self.assertEqual(doc.audience_level, SOPAudienceLevel.INTERMEDIATE)
        self.assertEqual(doc.tags, ["test", "document"])
        self.assertEqual(doc.steps, [])
        self.assertEqual(doc.references, [])
        self.assertEqual(doc.attachments, [])
    
    def test_add_step(self):
        """Test adding a step to a document."""
        doc = SOPDocument(
            doc_id="doc_1",
            title="Test Document",
            description="This is a test document"
        )
        
        step1 = SOPStep(
            step_id="step_1",
            title="Step 1",
            description="This is step 1",
            order=1
        )
        
        step2 = SOPStep(
            step_id="step_2",
            title="Step 2",
            description="This is step 2",
            order=2
        )
        
        doc.add_step(step2)
        doc.add_step(step1)
        
        self.assertEqual(len(doc.steps), 2)
        self.assertEqual(doc.steps[0].step_id, "step_1")  # Steps should be sorted by order
        self.assertEqual(doc.steps[1].step_id, "step_2")
    
    def test_remove_step(self):
        """Test removing a step from a document."""
        doc = SOPDocument(
            doc_id="doc_1",
            title="Test Document",
            description="This is a test document"
        )
        
        step1 = SOPStep(
            step_id="step_1",
            title="Step 1",
            description="This is step 1",
            order=1
        )
        
        step2 = SOPStep(
            step_id="step_2",
            title="Step 2",
            description="This is step 2",
            order=2
        )
        
        doc.add_step(step1)
        doc.add_step(step2)
        
        self.assertEqual(len(doc.steps), 2)
        
        result = doc.remove_step("step_1")
        
        self.assertTrue(result)
        self.assertEqual(len(doc.steps), 1)
        self.assertEqual(doc.steps[0].step_id, "step_2")
        
        result = doc.remove_step("non_existent_step")
        
        self.assertFalse(result)
        self.assertEqual(len(doc.steps), 1)
    
    def test_to_dict(self):
        """Test converting a document to a dictionary."""
        doc = SOPDocument(
            doc_id="doc_1",
            title="Test Document",
            description="This is a test document",
            version="1.0",
            status=SOPStatus.DRAFT,
            author="Test Author",
            department="Test Department",
            audience_level=SOPAudienceLevel.INTERMEDIATE,
            tags=["test", "document"]
        )
        
        step = SOPStep(
            step_id="step_1",
            title="Test Step",
            description="This is a test step",
            order=1
        )
        
        doc.add_step(step)
        
        doc_dict = doc.to_dict()
        
        self.assertEqual(doc_dict["id"], "doc_1")
        self.assertEqual(doc_dict["title"], "Test Document")
        self.assertEqual(doc_dict["description"], "This is a test document")
        self.assertEqual(doc_dict["version"], "1.0")
        self.assertEqual(doc_dict["status"], "draft")
        self.assertEqual(doc_dict["author"], "Test Author")
        self.assertEqual(doc_dict["department"], "Test Department")
        self.assertEqual(doc_dict["audienceLevel"], "intermediate")
        self.assertEqual(doc_dict["tags"], ["test", "document"])
        self.assertEqual(len(doc_dict["steps"]), 1)
        self.assertEqual(doc_dict["steps"][0]["id"], "step_1")
    
    def test_from_dict(self):
        """Test creating a document from a dictionary."""
        doc_dict = {
            "id": "doc_1",
            "title": "Test Document",
            "description": "This is a test document",
            "version": "1.0",
            "status": "draft",
            "author": "Test Author",
            "department": "Test Department",
            "audienceLevel": "intermediate",
            "tags": ["test", "document"],
            "steps": [
                {
                    "id": "step_1",
                    "title": "Test Step",
                    "description": "This is a test step",
                    "order": 1
                }
            ],
            "references": ["Reference 1"],
            "attachments": ["attachment.pdf"]
        }
        
        doc = SOPDocument.from_dict(doc_dict)
        
        self.assertEqual(doc.doc_id, "doc_1")
        self.assertEqual(doc.title, "Test Document")
        self.assertEqual(doc.description, "This is a test document")
        self.assertEqual(doc.version, "1.0")
        self.assertEqual(doc.status, SOPStatus.DRAFT)
        self.assertEqual(doc.author, "Test Author")
        self.assertEqual(doc.department, "Test Department")
        self.assertEqual(doc.audience_level, SOPAudienceLevel.INTERMEDIATE)
        self.assertEqual(doc.tags, ["test", "document"])
        self.assertEqual(len(doc.steps), 1)
        self.assertEqual(doc.steps[0].step_id, "step_1")
        self.assertEqual(doc.references, ["Reference 1"])
        self.assertEqual(doc.attachments, ["attachment.pdf"])

class TestSOPDocumentManager(unittest.TestCase):
    """Test cases for SOPDocumentManager class."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.manager = SOPDocumentManager(self.temp_dir)
        
        self.test_doc = SOPDocument(
            doc_id="test_doc",
            title="Test Document",
            description="This is a test document"
        )
        
        self.test_step = SOPStep(
            step_id="test_step",
            title="Test Step",
            description="This is a test step",
            order=1
        )
        
        self.test_doc.add_step(self.test_step)
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir)
    
    def test_save_and_load_document(self):
        """Test saving and loading a document."""
        # Save the document
        result = self.manager.save_document(self.test_doc)
        self.assertTrue(result)
        
        # Check that the file exists
        file_path = os.path.join(self.temp_dir, "test_doc.json")
        self.assertTrue(os.path.exists(file_path))
        
        # Load the document
        loaded_doc = self.manager.load_document("test_doc")
        
        self.assertIsNotNone(loaded_doc)
        self.assertEqual(loaded_doc.doc_id, "test_doc")
        self.assertEqual(loaded_doc.title, "Test Document")
        self.assertEqual(loaded_doc.description, "This is a test document")
        self.assertEqual(len(loaded_doc.steps), 1)
        self.assertEqual(loaded_doc.steps[0].step_id, "test_step")
    
    def test_delete_document(self):
        """Test deleting a document."""
        # Save the document
        self.manager.save_document(self.test_doc)
        
        # Check that the file exists
        file_path = os.path.join(self.temp_dir, "test_doc.json")
        self.assertTrue(os.path.exists(file_path))
        
        # Delete the document
        result = self.manager.delete_document("test_doc")
        self.assertTrue(result)
        
        # Check that the file no longer exists
        self.assertFalse(os.path.exists(file_path))
        
        # Try to delete a non-existent document
        result = self.manager.delete_document("non_existent_doc")
        self.assertFalse(result)
    
    def test_list_documents(self):
        """Test listing documents."""
        # Save multiple documents
        self.manager.save_document(self.test_doc)
        
        doc2 = SOPDocument(
            doc_id="test_doc2",
            title="Test Document 2",
            description="This is another test document"
        )
        
        self.manager.save_document(doc2)
        
        # List documents
        documents = self.manager.list_documents()
        
        self.assertEqual(len(documents), 2)
        
        # Check that the documents are listed correctly
        doc_ids = [doc["id"] for doc in documents]
        self.assertIn("test_doc", doc_ids)
        self.assertIn("test_doc2", doc_ids)

if __name__ == '__main__':
    unittest.main()
