"""
Helper functions for creating consistent HTTP exceptions.
"""
from typing import Optional
from fastapi import HTTPException, status


def unauthorized_error(detail: str = "Authentication required") -> HTTPException:
    """
    Create a 401 Unauthorized error.

    Requirements: Requirement 11 (Error Handling)
    - Returns 401 status code
    - Includes WWW-Authenticate header
    """
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"}
    )


def forbidden_error(detail: str = "Access denied") -> HTTPException:
    """
    Create a 403 Forbidden error.

    Requirements: Requirement 11 (Error Handling)
    - Returns 403 status code
    - Used when user doesn't have permission
    """
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=detail
    )


def not_found_error(resource: str, resource_id: Optional[int] = None) -> HTTPException:
    """
    Create a 404 Not Found error.

    Requirements: Requirement 11 (Error Handling)
    - Returns 404 status code
    - Provides clear message about missing resource
    """
    if resource_id:
        detail = f"{resource} {resource_id} not found"
    else:
        detail = f"{resource} not found"

    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=detail
    )


def bad_request_error(detail: str) -> HTTPException:
    """
    Create a 400 Bad Request error.

    Requirements: Requirement 11 (Error Handling)
    - Returns 400 status code
    - Used for validation errors and malformed requests
    """
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=detail
    )


def internal_server_error(detail: str = "An internal server error occurred") -> HTTPException:
    """
    Create a 500 Internal Server Error.

    Requirements: Requirement 11 (Error Handling)
    - Returns 500 status code
    - Used for unexpected server errors
    """
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=detail
    )
