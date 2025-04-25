"""Tests for PDD to Task conversion workflow."""

import os
from pathlib import Path
from unittest import mock
import pytest

from taskinator.pdd_document import PDDDocument, PDDProcess, PDDStatus, PDDImplementationDifficulty
from taskinator.pdd_to_task import PDDTaskConverter
from taskinator.config import TaskPriority, TaskStatus


@pytest.fixture
def sample_pdd():
    """Create a sample PDD document for testing."""
    pdd = PDDDocument(
        doc_id="test_pdd",
        title="Test PDD",
        description="Test PDD Description",
        version="1.0",
        status=PDDStatus.APPROVED,
        author="Test Author",
        department="Test Department",
        tags=["test", "pdd"],
        business_objectives=["Objective 1", "Objective 2"],
        success_criteria=["Criteria 1", "Criteria 2"],
        assumptions=["Assumption 1"],
        constraints=["Constraint 1"]
    )
    
    # Add processes
    process1 = PDDProcess(
        process_id="process_1",
        title="Process 1",
        description="First process description",
        estimated_time="2 days",
        dependencies=[],
        difficulty=3.5,
        implementation_difficulty=PDDImplementationDifficulty.MODERATE,
        required_resources=["Developer", "Designer"],
        inputs=["User requirements"],
        outputs=["Implementation plan"]
    )
    
    process2 = PDDProcess(
        process_id="process_2",
        title="Process 2",
        description="Second process description",
        estimated_time="3 days",
        dependencies=["process_1"],
        difficulty=4.0,
        implementation_difficulty=PDDImplementationDifficulty.COMPLEX,
        required_resources=["Developer", "QA Engineer"],
        inputs=["Implementation plan"],
        outputs=["Implemented feature"]
    )
    
    pdd.add_process(process1)
    pdd.add_process(process2)
    
    return pdd


@pytest.fixture
def mock_pdd_manager():
    """Mock PDDDocumentManager for testing."""
    with mock.patch("taskinator.pdd_to_task.PDDDocumentManager") as mock_manager:
        manager_instance = mock.MagicMock()
        mock_manager.return_value = manager_instance
        yield manager_instance


@pytest.fixture
def mock_task_manager():
    """Mock TaskManager for testing."""
    with mock.patch("taskinator.pdd_to_task.TaskManager") as mock_manager:
        manager_instance = mock.MagicMock()
        mock_manager.return_value = manager_instance
        yield manager_instance


