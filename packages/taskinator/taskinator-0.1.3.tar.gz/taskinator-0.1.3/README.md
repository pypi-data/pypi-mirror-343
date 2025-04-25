# Taskinator

A Python-based task management system for AI-driven development. Inspired by [claude-taskmaster](https://github.com/eyaltoledano/claude-taskmaster) project.

## Features

- Parse PRD documents into actionable tasks
- Break down tasks into subtasks using AI assistance
- Track task dependencies and status
- Research-backed task generation using Perplexity AI
- Rich terminal UI with progress indicators
- Comprehensive task management CLI
- Conflict resolution strategies
- External task sync
   - nextcloud
## Installation

1. Ensure you have Python 3.8 or later installed
2. Install using pip:

```bash
pip install taskinator
```

Or install from source:

```bash
# Clone the repository
git clone https://github.com/yourusername/taskinator.git
cd taskinator

# Install Poetry if you haven't already
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies and the package
poetry install

# Activate the virtual environment
poetry shell
```

## Configuration

Create a `.env` file in your project directory with your API keys:

```env
ANTHROPIC_API_KEY=your_claude_api_key
PERPLEXITY_API_KEY=your_perplexity_api_key  # Optional
CLAUDE_MODEL=claude-3-opus-20240229  # Optional, defaults to latest
PERPLEXITY_MODEL=sonar-pro  # Optional, defaults to sonar-pro
```

## Usage

### Initialize a Project

```bash
taskinator init
```

### Parse a PRD

```bash
taskinator parse path/to/prd.txt --num-tasks 10
```

### List Tasks

```bash
# List all tasks
taskinator list

# Filter by status
taskinator list --status pending

# Show subtasks
taskinator list --subtasks
```

### Expand a Task

```bash
# Basic expansion
taskinator expand 1

# With research
taskinator expand 1 --research

# Specify number of subtasks
taskinator expand 1 --num-subtasks 3

# Add context
taskinator expand 1 --context "Focus on security features"
```

### Update Task Status

```bash
# Update single task
taskinator status 1 done

# Update multiple tasks
taskinator status 1,2,3 in_progress
```

### Update Tasks with New Context

```bash
# Basic update
taskinator update 1 "New implementation details..."

# With research
taskinator update 1 "New implementation details..." --research
```

## Task Structure

Tasks are stored in both JSON format (`tasks.json`) and individual text files:

```
tasks/
├── tasks.json
├── task_001.txt
├── task_002.txt
└── ...
```

Each task includes:
- Unique ID
- Title
- Description
- Implementation details
- Test strategy
- Dependencies
- Priority
- Status
- Optional subtasks

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/taskinator.git
cd taskinator

# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install

# Run tests
poetry run pytest
```

### Code Style

The project uses:
- Black for code formatting
- isort for import sorting
- mypy for type checking

Format code before committing:

```bash
poetry run black .
poetry run isort .
poetry run mypy .
```

### Running Tests

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov

# Run specific test categories
poetry run pytest -m "not integration"  # Skip integration tests
poetry run pytest -m "unit"  # Run only unit tests
```

## Troubleshooting

### Common Issues

1. **Missing Dependencies**
   ```bash
   # If you see ModuleNotFoundError, try reinstalling dependencies
   poetry install --sync
   ```

2. **API Key Issues**
   ```bash
   # Verify your .env file is in the correct location
   taskinator init --debug
   ```

3. **Permission Issues**
   ```bash
   # If you can't run the CLI, try
   chmod +x $(which taskinator)
   ```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Credits

Original Node.js version by [Eyal Toledano](https://github.com/eyaltoledano)