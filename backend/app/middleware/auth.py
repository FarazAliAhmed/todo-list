"""
JWT Authentication Middleware for FastAPI.
Handles token verification and user authentication.
"""
from typing import Optional
from uuid import UUID
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlmodel import Session, select
from app.config import settings
from app.database import get_session
from app.models.user import User
from app.errors import unauthorized_error, forbidden_error, bad_request_error


# Security scheme for JWT Bearer tokens
# auto_error=True makes it return 403 by default, but we want 401
security = HTTPBearer(auto_error=False)


def verify_jwt_token(token: str) -> dict:
    """
    Verify and decode a JWT token.

    Args:
        token: The JWT token string to verify

    Returns:
        dict: The decoded token payload

    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        payload = jwt.decode(
            token,
            settings.effective_jwt_secret,
            algorithms=[settings.jwt_algorithm]
        )
        return payload
    except JWTError as e:
        raise unauthorized_error("Invalid or expired token") from e


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    session: Session = Depends(get_session)
) -> User:
    """
    Dependency to get the current authenticated user from JWT token.

    Args:
        credentials: HTTP Bearer token credentials
        session: Database session

    Returns:
        User: The authenticated user object

    Raises:
        HTTPException: If token is invalid or user not found
    """
    if credentials is None:
        raise unauthorized_error("Authentication required")

    token = credentials.credentials

    # Verify and decode token
    payload = verify_jwt_token(token)

    # Extract user_id from token payload
    user_id_str: Optional[str] = payload.get("sub")
    if user_id_str is None:
        raise unauthorized_error("Invalid token payload: missing user ID")

    # Convert string to UUID
    try:
        user_id = UUID(user_id_str)
    except ValueError as e:
        raise unauthorized_error("Invalid token payload: malformed user ID") from e

    # Query user from database
    statement = select(User).where(User.id == user_id)
    user = session.exec(statement).first()

    if user is None:
        raise unauthorized_error("User not found")

    return user


def validate_user_id(current_user: User, requested_user_id: str) -> None:
    """
    Validate that the authenticated user matches the requested user_id in the URL.
    This ensures users can only access their own resources.

    Args:
        current_user: The authenticated user from JWT token
        requested_user_id: The user_id from the URL path parameter

    Raises:
        HTTPException: If user_id doesn't match the authenticated user
    """
    try:
        requested_uuid = UUID(requested_user_id)
    except ValueError as e:
        raise bad_request_error("Invalid user ID format in URL") from e

    if current_user.id != requested_uuid:
        raise forbidden_error("Access denied: You can only access your own resources")
