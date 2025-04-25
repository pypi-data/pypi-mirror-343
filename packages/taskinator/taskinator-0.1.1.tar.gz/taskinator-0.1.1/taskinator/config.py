"""Configuration management for Taskinator."""

import os
from pathlib import Path
from typing import Dict, Optional, Annotated, List, Union, Literal

from pydantic import BaseModel, Field, BeforeValidator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()


class LLMConfig(BaseModel):
    """Base configuration for language models."""
    model_name: str
    provider: str
    api_base: Optional[str] = None
    api_key: Optional[str] = None
    max_tokens: int = 4000
    temperature: float = 0.7
    
    @model_validator(mode='after')
    def validate_api_key(self):
        """Validate that API key is provided when needed."""
        if self.provider not in ['ollama', 'local']:
            if not self.api_key:
                raise ValueError(f"API key is required for provider: {self.provider}")
        return self


class OllamaConfig(LLMConfig):
    """Configuration for Ollama models."""
    provider: Literal['ollama'] = 'ollama'
    api_base: str = "http://localhost:11434/api"
    
    @model_validator(mode='after')
    def validate_api_base(self):
        """Ensure API base is set correctly."""
        if not self.api_base:
            self.api_base = "http://localhost:11434/api"
        return self


class OpenAIConfig(LLMConfig):
    """Configuration for OpenAI models."""
    provider: Literal['openai'] = 'openai'
    api_base: str = "https://api.openai.com/v1"
    
    @model_validator(mode='after')
    def validate_api_key(self):
        """Validate that API key is provided."""
        if not self.api_key:
            self.api_key = os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("API key is required for OpenAI models")
        return self


class AnthropicConfig(LLMConfig):
    """Configuration for Anthropic models."""
    provider: Literal['anthropic'] = 'anthropic'
    api_base: str = "https://api.anthropic.com"
    
    @model_validator(mode='after')
    def validate_api_key(self):
        """Validate that API key is provided."""
        if not self.api_key:
            self.api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("API key is required for Anthropic models")
        return self


class PerplexityConfig(LLMConfig):
    """Configuration for Perplexity models."""
    provider: Literal['perplexity'] = 'perplexity'
    
    @model_validator(mode='after')
    def validate_api_key(self):
        """Validate that API key is provided."""
        if not self.api_key:
            self.api_key = os.environ.get("PERPLEXITY_API_KEY")
        if not self.api_key:
            raise ValueError("API key is required for Perplexity models")
        return self


class ModelConfigurationManager:
    """Manager for model configurations."""
    
    def __init__(self):
        """Initialize the model configuration manager."""
        self.models: Dict[str, LLMConfig] = {}
        self.default_model: Optional[str] = None
        self.fallback_models: List[str] = []
    
    def add_model(self, model_id: str, config: LLMConfig, is_default: bool = False, is_fallback: bool = False):
        """Add a model configuration.
        
        Args:
            model_id: Unique identifier for the model
            config: Model configuration
            is_default: Whether this is the default model
            is_fallback: Whether this is a fallback model
        """
        self.models[model_id] = config
        
        if is_default:
            self.default_model = model_id
            
        if is_fallback and model_id not in self.fallback_models:
            self.fallback_models.append(model_id)
    
    def get_model(self, model_id: Optional[str] = None) -> LLMConfig:
        """Get a model configuration.
        
        Args:
            model_id: Model identifier or None for default
            
        Returns:
            Model configuration
            
        Raises:
            ValueError: If model is not found
        """
        if model_id is None:
            if self.default_model is None:
                raise ValueError("No default model configured")
            return self.models[self.default_model]
        
        if model_id not in self.models:
            raise ValueError(f"Model not found: {model_id}")
        
        return self.models[model_id]
    
    def get_fallback_model(self, excluded_models: List[str] = None) -> Optional[LLMConfig]:
        """Get a fallback model configuration.
        
        Args:
            excluded_models: Models to exclude from fallback
            
        Returns:
            Fallback model configuration or None if no fallback is available
        """
        excluded = excluded_models or []
        
        for model_id in self.fallback_models:
            if model_id not in excluded:
                return self.models[model_id]
        
        return None
    
    def list_models(self) -> Dict[str, Dict]:
        """List all available models.
        
        Returns:
            Dictionary of model configurations
        """
        return {
            model_id: {
                "provider": config.provider,
                "model_name": config.model_name,
                "is_default": model_id == self.default_model,
                "is_fallback": model_id in self.fallback_models
            }
            for model_id, config in self.models.items()
        }


