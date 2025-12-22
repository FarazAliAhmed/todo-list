"""
User model for authentication and task ownership.
"""
from datetime import datetime, UTC
from typing import Optional, List
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Relationship


def utc_now():
    """Return current UTC time as timezone-aware datetime."""
    return datetime.now(UTC)


class User(SQLModel, table=True):
    """
    User model representing authenticated users.
    Managed by Better Auth on the frontend.
    """
    __tablename__ = "user"  # Match Better Auth table name

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    password_hash: str = Field(max_length=255)
    name: Optional[str] = Field(default=None, max_length=255)
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)

    # Relationships removed - no foreign keys