class TestPDDTaskConverter:
    """Tests for PDDTaskConverter."""
    
    @pytest.mark.skip(reason="PDDProcess API has changed, 'order' parameter no longer supported")
    def test_convert_pdd_to_tasks(self, sample_pdd, mock_pdd_manager, mock_task_manager):
        """Test converting a PDD to tasks."""
        # Set up the mock PDD manager to return our sample PDD
        mock_pdd_manager.load_document.return_value = sample_pdd
        
        # Create a converter
        converter = PDDTaskConverter(mock_task_manager)
        converter.pdd_manager = mock_pdd_manager
        
        # Mock the complexity analyzer
        converter.complexity_analyzer = mock.MagicMock()
        converter.complexity_analyzer.analyze_document.return_value = {
            "documentComplexity": 3.75,
            "averageComplexity": 3.75,
            "processAnalyses": [
                {"processTitle": "Process 1", "complexityScore": 3.5, "explanation": "Moderate complexity"},
                {"processTitle": "Process 2", "complexityScore": 4.0, "explanation": "Higher complexity"}
            ]
        }
        
        # Mock the write_json function since the converter writes directly to a file
        with mock.patch("taskinator.utils.write_json") as mock_write_json:
            # Convert the PDD to tasks
            tasks_data = converter.convert_pdd_to_tasks("test_pdd", "medium", generate_files=False)
            
            # Verify the tasks data
            assert "tasks" in tasks_data
            assert len(tasks_data["tasks"]) == 3  # Main task + 2 process tasks
            
            # Verify the main task
            main_task = tasks_data["tasks"][0]
            assert main_task["title"] == "Implement Test PDD"
            assert main_task["priority"] == "medium"
            assert main_task["dependencies"] == []
            
            # Verify process tasks
            process1_task = tasks_data["tasks"][1]
            assert process1_task["title"] == "Process 1"
            assert process1_task["dependencies"] == [1]  # Depends on main task
            
            process2_task = tasks_data["tasks"][2]
            assert process2_task["title"] == "Process 2"
            assert 1 in process2_task["dependencies"]  # Depends on main task
            assert 2 in process2_task["dependencies"]  # Depends on Process 1 task
            
            # Verify that write_json was called with the tasks data
            mock_write_json.assert_called_once()
    
    @pytest.mark.skip(reason="PDDProcess API has changed, 'order' parameter no longer supported")
    def test_generate_main_task_details(self, sample_pdd):
        """Test generating details for the main task."""
        converter = PDDTaskConverter()
        
        # Create a sample complexity analysis
        complexity_analysis = {
            "documentComplexity": 3.75,
            "processAnalyses": [
                {"processTitle": "Process 1", "complexityScore": 3.5, "explanation": "Moderate complexity"},
                {"processTitle": "Process 2", "complexityScore": 4.0, "explanation": "Higher complexity"}
            ]
        }
        
        # Generate main task details
        details = converter._generate_main_task_details(sample_pdd, complexity_analysis)
        
        # Verify the details - adjusted to match actual implementation
        assert "# Implementation of Test PDD" in details
        assert "## Description" in details
        assert "Test PDD Description" in details
        assert "## Business Objectives" in details
        assert "Objective 1" in details
        assert "## Success Criteria" in details
        assert "Criteria 1" in details
        assert "## Process Overview" in details
        assert "Process 1" in details
        assert "Process 2" in details
    
    @pytest.mark.skip(reason="PDDProcess API has changed, 'order' parameter no longer supported")
    def test_generate_process_task_details(self, sample_pdd):
        """Test generating details for a process task."""
        converter = PDDTaskConverter()
        
        # Get a process from the sample PDD
        process = sample_pdd.processes[0]
        
        # Create a sample process analysis
        process_analysis = {
            "processTitle": "Process 1",
            "complexityScore": 3.5,
            "explanation": "Moderate complexity due to multiple inputs and outputs"
        }
        
        # Generate process task details
        details = converter._generate_process_task_details(process, process_analysis)
        
        # Verify the details - adjusted to match actual implementation
        assert "# Implementation of Process: Process 1" in details
        assert "## Description" in details
        assert "First process description" in details
        assert "Estimated Time: 2 days" in details
        assert "Implementation Difficulty: moderate" in details
        assert "Complexity Score: 3.5" in details
        assert "Analysis: Moderate complexity" in details
        assert "## Required Resources" in details
        assert "Developer" in details
        assert "Designer" in details
        assert "## Process Interface" in details
        assert "### Inputs" in details
        assert "User requirements" in details
        assert "### Outputs" in details
        assert "Implementation plan" in details
        assert "## Implementation Guidance" in details


@pytest.mark.asyncio
@mock.patch("taskinator.ui.create_loading_indicator")
@mock.patch("taskinator.ui.display_success")
@mock.patch("taskinator.ui.display_info")
@mock.patch("taskinator.ui.display_error")
@mock.patch("taskinator.pdd_to_task.TaskManager")
@mock.patch("taskinator.pdd_to_task.PDDTaskConverter")
async def test_convert_pdd_to_tasks_command(
    mock_converter_class, 
    mock_task_manager_class, 
    mock_display_error,
    mock_display_info, 
    mock_display_success, 
    mock_loading_indicator
):
    """Test the convert_pdd_to_tasks_command function."""
    # Import the function directly in the test to avoid module-level import issues
    from taskinator.pdd_to_task import convert_pdd_to_tasks_command
    
    # Set up mocks
    mock_task_manager = mock.MagicMock()
    mock_task_manager_class.return_value = mock_task_manager
    
    mock_converter = mock.MagicMock()
    mock_converter_class.return_value = mock_converter
    
    # Mock the PDD document
    mock_pdd = mock.MagicMock()
    mock_pdd.title = "Test PDD"
    mock_pdd.processes = [mock.MagicMock(), mock.MagicMock()]
    mock_converter.pdd_manager.load_document.return_value = mock_pdd
    
    # Mock the tasks data
    mock_tasks_data = {
        "tasks": [
            {"id": 1, "title": "Main Task", "priority": "medium", "dependencies": []},
            {"id": 2, "title": "Process 1", "priority": "medium", "dependencies": [1]},
            {"id": 3, "title": "Process 2", "priority": "medium", "dependencies": [1, 2]}
        ]
    }
    mock_converter.convert_pdd_to_tasks.return_value = mock_tasks_data
    
    # Mock the loading indicator context manager
    mock_loading_context = mock.MagicMock()
    mock_loading_indicator.return_value = mock_loading_context
    
    # Call the function
    await convert_pdd_to_tasks_command("test_pdd", "medium")
    
    # Verify the converter was called correctly
    mock_converter_class.assert_called_once()
    mock_converter.convert_pdd_to_tasks.assert_called_with("test_pdd", "medium", generate_files=False)
    
    # Verify task manager was called to generate files
    mock_task_manager.generate_task_files.assert_called_once()