class Config(BaseSettings):
    """Main configuration settings."""

    # Model Settings
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="allow"
    )
    
    # AI Service Settings
    anthropic_api_key: Optional[str] = Field(
        None,
        env="ANTHROPIC_API_KEY",
        description="API key for direct Anthropic/Claude services"
    )
    
    # AWS Bedrock Settings
    use_bedrock: bool = Field(
        False,
        env="USE_BEDROCK",
        description="Whether to use AWS Bedrock for Claude"
    )
    aws_access_key: Optional[str] = Field(
        None,
        env="AWS_ACCESS_KEY_ID",
        description="AWS access key for Bedrock"
    )
    aws_secret_key: Optional[str] = Field(
        None,
        env="AWS_SECRET_ACCESS_KEY",
        description="AWS secret key for Bedrock"
    )
    aws_session_token: Optional[str] = Field(
        None,
        env="AWS_SESSION_TOKEN",
        description="AWS session token for temporary credentials"
    )
    aws_region: str = Field(
        "us-east-1",
        env="AWS_REGION",
        description="AWS region for Bedrock"
    )
    
    # Perplexity Settings
    perplexity_api_key: Optional[str] = Field(
        None,
        env="PERPLEXITY_API_KEY",
        description="API key for Perplexity AI services"
    )
    perplexity_model: str = Field(
        "sonar-pro",
        env="PERPLEXITY_MODEL",
        description="Model to use for Perplexity AI"
    )
    
    # OpenAI Settings
    openai_api_key: Optional[str] = Field(
        None,
        env="OPENAI_API_KEY",
        description="API key for OpenAI services"
    )
    openai_model: str = Field(
        "gpt-4",
        env="OPENAI_MODEL",
        description="Model to use for OpenAI"
    )
    
    # Ollama Settings
    use_ollama: bool = Field(
        False,
        env="USE_OLLAMA",
        description="Whether to use Ollama for local models"
    )
    ollama_api_base: str = Field(
        "http://localhost:11434/api",
        env="OLLAMA_API_BASE",
        description="Base URL for Ollama API"
    )
    ollama_model: str = Field(
        "llama3",
        env="OLLAMA_MODEL",
        description="Model to use for Ollama"
    )
    
    # Model Settings
    claude_model: str = Field(
        "claude-3-sonnet-20240229",
        env="CLAUDE_MODEL",
        description="Model to use for Claude AI"
    )
    
    # Task Generation Settings
    max_tokens: int = Field(
        4000,
        env="MAX_TOKENS",
        ge=1,
        le=100000,
        description="Maximum tokens for AI responses"
    )
    temperature: float = Field(
        0.7,
        env="TEMPERATURE",
        ge=0.0,
        le=1.0,
        description="Temperature for AI responses"
    )
    default_subtasks: int = Field(
        5,
        env="DEFAULT_SUBTASKS",
        ge=1,
        le=20,
        description="Default number of subtasks to generate"
    )
    
    # File Paths
    tasks_dir: Path = Field(
        default_factory=lambda: Path("tasks"),
        description="Directory for task files"
    )
    output_file: Path = Field(
        default_factory=lambda: Path("output.json"),
        description="Path for output JSON file"
    )
    
    # Debug Settings
    debug: bool = Field(
        False,
        env="DEBUG",
        description="Enable debug mode"
    )
    
    def ensure_directories(self) -> None:
        """Ensure all required directories exist."""
        self.tasks_dir.mkdir(parents=True, exist_ok=True)
    
    def has_aws_credentials(self) -> bool:
        """Check if AWS credentials are available.
        
        Returns:
            True if AWS credentials are available either through environment
            variables or AWS credential file
        """
        # Check environment variables
        if self.aws_access_key and self.aws_secret_key:
            return True
        
        # Check AWS credentials file
        aws_creds_file = os.path.expanduser("~/.aws/credentials")
        return os.path.exists(aws_creds_file)
    
    def validate_ai_config(self) -> Dict[str, bool]:
        """Validate AI service configuration.
        
        Returns:
            Dictionary indicating which services are available
        """
        services = {
            "claude_direct": False,
            "claude_bedrock": False,
            "perplexity": False,
            "openai": False,
            "ollama": False
        }
        
        # Check direct Claude access
        if self.anthropic_api_key:
            services["claude_direct"] = True
        
        # Check AWS Bedrock access
        if self.use_bedrock and self.has_aws_credentials():
            services["claude_bedrock"] = True
        
        # Check Perplexity access
        if self.perplexity_api_key:
            services["perplexity"] = True
            
        # Check OpenAI access
        if self.openai_api_key:
            services["openai"] = True
            
        # Check Ollama access
        if self.use_ollama:
            import requests
            try:
                response = requests.get(f"{self.ollama_api_base.rstrip('/api')}/version")
                if response.status_code == 200:
                    services["ollama"] = True
            except Exception:
                pass
        
        return services
    
    def setup_model_manager(self) -> ModelConfigurationManager:
        """Set up the model configuration manager based on environment settings.
        
        Returns:
            Configured model manager
        """
        manager = ModelConfigurationManager()
        
        # Add Ollama model if enabled
        if self.use_ollama:
            manager.add_model(
                "ollama",
                OllamaConfig(
                    model_name=self.ollama_model,
                    api_base=self.ollama_api_base,
                    max_tokens=self.max_tokens,
                    temperature=self.temperature
                ),
                is_default=True,
                is_fallback=False
            )
        
        # Add Claude model if available
        if self.anthropic_api_key:
            manager.add_model(
                "claude",
                AnthropicConfig(
                    model_name=self.claude_model,
                    api_key=self.anthropic_api_key,
                    max_tokens=self.max_tokens,
                    temperature=self.temperature
                ),
                is_default=not self.use_ollama,
                is_fallback=True
            )
        
        # Add OpenAI model if available
        if self.openai_api_key:
            manager.add_model(
                "openai",
                OpenAIConfig(
                    model_name=self.openai_model,
                    api_key=self.openai_api_key,
                    max_tokens=self.max_tokens,
                    temperature=self.temperature
                ),
                is_default=not (self.use_ollama or self.anthropic_api_key),
                is_fallback=True
            )
        
        # Add Perplexity model if available
        if self.perplexity_api_key:
            manager.add_model(
                "perplexity",
                PerplexityConfig(
                    model_name=self.perplexity_model,
                    api_key=self.perplexity_api_key,
                    max_tokens=self.max_tokens,
                    temperature=self.temperature
                ),
                is_default=not (self.use_ollama or self.anthropic_api_key or self.openai_api_key),
                is_fallback=True
            )
        
        return manager


