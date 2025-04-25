"""
SOP Complexity Analysis for Taskinator.

This module provides SOP-specific complexity analysis using the DSPy signatures.
"""

import traceback
from typing import Dict, List, Optional, Union, Any

from loguru import logger
from taskinator.sop_document import SOPDocument, SOPStep
from taskinator.dspy_signatures import (
    SOPComplexityInput, 
    SOPComplexityOutput, 
    SOPComplexitySignature,
    DSPY_AVAILABLE
)

class SOPComplexityAnalyzer:
    """Analyzes the complexity of SOP documents and steps."""
    
    def __init__(self, use_dspy: bool = True):
        """Initialize the SOP complexity analyzer.
        
        Args:
            use_dspy: Whether to use DSPy for analysis (if available)
        """
        self.use_dspy = use_dspy and DSPY_AVAILABLE
        self.complexity_predictor = None
        
        if self.use_dspy:
            try:
                import dspy
                
                # Define a simple predictor for complexity analysis
                class SOPComplexityPredictor(dspy.Module):
                    def __init__(self):
                        super().__init__()
                        self.predictor = dspy.ChainOfThought(SOPComplexitySignature)
                    
                    def forward(self, task_id, task_title, task_description, task_details, 
                               procedure_type="task", audience_expertise="intermediate"):
                        result = self.predictor(
                            task_id=task_id,
                            task_title=task_title,
                            task_description=task_description,
                            task_details=task_details,
                            procedure_type=procedure_type,
                            audience_expertise=audience_expertise
                        )
                        return result
                
                # Initialize the predictor
                self.complexity_predictor = SOPComplexityPredictor()
                logger.info("Initialized DSPy complexity predictor for SOP analysis")
            except Exception as e:
                logger.error(f"Failed to initialize DSPy for SOP complexity analysis: {e}")
                logger.debug(f"Initialization error details: {traceback.format_exc()}")
                self.use_dspy = False
    
    def analyze_step(self, step: SOPStep, audience_expertise: str = "intermediate") -> Dict[str, Any]:
        """Analyze the complexity of a single SOP step.
        
        Args:
            step: The step to analyze
            audience_expertise: Target audience expertise level
            
        Returns:
            Dictionary with complexity assessment
        """
        if not self.use_dspy or not self.complexity_predictor:
            # Fallback to heuristic analysis if DSPy is not available
            return self._heuristic_analysis(step, audience_expertise)
        
        try:
            # Prepare input for the predictor
            task_id = step.step_id
            task_title = step.title
            task_description = step.description
            
            # Combine additional details
            task_details = f"Prerequisites: {', '.join(step.prerequisites)}\n"
            task_details += f"Required Skills: {', '.join(step.required_skills)}\n"
            if step.estimated_time:
                task_details += f"Estimated Time: {step.estimated_time}"
            
            # Use DSPy for analysis
            result = self.complexity_predictor.forward(
                task_id=task_id,
                task_title=task_title,
                task_description=task_description,
                task_details=task_details,
                procedure_type="step",
                audience_expertise=audience_expertise
            )
            
            # Convert the result to a dictionary
            return {
                "stepId": task_id,
                "stepTitle": task_title,
                "complexityScore": result.complexity_score,
                "explanation": result.explanation,
                "requiredSkills": result.required_skills,
                "estimatedTime": result.estimated_time if hasattr(result, 'estimated_time') else step.estimated_time,
                "prerequisites": result.prerequisites if hasattr(result, 'prerequisites') else step.prerequisites
            }
        
        except Exception as e:
            logger.error(f"Error analyzing SOP step complexity: {e}")
            logger.debug(f"Analysis error details: {traceback.format_exc()}")
            
            # Fallback to heuristic analysis
            return self._heuristic_analysis(step, audience_expertise)
    
    def _heuristic_analysis(self, step: SOPStep, audience_expertise: str) -> Dict[str, Any]:
        """Perform heuristic complexity analysis based on step attributes.
        
        Args:
            step: The step to analyze
            audience_expertise: Target audience expertise level
            
        Returns:
            Dictionary with complexity assessment
        """
        # Base complexity score
        complexity_score = 3.0  # Default to medium complexity
        
        # Adjust based on required skills
        if step.required_skills:
            complexity_score += min(len(step.required_skills) * 0.5, 2.0)
        
        # Adjust based on prerequisites
        if step.prerequisites:
            complexity_score += min(len(step.prerequisites) * 0.3, 1.0)
        
        # Adjust based on description length (longer descriptions often indicate complexity)
        description_length = len(step.description)
        if description_length > 1000:
            complexity_score += 1.0
        elif description_length > 500:
            complexity_score += 0.5
        
        # Adjust based on audience expertise
        if audience_expertise == "beginner":
            complexity_score += 1.0
        elif audience_expertise == "expert":
            complexity_score -= 1.0
        
        # Ensure score is within range (1-5)
        complexity_score = max(1.0, min(5.0, complexity_score))
        
        # Generate explanation
        explanation = f"This step has been assigned a complexity score of {complexity_score:.1f} "
        explanation += f"based on {len(step.required_skills)} required skills, "
        explanation += f"{len(step.prerequisites)} prerequisites, "
        explanation += f"and a description length of {description_length} characters. "
        
        if audience_expertise != "intermediate":
            explanation += f"The score was adjusted for {audience_expertise} audience expertise. "
        
        # Return the analysis
        return {
            "stepId": step.step_id,
            "stepTitle": step.title,
            "complexityScore": complexity_score,
            "explanation": explanation,
            "requiredSkills": step.required_skills,
            "estimatedTime": step.estimated_time,
            "prerequisites": step.prerequisites
        }
    
    def analyze_document(self, document: SOPDocument) -> Dict[str, Any]:
        """Analyze the complexity of an entire SOP document.
        
        Args:
            document: The document to analyze
            
        Returns:
            Dictionary with document complexity assessment and step analyses
        """
        # Analyze each step
        step_analyses = []
        for step in document.steps:
            step_analysis = self.analyze_step(step, document.audience_level.value)
            step_analyses.append(step_analysis)
        
        # Calculate overall document complexity
        if step_analyses:
            avg_complexity = sum(analysis["complexityScore"] for analysis in step_analyses) / len(step_analyses)
            max_complexity = max(analysis["complexityScore"] for analysis in step_analyses)
        else:
            avg_complexity = 0.0
            max_complexity = 0.0
        
        # Generate document complexity explanation
        if step_analyses:
            explanation = f"This SOP document contains {len(step_analyses)} steps with an average complexity of {avg_complexity:.1f}. "
            explanation += f"The most complex step has a score of {max_complexity:.1f}. "
            explanation += f"The document is targeted at {document.audience_level.value} audience. "
            
            if max_complexity >= 4.0:
                explanation += "This document contains highly complex steps that may require expert knowledge. "
            elif max_complexity >= 3.0:
                explanation += "This document contains moderately complex steps that require good understanding of the domain. "
            else:
                explanation += "This document contains relatively simple steps that should be accessible to most users. "
        else:
            explanation = "This SOP document does not contain any steps to analyze."
        
        # Return the complete analysis
        return {
            "documentId": document.doc_id,
            "documentTitle": document.title,
            "averageComplexity": avg_complexity,
            "maxComplexity": max_complexity,
            "targetAudience": document.audience_level.value,
            "explanation": explanation,
            "stepAnalyses": step_analyses
        }
