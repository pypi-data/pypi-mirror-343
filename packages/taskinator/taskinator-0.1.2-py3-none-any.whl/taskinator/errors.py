"""Centralized error handling for Taskinator.

This module provides a comprehensive error handling framework for the Taskinator
application, including a standardized error hierarchy, error codes, and utilities
for consistent error handling across the codebase.
"""

import inspect
import json
import os
import sys
import traceback
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Type, Union, Callable

from loguru import logger


class ErrorSeverity(str, Enum):
    """Severity levels for errors."""
    CRITICAL = "CRITICAL"  # System cannot continue operation
    ERROR = "ERROR"        # Operation failed, but system can continue
    WARNING = "WARNING"    # Issue detected, but operation succeeded
    INFO = "INFO"          # Informational message about potential issues


class ErrorCategory(str, Enum):
    """Categories for error classification."""
    # Input errors
    INPUT = "INP"          # Errors related to invalid user input
    
    # Storage errors
    STORAGE = "STG"        # Errors related to file and data storage operations
    
    # Sync errors
    SYNC = "SYN"           # Errors related to synchronization with external systems
    
    # Processing errors
    PROCESSING = "PRC"     # Errors during task processing and manipulation
    
    # Configuration errors
    CONFIG = "CFG"         # Errors in system configuration
    
    # AI service errors
    AI_SERVICE = "AIS"     # Errors related to AI service interactions
    
    # System errors
    SYSTEM = "SYS"         # Internal system errors


# Error code registry
ERROR_REGISTRY: Dict[str, Dict[str, Any]] = {}


def register_error(
    error_code: str,
    error_class: Type["TaskinatorError"],
    message_template: str,
    severity: ErrorSeverity = ErrorSeverity.ERROR,
    user_message_template: Optional[str] = None,
    recommended_actions: Optional[List[str]] = None
) -> None:
    """Register an error code in the registry.
    
    Args:
        error_code: Unique error code (format: TKN-XXX-NNN)
        error_class: Error class associated with this code
        message_template: Template for the technical error message
        severity: Error severity level
        user_message_template: Template for the user-facing message
        recommended_actions: List of recommended actions to resolve the error
    """
    if error_code in ERROR_REGISTRY:
        logger.warning(f"Error code {error_code} already registered, overwriting")
    
    ERROR_REGISTRY[error_code] = {
        "error_class": error_class,
        "message_template": message_template,
        "user_message_template": user_message_template or message_template,
        "severity": severity,
        "recommended_actions": recommended_actions or []
    }


def get_error_info(error_code: str) -> Dict[str, Any]:
    """Get information about a registered error code.
    
    Args:
        error_code: The error code to look up
        
    Returns:
        Dictionary with error information
        
    Raises:
        ValueError: If the error code is not registered
    """
    if error_code not in ERROR_REGISTRY:
        raise ValueError(f"Error code {error_code} is not registered")
    
    return ERROR_REGISTRY[error_code]


