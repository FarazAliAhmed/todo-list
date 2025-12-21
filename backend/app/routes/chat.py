"""
Chat API routes for AI-powered task management.
Uses OpenAI Agents SDK.
"""
from typing import Optional
from uuid import UUID
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.services.chat_service import ChatService
from app.auth import get_current_user


router = APIRouter(prefix="/api", tags=["chat"])


class ChatRequest(BaseModel):
    """Request body for chat endpoint."""
    conversation_id: Optional[int] = None
    message: str


class ChatResponse(BaseModel):
    """Response body for chat endpoint."""
    conversation_id: int
    response: str
    tool_calls: list = []


# Singleton chat service instance
_chat_service: Optional[ChatService] = None


def get_chat_service() -> ChatService:
    """Dependency to get chat service instance."""
    global _chat_service
    if _chat_service is None:
        _chat_service = ChatService()
    return _chat_service


@router.post("/{user_id}/chat", response_model=ChatResponse)
async def chat(
    user_id: UUID,
    request: ChatRequest,
    chat_service: ChatService = Depends(get_chat_service),
    current_user: dict = Depends(get_current_user)
):
    """
    Send a message to the AI assistant and get a response.
    
    The AI can manage tasks through natural language:
    - "Add a task to buy groceries"
    - "Show me my pending tasks"
    - "Mark task 3 as complete"
    - "Delete the meeting task"
    """
    # Verify user is accessing their own data
    if str(current_user["id"]) != str(user_id):
        raise HTTPException(
            status_code=403,
            detail="Not authorized to access this user's chat"
        )
    
    try:
        result = await chat_service.chat_async(
            user_id=str(user_id),
            message=request.message,
            conversation_id=request.conversation_id
        )
        return ChatResponse(**result)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Chat error: {str(e)}"
        )


@router.get("/{user_id}/conversations")
async def list_conversations(
    user_id: UUID,
    chat_service: ChatService = Depends(get_chat_service),
    current_user: dict = Depends(get_current_user)
):
    """Get all conversations for the user."""
    if str(current_user["id"]) != str(user_id):
        raise HTTPException(
            status_code=403,
            detail="Not authorized to access this user's conversations"
        )
    
    try:
        conversations = chat_service.get_conversations(str(user_id))
        return {"conversations": conversations}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching conversations: {str(e)}"
        )


@router.get("/{user_id}/conversations/{conversation_id}")
async def get_conversation(
    user_id: UUID,
    conversation_id: int,
    chat_service: ChatService = Depends(get_chat_service),
    current_user: dict = Depends(get_current_user)
):
    """Get a specific conversation with all messages."""
    if str(current_user["id"]) != str(user_id):
        raise HTTPException(
            status_code=403,
            detail="Not authorized to access this conversation"
        )
    
    try:
        conversation = chat_service.get_conversation_messages(
            str(user_id), conversation_id
        )
        if not conversation:
            raise HTTPException(
                status_code=404,
                detail="Conversation not found"
            )
        return conversation
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching conversation: {str(e)}"
        )
