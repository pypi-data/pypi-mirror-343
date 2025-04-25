"""
SOP Patterns for Taskinator.

This module defines standard patterns for SOPs that can be applied across different tasks.
"""

from enum import Enum
from typing import Dict, List, Any

class SOPPatternType(str, Enum):
    """Types of SOP patterns."""
    DESIGN = "design"
    IMPLEMENTATION = "implementation"
    TESTING = "testing"
    DOCUMENTATION = "documentation"
    INTEGRATION = "integration"
    DEPLOYMENT = "deployment"
    MAINTENANCE = "maintenance"
    ANALYSIS = "analysis"
    RESEARCH = "research"


# Standard SOP patterns that can be applied to different tasks
SOP_PATTERNS = {
    SOPPatternType.DESIGN: {
        "title": "System Design Procedure",
        "description": "Standard procedure for designing new system components",
        "applicability": [
            "tasks containing 'design', 'architect', 'structure', 'model'",
            "tasks with high complexity scores (7+)",
            "tasks that create new system components"
        ],
        "steps": [
            {
                "title": "Requirements Analysis",
                "description": "Analyze and document the requirements for the system component",
                "order": 1,
                "estimated_time": "2-4 hours",
                "prerequisites": [],
                "required_skills": ["Requirements Analysis", "System Design"]
            },
            {
                "title": "Architecture Planning",
                "description": "Define the architecture, interfaces, and integration points with existing systems",
                "order": 2,
                "estimated_time": "4-8 hours",
                "prerequisites": ["step1"],
                "required_skills": ["System Architecture", "Interface Design"]
            },
            {
                "title": "Component Design",
                "description": "Design the internal structure, data models, and algorithms for the component",
                "order": 3,
                "estimated_time": "8-16 hours",
                "prerequisites": ["step2"],
                "required_skills": ["Software Design", "Data Modeling"]
            },
            {
                "title": "Design Review",
                "description": "Review the design with stakeholders and incorporate feedback",
                "order": 4,
                "estimated_time": "2-4 hours",
                "prerequisites": ["step3"],
                "required_skills": ["Technical Communication", "Design Review"]
            },
            {
                "title": "Design Documentation",
                "description": "Document the final design for implementation",
                "order": 5,
                "estimated_time": "4-8 hours",
                "prerequisites": ["step4"],
                "required_skills": ["Technical Writing", "Documentation"]
            }
        ]
    },
    
    SOPPatternType.IMPLEMENTATION: {
        "title": "System Implementation Procedure",
        "description": "Standard procedure for implementing system components",
        "applicability": [
            "tasks containing 'implement', 'build', 'develop', 'code', 'create'",
            "tasks that follow design tasks",
            "tasks that produce working code"
        ],
        "steps": [
            {
                "title": "Environment Setup",
                "description": "Set up the development environment and required dependencies",
                "order": 1,
                "estimated_time": "1-2 hours",
                "prerequisites": [],
                "required_skills": ["Development Environment", "Dependency Management"]
            },
            {
                "title": "Core Implementation",
                "description": "Implement the core functionality of the component",
                "order": 2,
                "estimated_time": "8-16 hours",
                "prerequisites": ["step1"],
                "required_skills": ["Software Development", "Programming"]
            },
            {
                "title": "Unit Testing",
                "description": "Create and run unit tests for the implemented functionality",
                "order": 3,
                "estimated_time": "4-8 hours",
                "prerequisites": ["step2"],
                "required_skills": ["Unit Testing", "Test Design"]
            },
            {
                "title": "Code Review",
                "description": "Conduct a code review and address feedback",
                "order": 4,
                "estimated_time": "2-4 hours",
                "prerequisites": ["step3"],
                "required_skills": ["Code Review", "Refactoring"]
            },
            {
                "title": "Integration Testing",
                "description": "Test the component with other system components",
                "order": 5,
                "estimated_time": "4-8 hours",
                "prerequisites": ["step4"],
                "required_skills": ["Integration Testing", "System Testing"]
            }
        ]
    },
    
    SOPPatternType.TESTING: {
        "title": "System Testing Procedure",
        "description": "Standard procedure for testing system components",
        "applicability": [
            "tasks containing 'test', 'verify', 'validate', 'quality'",
            "tasks that follow implementation tasks",
            "tasks focused on quality assurance"
        ],
        "steps": [
            {
                "title": "Test Planning",
                "description": "Define the test strategy, scope, and test cases",
                "order": 1,
                "estimated_time": "2-4 hours",
                "prerequisites": [],
                "required_skills": ["Test Planning", "Test Strategy"]
            },
            {
                "title": "Test Environment Setup",
                "description": "Set up the test environment and test data",
                "order": 2,
                "estimated_time": "2-4 hours",
                "prerequisites": ["step1"],
                "required_skills": ["Test Environment", "Test Data Management"]
            },
            {
                "title": "Test Execution",
                "description": "Execute the test cases and document results",
                "order": 3,
                "estimated_time": "4-8 hours",
                "prerequisites": ["step2"],
                "required_skills": ["Test Execution", "Defect Reporting"]
            },
            {
                "title": "Defect Resolution",
                "description": "Address and verify fixes for identified defects",
                "order": 4,
                "estimated_time": "4-8 hours",
                "prerequisites": ["step3"],
                "required_skills": ["Debugging", "Defect Management"]
            },
            {
                "title": "Test Report Generation",
                "description": "Generate and communicate test results and quality metrics",
                "order": 5,
                "estimated_time": "2-4 hours",
                "prerequisites": ["step4"],
                "required_skills": ["Reporting", "Technical Communication"]
            }
        ]
    },
    
    SOPPatternType.ANALYSIS: {
        "title": "System Analysis Procedure",
        "description": "Standard procedure for analyzing system requirements and data",
        "applicability": [
            "tasks containing 'analyze', 'assess', 'evaluate', 'research'",
            "tasks that involve data processing or algorithm development",
            "tasks that require understanding complex domains"
        ],
        "steps": [
            {
                "title": "Define Analysis Objectives",
                "description": "Clearly define the objectives and scope of the analysis",
                "order": 1,
                "estimated_time": "2-4 hours",
                "prerequisites": [],
                "required_skills": ["Requirements Analysis", "Scope Definition"]
            },
            {
                "title": "Data Collection",
                "description": "Gather and organize the data needed for analysis",
                "order": 2,
                "estimated_time": "4-8 hours",
                "prerequisites": ["step1"],
                "required_skills": ["Data Collection", "Data Organization"]
            },
            {
                "title": "Data Processing and Analysis",
                "description": "Process and analyze the data using appropriate techniques",
                "order": 3,
                "estimated_time": "8-16 hours",
                "prerequisites": ["step2"],
                "required_skills": ["Data Analysis", "Statistical Methods"]
            },
            {
                "title": "Pattern Identification",
                "description": "Identify patterns, trends, and insights from the analysis",
                "order": 4,
                "estimated_time": "4-8 hours",
                "prerequisites": ["step3"],
                "required_skills": ["Pattern Recognition", "Critical Thinking"]
            },
            {
                "title": "Findings Documentation",
                "description": "Document and communicate the analysis findings and recommendations",
                "order": 5,
                "estimated_time": "4-8 hours",
                "prerequisites": ["step4"],
                "required_skills": ["Technical Writing", "Data Visualization"]
            }
        ]
    },
    
    SOPPatternType.INTEGRATION: {
        "title": "System Integration Procedure",
        "description": "Standard procedure for integrating system components",
        "applicability": [
            "tasks containing 'integrate', 'connect', 'interface', 'plugin'",
            "tasks that involve combining multiple components",
            "tasks that require working with external systems"
        ],
        "steps": [
            {
                "title": "Integration Planning",
                "description": "Define the integration approach, interfaces, and dependencies",
                "order": 1,
                "estimated_time": "2-4 hours",
                "prerequisites": [],
                "required_skills": ["Integration Planning", "System Architecture"]
            },
            {
                "title": "Interface Implementation",
                "description": "Implement the interfaces required for integration",
                "order": 2,
                "estimated_time": "4-8 hours",
                "prerequisites": ["step1"],
                "required_skills": ["API Development", "Interface Design"]
            },
            {
                "title": "Component Connection",
                "description": "Connect the components and establish communication",
                "order": 3,
                "estimated_time": "4-8 hours",
                "prerequisites": ["step2"],
                "required_skills": ["System Integration", "Debugging"]
            },
            {
                "title": "Integration Testing",
                "description": "Test the integrated components to ensure proper functioning",
                "order": 4,
                "estimated_time": "4-8 hours",
                "prerequisites": ["step3"],
                "required_skills": ["Integration Testing", "System Testing"]
            },
            {
                "title": "Integration Documentation",
                "description": "Document the integration details and usage instructions",
                "order": 5,
                "estimated_time": "2-4 hours",
                "prerequisites": ["step4"],
                "required_skills": ["Technical Writing", "Documentation"]
            }
        ]
    }
}


