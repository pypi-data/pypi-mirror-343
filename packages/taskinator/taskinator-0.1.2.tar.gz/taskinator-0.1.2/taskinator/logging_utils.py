"""Logging utilities for Taskinator.

This module provides utilities for configuring and using loguru for logging
throughout the Taskinator application.
"""

import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Union

from loguru import logger


def configure_logging(
    log_level: str = "INFO",
    log_file: Optional[Union[str, Path]] = None,
    rotation: str = "10 MB",
    retention: str = "1 week",
    format_string: Optional[str] = None,
    enable_console: bool = True,
    enable_file: bool = True,
    log_dir: Optional[Union[str, Path]] = None
) -> None:
    """Configure loguru logger for the application.
    
    Args:
        log_level: Minimum log level to capture
        log_file: Path to log file (default: taskinator.log in log_dir)
        rotation: When to rotate log files (size or time)
        retention: How long to keep log files
        format_string: Custom format string for log messages
        enable_console: Whether to log to console
        enable_file: Whether to log to file
        log_dir: Directory for log files (default: logs/ in current directory)
    """
    # Remove default handlers
    logger.remove()
    
    # Default format string
    if format_string is None:
        format_string = (
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>"
        )
    
    # Add console handler if enabled
    if enable_console:
        logger.add(
            sys.stderr,
            format=format_string,
            level=log_level,
            colorize=True
        )
    
    # Add file handler if enabled
    if enable_file:
        # Determine log file path
        if log_file is None:
            if log_dir is None:
                log_dir = Path("logs")
            else:
                log_dir = Path(log_dir)
            
            # Create log directory if it doesn't exist
            log_dir.mkdir(parents=True, exist_ok=True)
            
            # Default log file name with date
            date_str = datetime.now().strftime("%Y%m%d")
            log_file = log_dir / f"taskinator_{date_str}.log"
        
        logger.add(
            str(log_file),
            format=format_string,
            level=log_level,
            rotation=rotation,
            retention=retention,
            compression="zip"
        )
    
    # Log the configuration
    logger.info(
        f"Logging configured: level={log_level}, "
        f"console={enable_console}, file={enable_file}, "
        f"log_file={log_file if enable_file else 'disabled'}"
    )


def get_logger(name: str = None):
    """Get a logger with the specified name.
    
    This is a wrapper around loguru.logger to maintain compatibility
    with code that expects a logger with a name.
    
    Args:
        name: Logger name (module name)
        
    Returns:
        loguru.logger instance
    """
    # loguru doesn't use named loggers like the standard logging module,
    # but we can add context to include the name
    if name:
        return logger.bind(name=name)
    return logger


# Error-specific logging utilities
def log_error_with_context(
    message: str,
    error: Optional[Exception] = None,
    level: str = "ERROR",
    **context
) -> None:
    """Log an error message with additional context.
    
    Args:
        message: Error message
        error: Exception object
        level: Log level (ERROR, WARNING, etc.)
        **context: Additional context to include in the log
    """
    log_func = getattr(logger, level.lower(), logger.error)
    
    # Add exception info to context if provided
    if error:
        context["error_type"] = type(error).__name__
        context["error_message"] = str(error)
    
    # Log with context
    log_func(message, **context)


def log_exception(
    message: str,
    exc_info: Optional[Exception] = None,
    **context
) -> None:
    """Log an exception with traceback and context.
    
    Args:
        message: Error message
        exc_info: Exception object (defaults to current exception)
        **context: Additional context to include in the log
    """
    logger.exception(message, **context)
