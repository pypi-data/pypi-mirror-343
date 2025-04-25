"""
PDD Complexity Analysis for Taskinator.

This module provides PDD-specific complexity analysis using the DSPy signatures.
"""

import traceback
from typing import Dict, List, Optional, Union, Any

from loguru import logger
from taskinator.pdd_document import PDDDocument, PDDProcess, PDDImplementationDifficulty
from taskinator.dspy_signatures import (
    PDDComplexityInput, 
    PDDComplexityOutput, 
    PDDComplexitySignature,
    DSPY_AVAILABLE
)

class PDDComplexityAnalyzer:
    """Analyzes the complexity of PDD documents and processes."""
    
    def __init__(self, use_dspy: bool = True):
        """Initialize the PDD complexity analyzer.
        
        Args:
            use_dspy: Whether to use DSPy for analysis (if available)
        """
        self.use_dspy = use_dspy and DSPY_AVAILABLE
        self.complexity_predictor = None
        
        if self.use_dspy:
            try:
                import dspy
                
                # Define a simple predictor for complexity analysis
                class PDDComplexityPredictor(dspy.Module):
                    def __init__(self):
                        super().__init__()
                        self.predictor = dspy.ChainOfThought(PDDComplexitySignature)
                    
                    def forward(self, process_id, process_title, process_description, process_details, 
                               implementation_type="process", resource_availability="moderate"):
                        result = self.predictor(
                            process_id=process_id,
                            process_title=process_title,
                            process_description=process_description,
                            process_details=process_details,
                            implementation_type=implementation_type,
                            resource_availability=resource_availability
                        )
                        return result
                
                # Initialize the predictor
                self.complexity_predictor = PDDComplexityPredictor()
                logger.info("Initialized DSPy complexity predictor for PDD analysis")
            except Exception as e:
                logger.error(f"Failed to initialize DSPy for PDD complexity analysis: {e}")
                logger.debug(f"Initialization error details: {traceback.format_exc()}")
                self.use_dspy = False
    
    def analyze_process(self, process: PDDProcess, resource_availability: str = "moderate") -> Dict[str, Any]:
        """Analyze the complexity of a single PDD process.
        
        Args:
            process: The process to analyze
            resource_availability: Availability of resources for implementation
            
        Returns:
            Dictionary with complexity assessment
        """
        if not self.use_dspy or not self.complexity_predictor:
            # Fallback to heuristic analysis if DSPy is not available
            return self._heuristic_analysis(process, resource_availability)
        
        try:
            # Prepare input for the predictor
            process_id = process.process_id
            process_title = process.title
            process_description = process.description
            
            # Combine additional details
            process_details = f"Dependencies: {', '.join(process.dependencies)}\n"
            process_details += f"Required Resources: {', '.join(process.required_resources)}\n"
            process_details += f"Inputs: {', '.join(process.inputs)}\n"
            process_details += f"Outputs: {', '.join(process.outputs)}\n"
            if process.estimated_time:
                process_details += f"Estimated Time: {process.estimated_time}"
            
            # Use DSPy for analysis
            result = self.complexity_predictor.forward(
                process_id=process_id,
                process_title=process_title,
                process_description=process_description,
                process_details=process_details,
                implementation_type="process",
                resource_availability=resource_availability
            )
            
            # Convert the result to a dictionary
            return {
                "processId": process_id,
                "processTitle": process_title,
                "complexityScore": result.complexity_score,
                "implementationDifficulty": result.implementation_difficulty,
                "explanation": result.explanation,
                "requiredResources": process.required_resources,
                "estimatedTime": process.estimated_time,
                "dependencies": process.dependencies,
                "inputs": process.inputs,
                "outputs": process.outputs
            }
        except Exception as e:
            logger.error(f"Error analyzing process {process.process_id} with DSPy: {e}")
            logger.debug(f"Analysis error details: {traceback.format_exc()}")
            
            # Fallback to heuristic analysis
            return self._heuristic_analysis(process, resource_availability)
    
    def _heuristic_analysis(self, process: PDDProcess, resource_availability: str) -> Dict[str, Any]:
        """Perform heuristic complexity analysis based on process attributes.
        
        Args:
            process: The process to analyze
            resource_availability: Availability of resources for implementation
            
        Returns:
            Dictionary with complexity assessment
        """
        # Start with a base complexity score
        complexity_score = 3.0
        
        # Adjust based on existing difficulty if available
        if process.difficulty is not None:
            complexity_score = process.difficulty
        
        # Adjust based on implementation difficulty if available
        if process.implementation_difficulty:
            if process.implementation_difficulty == PDDImplementationDifficulty.SIMPLE:
                complexity_score = min(complexity_score, 2.0)
            elif process.implementation_difficulty == PDDImplementationDifficulty.MODERATE:
                complexity_score = max(2.0, min(complexity_score, 3.0))
            elif process.implementation_difficulty == PDDImplementationDifficulty.COMPLEX:
                complexity_score = max(3.0, min(complexity_score, 4.0))
            elif process.implementation_difficulty == PDDImplementationDifficulty.VERY_COMPLEX:
                complexity_score = max(4.0, min(complexity_score, 4.5))
            elif process.implementation_difficulty == PDDImplementationDifficulty.EXTREME:
                complexity_score = max(4.5, complexity_score)
        
        # Adjust based on required resources
        if process.required_resources:
            complexity_score += min(len(process.required_resources) * 0.3, 1.0)
        
        # Adjust based on dependencies
        if process.dependencies:
            complexity_score += min(len(process.dependencies) * 0.3, 1.0)
        
        # Adjust based on inputs and outputs
        complexity_score += min((len(process.inputs) + len(process.outputs)) * 0.2, 1.0)
        
        # Adjust based on description length (longer descriptions often indicate complexity)
        description_length = len(process.description)
        if description_length > 1000:
            complexity_score += 0.5
        elif description_length > 500:
            complexity_score += 0.2
        
        # Adjust based on resource availability
        if resource_availability == "limited":
            complexity_score += 0.5
        elif resource_availability == "abundant":
            complexity_score -= 0.5
        
        # Ensure score is within range (1-5)
        complexity_score = max(1.0, min(5.0, complexity_score))
        
        # Determine implementation difficulty based on complexity score
        if complexity_score <= 2.0:
            implementation_difficulty = "simple"
        elif complexity_score <= 3.0:
            implementation_difficulty = "moderate"
        elif complexity_score <= 4.0:
            implementation_difficulty = "complex"
        elif complexity_score <= 4.5:
            implementation_difficulty = "very_complex"
        else:
            implementation_difficulty = "extreme"
        
        # Generate explanation
        explanation = f"This process has been assigned a complexity score of {complexity_score:.1f} "
        explanation += f"based on {len(process.required_resources)} required resources, "
        explanation += f"{len(process.dependencies)} dependencies, "
        explanation += f"{len(process.inputs)} inputs, {len(process.outputs)} outputs, "
        explanation += f"and a description length of {description_length} characters. "
        
        if resource_availability != "moderate":
            explanation += f"The score was adjusted for {resource_availability} resource availability. "
        
        # Return the analysis
        return {
            "processId": process.process_id,
            "processTitle": process.title,
            "complexityScore": complexity_score,
            "implementationDifficulty": implementation_difficulty,
            "explanation": explanation,
            "requiredResources": process.required_resources,
            "estimatedTime": process.estimated_time,
            "dependencies": process.dependencies,
            "inputs": process.inputs,
            "outputs": process.outputs
        }
    
    def analyze_document(self, document: PDDDocument, resource_availability: str = "moderate") -> Dict[str, Any]:
        """Analyze the complexity of an entire PDD document.
        
        Args:
            document: The document to analyze
            resource_availability: Availability of resources for implementation
            
        Returns:
            Dictionary with document complexity assessment and process analyses
        """
        # Analyze each process
        process_analyses = []
        for process in document.processes:
            process_analysis = self.analyze_process(process, resource_availability)
            process_analyses.append(process_analysis)
        
        # Calculate overall document complexity
        if process_analyses:
            avg_complexity = sum(analysis["complexityScore"] for analysis in process_analyses) / len(process_analyses)
            max_complexity = max(analysis["complexityScore"] for analysis in process_analyses)
        else:
            avg_complexity = 0.0
            max_complexity = 0.0
        
        # Determine overall implementation difficulty
        if avg_complexity <= 2.0:
            overall_difficulty = "simple"
        elif avg_complexity <= 3.0:
            overall_difficulty = "moderate"
        elif avg_complexity <= 4.0:
            overall_difficulty = "complex"
        elif avg_complexity <= 4.5:
            overall_difficulty = "very_complex"
        else:
            overall_difficulty = "extreme"
        
        # Generate document complexity explanation
        if process_analyses:
            explanation = f"This PDD document contains {len(process_analyses)} processes with an average complexity of {avg_complexity:.1f}. "
            explanation += f"The most complex process has a score of {max_complexity:.1f}. "
            explanation += f"The overall implementation difficulty is assessed as '{overall_difficulty}'. "
            
            if max_complexity >= 4.0:
                explanation += "This document contains highly complex processes that may require specialized expertise and significant resources. "
            elif max_complexity >= 3.0:
                explanation += "This document contains moderately complex processes that require good planning and adequate resources. "
            else:
                explanation += "This document contains relatively simple processes that should be straightforward to implement. "
        else:
            explanation = "This PDD document does not contain any processes to analyze."
        
        # Return the complete analysis
        return {
            "documentId": document.doc_id,
            "documentTitle": document.title,
            "averageComplexity": avg_complexity,
            "maxComplexity": max_complexity,
            "overallDifficulty": overall_difficulty,
            "resourceAvailability": resource_availability,
            "explanation": explanation,
            "processAnalyses": process_analyses,
            "businessObjectives": document.business_objectives,
            "successCriteria": document.success_criteria,
            "assumptions": document.assumptions,
            "constraints": document.constraints
        }
