"""Utility functions for MCP tools."""

from typing import Any, Dict, Optional

def create_content_response(content: Any) -> Dict:
    """Create a successful response with content.
    
    Args:
        content: Response content
    
    Returns:
        Response dictionary with content
    """
    return {
        "success": True,
        "content": content
    }

def create_error_response(message: str, details: Optional[Dict] = None) -> Dict:
    """Create an error response.
    
    Args:
        message: Error message
        details: Optional error details
    
    Returns:
        Response dictionary with error information
    """
    response = {
        "success": False,
        "error": {
            "message": message
        }
    }
    
    if details:
        response["error"]["details"] = details
    
    return response