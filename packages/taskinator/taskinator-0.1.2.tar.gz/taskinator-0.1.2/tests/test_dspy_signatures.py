"""
Unit tests for DSPy Signatures.
"""

import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Add the parent directory to the path so we can import the taskinator module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from taskinator.dspy_signatures import (
    DSPY_AVAILABLE,
    # Base signatures
    TextSimilarityInput,
    TextSimilarityOutput,
    ComplexityInput,
    ComplexityOutput,
    TextSimilaritySignature,
    ComplexitySignature,
    # SOP-specific signatures
    SOPTextSimilarityInput,
    SOPTextSimilarityOutput,
    SOPComplexityInput,
    SOPComplexityOutput,
    SOPTextSimilaritySignature,
    SOPComplexitySignature,
    # PDD-specific signatures
    PDDTextSimilarityInput,
    PDDTextSimilarityOutput,
    PDDComplexityInput,
    PDDComplexityOutput,
    PDDTextSimilaritySignature,
    PDDComplexitySignature
)


class TestDSPySignatures(unittest.TestCase):
    """Test cases for DSPy Signatures."""

    def test_dspy_availability(self):
        """Test that we can detect DSPy availability."""
        # This just verifies that the module loaded and set DSPY_AVAILABLE correctly
        self.assertIsNotNone(DSPY_AVAILABLE)
    
    # Base Signature Tests
    
    def test_text_similarity_input(self):
        """Test TextSimilarityInput initialization."""
        text_a = "This is the first text"
        text_b = "This is the second text"
        cosine_similarity = 0.85
        
        # Create an input object
        input_obj = TextSimilarityInput(
            text_a=text_a,
            text_b=text_b,
            cosine_similarity=cosine_similarity
        )
        
        # Verify attributes
        self.assertEqual(input_obj.text_a, text_a)
        self.assertEqual(input_obj.text_b, text_b)
        self.assertEqual(input_obj.cosine_similarity, cosine_similarity)
    
    def test_text_similarity_output(self):
        """Test TextSimilarityOutput initialization."""
        similarity_score = 0.75
        explanation = "The texts share common themes but differ in specifics."
        
        # Create an output object
        output_obj = TextSimilarityOutput(
            similarity_score=similarity_score,
            explanation=explanation
        )
        
        # Verify attributes
        self.assertEqual(output_obj.similarity_score, similarity_score)
        self.assertEqual(output_obj.explanation, explanation)
    
    def test_complexity_input(self):
        """Test ComplexityInput initialization."""
        task_id = 123
        task_title = "Implement DSPy Signatures"
        task_description = "Define the DSPy Signatures for task analysis"
        task_details = "Create signature classes with appropriate fields"
        
        # Create an input object
        input_obj = ComplexityInput(
            task_id=task_id,
            task_title=task_title,
            task_description=task_description,
            task_details=task_details
        )
        
        # Verify attributes
        self.assertEqual(input_obj.task_id, task_id)
        self.assertEqual(input_obj.task_title, task_title)
        self.assertEqual(input_obj.task_description, task_description)
        self.assertEqual(input_obj.task_details, task_details)
    
    def test_complexity_output(self):
        """Test ComplexityOutput initialization."""
        complexity_score = 7.5
        explanation = "This task requires understanding of DSPy and signature design"
        required_skills = ["Python", "DSPy", "API Design"]
        recommended_subtasks = 3
        expansion_prompt = "Break down the task into signature design, implementation, and testing"
        
        # Create an output object
        output_obj = ComplexityOutput(
            complexity_score=complexity_score,
            explanation=explanation,
            required_skills=required_skills,
            recommended_subtasks=recommended_subtasks,
            expansionPrompt=expansion_prompt
        )
        
        # Verify attributes
        self.assertEqual(output_obj.complexity_score, complexity_score)
        self.assertEqual(output_obj.explanation, explanation)
        self.assertEqual(output_obj.required_skills, required_skills)
        self.assertEqual(output_obj.recommended_subtasks, recommended_subtasks)
        self.assertEqual(output_obj.expansionPrompt, expansion_prompt)
    
    # SOP-specific Signature Tests
    
    def test_sop_text_similarity_input(self):
        """Test SOPTextSimilarityInput initialization."""
        text_a = "First, open the file. Then, edit the content."
        text_b = "Step 1: Open the file. Step 2: Modify the text."
        cosine_similarity = 0.88
        procedure_type = "workflow"
        
        # Create an input object
        input_obj = SOPTextSimilarityInput(
            text_a=text_a,
            text_b=text_b,
            cosine_similarity=cosine_similarity,
            procedure_type=procedure_type
        )
        
        # Verify attributes
        self.assertEqual(input_obj.text_a, text_a)
        self.assertEqual(input_obj.text_b, text_b)
        self.assertEqual(input_obj.cosine_similarity, cosine_similarity)
        self.assertEqual(input_obj.procedure_type, procedure_type)
    
    def test_sop_text_similarity_output(self):
        """Test SOPTextSimilarityOutput initialization."""
        similarity_score = 0.82
        explanation = "Both procedures describe the same file editing process with different wording."
        common_steps = ["Open file", "Edit content"]
        divergent_steps = ["Save file (only in procedure B)"]
        
        # Create an output object
        output_obj = SOPTextSimilarityOutput(
            similarity_score=similarity_score,
            explanation=explanation,
            common_steps=common_steps,
            divergent_steps=divergent_steps
        )
        
        # Verify attributes
        self.assertEqual(output_obj.similarity_score, similarity_score)
        self.assertEqual(output_obj.explanation, explanation)
        self.assertEqual(output_obj.common_steps, common_steps)
        self.assertEqual(output_obj.divergent_steps, divergent_steps)
    
    def test_sop_complexity_input(self):
        """Test SOPComplexityInput initialization."""
        task_id = 456
        task_title = "Configure Server Environment"
        task_description = "Set up the server environment for deployment"
        task_details = "Install dependencies, configure settings, and verify connectivity"
        procedure_type = "process"
        audience_expertise = "expert"
        
        # Create an input object
        input_obj = SOPComplexityInput(
            task_id=task_id,
            task_title=task_title,
            task_description=task_description,
            task_details=task_details,
            procedure_type=procedure_type,
            audience_expertise=audience_expertise
        )
        
        # Verify attributes
        self.assertEqual(input_obj.task_id, task_id)
        self.assertEqual(input_obj.task_title, task_title)
        self.assertEqual(input_obj.task_description, task_description)
        self.assertEqual(input_obj.task_details, task_details)
        self.assertEqual(input_obj.procedure_type, procedure_type)
        self.assertEqual(input_obj.audience_expertise, audience_expertise)
    
    def test_sop_complexity_output(self):
        """Test SOPComplexityOutput initialization."""
        complexity_score = 8.0
        explanation = "This is a complex server configuration task requiring expert knowledge."
        required_skills = ["Linux", "Networking", "Security"]
        recommended_subtasks = 5
        expansion_prompt = "Break down the server configuration task into installation, configuration, security, testing, and documentation steps."
        estimated_time = "4-6 hours"
        prerequisites = ["Access to server", "Admin credentials"]
        
        # Create an output object
        output_obj = SOPComplexityOutput(
            complexity_score=complexity_score,
            explanation=explanation,
            required_skills=required_skills,
            recommended_subtasks=recommended_subtasks,
            expansionPrompt=expansion_prompt,
            estimated_time=estimated_time,
            prerequisites=prerequisites
        )
        
        # Verify attributes
        self.assertEqual(output_obj.complexity_score, complexity_score)
        self.assertEqual(output_obj.explanation, explanation)
        self.assertEqual(output_obj.required_skills, required_skills)
        self.assertEqual(output_obj.recommended_subtasks, recommended_subtasks)
        self.assertEqual(output_obj.expansionPrompt, expansion_prompt)
        self.assertEqual(output_obj.estimated_time, estimated_time)
        self.assertEqual(output_obj.prerequisites, prerequisites)
    
    # PDD-specific Signature Tests
    
    def test_pdd_text_similarity_input(self):
        """Test PDDTextSimilarityInput initialization."""
        text_a = "The product will include a user authentication system with password recovery."
        text_b = "User login functionality with password reset capabilities will be implemented."
        cosine_similarity = 0.91
        domain = "web application"
        
        # Create an input object
        input_obj = PDDTextSimilarityInput(
            text_a=text_a,
            text_b=text_b,
            cosine_similarity=cosine_similarity,
            domain=domain
        )
        
        # Verify attributes
        self.assertEqual(input_obj.text_a, text_a)
        self.assertEqual(input_obj.text_b, text_b)
        self.assertEqual(input_obj.cosine_similarity, cosine_similarity)
        self.assertEqual(input_obj.domain, domain)
    
    def test_pdd_text_similarity_output(self):
        """Test PDDTextSimilarityOutput initialization."""
        similarity_score = 0.89
        explanation = "Both descriptions refer to the same authentication feature set with different terminology."
        feature_overlap = "User authentication, password recovery/reset"
        unique_features = "Text A mentions a 'system', Text B focuses on 'functionality'"
        
        # Create an output object
        output_obj = PDDTextSimilarityOutput(
            similarity_score=similarity_score,
            explanation=explanation,
            feature_overlap=feature_overlap,
            unique_features=unique_features
        )
        
        # Verify attributes
        self.assertEqual(output_obj.similarity_score, similarity_score)
        self.assertEqual(output_obj.explanation, explanation)
        self.assertEqual(output_obj.feature_overlap, feature_overlap)
        self.assertEqual(output_obj.unique_features, unique_features)
    
    def test_pdd_complexity_input(self):
        """Test PDDComplexityInput initialization."""
        task_id = 789
        task_title = "Implement OAuth Integration"
        task_description = "Add OAuth authentication with multiple providers"
        task_details = "Integrate with Google, Facebook, and Twitter OAuth APIs"
        product_domain = "mobile app"
        development_stage = "implementation"
        
        # Create an input object
        input_obj = PDDComplexityInput(
            task_id=task_id,
            task_title=task_title,
            task_description=task_description,
            task_details=task_details,
            product_domain=product_domain,
            development_stage=development_stage
        )
        
        # Verify attributes
        self.assertEqual(input_obj.task_id, task_id)
        self.assertEqual(input_obj.task_title, task_title)
        self.assertEqual(input_obj.task_description, task_description)
        self.assertEqual(input_obj.task_details, task_details)
        self.assertEqual(input_obj.product_domain, product_domain)
        self.assertEqual(input_obj.development_stage, development_stage)
    
    def test_pdd_complexity_output(self):
        """Test PDDComplexityOutput initialization."""
        complexity_score = 8.5
        explanation = "OAuth integration with multiple providers is complex due to different API requirements and security considerations."
        required_skills = ["OAuth", "API Integration", "Security", "Mobile Development"]
        recommended_subtasks = 6
        expansion_prompt = "Break down the OAuth integration task into provider-specific implementations and shared components."
        technical_dependencies = ["HTTP Client", "Secure Storage", "UI Components"]
        risk_assessment = "High risk due to security implications and potential API changes from providers."
        
        # Create an output object
        output_obj = PDDComplexityOutput(
            complexity_score=complexity_score,
            explanation=explanation,
            required_skills=required_skills,
            recommended_subtasks=recommended_subtasks,
            expansionPrompt=expansion_prompt,
            technical_dependencies=technical_dependencies,
            risk_assessment=risk_assessment
        )
        
        # Verify attributes
        self.assertEqual(output_obj.complexity_score, complexity_score)
        self.assertEqual(output_obj.explanation, explanation)
        self.assertEqual(output_obj.required_skills, required_skills)
        self.assertEqual(output_obj.recommended_subtasks, recommended_subtasks)
        self.assertEqual(output_obj.expansionPrompt, expansion_prompt)
        self.assertEqual(output_obj.technical_dependencies, technical_dependencies)
        self.assertEqual(output_obj.risk_assessment, risk_assessment)
    
    # Signature Tests (only if DSPy is available)
    
    @unittest.skipIf(not DSPY_AVAILABLE, "DSPy is not available")
    def test_text_similarity_signature(self):
        """Test TextSimilaritySignature with DSPy."""
        # This test only runs if DSPy is available
        import dspy
        
        # Verify the signature is a DSPy signature
        self.assertTrue(issubclass(TextSimilaritySignature, dspy.Signature))
    
    @unittest.skipIf(not DSPY_AVAILABLE, "DSPy is not available")
    def test_sop_text_similarity_signature(self):
        """Test SOPTextSimilaritySignature with DSPy."""
        # This test only runs if DSPy is available
        import dspy
        
        # Verify the signature is a DSPy signature
        self.assertTrue(issubclass(SOPTextSimilaritySignature, dspy.Signature))
    
    @unittest.skipIf(not DSPY_AVAILABLE, "DSPy is not available")
    def test_pdd_text_similarity_signature(self):
        """Test PDDTextSimilaritySignature with DSPy."""
        # This test only runs if DSPy is available
        import dspy
        
        # Verify the signature is a DSPy signature
        self.assertTrue(issubclass(PDDTextSimilaritySignature, dspy.Signature))
    
    @unittest.skipIf(not DSPY_AVAILABLE, "DSPy is not available")
    def test_complexity_signature(self):
        """Test ComplexitySignature with DSPy."""
        # This test only runs if DSPy is available
        import dspy
        
        # Verify the signature is a DSPy signature
        self.assertTrue(issubclass(ComplexitySignature, dspy.Signature))
    
    @unittest.skipIf(not DSPY_AVAILABLE, "DSPy is not available")
    def test_sop_complexity_signature(self):
        """Test SOPComplexitySignature with DSPy."""
        # This test only runs if DSPy is available
        import dspy
        
        # Verify the signature is a DSPy signature
        self.assertTrue(issubclass(SOPComplexitySignature, dspy.Signature))
    
    @unittest.skipIf(not DSPY_AVAILABLE, "DSPy is not available")
    def test_pdd_complexity_signature(self):
        """Test PDDComplexitySignature with DSPy."""
        # This test only runs if DSPy is available
        import dspy
        
        # Verify the signature is a DSPy signature
        self.assertTrue(issubclass(PDDComplexitySignature, dspy.Signature))


if __name__ == '__main__':
    unittest.main()
