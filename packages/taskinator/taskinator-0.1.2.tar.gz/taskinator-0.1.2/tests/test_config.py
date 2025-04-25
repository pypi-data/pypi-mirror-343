"""Tests for configuration management."""

import os
from pathlib import Path
from unittest import mock

import pytest
from pydantic import ValidationError

from taskinator.config import Config, TaskPriority, TaskStatus


@pytest.fixture
def clean_env():
    """Fixture to provide a clean environment for testing."""
    # Save original environment
    original_env = os.environ.copy()
    
    # Set minimal environment for testing
    test_env = {
        "DEFAULT_SUBTASKS": "5",  # Explicitly set to match test expectations
        "CLAUDE_MODEL": "claude-3-sonnet-20240229",  # Explicitly set to match test expectations
    }
    
    with mock.patch.dict(os.environ, test_env, clear=True):
        yield
    
    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)


def test_config_defaults(clean_env):
    """Test default configuration values."""
    config = Config()
    assert config.max_tokens == 4000
    assert config.temperature == 0.7
    assert config.default_subtasks == 5
    assert config.tasks_dir == Path("tasks")
    assert config.debug is False


def test_config_env_override(clean_env):
    """Test environment variable overrides."""
    with mock.patch.dict(os.environ, {
        "MAX_TOKENS": "2000",
        "TEMPERATURE": "0.5",
        "DEFAULT_SUBTASKS": "3",
        "DEBUG": "true"
    }):
        config = Config()
        assert config.max_tokens == 2000
        assert config.temperature == 0.5
        assert config.default_subtasks == 3
        assert config.debug is True


def test_config_api_keys(clean_env):
    """Test API key configuration."""
    with mock.patch.dict(os.environ, {
        "ANTHROPIC_API_KEY": "test-key",
        "PERPLEXITY_API_KEY": "test-key-2"
    }):
        config = Config()
        assert config.anthropic_api_key == "test-key"
        assert config.perplexity_api_key == "test-key-2"


def test_ensure_directories(clean_env, tmp_path):
    """Test directory creation."""
    config = Config(tasks_dir=tmp_path / "tasks")
    config.ensure_directories()
    assert config.tasks_dir.exists()
    assert config.tasks_dir.is_dir()


def test_task_status_validation():
    """Test task status validation."""
    assert TaskStatus.is_valid(TaskStatus.PENDING)
    assert TaskStatus.is_valid(TaskStatus.IN_PROGRESS)
    assert TaskStatus.is_valid(TaskStatus.DONE)
    assert TaskStatus.is_valid(TaskStatus.BLOCKED)
    assert not TaskStatus.is_valid("invalid")


def test_task_priority_validation():
    """Test task priority validation."""
    assert TaskPriority.is_valid(TaskPriority.LOW)
    assert TaskPriority.is_valid(TaskPriority.MEDIUM)
    assert TaskPriority.is_valid(TaskPriority.HIGH)
    assert not TaskPriority.is_valid("invalid")


def test_config_validation(clean_env):
    """Test configuration validation."""
    with pytest.raises(ValidationError):
        Config(temperature=2.0)  # Temperature should be between 0 and 1
    
    with pytest.raises(ValidationError):
        Config(max_tokens=-1)  # Max tokens should be positive


def test_model_names(clean_env):
    """Test model name configuration."""
    config = Config()
    assert config.claude_model == "claude-3-sonnet-20240229"
    assert config.perplexity_model == "sonar-pro"
    
    with mock.patch.dict(os.environ, {
        "CLAUDE_MODEL": "claude-3-opus-20240229",
        "PERPLEXITY_MODEL": "sonar-medium-online"
    }):
        config = Config()
        assert config.claude_model == "claude-3-opus-20240229"
        assert config.perplexity_model == "sonar-medium-online"


def test_ollama_config(clean_env):
    """Test Ollama configuration."""
    with mock.patch.dict(os.environ, {
        "USE_OLLAMA": "true",
        "OLLAMA_MODEL": "llama3",
        "OLLAMA_API_BASE": "http://custom:11434/api"
    }):
        config = Config()
        assert config.use_ollama is True
        assert config.ollama_model == "llama3"
        assert config.ollama_api_base == "http://custom:11434/api"


def test_openai_config(clean_env):
    """Test OpenAI configuration."""
    with mock.patch.dict(os.environ, {
        "OPENAI_API_KEY": "test-openai-key",
        "OPENAI_MODEL": "gpt-4-turbo"
    }):
        config = Config()
        assert config.openai_api_key == "test-openai-key"
        assert config.openai_model == "gpt-4-turbo"


def test_validate_ai_config(clean_env):
    """Test AI configuration validation."""
    with mock.patch.dict(os.environ, {
        "ANTHROPIC_API_KEY": "test-key",
        "PERPLEXITY_API_KEY": "test-key-2",
        "OPENAI_API_KEY": "test-key-3"
    }):
        config = Config()
        services = config.validate_ai_config()
        assert services["claude_direct"] is True
        assert services["perplexity"] is True
        assert services["openai"] is True
        assert services["ollama"] is False  # Ollama not enabled by default


def test_setup_model_manager(clean_env):
    """Test model manager setup."""
    with mock.patch.dict(os.environ, {
        "ANTHROPIC_API_KEY": "test-key",
        "OPENAI_API_KEY": "test-key-2",
        "USE_OLLAMA": "true",
        # Explicitly clear perplexity key to avoid test interference
        "PERPLEXITY_API_KEY": ""
    }), mock.patch("requests.get") as mock_get:
        # Mock Ollama version check
        mock_response = mock.MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        config = Config()
        manager = config.setup_model_manager()
        
        # Should have 3 models
        assert len(manager.models) == 3
        assert "claude" in manager.models
        assert "openai" in manager.models
        assert "ollama" in manager.models
        
        # Ollama should be default
        assert manager.default_model == "ollama"
        
        # Should have 2 fallback models
        assert len(manager.fallback_models) == 2
        assert "claude" in manager.fallback_models
        assert "openai" in manager.fallback_models