"""
Unit tests for SOP complexity analysis.
"""

import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Add the parent directory to the path so we can import the taskinator module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from taskinator.sop_complexity import SOPComplexityAnalyzer
from taskinator.sop_document import SOPDocument, SOPStep, SOPAudienceLevel
from taskinator.dspy_signatures import DSPY_AVAILABLE

class TestSOPComplexityAnalyzer(unittest.TestCase):
    """Test cases for SOPComplexityAnalyzer class."""
    
    def setUp(self):
        """Set up test environment."""
        # Create a test document with steps
        self.test_doc = SOPDocument(
            doc_id="test_doc",
            title="Test Document",
            description="This is a test document",
            audience_level=SOPAudienceLevel.INTERMEDIATE
        )
        
        # Simple step
        self.simple_step = SOPStep(
            step_id="simple_step",
            title="Simple Step",
            description="This is a simple step with minimal requirements.",
            order=1,
            estimated_time="10 minutes",
            prerequisites=[],
            required_skills=[]
        )
        
        # Medium complexity step
        self.medium_step = SOPStep(
            step_id="medium_step",
            title="Medium Step",
            description="This is a medium complexity step that requires some skills and prerequisites.",
            order=2,
            estimated_time="30 minutes",
            prerequisites=["Simple Step"],
            required_skills=["Basic Python"]
        )
        
        # Complex step
        self.complex_step = SOPStep(
            step_id="complex_step",
            title="Complex Step",
            description="This is a complex step that requires multiple skills and prerequisites. " * 10,  # Long description
            order=3,
            estimated_time="2 hours",
            prerequisites=["Simple Step", "Medium Step", "External Knowledge"],
            required_skills=["Advanced Python", "Database Design", "API Integration", "Testing"]
        )
        
        # Add steps to document
        self.test_doc.add_step(self.simple_step)
        self.test_doc.add_step(self.medium_step)
        self.test_doc.add_step(self.complex_step)
        
        # Create analyzer without DSPy
        self.analyzer = SOPComplexityAnalyzer(use_dspy=False)
    
    def test_heuristic_analysis(self):
        """Test heuristic complexity analysis."""
        # Analyze simple step
        simple_analysis = self.analyzer._heuristic_analysis(self.simple_step, "intermediate")
        
        self.assertEqual(simple_analysis["stepId"], "simple_step")
        self.assertEqual(simple_analysis["stepTitle"], "Simple Step")
        self.assertLessEqual(simple_analysis["complexityScore"], 3.0)  # Should be low complexity
        
        # Analyze medium step
        medium_analysis = self.analyzer._heuristic_analysis(self.medium_step, "intermediate")
        
        self.assertEqual(medium_analysis["stepId"], "medium_step")
        self.assertEqual(medium_analysis["stepTitle"], "Medium Step")
        self.assertGreater(medium_analysis["complexityScore"], simple_analysis["complexityScore"])
        
        # Analyze complex step
        complex_analysis = self.analyzer._heuristic_analysis(self.complex_step, "intermediate")
        
        self.assertEqual(complex_analysis["stepId"], "complex_step")
        self.assertEqual(complex_analysis["stepTitle"], "Complex Step")
        self.assertGreater(complex_analysis["complexityScore"], medium_analysis["complexityScore"])
        self.assertGreaterEqual(complex_analysis["complexityScore"], 4.0)  # Should be high complexity
    
    def test_audience_adjustment(self):
        """Test complexity adjustment based on audience level."""
        # Analyze for beginner audience
        beginner_analysis = self.analyzer._heuristic_analysis(self.medium_step, "beginner")
        
        # Analyze for intermediate audience
        intermediate_analysis = self.analyzer._heuristic_analysis(self.medium_step, "intermediate")
        
        # Analyze for expert audience
        expert_analysis = self.analyzer._heuristic_analysis(self.medium_step, "expert")
        
        # Complexity should be higher for beginners and lower for experts
        self.assertGreater(beginner_analysis["complexityScore"], intermediate_analysis["complexityScore"])
        self.assertLess(expert_analysis["complexityScore"], intermediate_analysis["complexityScore"])
    
    def test_analyze_step(self):
        """Test analyzing a single step."""
        # Analyze medium step
        step_analysis = self.analyzer.analyze_step(self.medium_step)
        
        self.assertEqual(step_analysis["stepId"], "medium_step")
        self.assertEqual(step_analysis["stepTitle"], "Medium Step")
        self.assertIsInstance(step_analysis["complexityScore"], float)
        self.assertGreaterEqual(step_analysis["complexityScore"], 1.0)
        self.assertLessEqual(step_analysis["complexityScore"], 5.0)
        self.assertIsInstance(step_analysis["explanation"], str)
        self.assertEqual(step_analysis["requiredSkills"], ["Basic Python"])
        self.assertEqual(step_analysis["prerequisites"], ["Simple Step"])
    
    def test_analyze_document(self):
        """Test analyzing an entire document."""
        # Analyze document
        doc_analysis = self.analyzer.analyze_document(self.test_doc)
        
        self.assertEqual(doc_analysis["documentId"], "test_doc")
        self.assertEqual(doc_analysis["documentTitle"], "Test Document")
        self.assertEqual(doc_analysis["targetAudience"], "intermediate")
        self.assertIsInstance(doc_analysis["averageComplexity"], float)
        self.assertIsInstance(doc_analysis["maxComplexity"], float)
        self.assertIsInstance(doc_analysis["explanation"], str)
        self.assertEqual(len(doc_analysis["stepAnalyses"]), 3)
        
        # Check that step analyses are included
        step_ids = [analysis["stepId"] for analysis in doc_analysis["stepAnalyses"]]
        self.assertIn("simple_step", step_ids)
        self.assertIn("medium_step", step_ids)
        self.assertIn("complex_step", step_ids)
        
        # Max complexity should be from the complex step
        complex_analysis = next(a for a in doc_analysis["stepAnalyses"] if a["stepId"] == "complex_step")
        self.assertEqual(doc_analysis["maxComplexity"], complex_analysis["complexityScore"])

    @unittest.skipIf(not DSPY_AVAILABLE, "DSPy is not available")
    def test_dspy_initialization(self):
        """Test initialization with DSPy."""
        # Create analyzer with DSPy
        dspy_analyzer = SOPComplexityAnalyzer(use_dspy=True)
        
        # If DSPy is available, the predictor should be initialized
        if DSPY_AVAILABLE:
            self.assertIsNotNone(dspy_analyzer.complexity_predictor)
        else:
            self.assertIsNone(dspy_analyzer.complexity_predictor)

if __name__ == '__main__':
    unittest.main()
