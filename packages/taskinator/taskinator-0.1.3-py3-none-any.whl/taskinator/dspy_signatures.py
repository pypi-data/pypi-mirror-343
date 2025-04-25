"""
DSPy Signatures for Taskinator.

This module defines the DSPy Signatures used for task similarity and complexity analysis.
"""

import logging
from typing import List, Optional, Union

# Set up logging
logger = logging.getLogger(__name__)

# Check if DSPy is available
try:
    import dspy
    DSPY_AVAILABLE = True
    logger.info("DSPy is available")
except ImportError:
    DSPY_AVAILABLE = False
    logger.warning("DSPy is not available. Install with 'pip install dspy-ai'")

# Base class for all signatures
class BaseSignature:
    """Base class for all signature objects."""
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

# Text Similarity Signatures
class TextSimilarityInput(BaseSignature):
    """Base input for text similarity analysis."""
    def __init__(self, text_a=None, text_b=None, cosine_similarity=None, **kwargs):
        self.text_a = text_a
        self.text_b = text_b
        self.cosine_similarity = cosine_similarity
        super().__init__(**kwargs)

class TextSimilarityOutput(BaseSignature):
    """Base output for text similarity analysis."""
    def __init__(self, similarity_score=None, explanation=None, **kwargs):
        self.similarity_score = similarity_score
        self.explanation = explanation
        super().__init__(**kwargs)

# SOP-specific Text Similarity Signatures
class SOPTextSimilarityInput(TextSimilarityInput):
    """Input for SOP text similarity analysis."""
    def __init__(self, text_a=None, text_b=None, cosine_similarity=None, procedure_type="task", **kwargs):
        super().__init__(text_a, text_b, cosine_similarity, **kwargs)
        self.procedure_type = procedure_type

class SOPTextSimilarityOutput(TextSimilarityOutput):
    """Output for SOP text similarity analysis."""
    def __init__(self, similarity_score=None, explanation=None, common_steps=None, divergent_steps=None, **kwargs):
        super().__init__(similarity_score, explanation, **kwargs)
        self.common_steps = common_steps or []
        self.divergent_steps = divergent_steps or []

# PDD-specific Text Similarity Signatures
class PDDTextSimilarityInput(TextSimilarityInput):
    """Input for PDD text similarity analysis."""
    def __init__(self, text_a=None, text_b=None, cosine_similarity=None, domain="software", **kwargs):
        super().__init__(text_a, text_b, cosine_similarity, **kwargs)
        self.domain = domain

class PDDTextSimilarityOutput(TextSimilarityOutput):
    """Output for PDD text similarity analysis."""
    def __init__(self, similarity_score=None, explanation=None, feature_overlap=None, unique_features=None, **kwargs):
        super().__init__(similarity_score, explanation, **kwargs)
        self.feature_overlap = feature_overlap
        self.unique_features = unique_features

# Base Task Complexity Signatures
class ComplexityInput(BaseSignature):
    """Base input for task complexity analysis."""
    def __init__(self, task_id=None, task_title=None, task_description=None, task_details=None, **kwargs):
        self.task_id = task_id
        self.task_title = task_title
        self.task_description = task_description
        self.task_details = task_details
        super().__init__(**kwargs)

class ComplexityOutput(BaseSignature):
    """Base output for task complexity analysis."""
    def __init__(self, complexity_score=None, explanation=None, required_skills=None, 
                 recommended_subtasks=None, expansionPrompt=None, **kwargs):
        self.complexity_score = complexity_score
        self.explanation = explanation
        self.required_skills = required_skills or []
        self.recommended_subtasks = recommended_subtasks
        self.expansionPrompt = expansionPrompt
        super().__init__(**kwargs)

# SOP-specific Complexity Signatures
class SOPComplexityInput(ComplexityInput):
    """Input for SOP task complexity analysis."""
    def __init__(self, task_id=None, task_title=None, task_description=None, task_details=None,
                 procedure_type="task", audience_expertise="intermediate", **kwargs):
        super().__init__(task_id, task_title, task_description, task_details, **kwargs)
        self.procedure_type = procedure_type
        self.audience_expertise = audience_expertise

class SOPComplexityOutput(ComplexityOutput):
    """Output for SOP task complexity analysis."""
    def __init__(self, complexity_score=None, explanation=None, required_skills=None,
                 recommended_subtasks=None, expansionPrompt=None, estimated_time=None, prerequisites=None, **kwargs):
        super().__init__(complexity_score, explanation, required_skills, recommended_subtasks, expansionPrompt, **kwargs)
        self.estimated_time = estimated_time
        self.prerequisites = prerequisites or []

# PDD-specific Complexity Signatures
class PDDComplexityInput(ComplexityInput):
    """Input for PDD task complexity analysis."""
    def __init__(self, task_id=None, task_title=None, task_description=None, task_details=None,
                 product_domain="software", development_stage="implementation", **kwargs):
        super().__init__(task_id, task_title, task_description, task_details, **kwargs)
        self.product_domain = product_domain
        self.development_stage = development_stage

class PDDComplexityOutput(ComplexityOutput):
    """Output for PDD task complexity analysis."""
    def __init__(self, complexity_score=None, explanation=None, required_skills=None,
                 recommended_subtasks=None, expansionPrompt=None, technical_dependencies=None, risk_assessment=None, **kwargs):
        super().__init__(complexity_score, explanation, required_skills, recommended_subtasks, expansionPrompt, **kwargs)
        self.technical_dependencies = technical_dependencies or []
        self.risk_assessment = risk_assessment

# Define Signature classes if DSPy is available
if DSPY_AVAILABLE:
    # Define wrapper classes that use DSPy signatures
    class TextSimilaritySignature(dspy.Signature):
        """Base signature for text similarity analysis."""
        def __init__(self):
            pass

    class SOPTextSimilaritySignature(dspy.Signature):
        """Signature for SOP text similarity analysis."""
        def __init__(self):
            pass

    class PDDTextSimilaritySignature(dspy.Signature):
        """Signature for PDD text similarity analysis."""
        def __init__(self):
            pass

    class ComplexitySignature(dspy.Signature):
        """Base signature for task complexity analysis."""
        def __init__(self):
            pass

    class SOPComplexitySignature(dspy.Signature):
        """Signature for SOP task complexity analysis."""
        def __init__(self):
            pass

    class PDDComplexitySignature(dspy.Signature):
        """Signature for PDD task complexity analysis."""
        def __init__(self):
            pass
else:
    # Define placeholder classes when DSPy is not available
    class TextSimilaritySignature(BaseSignature):
        """Placeholder for TextSimilaritySignature when DSPy is not available."""
        pass

    class SOPTextSimilaritySignature(BaseSignature):
        """Placeholder for SOPTextSimilaritySignature when DSPy is not available."""
        pass

    class PDDTextSimilaritySignature(BaseSignature):
        """Placeholder for PDDTextSimilaritySignature when DSPy is not available."""
        pass

    class ComplexitySignature(BaseSignature):
        """Placeholder for ComplexitySignature when DSPy is not available."""
        pass

    class SOPComplexitySignature(BaseSignature):
        """Placeholder for SOPComplexitySignature when DSPy is not available."""
        pass

    class PDDComplexitySignature(BaseSignature):
        """Placeholder for PDDComplexitySignature when DSPy is not available."""
        pass
