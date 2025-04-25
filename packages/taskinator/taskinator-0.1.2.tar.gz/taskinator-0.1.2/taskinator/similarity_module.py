"""
Task Similarity Module for Taskinator.

This module provides functionality to compare tasks based on semantic similarity
using embedding models. It can be used to identify similar tasks, detect duplicates,
and help with task organization.
"""

import logging
import os
from typing import Dict, List, Optional, Tuple, Union, Any
import json
import numpy as np
from pathlib import Path

# Optional imports for DSPy integration
try:
    import dspy
    DSPY_AVAILABLE = True
except ImportError:
    DSPY_AVAILABLE = False

# Import for embedding model
try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMER_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMER_AVAILABLE = False

from pydantic import BaseModel, Field

# Configure logging
logger = logging.getLogger(__name__)

class TaskSimilarityResult(BaseModel):
    """Result of a task similarity comparison."""
    
    task_id1: int = Field(description="ID of the first task")
    task_id2: int = Field(description="ID of the second task")
    similarity_score: float = Field(description="Similarity score between 0 and 1")
    explanation: str = Field(description="Explanation of the similarity")

class TaskSimilarityModule:
    """Module for comparing tasks based on semantic similarity.
    
    This module uses the SentenceTransformer model to generate embeddings
    for task descriptions and calculate similarity scores between them.
    
    When the --optimize flag is provided, it also uses DSPy for enhanced
    similarity analysis with reasoning.
    """
    
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2', use_dspy: bool = False):
        """Initialize the TaskSimilarityModule.
        
        Args:
            model_name: Name of the SentenceTransformer model to use
            use_dspy: Whether to use DSPy for enhanced similarity analysis
        """
        self.use_dspy = use_dspy and DSPY_AVAILABLE
        
        # Check if SentenceTransformer is available
        if not SENTENCE_TRANSFORMER_AVAILABLE:
            logger.warning(
                "SentenceTransformer is not installed. Please install it with: "
                "pip install sentence-transformers"
            )
            self.model = None
        else:
            try:
                self.model = SentenceTransformer(model_name)
                logger.info(f"Initialized SentenceTransformer with model: {model_name}")
            except Exception as e:
                logger.error(f"Failed to initialize SentenceTransformer: {e}")
                self.model = None
        
        # Initialize DSPy if available and requested
        if self.use_dspy:
            try:
                # Define DSPy signature for similarity analysis
                class SimilaritySignature(dspy.Signature):
                    """DSPy signature for similarity analysis."""
                    text1: str = dspy.InputField(description="First text to compare")
                    text2: str = dspy.InputField(description="Second text to compare")
                    cosine_similarity: float = dspy.InputField(description="Cosine similarity score between the texts")
                    
                    similarity_assessment: str = dspy.OutputField(description="Assessment of how similar the texts are")
                    explanation: str = dspy.OutputField(description="Detailed explanation of the similarities and differences")
                
                # Create DSPy module for similarity analysis with few-shot examples
                class SimilarityPredictor(dspy.Module):
                    """DSPy module for predicting similarity with reasoning."""
                    
                    def __init__(self):
                        super().__init__()
                        # Initialize with ChainOfThought for better reasoning
                        self.predictor = dspy.ChainOfThought(SimilaritySignature)
                        
                        # Create few-shot examples to guide the model
                        self.examples = [
                            # Example 1: Similar tasks
                            dspy.Example(
                                text1="Implement user authentication system with JWT tokens. Create login, registration, and password reset endpoints. Integrate with the existing user database and ensure proper validation.",
                                text2="Create authentication API endpoints for user login and registration. Implement JWT token generation and validation. Add password reset functionality with email verification.",
                                cosine_similarity=0.85,
                                similarity_assessment="These tasks are highly similar and likely have overlapping requirements.",
                                explanation="Both tasks involve implementing authentication functionality including login, registration, and password reset. Both specifically mention JWT tokens. The core functionality is the same, though the second task explicitly mentions email verification for password reset while the first mentions integration with an existing database. These tasks could potentially be merged into a single task with clear subtasks."
                            ),
                            # Example 2: Dissimilar tasks
                            dspy.Example(
                                text1="Design and implement the database schema for storing user profiles. Create tables for user information, preferences, and activity history with proper relationships and indexes.",
                                text2="Develop the frontend dashboard UI with React components. Implement data visualization charts and responsive layout for mobile and desktop views.",
                                cosine_similarity=0.25,
                                similarity_assessment="These tasks are distinct with minimal similarity.",
                                explanation="These tasks target completely different aspects of the system. The first task focuses on backend database design for user data storage, while the second is about frontend UI development with React. The only slight connection is that the frontend might eventually display user data from the database, but the tasks themselves require different skills and would be implemented separately by different team members."
                            )
                        ]
                        
                        # Configure the predictor with few-shot examples
                        # Note: In a future enhancement, we could implement a training pipeline
                        # to fine-tune this model with more domain-specific examples
                        self.predictor.compile(dspy.BootstrapFewShot(k=2), examples=self.examples)
                    
                    def forward(self, text1: str, text2: str, cosine_similarity: float) -> Dict[str, Any]:
                        """Generate similarity assessment with reasoning."""
                        result = self.predictor(
                            text1=text1,
                            text2=text2,
                            cosine_similarity=cosine_similarity
                        )
                        return {
                            "similarity_assessment": result.similarity_assessment,
                            "explanation": result.explanation
                        }
                
                self.similarity_predictor = SimilarityPredictor()
                logger.info("Initialized DSPy similarity predictor with few-shot examples")
                
                # Note: Future enhancement could include a method to train the model with more examples:
                # def train_with_examples(self, examples: List[Dict[str, Any]]) -> None:
                #     """Train the similarity predictor with additional examples."""
                #     # Convert examples to DSPy Example format
                #     dspy_examples = [dspy.Example(**example) for example in examples]
                #     # Combine with existing examples
                #     all_examples = self.similarity_predictor.examples + dspy_examples
                #     # Recompile the predictor with the expanded example set
                #     self.similarity_predictor.predictor.compile(
                #         dspy.BootstrapFewShot(k=min(len(all_examples), 5)), 
                #         examples=all_examples
                #     )
                
            except Exception as e:
                logger.error(f"Failed to initialize DSPy: {e}")
                self.use_dspy = False
    
    def _generate_embedding(self, text: str) -> Optional[np.ndarray]:
        """Generate embedding for the given text.
        
        Args:
            text: Text to generate embedding for
            
        Returns:
            Embedding vector or None if model is not available
        """
        if not self.model:
            logger.warning("SentenceTransformer model not available")
            return None
        
        if not text or not isinstance(text, str):
            logger.warning(f"Invalid text input: {text}")
            return None
        
        try:
            # Generate embedding
            embedding = self.model.encode(text, convert_to_numpy=True)
            return embedding
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            return None
    
    def _calculate_similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """Calculate cosine similarity between two embedding vectors.
        
        Args:
            embedding1: First embedding vector
            embedding2: Second embedding vector
            
        Returns:
            Cosine similarity score between 0 and 1
        """
        if embedding1 is None or embedding2 is None:
            return 0.0
        
        try:
            # Calculate cosine similarity
            dot_product = np.dot(embedding1, embedding2)
            norm1 = np.linalg.norm(embedding1)
            norm2 = np.linalg.norm(embedding2)
            
            # Handle zero vectors
            if norm1 == 0 or norm2 == 0:
                return 0.0
            
            similarity = dot_product / (norm1 * norm2)
            
            # Ensure the result is between 0 and 1
            return max(0.0, min(1.0, similarity))
        except Exception as e:
            logger.error(f"Error calculating similarity: {e}")
            return 0.0
    
    def compare_tasks(self, task1: Dict[str, Any], task2: Dict[str, Any]) -> TaskSimilarityResult:
        """Compare two tasks and return similarity score with explanation.
        
        Args:
            task1: First task dictionary
            task2: Second task dictionary
            
        Returns:
            TaskSimilarityResult with similarity score and explanation
        """
        # Extract task IDs
        task_id1 = task1.get('id', 0)
        task_id2 = task2.get('id', 0)
        
        # Combine title, description, and details for better comparison
        text1 = f"{task1.get('title', '')} {task1.get('description', '')} {task1.get('details', '')}"
        text2 = f"{task2.get('title', '')} {task2.get('description', '')} {task2.get('details', '')}"
        
        # Generate embeddings
        embedding1 = self._generate_embedding(text1)
        embedding2 = self._generate_embedding(text2)
        
        # Calculate similarity
        similarity_score = self._calculate_similarity(embedding1, embedding2)
        
        # Generate explanation
        if self.use_dspy:
            try:
                # Use DSPy for enhanced explanation
                result = self.similarity_predictor.forward(
                    text1=text1,
                    text2=text2,
                    cosine_similarity=similarity_score
                )
                explanation = result.get('explanation', '')
            except Exception as e:
                logger.error(f"Error using DSPy for explanation: {e}")
                explanation = self._generate_basic_explanation(similarity_score, task1, task2)
        else:
            explanation = self._generate_basic_explanation(similarity_score, task1, task2)
        
        return TaskSimilarityResult(
            task_id1=task_id1,
            task_id2=task_id2,
            similarity_score=similarity_score,
            explanation=explanation
        )
    
    def _generate_basic_explanation(self, similarity_score: float, task1: Dict[str, Any], task2: Dict[str, Any]) -> str:
        """Generate a basic explanation of the similarity score.
        
        Args:
            similarity_score: Similarity score between 0 and 1
            task1: First task dictionary
            task2: Second task dictionary
            
        Returns:
            Basic explanation of the similarity
        """
        if similarity_score >= 0.9:
            return f"Tasks {task1.get('id')} and {task2.get('id')} are extremely similar and may be duplicates."
        elif similarity_score >= 0.7:
            return f"Tasks {task1.get('id')} and {task2.get('id')} are highly similar and may have overlapping requirements."
        elif similarity_score >= 0.5:
            return f"Tasks {task1.get('id')} and {task2.get('id')} have moderate similarity and may be related."
        elif similarity_score >= 0.3:
            return f"Tasks {task1.get('id')} and {task2.get('id')} have low similarity but may share some concepts."
        else:
            return f"Tasks {task1.get('id')} and {task2.get('id')} are distinct with minimal similarity."
    
    def find_similar_tasks(self, tasks: List[Dict[str, Any]], threshold: float = 0.7) -> List[TaskSimilarityResult]:
        """Find similar tasks in a list of tasks.
        
        Args:
            tasks: List of task dictionaries
            threshold: Similarity threshold (0-1) for considering tasks similar
            
        Returns:
            List of TaskSimilarityResult for similar task pairs
        """
        similar_pairs = []
        
        # Compare each pair of tasks
        for i in range(len(tasks)):
            for j in range(i + 1, len(tasks)):
                result = self.compare_tasks(tasks[i], tasks[j])
                if result.similarity_score >= threshold:
                    similar_pairs.append(result)
        
        # Sort by similarity score (highest first)
        similar_pairs.sort(key=lambda x: x.similarity_score, reverse=True)
        
        return similar_pairs
    
    def analyze_task_similarities(self, tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze similarities between all tasks and generate a report.
        
        Args:
            tasks: List of task dictionaries
            
        Returns:
            Dictionary with similarity analysis results
        """
        # Find all similar task pairs
        all_pairs = []
        for i in range(len(tasks)):
            for j in range(i + 1, len(tasks)):
                result = self.compare_tasks(tasks[i], tasks[j])
                all_pairs.append(result)
        
        # Sort by similarity score (highest first)
        all_pairs.sort(key=lambda x: x.similarity_score, reverse=True)
        
        # Group results by similarity level
        very_high = [p for p in all_pairs if p.similarity_score >= 0.9]
        high = [p for p in all_pairs if 0.7 <= p.similarity_score < 0.9]
        moderate = [p for p in all_pairs if 0.5 <= p.similarity_score < 0.7]
        
        # Generate report
        report = {
            "totalTasksAnalyzed": len(tasks),
            "totalPairsCompared": len(all_pairs),
            "potentialDuplicates": [p.dict() for p in very_high],
            "highSimilarity": [p.dict() for p in high],
            "moderateSimilarity": [p.dict() for p in moderate],
            "summary": {
                "potentialDuplicatesCount": len(very_high),
                "highSimilarityCount": len(high),
                "moderateSimilarityCount": len(moderate),
            }
        }
        
        return report
