"""Error handling for synchronization operations.

This module provides a comprehensive error handling system for synchronization
operations, including error categorization, user-friendly error messages,
and retry logic for transient errors.
"""

from enum import Enum, auto
from typing import Dict, Any, Optional, List, Callable, Tuple
import time
import asyncio
from loguru import logger


class ErrorCategory(Enum):
    """Categories of synchronization errors."""
    
    # Connection errors
    CONNECTION = auto()  # Network or connection issues
    AUTHENTICATION = auto()  # Authentication failures
    
    # Server errors
    SERVER = auto()  # Server-side errors (5xx)
    RATE_LIMIT = auto()  # Rate limiting or throttling
    
    # Resource errors
    NOT_FOUND = auto()  # Resource not found (404)
    CONFLICT = auto()  # Resource conflicts (409)
    
    # Client errors
    VALIDATION = auto()  # Validation errors (400)
    PERMISSION = auto()  # Permission errors (403)
    
    # Data errors
    PARSING = auto()  # Data parsing errors
    MAPPING = auto()  # Data mapping errors
    
    # Other errors
    UNKNOWN = auto()  # Unknown or unclassified errors


class SyncError(Exception):
    """Base class for synchronization errors."""
    
    def __init__(
        self, 
        message: str, 
        category: ErrorCategory = ErrorCategory.UNKNOWN,
        original_error: Optional[Exception] = None,
        retry_after: Optional[int] = None,
        context: Optional[Dict[str, Any]] = None
    ):
        """Initialize a synchronization error.
        
        Args:
            message: Error message
            category: Error category
            original_error: Original exception that caused this error
            retry_after: Seconds to wait before retrying (if applicable)
            context: Additional context about the error
        """
        self.message = message
        self.category = category
        self.original_error = original_error
        self.retry_after = retry_after
        self.context = context or {}
        
        # Build the full error message
        full_message = f"{message}"
        if original_error:
            full_message += f" (Original error: {str(original_error)})"
        
        super().__init__(full_message)
    
    @property
    def is_retryable(self) -> bool:
        """Whether this error can be retried."""
        # Connection errors and server errors are generally retryable
        retryable_categories = [
            ErrorCategory.CONNECTION,
            ErrorCategory.SERVER,
            ErrorCategory.RATE_LIMIT
        ]
        return self.category in retryable_categories
    
    def get_user_friendly_message(self) -> str:
        """Get a user-friendly error message."""
        # Map error categories to user-friendly messages
        messages = {
            ErrorCategory.CONNECTION: "Could not connect to the server. Please check your internet connection.",
            ErrorCategory.AUTHENTICATION: "Authentication failed. Please check your credentials.",
            ErrorCategory.SERVER: "The server encountered an error. Please try again later.",
            ErrorCategory.RATE_LIMIT: "You've reached the rate limit. Please try again later.",
            ErrorCategory.NOT_FOUND: "The requested resource was not found.",
            ErrorCategory.CONFLICT: "There was a conflict with the remote resource.",
            ErrorCategory.VALIDATION: "The data provided was invalid.",
            ErrorCategory.PERMISSION: "You don't have permission to perform this action.",
            ErrorCategory.PARSING: "Could not parse the response from the server.",
            ErrorCategory.MAPPING: "Could not map the data between systems.",
            ErrorCategory.UNKNOWN: "An unknown error occurred."
        }
        
        base_message = messages.get(self.category, "An error occurred.")
        
        # Add specific context if available
        if self.context:
            if "task_id" in self.context:
                base_message += f" (Task ID: {self.context['task_id']})"
            if "system" in self.context:
                base_message += f" (System: {self.context['system']})"
        
        return base_message


class ConnectionError(SyncError):
    """Error when connecting to the external system."""
    
    def __init__(self, message: str, **kwargs):
        super().__init__(message, category=ErrorCategory.CONNECTION, **kwargs)


