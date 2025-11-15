"""
Error handling utility (Phase 2A).

Generated - do not edit directly.
"""

from typing import Optional, Any


class FinaticError(Exception):
    """Base error class for Finatic SDK."""
    
    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        request_id: Optional[str] = None,
        original_error: Optional[Exception] = None
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.request_id = request_id
        self.original_error = original_error


class ApiError(FinaticError):
    """Error for API call failures."""
    
    def __init__(
        self,
        message: str,
        status_code: int,
        request_id: Optional[str] = None,
        original_error: Optional[Exception] = None
    ):
        super().__init__(message, status_code, request_id, original_error)


class ValidationError(FinaticError):
    """Error for validation failures."""
    
    def __init__(
        self,
        message: str,
        request_id: Optional[str] = None,
        original_error: Optional[Exception] = None
    ):
        super().__init__(message, 422, request_id, original_error)


def handle_error(error: Exception, request_id: Optional[str] = None) -> Exception:
    """Handle and transform errors from API calls.
    
    Args:
        error: Original exception
        request_id: Request ID for tracking
    
    Returns:
        Transformed error (FinaticError or subclass)
    """
    # Extract status code
    status_code = getattr(error, 'status_code', None) or getattr(error, 'status', None)
    
    # Extract error message
    message = str(error) or 'Unknown error'
    
    # Try to extract message from response
    if hasattr(error, 'response') and hasattr(error.response, 'json'):
        try:
            data = error.response.json()
            if 'detail' in data:
                detail = data['detail']
                message = detail if isinstance(detail, str) else str(detail)
            elif 'message' in data:
                message = data['message']
        except:
            pass
    
    # Create appropriate error type
    if status_code == 422:
        return ValidationError(message, request_id, error)
    elif status_code and status_code >= 400:
        return ApiError(message, status_code, request_id, error)
    
    return FinaticError(message, status_code, request_id, error)
