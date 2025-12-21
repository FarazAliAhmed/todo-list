"""
Chat API routes for AI-powered task management.
Auth temporarily disabled for testing.
"""
from typing import Optional
from uuid import UUID
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.services.chat_service import ChatService


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
    user_id: str,
    request: ChatRequest,
    chat_service: ChatService = Depends(get_chat_service)
):
    """
    Send a message to the AI assistant and get a response.
    """
    try:
        # Validate UUID format
        UUID(user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user ID format")
    
    try:
        result = await chat_service.chat_async(
            user_id=user_id,
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
    user_id: str,
    chat_service: ChatService = Depends(get_chat_service)
):
    """Get all conversations for the user."""
    try:
        UUID(user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user ID format")
    
    try:
        conversations = chat_service.get_conversations(user_id)
        return {"conversations": conversations}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching conversations: {str(e)}"
        )


@router.get("/{user_id}/conversations/{conversation_id}")
async def get_conversation(
    user_id: str,
    conversation_id: int,
    chat_service: ChatService = Depends(get_chat_service)
):
    """Get a specific conversation with all messages."""
    try:
        UUID(user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user ID format")
    
    try:
        conversation = chat_service.get_conversation_messages(
            user_id, conversation_id
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