class TaskStatus:
    """Task status constants."""
    
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    BLOCKED = "blocked"
    
    _VALID_STATUSES = {PENDING, IN_PROGRESS, DONE, BLOCKED}
    
    @classmethod
    def is_valid(cls, status: str) -> bool:
        """Check if a status is valid."""
        return status in cls._VALID_STATUSES
    
    @classmethod
    def get_valid_statuses(cls) -> set:
        """Get set of valid statuses."""
        return cls._VALID_STATUSES.copy()


class TaskPriority:
    """Task priority constants."""
    
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    
    _VALID_PRIORITIES = {LOW, MEDIUM, HIGH}
    
    @classmethod
    def is_valid(cls, priority: str) -> bool:
        """Check if a priority is valid."""
        return priority in cls._VALID_PRIORITIES
    
    @classmethod
    def get_valid_priorities(cls) -> set:
        """Get set of valid priorities."""
        return cls._VALID_PRIORITIES.copy()


# Create a global config instance
config = Config()

# Ensure required directories exist
config.ensure_directories()

# Validate AI configuration
available_services = config.validate_ai_config()

# Set up model manager
model_manager = config.setup_model_manager()

# Only show warning if no LLM service is available
if not any(available_services.values()):
    import warnings
    warnings.warn(
        "No LLM service is available. Please configure at least one of:\n"
        "1. Set ANTHROPIC_API_KEY for Claude access\n"
        "2. Set OPENAI_API_KEY for OpenAI access\n"
        "3. Set PERPLEXITY_API_KEY for Perplexity access\n"
        "4. Set USE_OLLAMA=true and ensure Ollama is running locally\n"
        "5. Set USE_BEDROCK=true and configure AWS credentials for Bedrock access"
    )