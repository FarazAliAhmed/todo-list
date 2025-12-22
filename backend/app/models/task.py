"""
Task model for todo items.
"""
from datetime import datetime, UTC
from typing import Optional
from uuid import UUID
from sqlmodel import SQLModel, Field, Relationship


def utc_now():
    """Return current UTC time as timezone-aware datetime."""
    return datetime.now(UTC)


class Task(SQLModel, table=True):
    """
    Task model representing a todo item.
    Each task belongs to a specific user.
    """
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", index=True)
    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)

    # Relationship to user
    user: Optional["User"] = Relationship(back_populates="tasks")