def get_pattern_for_task(task_title: str, task_description: str, complexity: float) -> Dict[str, Any]:
    """Determine the appropriate SOP pattern for a given task.
    
    Args:
        task_title: Title of the task
        task_description: Description of the task
        complexity: Complexity score of the task
        
    Returns:
        The most appropriate SOP pattern
    """
    # Combine title and description for keyword matching
    text = (task_title + " " + task_description).lower()
    
    # Check for design tasks
    if any(keyword in text for keyword in ["design", "architect", "structure", "model"]) or complexity >= 7:
        return SOP_PATTERNS[SOPPatternType.DESIGN]
    
    # Check for implementation tasks
    if any(keyword in text for keyword in ["implement", "build", "develop", "code", "create"]):
        return SOP_PATTERNS[SOPPatternType.IMPLEMENTATION]
    
    # Check for testing tasks
    if any(keyword in text for keyword in ["test", "verify", "validate", "quality"]):
        return SOP_PATTERNS[SOPPatternType.TESTING]
    
    # Check for analysis tasks
    if any(keyword in text for keyword in ["analyze", "assess", "evaluate", "research"]):
        return SOP_PATTERNS[SOPPatternType.ANALYSIS]
    
    # Check for integration tasks
    if any(keyword in text for keyword in ["integrate", "connect", "interface", "plugin"]):
        return SOP_PATTERNS[SOPPatternType.INTEGRATION]
    
    # Default to implementation if no clear pattern is found
    return SOP_PATTERNS[SOPPatternType.IMPLEMENTATION]


def get_all_pattern_types() -> List[str]:
    """Get a list of all available SOP pattern types.
    
    Returns:
        List of pattern type names
    """
    return [pattern_type.value for pattern_type in SOPPatternType]


def get_pattern_by_type(pattern_type: str) -> Dict[str, Any]:
    """Get an SOP pattern by its type.
    
    Args:
        pattern_type: Type of the pattern
        
    Returns:
        The SOP pattern
    """
    try:
        return SOP_PATTERNS[SOPPatternType(pattern_type)]
    except (KeyError, ValueError):
        # Return implementation as default if pattern type is not found
        return SOP_PATTERNS[SOPPatternType.IMPLEMENTATION]
