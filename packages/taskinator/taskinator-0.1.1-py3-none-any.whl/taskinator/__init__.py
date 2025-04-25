"""Taskinator - A Python-based task management system for AI-driven development."""

__version__ = "0.1.1"

from pathlib import Path

# Package paths
PACKAGE_DIR = Path(__file__).parent
PACKAGE_DATA_DIR = PACKAGE_DIR / "package_data"
EXAMPLES_DIR = PACKAGE_DATA_DIR / "examples"

# Import package data module
from . import package_data

# Version info
__title__ = "taskinator"
__description__ = "A Python-based task management system for AI-driven development"
__author__ = "Original by Eyal Toledano"
__license__ = "MIT"

# Make version info available
VERSION = __version__