"""
Task-related Pydantic schemas for request/response validation.

Requirements: Requirement 11 (Error Handling)
- Validates title length (1-200 chars)
- Validates description length (max 1000 chars)
- Provides clear validation error messages
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, field_validator


class TaskBase(BaseModel):
    """Base schema for task data."""
    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Task title (1-200 characters)"
    )
    description: Optional[str] = Field(
        None,
        max_length=1000,
        description="Task description (max 1000 characters)"
    )

    @field_validator('title')
    @classmethod
    def validate_title(cls, v: str) -> str:
        """Validate title is not empty or whitespace only."""
        if not v or not v.strip():
            raise ValueError("Title cannot be empty or whitespace only")
        return v.strip()

    @field_validator('description')
    @classmethod
    def validate_description(cls, v: Optional[str]) -> Optional[str]:
        """Validate and clean description."""
        if v is not None:
            v = v.strip()
            if not v:
                return None
        return v


class TaskCreate(TaskBase):
    """Schema for creating a new task."""
    pass


class TaskUpdate(BaseModel):
    """Schema for updating a task."""
    title: Optional[str] = Field(
        None,
        min_length=1,
        max_length=200,
        description="Task title (1-200 characters)"
    )
    description: Optional[str] = Field(
        None,
        max_length=1000,
        description="Task description (max 1000 characters)"
    )
    completed: Optional[bool] = None

    @field_validator('title')
    @classmethod
    def validate_title(cls, v: Optional[str]) -> Optional[str]:
        """Validate title is not empty or whitespace only."""
        if v is not None:
            if not v.strip():
                raise ValueError("Title cannot be empty or whitespace only")
            return v.strip()
        return v

    @field_validator('description')
    @classmethod
    def validate_description(cls, v: Optional[str]) -> Optional[str]:
        """Validate and clean description."""
        if v is not None:
            v = v.strip()
            if not v:
                return None
        return v


class TaskResponse(TaskBase):
    """Schema for task response."""
    id: int
    user_id: str
    completed: bool
    created_at: datetime
    updated_at: datetime

    @field_validator('user_id', mode='before')
    @classmethod
    def convert_uuid_to_str(cls, v):
        """Convert UUID to string for serialization."""
        from uuid import UUID
        if isinstance(v, UUID):
            return str(v)
        return v

    class Config:
        from_attributes = True
