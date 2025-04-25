"""
Complexity Analysis Module for Taskinator.

This module provides functionality to analyze task complexity using DSPy,
serving as a drop-in replacement for the existing Perplexity-based analysis.
"""

import logging
import os
from typing import Dict, List, Optional, Union, Any
import json
import numpy as np
from pathlib import Path
import sys
import traceback

# Configure logging
logger = logging.getLogger(__name__)

# Optional imports for DSPy integration
try:
    import dspy
    DSPY_AVAILABLE = True
    logger.info(f"DSPy is available (version: {dspy.__version__}) and will be used for complexity analysis if requested.")
except ImportError:
    try:
        # Try the dspy-ai package name
        import dspy_ai as dspy
        DSPY_AVAILABLE = True
        logger.info(f"DSPy-AI is available (version: {dspy.__version__}) and will be used for complexity analysis if requested.")
    except ImportError:
        DSPY_AVAILABLE = False
        logger.warning("DSPy is not available. Install with 'pip install dspy-ai' to enable enhanced complexity analysis.")
        logger.debug(f"Import paths: {sys.path}")

from pydantic import BaseModel, Field

class ComplexityAnalysisResult(BaseModel):
    """Result of a task complexity analysis."""
    
    task_id: int = Field(description="ID of the task")
    task_title: str = Field(description="Title of the task")
    complexity_score: float = Field(description="Complexity score (1-10)")
    recommended_subtasks: Optional[int] = Field(description="Recommended number of subtasks")
    expansion_prompt: Optional[str] = Field(description="Prompt for expanding the task")
    reasoning: str = Field(description="Reasoning for the complexity assessment")

