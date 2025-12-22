"""
Conversation and Message models for AI chatbot.
"""
from datetime import datetime, UTC
from typing import Optional, List
from uuid import UUID
from sqlmodel import SQLModel, Field, Relationship


def utc_now():
    """Return current UTC time as timezone-aware datetime."""
    return datetime.now(UTC)


class Conversation(SQLModel, table=True):
    """
    Conversation model representing a chat session.
    Each conversation belongs to a specific user.
    """
    __tablename__ = "conversations"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: UUID = Field(index=True)  # No foreign key constraint
    title: Optional[str] = Field(default="New Conversation", max_length=200)
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)

    # Relationships removed - no foreign keys


class Message(SQLModel, table=True):
    """
    Message model representing a single message in a conversation.
    """
    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversations.id", index=True)
    user_id: UUID = Field(index=True)  # No foreign key constraint
    role: str = Field(max_length=20)  # "user" or "assistant"
    content: str = Field()
    tool_calls: Optional[str] = Field(default=None)  # JSON string of tool calls
    created_at: datetime = Field(default_factory=utc_now)

    # Relationships removed - no foreign keys
