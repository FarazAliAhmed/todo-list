"""
Custom exceptions and global exception handlers for the Todo API.
Provides consistent error response format across all endpoints.
"""
from typing import Any, Dict, Optional
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
import logging

logger = logging.getLogger(__name__)


class TodoAPIException(Exception):
    """Base exception for Todo API errors."""

    def __init__(
        self,
        status_code: int,
        detail: str,
        headers: Optional[Dict[str, str]] = None
    ):
        self.status_code = status_code
        self.detail = detail
        self.headers = headers
        super().__init__(detail)


def create_error_response(
    status_code: int,
    detail: str,
    errors: Optional[list] = None
) -> Dict[str, Any]:
    """
    Create a consistent error response format.

    Args:
        status_code: HTTP status code
        detail: Error message
        errors: Optional list of validation errors

    Returns:
        dict: Standardized error response
    """
    response = {
        "detail": detail,
        "status_code": status_code
    }

    if errors:
        response["errors"] = errors

    return response


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
) -> JSONResponse:
    """
    Handle Pydantic validation errors (400 Bad Request).

    Requirements: Requirement 11 (Error Handling and User Feedback)
    - Returns 400 status code for validation errors
    - Provides detailed field-level error messages
    """
    errors = []
    for error in exc.errors():
        field = ".".join(str(loc) for loc in error["loc"] if loc != "body")
        errors.append({
            "field": field,
            "message": error["msg"],
            "type": error["type"]
        })

    logger.warning(f"Validation error on {request.url.path}: {errors}")

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=create_error_response(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Validation error",
            errors=errors
        )
    )


async def sqlalchemy_exception_handler(
    request: Request,
    exc: SQLAlchemyError
) -> JSONResponse:
    """
    Handle database errors (500 Internal Server Error).

    Requirements: Requirement 11 (Error Handling and User Feedback)
    - Returns 500 status code for database errors
    - Logs error details for debugging
    - Returns generic message to user (don't expose internal details)
    """
    logger.error(f"Database error on {request.url.path}: {str(exc)}", exc_info=True)

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=create_error_response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal server error occurred. Please try again later."
        )
    )


async def generic_exception_handler(
    request: Request,
    exc: Exception
) -> JSONResponse:
    """
    Handle all unhandled exceptions (500 Internal Server Error).

    Requirements: Requirement 11 (Error Handling and User Feedback)
    - Catches all unexpected errors
    - Returns 500 status code
    - Logs error details for debugging
    - Returns generic message to user
    """
    logger.error(
        f"Unhandled exception on {request.url.path}: {str(exc)}",
        exc_info=True
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=create_error_response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again later."
        )
    )