class AuthenticationError(SyncError):
    """Error when authenticating with the external system."""
    
    def __init__(self, message: str, **kwargs):
        super().__init__(message, category=ErrorCategory.AUTHENTICATION, **kwargs)


class ServerError(SyncError):
    """Error on the server side."""
    
    def __init__(self, message: str, **kwargs):
        super().__init__(message, category=ErrorCategory.SERVER, **kwargs)


class RateLimitError(SyncError):
    """Error when rate limited by the external system."""
    
    def __init__(self, message: str, retry_after: Optional[int] = None, **kwargs):
        super().__init__(message, category=ErrorCategory.RATE_LIMIT, retry_after=retry_after, **kwargs)


class ResourceNotFoundError(SyncError):
    """Error when a resource is not found."""
    
    def __init__(self, message: str, **kwargs):
        super().__init__(message, category=ErrorCategory.NOT_FOUND, **kwargs)


class ResourceConflictError(SyncError):
    """Error when there's a conflict with a remote resource."""
    
    def __init__(self, message: str, **kwargs):
        super().__init__(message, category=ErrorCategory.CONFLICT, **kwargs)


class ValidationError(SyncError):
    """Error when data validation fails."""
    
    def __init__(self, message: str, **kwargs):
        super().__init__(message, category=ErrorCategory.VALIDATION, **kwargs)


class PermissionError(SyncError):
    """Error when permission is denied."""
    
    def __init__(self, message: str, **kwargs):
        super().__init__(message, category=ErrorCategory.PERMISSION, **kwargs)


class ParsingError(SyncError):
    """Error when parsing data from the external system."""
    
    def __init__(self, message: str, **kwargs):
        super().__init__(message, category=ErrorCategory.PARSING, **kwargs)


class MappingError(SyncError):
    """Error when mapping data between systems."""
    
    def __init__(self, message: str, **kwargs):
        super().__init__(message, category=ErrorCategory.MAPPING, **kwargs)


async def with_retry(
    func: Callable,
    max_retries: int = 3,
    initial_delay: float = 1.0,
    backoff_factor: float = 2.0,
    retryable_errors: Optional[List[ErrorCategory]] = None,
    *args,
    **kwargs
) -> Any:
    """Execute a function with retry logic.
    
    Args:
        func: Function to execute
        max_retries: Maximum number of retries
        initial_delay: Initial delay between retries in seconds
        backoff_factor: Factor to increase delay by after each retry
        retryable_errors: List of error categories to retry on (defaults to connection and server errors)
        *args: Arguments to pass to the function
        **kwargs: Keyword arguments to pass to the function
        
    Returns:
        Result of the function
        
    Raises:
        SyncError: If all retries fail
    """
    if retryable_errors is None:
        retryable_errors = [
            ErrorCategory.CONNECTION,
            ErrorCategory.SERVER,
            ErrorCategory.RATE_LIMIT
        ]
    
    last_error = None
    delay = initial_delay
    
    for attempt in range(max_retries + 1):
        try:
            if asyncio.iscoroutinefunction(func):
                return await func(*args, **kwargs)
            else:
                return func(*args, **kwargs)
        except SyncError as e:
            last_error = e
            
            # Only retry if the error is retryable
            if e.category not in retryable_errors:
                logger.warning(f"Non-retryable error: {e}")
                raise
            
            # Use the retry_after value if provided, otherwise use the calculated delay
            retry_after = e.retry_after or delay
            
            # If this was the last attempt, raise the error
            if attempt == max_retries:
                logger.error(f"Max retries ({max_retries}) reached: {e}")
                raise
            
            logger.warning(f"Retryable error (attempt {attempt + 1}/{max_retries + 1}): {e}. Retrying in {retry_after}s")
            
            # Wait before retrying
            await asyncio.sleep(retry_after)
            
            # Increase the delay for the next retry
            delay *= backoff_factor
        except Exception as e:
            # Wrap other exceptions in a SyncError
            last_error = SyncError(
                message=f"Unexpected error: {str(e)}",
                original_error=e
            )
            logger.error(f"Unexpected error: {e}")
            raise last_error
    
    # This should never happen, but just in case
    if last_error:
        raise last_error
    else:
        raise SyncError("Unknown error in retry logic")


