"""
Pydantic schemas for chat API.
"""
from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime


class ChatRequest(BaseModel):
    """Request schema for chat endpoint."""
    conversation_id: Optional[int] = None
    message: str


class ToolCall(BaseModel):
    """Schema for a tool call made by the agent."""
    tool_name: str
    arguments: dict
    result: Optional[dict] = None


class ChatResponse(BaseModel):
    """Response schema for chat endpoint."""
    conversation_id: int
    response: str
    tool_calls: List[ToolCall] = []


class MessageSchema(BaseModel):
    """Schema for a message in conversation history."""
    id: int
    role: str
    content: str
    created_at: datetime


class ConversationSchema(BaseModel):
    """Schema for a conversation."""
    id: int
    title: str
    created_at: datetime
    updated_at: datetime
    messages: List[MessageSchema] = []


class ConversationListSchema(BaseModel):
    """Schema for listing conversations."""
    id: int
    title: str
    created_at: datetime
    message_count: int = 0
