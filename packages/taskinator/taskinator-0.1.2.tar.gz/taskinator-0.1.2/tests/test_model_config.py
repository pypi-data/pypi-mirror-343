"""Tests for model configuration system."""

import os
import unittest
from unittest.mock import patch, MagicMock

from taskinator.config import (
    LLMConfig, OllamaConfig, OpenAIConfig, AnthropicConfig, PerplexityConfig,
    ModelConfigurationManager, config
)


class TestLLMConfig(unittest.TestCase):
    """Test the base LLM configuration class."""
    
    def test_base_config(self):
        """Test basic configuration."""
        config = LLMConfig(model_name="test-model", provider="test-provider", api_key="test-key")
        self.assertEqual(config.model_name, "test-model")
        self.assertEqual(config.provider, "test-provider")
        self.assertEqual(config.api_key, "test-key")
        self.assertEqual(config.max_tokens, 4000)  # Default value
        self.assertEqual(config.temperature, 0.7)  # Default value
    
    def test_api_key_validation(self):
        """Test API key validation."""
        # Should pass for Ollama provider
        config = LLMConfig(model_name="test-model", provider="ollama")
        self.assertIsNone(config.api_key)
        
        # Should fail for other providers without API key
        with self.assertRaises(ValueError):
            LLMConfig(model_name="test-model", provider="openai")


class TestOllamaConfig(unittest.TestCase):
    """Test Ollama configuration."""
    
    def test_default_api_base(self):
        """Test default API base URL."""
        config = OllamaConfig(model_name="llama3")
        self.assertEqual(config.api_base, "http://localhost:11434/api")
        self.assertEqual(config.provider, "ollama")
    
    def test_custom_api_base(self):
        """Test custom API base URL."""
        config = OllamaConfig(model_name="llama3", api_base="http://custom:11434/api")
        self.assertEqual(config.api_base, "http://custom:11434/api")


class TestOpenAIConfig(unittest.TestCase):
    """Test OpenAI configuration."""
    
    def test_api_key_validation(self):
        """Test API key validation."""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            config = OpenAIConfig(model_name="gpt-4")
            self.assertEqual(config.api_key, "test-key")
        
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ValueError):
                OpenAIConfig(model_name="gpt-4")


class TestAnthropicConfig(unittest.TestCase):
    """Test Anthropic configuration."""
    
    def test_api_key_validation(self):
        """Test API key validation."""
        with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"}):
            config = AnthropicConfig(model_name="claude-3-sonnet")
            self.assertEqual(config.api_key, "test-key")
        
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ValueError):
                AnthropicConfig(model_name="claude-3-sonnet")


class TestModelConfigurationManager(unittest.TestCase):
    """Test the model configuration manager."""
    
    def setUp(self):
        """Set up test environment."""
        self.manager = ModelConfigurationManager()
        self.ollama_config = OllamaConfig(model_name="llama3")
        self.openai_config = OpenAIConfig(model_name="gpt-4", api_key="test-key")
    
    def test_add_model(self):
        """Test adding models."""
        self.manager.add_model("ollama", self.ollama_config, is_default=True)
        self.manager.add_model("openai", self.openai_config, is_fallback=True)
        
        self.assertEqual(len(self.manager.models), 2)
        self.assertEqual(self.manager.default_model, "ollama")
        self.assertEqual(self.manager.fallback_models, ["openai"])
    
    def test_get_model(self):
        """Test getting models."""
        self.manager.add_model("ollama", self.ollama_config, is_default=True)
        self.manager.add_model("openai", self.openai_config)
        
        # Get by ID
        model = self.manager.get_model("ollama")
        self.assertEqual(model.model_name, "llama3")
        
        # Get default
        model = self.manager.get_model()
        self.assertEqual(model.model_name, "llama3")
        
        # Test not found
        with self.assertRaises(ValueError):
            self.manager.get_model("not-found")
    
    def test_get_fallback_model(self):
        """Test getting fallback models."""
        self.manager.add_model("ollama", self.ollama_config, is_default=True)
        self.manager.add_model("openai", self.openai_config, is_fallback=True)
        self.manager.add_model("claude", AnthropicConfig(model_name="claude", api_key="test"), is_fallback=True)
        
        # Get first fallback
        model = self.manager.get_fallback_model()
        self.assertEqual(model.model_name, "gpt-4")
        
        # Get fallback with exclusion
        model = self.manager.get_fallback_model(excluded_models=["openai"])
        self.assertEqual(model.model_name, "claude")
        
        # No fallback available
        model = self.manager.get_fallback_model(excluded_models=["openai", "claude"])
        self.assertIsNone(model)
    
    def test_list_models(self):
        """Test listing models."""
        self.manager.add_model("ollama", self.ollama_config, is_default=True)
        self.manager.add_model("openai", self.openai_config, is_fallback=True)
        
        models = self.manager.list_models()
        self.assertEqual(len(models), 2)
        self.assertTrue(models["ollama"]["is_default"])
        self.assertTrue(models["openai"]["is_fallback"])
        self.assertEqual(models["ollama"]["provider"], "ollama")
        self.assertEqual(models["openai"]["model_name"], "gpt-4")


class TestConfigModelSetup(unittest.TestCase):
    """Test model setup from config."""
    
    @patch("taskinator.config.Config.validate_ai_config")
    def test_setup_model_manager(self, mock_validate):
        """Test setting up model manager from config."""
        mock_validate.return_value = {
            "claude_direct": True,
            "claude_bedrock": False,
            "perplexity": True,
            "openai": True,
            "ollama": True
        }
        
        with patch.object(config, "use_ollama", True), \
             patch.object(config, "anthropic_api_key", "test-key"), \
             patch.object(config, "openai_api_key", "test-key"), \
             patch.object(config, "perplexity_api_key", "test-key"):
            
            manager = config.setup_model_manager()
            
            # Should have 4 models
            self.assertEqual(len(manager.models), 4)
            
            # Ollama should be default
            self.assertEqual(manager.default_model, "ollama")
            
            # Should have 3 fallback models
            self.assertEqual(len(manager.fallback_models), 3)
            
            # Test model retrieval
            ollama_model = manager.get_model("ollama")
            self.assertEqual(ollama_model.provider, "ollama")
            
            claude_model = manager.get_model("claude")
            self.assertEqual(claude_model.provider, "anthropic")


if __name__ == "__main__":
    unittest.main()
