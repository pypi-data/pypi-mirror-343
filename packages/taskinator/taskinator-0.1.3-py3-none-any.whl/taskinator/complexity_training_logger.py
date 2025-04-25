"""
Complexity Analysis Training Logger

This module provides functionality to log inputs and outputs from the existing
Perplexity-based complexity analysis to create training data for the DSPy version.
"""

import json
import os
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

# Configure logging
logger = logging.getLogger(__name__)

class ComplexityTrainingLogger:
    """Logger for collecting training data for the ComplexityAnalysisModule.
    
    This class records the inputs and outputs from the existing Perplexity-based
    complexity analysis to create training data for the DSPy version.
    """
    
    def __init__(self, log_dir: str = "training_data/complexity"):
        """Initialize the ComplexityTrainingLogger.
        
        Args:
            log_dir: Directory to store the training data logs
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.current_session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        logger.info(f"Initialized ComplexityTrainingLogger with session ID: {self.current_session_id}")
    
    def log_analysis_request(
        self,
        tasks: List[Dict[str, Any]],
        prompt: str,
        use_research: bool,
        model: Optional[str] = None
    ) -> str:
        """Log a complexity analysis request.
        
        Args:
            tasks: List of tasks to analyze
            prompt: The prompt sent to the AI model
            use_research: Whether research was used
            model: The model used for analysis
            
        Returns:
            The ID of the logged request
        """
        request_id = f"{self.current_session_id}_{len(os.listdir(self.log_dir))}"
        
        request_data = {
            "request_id": request_id,
            "timestamp": datetime.now().isoformat(),
            "tasks": tasks,
            "prompt": prompt,
            "use_research": use_research,
            "model": model,
        }
        
        request_file = self.log_dir / f"{request_id}_request.json"
        with open(request_file, 'w') as f:
            json.dump(request_data, f, indent=2)
        
        logger.info(f"Logged complexity analysis request: {request_id}")
        return request_id
    
    def log_analysis_response(
        self,
        request_id: str,
        response: List[Dict[str, Any]],
        raw_response: Optional[str] = None,
        error: Optional[str] = None
    ) -> None:
        """Log a complexity analysis response.
        
        Args:
            request_id: The ID of the corresponding request
            response: The parsed response from the AI model
            raw_response: The raw response from the AI model
            error: Any error that occurred during analysis
        """
        response_data = {
            "request_id": request_id,
            "timestamp": datetime.now().isoformat(),
            "response": response,
            "raw_response": raw_response,
            "error": error,
        }
        
        response_file = self.log_dir / f"{request_id}_response.json"
        with open(response_file, 'w') as f:
            json.dump(response_data, f, indent=2)
        
        logger.info(f"Logged complexity analysis response for request: {request_id}")
    
    def create_training_example(self, request_id: str) -> Dict[str, Any]:
        """Create a training example from a logged request and response.
        
        Args:
            request_id: The ID of the request to create a training example from
            
        Returns:
            A training example for DSPy
        """
        request_file = self.log_dir / f"{request_id}_request.json"
        response_file = self.log_dir / f"{request_id}_response.json"
        
        if not request_file.exists() or not response_file.exists():
            logger.error(f"Request or response file not found for ID: {request_id}")
            return {}
        
        try:
            with open(request_file, 'r') as f:
                request_data = json.load(f)
            
            with open(response_file, 'r') as f:
                response_data = json.load(f)
            
            # Extract the tasks and responses
            tasks = request_data.get("tasks", [])
            responses = response_data.get("response", [])
            
            # Create training examples for each task
            examples = []
            for task in tasks:
                # Find the corresponding response
                response = next((r for r in responses if r.get("taskId") == task.get("id")), None)
                
                if response:
                    example = {
                        "task_id": task.get("id"),
                        "task_title": task.get("title"),
                        "task_description": task.get("description"),
                        "task_details": task.get("details"),
                        "complexity_score": response.get("complexityScore"),
                        "recommended_subtasks": response.get("recommendedSubtasks"),
                        "expansion_prompt": response.get("expansionPrompt"),
                        "reasoning": response.get("reasoning"),
                    }
                    examples.append(example)
            
            return {
                "request_id": request_id,
                "timestamp": datetime.now().isoformat(),
                "use_research": request_data.get("use_research", False),
                "examples": examples,
            }
            
        except Exception as e:
            logger.error(f"Error creating training example: {e}")
            return {}
    
    def export_training_dataset(self, output_file: str = "training_data/complexity_dataset.json") -> None:
        """Export all logged data as a training dataset.
        
        Args:
            output_file: Path to save the training dataset
        """
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # Find all request files
        request_files = list(self.log_dir.glob("*_request.json"))
        
        # Create training examples for each request
        training_examples = []
        for request_file in request_files:
            request_id = request_file.stem.split("_request")[0]
            example = self.create_training_example(request_id)
            if example:
                training_examples.append(example)
        
        # Save the training dataset
        with open(output_file, 'w') as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "examples": training_examples,
            }, f, indent=2)
        
        logger.info(f"Exported {len(training_examples)} training examples to {output_file}")


# Create a singleton instance
complexity_logger = ComplexityTrainingLogger()