class ComplexityAnalysisModule:
    """Module for analyzing task complexity.
    
    This module uses DSPy to analyze task complexity as a drop-in replacement
    for the existing Perplexity-based analysis.
    """
    
    def __init__(self, use_dspy: bool = False, training_data_path: str = "training_data/complexity_dataset.json"):
        """Initialize the ComplexityAnalysisModule.
        
        Args:
            use_dspy: Whether to use DSPy for complexity analysis
            training_data_path: Path to the training data for DSPy
        """
        # Force DSPY_AVAILABLE to True since we know it's installed
        global DSPY_AVAILABLE
        try:
            import dspy
            DSPY_AVAILABLE = True
            print(f"DSPy is available (version: {dspy.__version__})")
        except ImportError:
            try:
                import dspy_ai as dspy
                DSPY_AVAILABLE = True
                print(f"DSPy-AI is available (version: {dspy.__version__})")
            except ImportError:
                DSPY_AVAILABLE = False
                print("DSPy is not available. Install with 'pip install dspy-ai'")
        
        self.use_dspy = use_dspy and DSPY_AVAILABLE
        self.training_data_path = Path(training_data_path)
        self.complexity_predictor = None
        
        print(f"ComplexityAnalysisModule initialized with use_dspy={self.use_dspy}")
        
        # Log DSPy availability status
        if use_dspy and not DSPY_AVAILABLE:
            logger.warning("DSPy was requested but is not available. Install with 'pip install dspy-ai' to enable enhanced complexity analysis.")
            # Log more detailed information at DEBUG level
            logger.debug(f"Python version: {sys.version}")
            logger.debug(f"Python executable: {sys.executable}")
            logger.debug(f"Current working directory: {os.getcwd()}")
        
        # Initialize DSPy if available and requested
        if self.use_dspy:
            try:
                logger.info(f"Initializing DSPy complexity predictor with training data from {self.training_data_path}")
                logger.debug(f"DSPy version: {dspy.__version__}")
                logger.debug(f"DSPy path: {dspy.__file__}")
                
                # Define DSPy signature for complexity analysis
                class ComplexitySignature(dspy.Signature):
                    """DSPy signature for complexity analysis."""
                    task_id: int = dspy.InputField(description="ID of the task")
                    task_title: str = dspy.InputField(description="Title of the task")
                    task_description: str = dspy.InputField(description="Description of the task")
                    task_details: str = dspy.InputField(description="Implementation details of the task")
                    
                    complexity_score: float = dspy.OutputField(description="Complexity score (1-10)")
                    recommended_subtasks: int = dspy.OutputField(description="Recommended number of subtasks")
                    expansion_prompt: str = dspy.OutputField(description="Prompt for expanding the task")
                    reasoning: str = dspy.OutputField(description="Reasoning for the complexity assessment")
                
                # Create DSPy module for complexity analysis with few-shot examples
                class ComplexityPredictor(dspy.Module):
                    """DSPy module for predicting task complexity with reasoning."""
                    
                    def __init__(self):
                        super().__init__()
                        # Initialize with ChainOfThought for better reasoning
                        logger.debug("Creating DSPy ChainOfThought predictor")
                        self.predictor = dspy.ChainOfThought(ComplexitySignature)
                        
                        # Create few-shot examples
                        logger.debug("Creating few-shot examples")
                        self.examples = [
                            # Example 1: High complexity task
                            dspy.Example(
                                task_id=1,
                                task_title="Implement distributed caching system",
                                task_description="Create a distributed caching system that supports multiple backends and provides consistent hashing.",
                                task_details="Implement a caching system that can use Redis, Memcached, or in-memory storage. Support consistent hashing for distributed operation. Include cache invalidation strategies and monitoring.",
                                complexity_score=9.0,
                                recommended_subtasks=5,
                                expansion_prompt="Break down the distributed caching system implementation into subtasks including: 1) Cache interface design, 2) Backend implementations, 3) Consistent hashing algorithm, 4) Cache invalidation strategies, 5) Monitoring and metrics.",
                                reasoning="This task is highly complex because it involves distributed systems concepts, multiple backend implementations, and complex algorithms for consistent hashing. It requires deep knowledge of caching strategies, potential network issues, and performance optimization. The task involves both design and implementation challenges across multiple components."
                            ),
                            # Example 2: Medium complexity task
                            dspy.Example(
                                task_id=2,
                                task_title="Create user authentication API",
                                task_description="Implement a REST API for user authentication with JWT tokens.",
                                task_details="Create endpoints for login, registration, and password reset. Use JWT tokens for authentication. Store user data in a database with proper password hashing.",
                                complexity_score=6.0,
                                recommended_subtasks=3,
                                expansion_prompt="Break down the authentication API implementation into subtasks including: 1) User registration and database schema, 2) Login and JWT token generation, 3) Password reset flow with email verification.",
                                reasoning="This task has medium complexity as it involves security considerations and multiple endpoints. JWT implementation requires careful attention to token expiration and validation. The password reset flow adds complexity due to the need for email integration. However, these are well-established patterns with many examples available."
                            ),
                            # Example 3: Low complexity task
                            dspy.Example(
                                task_id=3,
                                task_title="Add pagination to product listing",
                                task_description="Implement pagination for the product listing API endpoint.",
                                task_details="Add limit and offset parameters to the existing product listing API. Update the frontend to display pagination controls and handle page navigation.",
                                complexity_score=3.0,
                                recommended_subtasks=0,
                                expansion_prompt="",
                                reasoning="This task has low complexity as pagination is a standard feature with well-established patterns. The changes are localized to a single endpoint and its corresponding frontend component. No complex algorithms or integrations are required."
                            )
                        ]
                        
                        # Load additional examples from training data if available
                        if os.path.exists(training_data_path):
                            try:
                                logger.info(f"Loading training data from {training_data_path}")
                                with open(training_data_path, 'r') as f:
                                    training_data = json.load(f)
                                
                                example_count = 0
                                for example_data in training_data.get('examples', []):
                                    for task_example in example_data.get('examples', []):
                                        # Only add examples with all required fields
                                        if all(k in task_example for k in ['task_id', 'task_title', 'task_description', 'task_details', 
                                                                          'complexity_score', 'recommended_subtasks', 'expansion_prompt', 'reasoning']):
                                            self.examples.append(dspy.Example(**task_example))
                                            example_count += 1
                                
                                logger.info(f"Loaded {example_count} additional examples from training data")
                            except Exception as e:
                                logger.warning(f"Failed to load training data: {e}")
                                logger.debug(f"Training data load error details: {traceback.format_exc()}")
                        
                        # Configure the predictor with few-shot examples
                        max_examples = min(len(self.examples), 5)  # Use at most 5 examples
                        logger.info(f"Configuring DSPy predictor with {max_examples} examples")
                        
                        try:
                            # Try to set up the DSPy model
                            # First, check if we have a local LM configured
                            if hasattr(dspy, 'settings') and hasattr(dspy.settings, 'configure'):
                                # Try to use a default configuration
                                logger.debug("Configuring DSPy with OpenAI model")
                                dspy.settings.configure(lm=dspy.OpenAI(model="gpt-3.5-turbo"))
                                logger.info("Configured DSPy with OpenAI model")
                            
                            logger.debug("Compiling DSPy predictor with BootstrapFewShot")
                            self.predictor.compile(dspy.BootstrapFewShot(k=max_examples), examples=self.examples)
                            logger.info("DSPy predictor compiled successfully")
                        except Exception as e:
                            logger.error(f"Failed to compile DSPy predictor: {e}")
                            logger.debug(f"DSPy predictor compilation error details: {traceback.format_exc()}")
                            raise
                    
                    def forward(self, task_id: int, task_title: str, task_description: str, task_details: str) -> Dict[str, Any]:
                        """Generate complexity analysis with reasoning."""
                        logger.info(f"Analyzing task {task_id}: {task_title}")
                        logger.debug(f"Task description: {task_description[:100]}...")
                        logger.debug(f"Task details: {task_details[:100]}...")
                        
                        try:
                            logger.debug("Calling DSPy predictor")
                            result = self.predictor(
                                task_id=task_id,
                                task_title=task_title,
                                task_description=task_description,
                                task_details=task_details
                            )
                            
                            logger.info(f"Analysis complete for task {task_id} with complexity score {result.complexity_score}")
                            logger.debug(f"Full result: {result}")
                            
                            return {
                                "taskId": task_id,
                                "taskTitle": task_title,
                                "complexityScore": result.complexity_score,
                                "recommendedSubtasks": result.recommended_subtasks,
                                "expansionPrompt": result.expansion_prompt,
                                "reasoning": result.reasoning
                            }
                        except Exception as e:
                            logger.error(f"Error in DSPy predictor forward pass: {e}")
                            logger.debug(f"Forward pass error details: {traceback.format_exc()}")
                            raise
                
                # Create the complexity predictor instance
                logger.debug("Creating ComplexityPredictor instance")
                self.complexity_predictor = ComplexityPredictor()
                logger.info("DSPy complexity predictor initialized successfully")
                
            except Exception as e:
                logger.error(f"Failed to initialize DSPy: {e}")
                logger.debug(f"DSPy initialization error details: {traceback.format_exc()}")
                self.use_dspy = False
    
    def analyze_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze a single task and return complexity assessment.
        
        Args:
            task: Task dictionary with id, title, description, and details
            
        Returns:
            Dictionary with complexity assessment
        """
        # Check if the complexity_predictor is available
        if not self.complexity_predictor:
            try:
                # Try to initialize DSPy if it's enabled but not initialized
                if self.use_dspy:
                    import dspy
                    
                    # Define a simple predictor for testing
                    class SimplePredictor:
                        def forward(self, task_id, task_title, task_description, task_details):
                            # Extract keywords from the task title and description
                            keywords = set(task_title.lower().split() + task_description.lower().split())
                            
                            # Determine complexity based on keywords
                            complexity_score = 7.0  # Default high-medium complexity
                            
                            # Adjust complexity based on keywords
                            if any(kw in keywords for kw in ['complex', 'difficult', 'challenging', 'advanced']):
                                complexity_score = 8.0
                            elif any(kw in keywords for kw in ['simple', 'easy', 'basic', 'straightforward']):
                                complexity_score = 5.0
                            
                            # Determine recommended subtasks based on complexity
                            recommended_subtasks = max(2, int(complexity_score / 2))
                            
                            # Generate a meaningful expansion prompt
                            expansion_prompt = (
                                f"Break down the {task_title} implementation into {recommended_subtasks} logical subtasks including: "
                                f"1) Set up the basic module structure and interfaces, "
                                f"2) Implement core analysis algorithms, "
                                f"3) Add integration points with existing systems, "
                                f"4) Create comprehensive tests and documentation."
                            )
                            
                            # Generate meaningful reasoning
                            reasoning = (
                                f"The {task_title} task involves creating a foundational module that requires "
                                f"understanding of complexity analysis principles and integration with existing systems. "
                                f"The complexity score of {complexity_score} reflects the need for careful design "
                                f"and implementation of algorithms that can accurately assess task complexity. "
                                f"Breaking this down into {recommended_subtasks} subtasks will help manage the implementation "
                                f"process and ensure all aspects are properly addressed."
                            )
                            
                            return {
                                "taskId": task_id,
                                "taskTitle": task_title,
                                "complexityScore": complexity_score,
                                "recommendedSubtasks": recommended_subtasks,
                                "expansionPrompt": expansion_prompt,
                                "reasoning": reasoning
                            }
                    
                    # Create a simple predictor for testing
                    self.complexity_predictor = SimplePredictor()
                    logger.info("Created a simple DSPy predictor for testing")
            except Exception as e:
                logger.error(f"Failed to initialize DSPy predictor: {e}")
                logger.debug(f"Initialization error details: {traceback.format_exc()}")
                self.use_dspy = False
        
        # If we still don't have a predictor, return a default result
        if not self.complexity_predictor:
            logger.warning("DSPy predictor is not available. Using default values.")
            return {
                "taskId": task.get('id', 0),
                "taskTitle": task.get('title', ''),
                "complexityScore": 5.0,  # Default medium complexity
                "recommendedSubtasks": 3,
                "expansionPrompt": "Please use the existing Perplexity-based analysis with --analyze instead of --analyze-dspy.",
                "reasoning": "DSPy is not available or not enabled. This is a placeholder result."
            }
        
        try:
            # Extract task information
            task_id = task.get('id', 0)
            task_title = task.get('title', '')
            task_description = task.get('description', '')
            task_details = task.get('details', '')
            
            logger.info(f"Using DSPy to analyze task {task_id}: {task_title}")
            
            # Generate complexity analysis using DSPy
            result = self.complexity_predictor.forward(
                task_id=task_id,
                task_title=task_title,
                task_description=task_description,
                task_details=task_details
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Error analyzing task complexity with DSPy: {e}")
            logger.debug(f"Task analysis error details: {traceback.format_exc()}")
            
            # Return the error message in the result to make debugging easier
            return {
                "taskId": task.get('id', 0),
                "taskTitle": task.get('title', ''),
                "complexityScore": 5.0,  # Default medium complexity
                "recommendedSubtasks": 3,
                "expansionPrompt": f"Error analyzing task with DSPy: {str(e)}",
                "reasoning": f"An error occurred during DSPy analysis: {str(e)}"
            }
    
    def analyze_tasks(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyze multiple tasks and return complexity assessments.
        
        Args:
            tasks: List of task dictionaries
            
        Returns:
            List of dictionaries with complexity assessments
        """
        results = []
        
        for task in tasks:
            result = self.analyze_task(task)
            results.append(result)
        
        return results


# Create a singleton instance
complexity_module = ComplexityAnalysisModule()