def categorize_error(error: Exception) -> Tuple[ErrorCategory, Optional[int]]:
    """Categorize an error and determine if it's retryable.
    
    Args:
        error: The error to categorize
        
    Returns:
        Tuple of (error category, retry after seconds or None)
    """
    # If it's already a SyncError, use its category
    if isinstance(error, SyncError):
        return error.category, error.retry_after
    
    # Check for common error types and categorize them
    error_str = str(error).lower()
    
    # Connection errors
    if any(s in error_str for s in ["connection", "timeout", "network", "unreachable"]):
        return ErrorCategory.CONNECTION, None
    
    # Authentication errors
    if any(s in error_str for s in ["auth", "unauthorized", "401", "credentials"]):
        return ErrorCategory.AUTHENTICATION, None
    
    # Server errors
    if any(s in error_str for s in ["server error", "500", "502", "503", "504"]):
        return ErrorCategory.SERVER, None
    
    # Rate limit errors
    if any(s in error_str for s in ["rate limit", "too many requests", "429"]):
        # Try to extract retry-after value
        retry_after = None
        if "retry after" in error_str:
            try:
                retry_after = int(error_str.split("retry after")[1].strip().split()[0])
            except (IndexError, ValueError):
                pass
        return ErrorCategory.RATE_LIMIT, retry_after
    
    # Resource not found
    if any(s in error_str for s in ["not found", "404"]):
        return ErrorCategory.NOT_FOUND, None
    
    # Resource conflict
    if any(s in error_str for s in ["conflict", "409"]):
        return ErrorCategory.CONFLICT, None
    
    # Validation errors
    if any(s in error_str for s in ["invalid", "validation", "400"]):
        return ErrorCategory.VALIDATION, None
    
    # Permission errors
    if any(s in error_str for s in ["permission", "forbidden", "403"]):
        return ErrorCategory.PERMISSION, None
    
    # Parsing errors
    if any(s in error_str for s in ["parse", "json", "xml", "decode"]):
        return ErrorCategory.PARSING, None
    
    # Default to unknown
    return ErrorCategory.UNKNOWN, None


def wrap_error(
    error: Exception,
    context: Optional[Dict[str, Any]] = None
) -> SyncError:
    """Wrap an exception in a SyncError with appropriate categorization.
    
    Args:
        error: The error to wrap
        context: Additional context about the error
        
    Returns:
        A SyncError instance
    """
    # If it's already a SyncError, just add context
    if isinstance(error, SyncError):
        if context:
            error.context.update(context)
        return error
    
    # Categorize the error
    category, retry_after = categorize_error(error)
    
    # Create a new SyncError with the appropriate category
    error_classes = {
        ErrorCategory.CONNECTION: ConnectionError,
        ErrorCategory.AUTHENTICATION: AuthenticationError,
        ErrorCategory.SERVER: ServerError,
        ErrorCategory.RATE_LIMIT: RateLimitError,
        ErrorCategory.NOT_FOUND: ResourceNotFoundError,
        ErrorCategory.CONFLICT: ResourceConflictError,
        ErrorCategory.VALIDATION: ValidationError,
        ErrorCategory.PERMISSION: PermissionError,
        ErrorCategory.PARSING: ParsingError,
        ErrorCategory.MAPPING: MappingError,
        ErrorCategory.UNKNOWN: SyncError
    }
    
    error_class = error_classes.get(category, SyncError)
    
    # Create the appropriate error instance
    kwargs = {
        "message": str(error),
        "original_error": error,
        "context": context or {}
    }
    
    if retry_after is not None:
        kwargs["retry_after"] = retry_after
    
    return error_class(**kwargs)
