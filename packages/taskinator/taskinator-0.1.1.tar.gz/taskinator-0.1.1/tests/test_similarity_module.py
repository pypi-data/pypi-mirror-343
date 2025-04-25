"""
Unit tests for the TaskSimilarityModule.
"""

import os
import pytest
import numpy as np
from unittest.mock import patch, MagicMock

from taskinator.similarity_module import TaskSimilarityModule, TaskSimilarityResult

# Sample tasks for testing
SAMPLE_TASKS = [
    {
        "id": 1,
        "title": "Implement user authentication",
        "description": "Create login and registration endpoints with JWT tokens",
        "details": "Use bcrypt for password hashing and implement token refresh"
    },
    {
        "id": 2,
        "title": "Set up authentication system",
        "description": "Implement user login and registration with secure tokens",
        "details": "Create JWT authentication with proper validation and refresh mechanism"
    },
    {
        "id": 3,
        "title": "Design database schema",
        "description": "Create tables for user profiles and settings",
        "details": "Define relationships and indexes for optimal performance"
    }
]

class TestTaskSimilarityModule:
    """Tests for the TaskSimilarityModule class."""
    
    def test_init_without_sentence_transformer(self):
        """Test initialization when sentence_transformers is not available."""
        with patch('taskinator.similarity_module.SENTENCE_TRANSFORMER_AVAILABLE', False):
            module = TaskSimilarityModule()
            assert module.model is None
    
    def test_init_with_sentence_transformer(self):
        """Test initialization with sentence_transformers available."""
        with patch('taskinator.similarity_module.SENTENCE_TRANSFORMER_AVAILABLE', True):
            with patch('taskinator.similarity_module.SentenceTransformer') as mock_transformer:
                mock_model = MagicMock()
                mock_transformer.return_value = mock_model
                
                module = TaskSimilarityModule()
                
                # Verify model was initialized
                mock_transformer.assert_called_once_with('all-MiniLM-L6-v2')
                assert module.model == mock_model
    
    def test_generate_embedding(self):
        """Test embedding generation."""
        with patch('taskinator.similarity_module.SENTENCE_TRANSFORMER_AVAILABLE', True):
            with patch('taskinator.similarity_module.SentenceTransformer') as mock_transformer:
                mock_model = MagicMock()
                mock_model.encode.return_value = np.array([0.1, 0.2, 0.3])
                mock_transformer.return_value = mock_model
                
                module = TaskSimilarityModule()
                embedding = module._generate_embedding("test text")
                
                # Verify embedding was generated
                mock_model.encode.assert_called_once_with("test text", convert_to_numpy=True)
                assert isinstance(embedding, np.ndarray)
                assert embedding.tolist() == [0.1, 0.2, 0.3]
    
    def test_calculate_similarity(self):
        """Test similarity calculation."""
        module = TaskSimilarityModule()
        
        # Test with simple vectors
        embedding1 = np.array([1, 0, 0])
        embedding2 = np.array([0, 1, 0])
        similarity = module._calculate_similarity(embedding1, embedding2)
        assert similarity == 0.0
        
        # Test with identical vectors
        embedding1 = np.array([0.5, 0.5, 0.5])
        embedding2 = np.array([0.5, 0.5, 0.5])
        similarity = module._calculate_similarity(embedding1, embedding2)
        assert similarity == 1.0
        
        # Test with similar vectors
        embedding1 = np.array([0.8, 0.1, 0.1])
        embedding2 = np.array([0.7, 0.2, 0.1])
        similarity = module._calculate_similarity(embedding1, embedding2)
        assert 0.9 < similarity < 1.0
    
    def test_compare_tasks(self):
        """Test task comparison."""
        with patch('taskinator.similarity_module.SENTENCE_TRANSFORMER_AVAILABLE', True):
            with patch.object(TaskSimilarityModule, '_generate_embedding') as mock_generate:
                with patch.object(TaskSimilarityModule, '_calculate_similarity') as mock_calculate:
                    # Set up mocks
                    mock_generate.side_effect = lambda text: np.array([0.1, 0.2, 0.3])
                    mock_calculate.return_value = 0.85
                    
                    module = TaskSimilarityModule()
                    result = module.compare_tasks(SAMPLE_TASKS[0], SAMPLE_TASKS[1])
                    
                    # Verify result
                    assert isinstance(result, TaskSimilarityResult)
                    assert result.task_id1 == 1
                    assert result.task_id2 == 2
                    assert result.similarity_score == 0.85
                    assert "highly similar" in result.explanation.lower()
    
    def test_find_similar_tasks(self):
        """Test finding similar tasks."""
        with patch.object(TaskSimilarityModule, 'compare_tasks') as mock_compare:
            # Set up mock to return different similarity scores
            def side_effect(task1, task2):
                # Tasks 1 and 2 are similar, others are not
                if (task1['id'] == 1 and task2['id'] == 2) or (task1['id'] == 2 and task2['id'] == 1):
                    score = 0.85
                else:
                    score = 0.3
                
                return TaskSimilarityResult(
                    task_id1=task1['id'],
                    task_id2=task2['id'],
                    similarity_score=score,
                    explanation=f"Test explanation for {task1['id']} and {task2['id']}"
                )
            
            mock_compare.side_effect = side_effect
            
            module = TaskSimilarityModule()
            results = module.find_similar_tasks(SAMPLE_TASKS, threshold=0.7)
            
            # Verify results
            assert len(results) == 1
            assert results[0].task_id1 == 1
            assert results[0].task_id2 == 2
            assert results[0].similarity_score == 0.85
    
    def test_analyze_task_similarities(self):
        """Test task similarity analysis."""
        with patch.object(TaskSimilarityModule, 'compare_tasks') as mock_compare:
            # Set up mock to return different similarity scores
            def side_effect(task1, task2):
                # Set similarity scores based on task IDs
                if (task1['id'] == 1 and task2['id'] == 2) or (task1['id'] == 2 and task2['id'] == 1):
                    score = 0.85  # High similarity
                elif (task1['id'] == 1 and task2['id'] == 3) or (task1['id'] == 3 and task2['id'] == 1):
                    score = 0.55  # Moderate similarity
                else:
                    score = 0.25  # Low similarity
                
                return TaskSimilarityResult(
                    task_id1=task1['id'],
                    task_id2=task2['id'],
                    similarity_score=score,
                    explanation=f"Test explanation for {task1['id']} and {task2['id']}"
                )
            
            mock_compare.side_effect = side_effect
            
            module = TaskSimilarityModule()
            report = module.analyze_task_similarities(SAMPLE_TASKS)
            
            # Verify report structure
            assert "totalTasksAnalyzed" in report
            assert "totalPairsCompared" in report
            assert "highSimilarity" in report
            assert "moderateSimilarity" in report
            assert "summary" in report
            
            # Verify counts
            assert report["totalTasksAnalyzed"] == 3
            assert report["totalPairsCompared"] == 3
            assert len(report["highSimilarity"]) == 1
            assert len(report["moderateSimilarity"]) == 1
            assert report["summary"]["highSimilarityCount"] == 1
            assert report["summary"]["moderateSimilarityCount"] == 1
