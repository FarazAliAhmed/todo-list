"""
Test JWT authentication middleware with mock tokens.
"""
from datetime import datetime, timedelta, UTC
from uuid import uuid4
from jose import jwt
from fastapi import HTTPException
from app.config import settings
from app.middleware.auth import verify_jwt_token, validate_user_id
from app.models.user import User


def create_mock_jwt_token(user_id: str, expired: bool = False) -> str:
    """
    Create a mock JWT token for testing.

    Args:
        user_id: The user ID to include in the token
        expired: Whether to create an expired token

    Returns:
        str: The encoded JWT token
    """
    if expired:
        exp = datetime.now(UTC) - timedelta(days=1)
    else:
        exp = datetime.now(UTC) + timedelta(days=settings.jwt_expiration_days)

    payload = {
        "sub": user_id,
        "email": "test@example.com",
        "exp": exp,
        "iat": datetime.now(UTC)
    }

    token = jwt.encode(
        payload,
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm
    )

    return token


def test_verify_valid_token():
    """Test that a valid JWT token is verified successfully."""
    user_id = str(uuid4())
    token = create_mock_jwt_token(user_id)

    payload = verify_jwt_token(token)

    assert payload is not None
    assert payload["sub"] == user_id
    assert payload["email"] == "test@example.com"
    print("✓ Valid token verification passed")


def test_verify_expired_token():
    """Test that an expired JWT token raises an exception."""
    user_id = str(uuid4())
    token = create_mock_jwt_token(user_id, expired=True)

    try:
        verify_jwt_token(token)
        assert False, "Expected HTTPException but none was raised"
    except HTTPException as exc:
        assert exc.status_code == 401
        assert "Invalid or expired token" in exc.detail
        print("✓ Expired token rejection passed")


def test_verify_invalid_token():
    """Test that an invalid JWT token raises an exception."""
    invalid_token = "invalid.token.here"

    try:
        verify_jwt_token(invalid_token)
        assert False, "Expected HTTPException but none was raised"
    except HTTPException as exc:
        assert exc.status_code == 401
        assert "Invalid or expired token" in exc.detail
        print("✓ Invalid token rejection passed")


def test_verify_tampered_token():
    """Test that a tampered JWT token raises an exception."""
    user_id = str(uuid4())
    token = create_mock_jwt_token(user_id)

    # Tamper with the token by changing a character
    tampered_token = token[:-5] + "XXXXX"

    try:
        verify_jwt_token(tampered_token)
        assert False, "Expected HTTPException but none was raised"
    except HTTPException as exc:
        assert exc.status_code == 401
        print("✓ Tampered token rejection passed")


def test_validate_matching_user_id():
    """Test that matching user IDs pass validation."""
    user_id = uuid4()
    mock_user = User(
        id=user_id,
        email="test@example.com",
        password_hash="hashed_password"
    )

    # Should not raise an exception
    validate_user_id(mock_user, str(user_id))
    print("✓ Matching user ID validation passed")


def test_validate_mismatched_user_id():
    """Test that mismatched user IDs raise a 403 Forbidden exception."""
    user_id = uuid4()
    different_user_id = uuid4()

    mock_user = User(
        id=user_id,
        email="test@example.com",
        password_hash="hashed_password"
    )

    try:
        validate_user_id(mock_user, str(different_user_id))
        assert False, "Expected HTTPException but none was raised"
    except HTTPException as exc:
        assert exc.status_code == 403
        assert "Access denied" in exc.detail
        print("✓ Mismatched user ID rejection passed")


def test_validate_invalid_user_id_format():
    """Test that invalid user ID format raises a 400 Bad Request exception."""
    user_id = uuid4()
    mock_user = User(
        id=user_id,
        email="test@example.com",
        password_hash="hashed_password"
    )

    try:
        validate_user_id(mock_user, "not-a-valid-uuid")
        assert False, "Expected HTTPException but none was raised"
    except HTTPException as exc:
        assert exc.status_code == 400
        assert "Invalid user ID format" in exc.detail
        print("✓ Invalid user ID format rejection passed")


if __name__ == "__main__":
    print("\n=== Testing JWT Authentication Middleware ===\n")

    # Run tests
    test_verify_valid_token()
    test_verify_expired_token()
    test_verify_invalid_token()
    test_verify_tampered_token()
    test_validate_matching_user_id()
    test_validate_mismatched_user_id()
    test_validate_invalid_user_id_format()

    print("\n=== All middleware tests passed! ===\n")
