"""Package data for Taskinator."""

# This file ensures the package_data directory is treated as a Python package
# and is included in the distribution.

from pathlib import Path

# Get the directory containing the package data
PACKAGE_DATA_DIR = Path(__file__).parent

# Get the examples directory
EXAMPLES_DIR = PACKAGE_DATA_DIR / "examples"

# Get the templates directory
TEMPLATES_DIR = PACKAGE_DATA_DIR / "templates"
CURSOR_TEMPLATES_DIR = TEMPLATES_DIR / "cursor"
WINDSURF_TEMPLATES_DIR = TEMPLATES_DIR / "windsurf"