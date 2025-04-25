#!/bin/bash
set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}Taskinator Quickstart${NC}"
echo "=============================="

# Check Python version
echo -e "\n${BLUE}Checking Python version...${NC}"
python_version=$(python3 --version)
echo "Using $python_version"

# Check if Poetry is installed
echo -e "\n${BLUE}Checking Poetry installation...${NC}"
if ! command -v poetry &> /dev/null; then
    echo -e "${RED}Poetry not found. Installing...${NC}"
    curl -sSL https://install.python-poetry.org | python3 -
fi

# Install dependencies
echo -e "\n${BLUE}Installing dependencies...${NC}"
poetry install

# Activate virtual environment
echo -e "\n${BLUE}Activating virtual environment...${NC}"
source $(poetry env info --path)/bin/activate

# Check for environment variables
echo -e "\n${BLUE}Checking environment setup...${NC}"
if [ ! -f .env ]; then
    echo -e "${RED}No .env file found. Creating template...${NC}"
    cat > .env << EOL
ANTHROPIC_API_KEY=your_claude_api_key
PERPLEXITY_API_KEY=your_perplexity_api_key
CLAUDE_MODEL=claude-3-opus-20240229
PERPLEXITY_MODEL=sonar-pro
DEBUG=false
EOL
    echo "Please edit .env file with your API keys before continuing."
    exit 1
fi

# Initialize project
echo -e "\n${BLUE}Initializing Taskinator project...${NC}"
poetry run taskinator init --force

# Parse sample PRD
echo -e "\n${BLUE}Parsing sample PRD...${NC}"
poetry run taskinator parse examples/sample_prd.txt --num-tasks 5

# List generated tasks
echo -e "\n${BLUE}Listing generated tasks...${NC}"
poetry run taskinator list

# Expand first task
echo -e "\n${BLUE}Expanding first task...${NC}"
poetry run taskinator expand 1 --num-subtasks 3

# Show task details
echo -e "\n${BLUE}Showing expanded task details...${NC}"
poetry run taskinator list --subtasks

echo -e "\n${GREEN}Quickstart complete!${NC}"
echo "You can now try other commands like:"
echo "  taskinator status 1 in_progress"
echo "  taskinator update 1 'New implementation details'"
echo "  taskinator list --status pending"

# Cleanup instructions
echo -e "\n${BLUE}To clean up this test:${NC}"
echo "1. Remove the tasks directory: rm -rf tasks/"
echo "2. Remove the .env file if you don't need it: rm .env"
echo "3. Deactivate the virtual environment: deactivate"