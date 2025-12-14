"""
User-related Pydantic schemas for request/response validation.
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class UserBase(BaseModel):
    """Base schema for user data."""
    email: str


class UserCreate(UserBase):
    """Schema for creating a new user."""
    password: str = Field(..., min_length=8)
    name: Optional[str] = None


class UserResponse(UserBase):
    """Schema for user response."""
    id: str
    name: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
