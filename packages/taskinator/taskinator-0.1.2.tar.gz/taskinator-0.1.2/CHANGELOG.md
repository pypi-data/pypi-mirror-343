# Changelog

All notable changes to the Taskinator Python project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelogger.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.1] - 2025-04-20

### Added
- Implemented PDD to SOP conversion workflow
  - Added PDD content analysis for SOP generation
  - Created SOP structure generation based on PDD processes
  - Added Mermaid diagram generation for SOP step flows
  - Implemented CLI commands for PDD conversion
  - Added support for Markdown output format
- Added PDD to tasks conversion functionality
  - Implemented process to task mapping
  - Preserved dependencies between processes
  - Added CLI command for PDD to tasks conversion
- Implemented model configuration system for Ollama and cloud LLMs
  - Added support for local Ollama models
  - Integrated OpenAI, Anthropic, and Perplexity models
  - Created model fallback mechanisms
  - Implemented environment detection for model selection
  - Added comprehensive configuration options

### Improved
- Enhanced document relationship preservation between PDDs and SOPs
- Improved CLI output with detailed progress information
- Better error handling in document conversion workflows
- More flexible model configuration with automatic fallback support

## [0.1.0] - 2025-04-10

### Added
- Initial release of the Python version
- Complete rewrite of the original Node.js Task Master project
- New features and improvements:
  - Modern Python package structure using Poetry
  - Type hints throughout the codebase
  - Comprehensive test suite with pytest
  - Rich terminal UI using the `rich` library
  - Async support for AI operations
  - Improved error handling and validation
  - Better dependency management
  - Enhanced CLI using Typer

### Changed
- Replaced Commander.js with Typer for CLI
- Replaced chalk with Rich for terminal formatting
- Replaced cli-table3 with Rich tables
- Updated AI service integrations to use modern Python SDKs
- Improved configuration management using Pydantic
- Enhanced task file formatting and organization

### Improved
- Better error messages and user feedback
- More consistent API responses handling
- Stronger type safety throughout the application
- More maintainable and testable code structure
- Better handling of concurrent operations
- Enhanced documentation and examples

### Technical Details
- Minimum Python version: 3.8+
- Key dependencies:
  - typer[all]: Modern CLI framework
  - rich: Terminal formatting and UI
  - anthropic: Claude AI integration
  - openai: Perplexity AI integration
  - pydantic: Data validation and settings
  - pytest: Testing framework
  - poetry: Dependency management

### Migration Notes
- Task file format remains compatible with the Node.js version
- Environment variables remain the same
- CLI commands maintain similar structure for familiarity
- Added new Python-specific configuration options

### Known Issues
- None at this time

For more details about the changes and new features, please refer to the README.md file.