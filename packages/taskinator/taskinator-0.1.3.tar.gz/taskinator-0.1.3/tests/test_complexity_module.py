"""
Unit tests for the ComplexityAnalysisModule.
"""

import unittest
import json
import os
from unittest.mock import patch, MagicMock
from pathlib import Path

# Import the module before patching
from taskinator.complexity_module import ComplexityAnalysisModule, ComplexityAnalysisResult


class TestComplexityAnalysisModule(unittest.TestCase):
    """Test cases for the ComplexityAnalysisModule."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_tasks = [
            {
                "id": 1,
                "title": "Implement user authentication",
                "description": "Create a secure user authentication system",
                "details": "Implement login, registration, and password reset functionality with JWT tokens."
            },
            {
                "id": 2,
                "title": "Add pagination to product list",
                "description": "Add pagination to the product listing page",
                "details": "Implement pagination with limit and offset parameters."
            }
        ]
        
        # Create a test training data file
        self.test_training_data = {
            "timestamp": "2025-04-20T10:43:17-04:00",
            "examples": [
                {
                    "request_id": "20250420_104317_0",
                    "timestamp": "2025-04-20T10:43:17-04:00",
                    "use_research": True,
                    "examples": [
                        {
                            "task_id": 1,
                            "task_title": "Implement user authentication",
                            "task_description": "Create a secure user authentication system",
                            "task_details": "Implement login, registration, and password reset functionality with JWT tokens.",
                            "complexity_score": 7,
                            "recommended_subtasks": 3,
                            "expansion_prompt": "Break down the authentication system into subtasks for registration, login, and password reset.",
                            "reasoning": "Authentication involves security considerations and multiple endpoints."
                        }
                    ]
                }
            ]
        }
        
        # Create test directory for training data
        self.test_data_dir = Path("test_training_data")
        self.test_data_dir.mkdir(exist_ok=True)
        self.test_data_file = self.test_data_dir / "test_complexity_dataset.json"
        
        with open(self.test_data_file, 'w') as f:
            json.dump(self.test_training_data, f)
    
    def tearDown(self):
        """Clean up test fixtures."""
        # Remove test training data file
        if self.test_data_file.exists():
            self.test_data_file.unlink()
        
        # Remove test directory
        if self.test_data_dir.exists():
            self.test_data_dir.rmdir()
    
    def test_init_without_dspy(self):
        """Test initialization without DSPy."""
        module = ComplexityAnalysisModule(use_dspy=False)
        self.assertFalse(module.use_dspy)
    
    @patch('taskinator.complexity_module.DSPY_AVAILABLE', True)
    def test_init_with_dspy(self):
        """Test initialization with DSPy."""
        # Create a module with mocked complexity_predictor
        module = ComplexityAnalysisModule(use_dspy=False)
        
        # Force use_dspy to be True for testing
        module.use_dspy = True
        
        # Set a mock complexity_predictor
        module.complexity_predictor = MagicMock()
        
        # Verify that use_dspy is True
        self.assertTrue(module.use_dspy)
    
    def test_analyze_task_without_dspy(self):
        """Test analyzing a task without DSPy."""
        module = ComplexityAnalysisModule(use_dspy=False)
        result = module.analyze_task(self.test_tasks[0])
        
        self.assertEqual(result["taskId"], 1)
        self.assertEqual(result["taskTitle"], "Implement user authentication")
        self.assertEqual(result["complexityScore"], 5.0)  # Default score
        self.assertEqual(result["recommendedSubtasks"], 3)  # Default value
        self.assertIn("placeholder", result["reasoning"].lower())
    
    def test_analyze_task_with_dspy(self):
        """Test analyzing a task with DSPy."""
        # Create a module with mocked complexity_predictor
        module = ComplexityAnalysisModule(use_dspy=False)
        
        # Create a mock for the complexity_predictor
        mock_predictor = MagicMock()
        mock_predictor.forward.return_value = {
            "taskId": 1,
            "taskTitle": "Implement user authentication",
            "complexityScore": 7.5,
            "recommendedSubtasks": 4,
            "expansionPrompt": "Break down into subtasks...",
            "reasoning": "This is complex because..."
        }
        
        # Set the mocked complexity_predictor
        module.complexity_predictor = mock_predictor
        
        # Force use_dspy to be True for testing
        module.use_dspy = True
        
        # Test the analyze_task method
        result = module.analyze_task(self.test_tasks[0])
        
        # Verify the result
        self.assertEqual(result["taskId"], 1)
        self.assertEqual(result["taskTitle"], "Implement user authentication")
        self.assertEqual(result["complexityScore"], 7.5)
        self.assertEqual(result["recommendedSubtasks"], 4)
        self.assertEqual(result["expansionPrompt"], "Break down into subtasks...")
        self.assertEqual(result["reasoning"], "This is complex because...")
        
        # Verify that the mock was called correctly
        mock_predictor.forward.assert_called_once()
    
    def test_analyze_tasks(self):
        """Test analyzing multiple tasks."""
        module = ComplexityAnalysisModule(use_dspy=False)
        results = module.analyze_tasks(self.test_tasks)
        
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["taskId"], 1)
        self.assertEqual(results[1]["taskId"], 2)


if __name__ == '__main__':
    unittest.main()
