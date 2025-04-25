"""Tests for AI service integrations."""

import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from anthropic import Anthropic
from openai import OpenAI

from taskinator.ai_services import (
    call_claude,
    generate_complexity_analysis_prompt,
    generate_subtasks,
    generate_subtasks_with_perplexity,
)


@pytest.fixture
def mock_anthropic():
    """Fixture providing a mocked Anthropic client."""
    with patch("taskinator.ai_services.anthropic_client") as mock:
        # Mock the messages.create method
        mock.messages.create = AsyncMock()
        mock.messages.create.return_value.content = [
            MagicMock(text=json.dumps({
                "tasks": [
                    {
                        "id": 1,
                        "title": "Test Task",
                        "description": "Test Description",
                        "details": "Test Details",
                        "testStrategy": "Test Strategy",
                        "dependencies": [],
                        "priority": "medium",
                        "status": "pending"
                    }
                ]
            }))
        ]
        yield mock


@pytest.fixture
def mock_perplexity():
    """Fixture providing a mocked Perplexity client."""
    with patch("taskinator.ai_services.perplexity_client") as mock:
        # Mock the chat.completions.create method
        mock.chat.completions.create = AsyncMock()
        mock.chat.completions.create.return_value.choices = [
            MagicMock(
                message=MagicMock(
                    content=json.dumps([
                        {
                            "id": 1,
                            "title": "Test Subtask",
                            "description": "Test Description",
                            "details": "Test Details",
                            "dependencies": []
                        }
                    ])
                )
            )
        ]
        yield mock


@pytest.fixture
def sample_task():
    """Fixture providing a sample task for testing."""
    return {
        "id": 1,
        "title": "Test Task",
        "description": "Test task description",
        "details": "Test implementation details",
        "status": "pending",
        "dependencies": []
    }


@pytest.mark.asyncio
async def test_call_claude(mock_anthropic):
    """Test Claude API integration for task generation."""
    # Test successful API call
    result = await call_claude("Test PRD content", "test.prd")
    assert "tasks" in result
    assert len(result["tasks"]) > 0
    assert "id" in result["tasks"][0]
    
    # Verify API call parameters
    call_args = mock_anthropic.messages.create.call_args[1]
    assert "system" in call_args
    assert "messages" in call_args
    assert "Test PRD content" in str(call_args["messages"])
    
    # Test error handling
    mock_anthropic.messages.create.side_effect = Exception("API Error")
    with pytest.raises(Exception):
        await call_claude("Test PRD content", "test.prd")


@pytest.mark.asyncio
async def test_generate_subtasks(mock_anthropic, sample_task):
    """Test subtask generation with Claude."""
    # Test successful generation
    subtasks = await generate_subtasks(sample_task)
    assert isinstance(subtasks, list)
    assert len(subtasks) > 0
    assert "id" in subtasks[0]
    
    # Test with additional context
    subtasks = await generate_subtasks(
        sample_task,
        additional_context="Test context"
    )
    call_args = mock_anthropic.messages.create.call_args[1]
    assert "Test context" in str(call_args["messages"])
    
    # Test error handling
    mock_anthropic.messages.create.side_effect = Exception("API Error")
    with pytest.raises(Exception):
        await generate_subtasks(sample_task)


@pytest.mark.asyncio
async def test_generate_subtasks_with_perplexity(
    mock_perplexity,
    sample_task
):
    """Test subtask generation with Perplexity AI."""
    # Test successful generation
    subtasks = await generate_subtasks_with_perplexity(sample_task)
    assert isinstance(subtasks, list)
    assert len(subtasks) > 0
    assert "id" in subtasks[0]
    
    # Verify API call parameters
    call_args = mock_perplexity.chat.completions.create.call_args[1]
    assert len(call_args["messages"]) == 2  # system + user message
    assert "research" in str(call_args["messages"][0]["content"]).lower()
    
    # Test with additional context
    subtasks = await generate_subtasks_with_perplexity(
        sample_task,
        additional_context="Test context"
    )
    call_args = mock_perplexity.chat.completions.create.call_args[1]
    assert "Test context" in str(call_args["messages"][1]["content"])
    
    # Test error handling
    mock_perplexity.chat.completions.create.side_effect = Exception("API Error")
    with pytest.raises(Exception):
        await generate_subtasks_with_perplexity(sample_task)


def test_generate_complexity_analysis_prompt(sample_task):
    """Test complexity analysis prompt generation."""
    prompt = generate_complexity_analysis_prompt(sample_task)
    
    # Verify prompt content
    assert str(sample_task["id"]) in prompt
    assert sample_task["title"] in prompt
    assert sample_task["description"] in prompt
    assert sample_task["details"] in prompt
    assert "complexity" in prompt.lower()
    assert "requirements" in prompt.lower()


@pytest.mark.asyncio
async def test_api_response_parsing(mock_anthropic, mock_perplexity):
    """Test parsing of API responses."""
    # Test Claude response parsing
    mock_anthropic.messages.create.return_value.content = [
        MagicMock(text="Invalid JSON content")
    ]
    with pytest.raises(ValueError):
        await call_claude("Test content", "test.prd")
    
    # Test Perplexity response parsing
    mock_perplexity.chat.completions.create.return_value.choices = [
        MagicMock(message=MagicMock(content="Invalid JSON content"))
    ]
    with pytest.raises(ValueError):
        await generate_subtasks_with_perplexity(sample_task)


@pytest.mark.asyncio
async def test_api_configuration():
    """Test API client configuration."""
    # Test Anthropic client initialization
    with patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key"}):
        with patch("anthropic.Anthropic") as mock_anthropic:
            from taskinator.ai_services import anthropic_client
            mock_anthropic.assert_called_with(api_key="test-key")
    
    # Test Perplexity client initialization
    with patch.dict("os.environ", {
        "PERPLEXITY_API_KEY": "test-key",
        "PERPLEXITY_MODEL": "test-model"
    }):
        with patch("openai.OpenAI") as mock_openai:
            from taskinator.ai_services import perplexity_client
            mock_openai.assert_called_with(
                api_key="test-key",
                base_url="https://api.perplexity.ai"
            )


def test_prompt_sanitization():
    """Test prompt sanitization in API calls."""
    from taskinator.utils import sanitize_prompt
    
    # Test basic sanitization
    assert "\x00" not in sanitize_prompt("test\x00content")
    assert "  test  ".strip() == sanitize_prompt("  test  ")


@pytest.mark.asyncio
async def test_concurrent_api_calls(mock_anthropic, sample_task):
    """Test handling of concurrent API calls."""
    # Test multiple simultaneous subtask generations
    tasks = []
    for _ in range(3):
        tasks.append(generate_subtasks(sample_task))
    
    results = await asyncio.gather(*tasks)
    assert len(results) == 3
    assert all(isinstance(r, list) for r in results)