class TaskinatorError(Exception):
    """Base class for all Taskinator errors."""
    
    # Default values that can be overridden by subclasses
    DEFAULT_CODE: Optional[str] = None
    DEFAULT_MESSAGE: str = "An error occurred in Taskinator"
    DEFAULT_USER_MESSAGE: str = "An unexpected error occurred"
    CATEGORY: ErrorCategory = ErrorCategory.SYSTEM
    SEVERITY: ErrorSeverity = ErrorSeverity.ERROR
    
    def __init__(
        self, 
        message: Optional[str] = None,
        error_code: Optional[str] = None,
        user_message: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        original_error: Optional[Exception] = None,
        severity: Optional[ErrorSeverity] = None,
        recommended_actions: Optional[List[str]] = None
    ):
        """Initialize a Taskinator error.
        
        Args:
            message: Technical error message (for logs)
            error_code: Unique error code
            user_message: User-friendly error message
            details: Additional context about the error
            original_error: Original exception if this is wrapping another error
            severity: Error severity level
            recommended_actions: List of recommended actions to resolve the error
        """
        self.error_code = error_code or self.DEFAULT_CODE
        self.message = message or self.DEFAULT_MESSAGE
        self.user_message = user_message or self.DEFAULT_USER_MESSAGE
        self.details = details or {}
        self.original_error = original_error
        self.severity = severity or self.SEVERITY
        self.recommended_actions = recommended_actions or []
        self.timestamp = datetime.now()
        
        # Get caller information
        frame = inspect.currentframe()
        if frame:
            caller_frame = frame.f_back
            if caller_frame:
                self.details["file"] = caller_frame.f_code.co_filename
                self.details["line"] = caller_frame.f_lineno
                self.details["function"] = caller_frame.f_code.co_name
        
        # If we have an error code, try to get registered information
        if self.error_code and self.error_code in ERROR_REGISTRY:
            error_info = ERROR_REGISTRY[self.error_code]
            
            # Use registered values if not explicitly provided
            if not message:
                self.message = error_info["message_template"]
            
            if not user_message:
                self.user_message = error_info["user_message_template"]
            
            if not severity:
                self.severity = error_info["severity"]
            
            if not recommended_actions:
                self.recommended_actions = error_info["recommended_actions"]
        
        # Format the message with details if it contains placeholders
        try:
            if "{" in self.message and "}" in self.message:
                self.message = self.message.format(**self.details)
        except KeyError:
            # If formatting fails, just use the original message
            pass
        
        # Format the user message with details if it contains placeholders
        try:
            if "{" in self.user_message and "}" in self.user_message:
                self.user_message = self.user_message.format(**self.details)
        except KeyError:
            # If formatting fails, just use the original message
            pass
        
        # Call the parent constructor with the technical message
        super().__init__(self.message)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the error to a dictionary for logging and serialization.
        
        Returns:
            Dictionary representation of the error
        """
        result = {
            "error_code": self.error_code,
            "message": self.message,
            "user_message": self.user_message,
            "severity": self.severity,
            "timestamp": self.timestamp.isoformat(),
            "details": self.details,
            "recommended_actions": self.recommended_actions
        }
        
        if self.original_error:
            result["original_error"] = {
                "type": type(self.original_error).__name__,
                "message": str(self.original_error)
            }
        
        return result
    
    def to_json(self) -> str:
        """Convert the error to a JSON string.
        
        Returns:
            JSON representation of the error
        """
        return json.dumps(self.to_dict(), indent=2, default=str)
    
    def log(self, logger_instance=None) -> None:
        """Log the error with the appropriate severity level.
        
        Args:
            logger_instance: Logger instance to use (defaults to loguru.logger)
        """
        log = logger_instance or logger
        
        # Map severity to logging method
        log_method = {
            ErrorSeverity.CRITICAL: log.critical,
            ErrorSeverity.ERROR: log.error,
            ErrorSeverity.WARNING: log.warning,
            ErrorSeverity.INFO: log.info
        }.get(self.severity, log.error)
        
        # Log the error with context
        log_method(
            f"{self.error_code or 'ERROR'}: {self.message}",
            **self.details
        )
        
        # Log traceback for non-INFO severity
        if self.severity != ErrorSeverity.INFO and self.original_error:
            log.debug(f"Original error: {traceback.format_exc()}")
    
    @classmethod
    def from_exception(
        cls,
        exception: Exception,
        message: Optional[str] = None,
        error_code: Optional[str] = None,
        user_message: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ) -> "TaskinatorError":
        """Create a TaskinatorError from another exception.
        
        Args:
            exception: The exception to wrap
            message: Optional message (defaults to exception message)
            error_code: Optional error code
            user_message: Optional user-friendly message
            details: Optional additional context
            
        Returns:
            A new TaskinatorError instance
        """
        return cls(
            message=message or str(exception),
            error_code=error_code,
            user_message=user_message,
            details=details,
            original_error=exception
        )


# Input Errors
class InputError(TaskinatorError):
    """Base class for errors related to invalid user input."""
    CATEGORY = ErrorCategory.INPUT
    DEFAULT_CODE = "TKN-INP-000"
    DEFAULT_MESSAGE = "Invalid input provided"
    DEFAULT_USER_MESSAGE = "The provided input is invalid"


class ValidationError(InputError):
    """Error for invalid data format or content."""
    DEFAULT_CODE = "TKN-INP-001"
    DEFAULT_MESSAGE = "Validation error: {details}"
    DEFAULT_USER_MESSAGE = "The provided data is invalid"


class MissingParameterError(InputError):
    """Error for missing required parameter."""
    DEFAULT_CODE = "TKN-INP-002"
    DEFAULT_MESSAGE = "Missing required parameter: {parameter}"
    DEFAULT_USER_MESSAGE = "A required parameter is missing"


class InvalidParameterError(InputError):
    """Error for invalid parameter value."""
    DEFAULT_CODE = "TKN-INP-003"
    DEFAULT_MESSAGE = "Invalid parameter value for {parameter}: {value}"
    DEFAULT_USER_MESSAGE = "The provided parameter value is invalid"


class PermissionError(InputError):
    """Error for insufficient permissions."""
    DEFAULT_CODE = "TKN-INP-004"
    DEFAULT_MESSAGE = "Permission denied: {operation} requires {required_permission}"
    DEFAULT_USER_MESSAGE = "You don't have permission to perform this operation"


# Storage Errors
class StorageError(TaskinatorError):
    """Base class for errors related to file and data storage operations."""
    CATEGORY = ErrorCategory.STORAGE
    DEFAULT_CODE = "TKN-STG-000"
    DEFAULT_MESSAGE = "Storage operation failed"
    DEFAULT_USER_MESSAGE = "Failed to access or modify stored data"


class StorageFileNotFoundError(StorageError):
    """Error for file not found."""
    DEFAULT_CODE = "TKN-STG-001"
    DEFAULT_MESSAGE = "File not found: {file_path}"
    DEFAULT_USER_MESSAGE = "The requested file could not be found"


class StorageFileAccessError(StorageError):
    """Error for file access issues."""
    DEFAULT_CODE = "TKN-STG-002"
    DEFAULT_MESSAGE = "Cannot access file: {file_path}, reason: {reason}"
    DEFAULT_USER_MESSAGE = "Cannot access the requested file"


class StorageFileFormatError(StorageError):
    """Error for invalid file format."""
    DEFAULT_CODE = "TKN-STG-003"
    DEFAULT_MESSAGE = "Invalid file format in {file_path}: {error}"
    DEFAULT_USER_MESSAGE = "The file has an invalid format"


class StorageFileLockError(StorageError):
    """Error for file locking issues."""
    DEFAULT_CODE = "TKN-STG-004"
    DEFAULT_MESSAGE = "Cannot acquire lock on file: {file_path}, reason: {reason}"
    DEFAULT_USER_MESSAGE = "Cannot access the file because it is locked"


class StorageConsistencyError(StorageError):
    """Error for data consistency issues."""
    DEFAULT_CODE = "TKN-STG-005"
    DEFAULT_MESSAGE = "Data consistency error: {details}"
    DEFAULT_USER_MESSAGE = "Inconsistency detected in stored data"


# Sync Errors
class SyncError(TaskinatorError):
    """Base class for errors related to synchronization with external systems."""
    CATEGORY = ErrorCategory.SYNC
    DEFAULT_CODE = "TKN-SYN-000"
    DEFAULT_MESSAGE = "Synchronization operation failed"
    DEFAULT_USER_MESSAGE = "Failed to synchronize with external system"


class SyncConnectionError(SyncError):
    """Error for connection issues with external systems."""
    DEFAULT_CODE = "TKN-SYN-001"
    DEFAULT_MESSAGE = "Cannot connect to external system: {system}, reason: {reason}"
    DEFAULT_USER_MESSAGE = "Cannot connect to external system"


class SyncAuthenticationError(SyncError):
    """Error for authentication issues with external systems."""
    DEFAULT_CODE = "TKN-SYN-002"
    DEFAULT_MESSAGE = "Authentication failed with external system: {system}"
    DEFAULT_USER_MESSAGE = "Authentication failed with external system"


class SyncResourceNotFoundError(SyncError):
    """Error for resource not found in external system."""
    DEFAULT_CODE = "TKN-SYN-003"
    DEFAULT_MESSAGE = "Resource not found in external system: {resource}"
    DEFAULT_USER_MESSAGE = "The requested resource was not found in the external system"


class SyncResourceConflictError(SyncError):
    """Error for resource conflicts with external system."""
    DEFAULT_CODE = "TKN-SYN-004"
    DEFAULT_MESSAGE = "Resource conflict in external system: {resource}, details: {details}"
    DEFAULT_USER_MESSAGE = "A conflict was detected with the external system"


class SyncRateLimitError(SyncError):
    """Error for rate limit exceeded with external system."""
    DEFAULT_CODE = "TKN-SYN-005"
    DEFAULT_MESSAGE = "Rate limit exceeded for external system: {system}"
    DEFAULT_USER_MESSAGE = "Rate limit exceeded for external system, please try again later"


# Processing Errors
class ProcessingError(TaskinatorError):
    """Base class for errors during task processing and manipulation."""
    CATEGORY = ErrorCategory.PROCESSING
    DEFAULT_CODE = "TKN-PRC-000"
    DEFAULT_MESSAGE = "Task processing operation failed"
    DEFAULT_USER_MESSAGE = "Failed to process task"


class TaskNotFoundError(ProcessingError):
    """Error for task not found."""
    DEFAULT_CODE = "TKN-PRC-001"
    DEFAULT_MESSAGE = "Task not found: {task_id}"
    DEFAULT_USER_MESSAGE = "The requested task could not be found"


class DependencyError(ProcessingError):
    """Error for issues with task dependencies."""
    DEFAULT_CODE = "TKN-PRC-002"
    DEFAULT_MESSAGE = "Dependency error: {details}"
    DEFAULT_USER_MESSAGE = "There is an issue with task dependencies"


class OperationError(ProcessingError):
    """Error for failed operations on tasks."""
    DEFAULT_CODE = "TKN-PRC-003"
    DEFAULT_MESSAGE = "Operation failed: {operation}, reason: {reason}"
    DEFAULT_USER_MESSAGE = "The requested operation could not be completed"


class WorkflowError(ProcessingError):
    """Error for issues in task workflow."""
    DEFAULT_CODE = "TKN-PRC-004"
    DEFAULT_MESSAGE = "Workflow error: {details}"
    DEFAULT_USER_MESSAGE = "There is an issue with the task workflow"


# Configuration Errors
class ConfigurationError(TaskinatorError):
    """Base class for errors in system configuration."""
    CATEGORY = ErrorCategory.CONFIG
    DEFAULT_CODE = "TKN-CFG-000"
    DEFAULT_MESSAGE = "Configuration error"
    DEFAULT_USER_MESSAGE = "There is an issue with the system configuration"


class InvalidConfigError(ConfigurationError):
    """Error for invalid configuration."""
    DEFAULT_CODE = "TKN-CFG-001"
    DEFAULT_MESSAGE = "Invalid configuration: {details}"
    DEFAULT_USER_MESSAGE = "The system configuration is invalid"


class MissingConfigError(ConfigurationError):
    """Error for missing required configuration."""
    DEFAULT_CODE = "TKN-CFG-002"
    DEFAULT_MESSAGE = "Missing required configuration: {config_key}"
    DEFAULT_USER_MESSAGE = "A required configuration setting is missing"


class EnvironmentError(ConfigurationError):
    """Error for issues with environment setup."""
    DEFAULT_CODE = "TKN-CFG-003"
    DEFAULT_MESSAGE = "Environment error: {details}"
    DEFAULT_USER_MESSAGE = "There is an issue with the environment setup"


# AI Service Errors
class AIServiceError(TaskinatorError):
    """Base class for errors related to AI service interactions."""
    CATEGORY = ErrorCategory.AI_SERVICE
    DEFAULT_CODE = "TKN-AIS-000"
    DEFAULT_MESSAGE = "AI service operation failed"
    DEFAULT_USER_MESSAGE = "Failed to perform AI service operation"


class AIConnectionError(AIServiceError):
    """Error for connection issues with AI services."""
    DEFAULT_CODE = "TKN-AIS-001"
    DEFAULT_MESSAGE = "Cannot connect to AI service: {service}, reason: {reason}"
    DEFAULT_USER_MESSAGE = "Cannot connect to AI service"


class AIResponseError(AIServiceError):
    """Error for invalid responses from AI services."""
    DEFAULT_CODE = "TKN-AIS-002"
    DEFAULT_MESSAGE = "Invalid response from AI service: {service}, details: {details}"
    DEFAULT_USER_MESSAGE = "Received an invalid response from the AI service"


class AIQuotaError(AIServiceError):
    """Error for AI service quota exceeded."""
    DEFAULT_CODE = "TKN-AIS-003"
    DEFAULT_MESSAGE = "AI service quota exceeded: {service}"
    DEFAULT_USER_MESSAGE = "AI service quota exceeded, please try again later"


class AIModelError(AIServiceError):
    """Error for issues with AI models."""
    DEFAULT_CODE = "TKN-AIS-004"
    DEFAULT_MESSAGE = "AI model error: {model}, details: {details}"
    DEFAULT_USER_MESSAGE = "There is an issue with the AI model"


# System Errors
class SystemError(TaskinatorError):
    """Base class for internal system errors."""
    CATEGORY = ErrorCategory.SYSTEM
    DEFAULT_CODE = "TKN-SYS-000"
    DEFAULT_MESSAGE = "Internal system error"
    DEFAULT_USER_MESSAGE = "An internal system error occurred"


class InternalError(SystemError):
    """Error for unexpected internal errors."""
    DEFAULT_CODE = "TKN-SYS-001"
    DEFAULT_MESSAGE = "Internal error: {details}"
    DEFAULT_USER_MESSAGE = "An unexpected internal error occurred"


class ResourceExhaustedError(SystemError):
    """Error for system resources exhausted."""
    DEFAULT_CODE = "TKN-SYS-002"
    DEFAULT_MESSAGE = "System resources exhausted: {resource}"
    DEFAULT_USER_MESSAGE = "System resources are currently exhausted, please try again later"


class ConcurrencyError(SystemError):
    """Error for concurrency-related issues."""
    DEFAULT_CODE = "TKN-SYS-003"
    DEFAULT_MESSAGE = "Concurrency error: {details}"
    DEFAULT_USER_MESSAGE = "A concurrency issue was detected"


# Register common errors
register_error(
    "TKN-INP-001",
    ValidationError,
    "Validation error: {details}",
    ErrorSeverity.ERROR,
    "The provided data is invalid",
    ["Check the input data format", "Ensure all required fields are provided"]
)

register_error(
    "TKN-STG-001",
    StorageFileNotFoundError,
    "File not found: {file_path}",
    ErrorSeverity.ERROR,
    "The requested file could not be found",
    ["Check if the file exists", "Verify the file path is correct"]
)

register_error(
    "TKN-PRC-001",
    TaskNotFoundError,
    "Task not found: {task_id}",
    ErrorSeverity.ERROR,
    "The requested task could not be found",
    ["Check if the task ID is correct", "Verify the task exists"]
)

register_error(
    "TKN-SYN-001",
    SyncConnectionError,
    "Cannot connect to external system: {system}, reason: {reason}",
    ErrorSeverity.ERROR,
    "Cannot connect to external system",
    ["Check your network connection", "Verify the external system is available"]
)

register_error(
    "TKN-AIS-001",
    AIConnectionError,
    "Cannot connect to AI service: {service}, reason: {reason}",
    ErrorSeverity.ERROR,
    "Cannot connect to AI service",
    ["Check your network connection", "Verify the AI service is available"]
)

register_error(
    "TKN-SYS-001",
    InternalError,
    "Internal error: {details}",
    ErrorSeverity.ERROR,
    "An unexpected internal error occurred",
    ["Check the application logs for more details", "Contact support if the issue persists"]
)


# Error handling utilities
def handle_error(
    error: Union[Exception, TaskinatorError],
    log: bool = True,
    raise_error: bool = True,
    default_return: Any = None,
    error_transformer: Optional[Callable[[Exception], TaskinatorError]] = None
) -> Any:
    """Handle an error with consistent logging and optional re-raising.
    
    Args:
        error: The error to handle
        log: Whether to log the error
        raise_error: Whether to re-raise the error
        default_return: Value to return if not raising
        error_transformer: Function to transform standard exceptions to TaskinatorError
        
    Returns:
        default_return if not raising
        
    Raises:
        TaskinatorError: The transformed error if raise_error is True
    """
    # Transform the error if it's not already a TaskinatorError
    if not isinstance(error, TaskinatorError):
        if error_transformer:
            error = error_transformer(error)
        else:
            error = TaskinatorError.from_exception(error)
    
    # Log the error if requested
    if log:
        error.log()
    
    # Re-raise if requested
    if raise_error:
        raise error
    
    return default_return


def safe_execute(
    func: Callable,
    *args,
    error_handler: Optional[Callable[[Exception], Any]] = None,
    log_error: bool = True,
    raise_error: bool = True,
    default_return: Any = None,
    error_transformer: Optional[Callable[[Exception], TaskinatorError]] = None,
    **kwargs
) -> Any:
    """Execute a function with consistent error handling.
    
    Args:
        func: Function to execute
        *args: Arguments to pass to the function
        error_handler: Custom error handler function
        log_error: Whether to log errors
        raise_error: Whether to re-raise errors
        default_return: Value to return on error if not raising
        error_transformer: Function to transform standard exceptions to TaskinatorError
        **kwargs: Keyword arguments to pass to the function
        
    Returns:
        Result of the function or default_return on error
        
    Raises:
        TaskinatorError: If an error occurs and raise_error is True
    """
    try:
        return func(*args, **kwargs)
    except Exception as e:
        if error_handler:
            return error_handler(e)
        else:
            return handle_error(
                e,
                log=log_error,
                raise_error=raise_error,
                default_return=default_return,
                error_transformer=error_transformer
            )


def error_handler(
    error_transformer: Optional[Callable[[Exception], TaskinatorError]] = None,
    log_error: bool = True,
    raise_error: bool = True,
    default_return: Any = None
) -> Callable:
    """Decorator for consistent error handling.
    
    Args:
        error_transformer: Function to transform standard exceptions to TaskinatorError
        log_error: Whether to log errors
        raise_error: Whether to re-raise errors
        default_return: Value to return on error if not raising
        
    Returns:
        Decorator function
    """
    def decorator(func: Callable) -> Callable:
        """Decorator function.
        
        Args:
            func: Function to decorate
            
        Returns:
            Wrapped function
        """
        def wrapper(*args, **kwargs) -> Any:
            """Wrapped function.
            
            Args:
                *args: Arguments to pass to the function
                **kwargs: Keyword arguments to pass to the function
                
            Returns:
                Result of the function or default_return on error
                
            Raises:
                TaskinatorError: If an error occurs and raise_error is True
            """
            return safe_execute(
                func,
                *args,
                error_transformer=error_transformer,
                log_error=log_error,
                raise_error=raise_error,
                default_return=default_return,
                **kwargs
            )
        
        # Preserve function metadata
        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__
        wrapper.__module__ = func.__module__
        
        return wrapper
    
    return decorator


# Context manager for error handling
class ErrorContext:
    """Context manager for consistent error handling.
    
    Example:
        with ErrorContext("Reading file", file_path=path) as ctx:
            data = json.load(open(path))
            return data
    """
    
    def __init__(
        self,
        operation: str,
        error_transformer: Optional[Callable[[Exception], TaskinatorError]] = None,
        log_error: bool = True,
        raise_error: bool = True,
        default_return: Any = None,
        **context_details
    ):
        """Initialize the error context.
        
        Args:
            operation: Description of the operation being performed
            error_transformer: Function to transform standard exceptions to TaskinatorError
            log_error: Whether to log errors
            raise_error: Whether to re-raise errors
            default_return: Value to return on error if not raising
            **context_details: Additional context details to include in error
        """
        self.operation = operation
        self.error_transformer = error_transformer
        self.log_error = log_error
        self.raise_error = raise_error
        self.default_return = default_return
        self.context_details = context_details
        self.result = None
    
    def __enter__(self):
        """Enter the context.
        
        Returns:
            Self for storing results
        """
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the context and handle any errors.
        
        Args:
            exc_type: Exception type
            exc_val: Exception value
            exc_tb: Exception traceback
            
        Returns:
            True if the exception was handled, False otherwise
        """
        if exc_val is None:
            return False
        
        # Create a default error transformer if none was provided
        if self.error_transformer is None:
            def default_transformer(e: Exception) -> TaskinatorError:
                return TaskinatorError.from_exception(
                    e,
                    message=f"Error during {self.operation}: {str(e)}",
                    details=self.context_details
                )
            
            self.error_transformer = default_transformer
        
        # Handle the error
        self.result = handle_error(
            exc_val,
            log=self.log_error,
            raise_error=self.raise_error,
            default_return=self.default_return,
            error_transformer=self.error_transformer
        )
        
        # Return True to suppress the exception if we're not raising
        return not self.raise_error
