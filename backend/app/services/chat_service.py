"""
Chat service using OpenAI Agents SDK for AI-powered task management.
Uses the latest openai-agents package with function tools and SQLiteSession.
"""
import json
import asyncio
import os
from typing import Optional, List
from uuid import UUID
from agents import Agent, Runner, function_tool, RunContextWrapper, SQLiteSession
from sqlmodel import Session, select
from app.database import engine
from app.models.conversation import Conversation, Message
from app.models.task import Task
from datetime import datetime, UTC


def utc_now():
    return datetime.now(UTC)


# ============ MCP Function Tools ============
# These tools use RunContextWrapper to access user_id

@function_tool
def add_task(ctx: RunContextWrapper[dict], title: str, description: str | None = None) -> str:
    """
    Create a new task for the user.
    
    Args:
        title: The title of the task (required)
        description: Optional description of the task
    """
    user_id = ctx.context.get("user_id")
    try:
        with Session(engine) as session:
            task = Task(
                user_id=UUID(user_id),
                title=title,
                description=description,
                completed=False,
                created_at=utc_now(),
                updated_at=utc_now()
            )
            session.add(task)
            session.commit()
            session.refresh(task)
            
            return json.dumps({
                "task_id": task.id,
                "status": "created",
                "title": task.title,
                "message": f"Task '{task.title}' created successfully!"
            })
    except Exception as e:
        return json.dumps({"error": str(e), "status": "failed"})


@function_tool
def list_tasks(ctx: RunContextWrapper[dict], status: str = "all") -> str:
    """
    List tasks for the user.
    
    Args:
        status: Filter by status - "all", "pending", or "completed"
    """
    user_id = ctx.context.get("user_id")
    try:
        with Session(engine) as session:
            query = select(Task).where(Task.user_id == UUID(user_id))
            
            if status == "pending":
                query = query.where(Task.completed == False)
            elif status == "completed":
                query = query.where(Task.completed == True)
            
            query = query.order_by(Task.created_at.desc())
            tasks = session.exec(query).all()
            
            task_list = [
                {
                    "id": t.id,
                    "title": t.title,
                    "description": t.description,
                    "completed": t.completed,
                    "created_at": t.created_at.isoformat() if t.created_at else None
                }
                for t in tasks
            ]
            
            return json.dumps({
                "tasks": task_list,
                "count": len(tasks),
                "status": "success"
            })
    except Exception as e:
        return json.dumps({"error": str(e), "status": "failed", "tasks": []})


@function_tool
def complete_task(ctx: RunContextWrapper[dict], task_id: int) -> str:
    """
    Mark a task as complete.
    
    Args:
        task_id: The ID of the task to mark as complete
    """
    user_id = ctx.context.get("user_id")
    try:
        with Session(engine) as session:
            task = session.exec(
                select(Task).where(
                    Task.id == task_id,
                    Task.user_id == UUID(user_id)
                )
            ).first()
            
            if not task:
                return json.dumps({"error": "Task not found", "status": "failed"})
            
            task.completed = True
            task.updated_at = utc_now()
            session.add(task)
            session.commit()
            
            return json.dumps({
                "task_id": task.id,
                "status": "completed",
                "title": task.title,
                "message": f"Task '{task.title}' marked as complete!"
            })
    except Exception as e:
        return json.dumps({"error": str(e), "status": "failed"})


@function_tool
def delete_task(ctx: RunContextWrapper[dict], task_id: int) -> str:
    """
    Delete a task.
    
    Args:
        task_id: The ID of the task to delete
    """
    user_id = ctx.context.get("user_id")
    try:
        with Session(engine) as session:
            task = session.exec(
                select(Task).where(
                    Task.id == task_id,
                    Task.user_id == UUID(user_id)
                )
            ).first()
            
            if not task:
                return json.dumps({"error": "Task not found", "status": "failed"})
            
            title = task.title
            session.delete(task)
            session.commit()
            
            return json.dumps({
                "task_id": task_id,
                "status": "deleted",
                "title": title,
                "message": f"Task '{title}' deleted successfully!"
            })
    except Exception as e:
        return json.dumps({"error": str(e), "status": "failed"})


@function_tool
def update_task(
    ctx: RunContextWrapper[dict], 
    task_id: int, 
    title: str | None = None, 
    description: str | None = None
) -> str:
    """
    Update a task's title or description.
    
    Args:
        task_id: The ID of the task to update
        title: New title for the task (optional)
        description: New description for the task (optional)
    """
    user_id = ctx.context.get("user_id")
    try:
        with Session(engine) as session:
            task = session.exec(
                select(Task).where(
                    Task.id == task_id,
                    Task.user_id == UUID(user_id)
                )
            ).first()
            
            if not task:
                return json.dumps({"error": "Task not found", "status": "failed"})
            
            if title is not None:
                task.title = title
            if description is not None:
                task.description = description
            task.updated_at = utc_now()
            
            session.add(task)
            session.commit()
            session.refresh(task)
            
            return json.dumps({
                "task_id": task.id,
                "status": "updated",
                "title": task.title,
                "message": f"Task '{task.title}' updated successfully!"
            })
    except Exception as e:
        return json.dumps({"error": str(e), "status": "failed"})


# ============ Chat Service ============

class ChatService:
    """Service for handling AI chat interactions using OpenAI Agents SDK."""
    
    def __init__(self):
        # Create the task management agent with function tools
        self.agent = Agent(
            name="TaskAssistant",
            instructions="""You are a helpful AI assistant for managing todo tasks. 
You help users add, view, update, complete, and delete their tasks through natural conversation.

When users want to:
- Add/create/remember something → use add_task
- See/show/list/view tasks → use list_tasks  
- Mark done/complete/finish → use complete_task
- Delete/remove/cancel → use delete_task
- Change/update/rename/modify → use update_task

Always be friendly and confirm actions. If a task operation fails, explain the error helpfully.
When listing tasks, format them nicely for the user with task IDs so they can reference them.
Keep responses concise but helpful.""",
            tools=[add_task, list_tasks, complete_task, delete_task, update_task],
        )
        
        # Session storage directory
        self.session_db = os.environ.get("SESSION_DB_PATH", "conversations.db")

    def _get_session(self, user_id: str, conversation_id: Optional[int] = None) -> SQLiteSession:
        """Get or create a SQLiteSession for the user/conversation."""
        # Create unique session ID combining user and conversation
        session_id = f"{user_id}_{conversation_id}" if conversation_id else f"{user_id}_new"
        return SQLiteSession(session_id, self.session_db)

    def _get_or_create_conversation(
        self, 
        db_session: Session, 
        user_id: UUID, 
        conversation_id: Optional[int]
    ) -> Conversation:
        """Get existing conversation or create a new one in our database."""
        if conversation_id:
            conversation = db_session.exec(
                select(Conversation).where(
                    Conversation.id == conversation_id,
                    Conversation.user_id == user_id
                )
            ).first()
            if conversation:
                return conversation
        
        # Create new conversation
        conversation = Conversation(
            user_id=user_id,
            title="New Conversation",
            created_at=utc_now(),
            updated_at=utc_now()
        )
        db_session.add(conversation)
        db_session.commit()
        db_session.refresh(conversation)
        return conversation

    def _save_message(
        self,
        db_session: Session,
        conversation_id: int,
        user_id: UUID,
        role: str,
        content: str,
        tool_calls: Optional[str] = None
    ) -> Message:
        """Save a message to our database for history display."""
        message = Message(
            conversation_id=conversation_id,
            user_id=user_id,
            role=role,
            content=content,
            tool_calls=tool_calls,
            created_at=utc_now()
        )
        db_session.add(message)
        db_session.commit()
        db_session.refresh(message)
        return message

    async def chat_async(
        self,
        user_id: str,
        message: str,
        conversation_id: Optional[int] = None
    ) -> dict:
        """
        Process a chat message asynchronously and return AI response.
        Uses SQLiteSession for automatic conversation history management.
        
        Args:
            user_id: The user's ID
            message: The user's message
            conversation_id: Optional existing conversation ID
            
        Returns:
            dict with conversation_id, response, and tool_calls
        """
        user_uuid = UUID(user_id)
        tool_calls_made = []
        
        with Session(engine) as db_session:
            # Get or create conversation in our database
            conversation = self._get_or_create_conversation(
                db_session, user_uuid, conversation_id
            )
            
            # Save user message to our database
            self._save_message(
                db_session, conversation.id, user_uuid, "user", message
            )
            
            # Get SQLiteSession for agent memory
            agent_session = self._get_session(user_id, conversation.id)
            
            # Run the agent with user context and session
            context = {"user_id": user_id}
            result = await Runner.run(
                self.agent, 
                input=message,
                context=context,
                session=agent_session
            )
            
            # Extract tool calls from the result
            if hasattr(result, 'new_items'):
                for item in result.new_items:
                    if hasattr(item, 'type') and item.type == 'function_call_output':
                        # This is a tool result
                        pass
                    elif hasattr(item, 'raw_item'):
                        raw = item.raw_item
                        if hasattr(raw, 'type') and raw.type == 'function_call':
                            tool_calls_made.append({
                                "tool_name": raw.name if hasattr(raw, 'name') else "unknown",
                                "arguments": json.loads(raw.arguments) if hasattr(raw, 'arguments') and raw.arguments else {},
                                "result": {}
                            })
            
            final_output = result.final_output or "I'm sorry, I couldn't process that request."
            
            # Save assistant response to our database
            self._save_message(
                db_session,
                conversation.id,
                user_uuid,
                "assistant",
                final_output,
                json.dumps(tool_calls_made) if tool_calls_made else None
            )
            
            # Update conversation timestamp
            conversation.updated_at = utc_now()
            db_session.add(conversation)
            db_session.commit()
            
            return {
                "conversation_id": conversation.id,
                "response": final_output,
                "tool_calls": tool_calls_made
            }

    def chat(
        self,
        user_id: str,
        message: str,
        conversation_id: Optional[int] = None
    ) -> dict:
        """
        Synchronous wrapper for chat_async.
        """
        return asyncio.run(self.chat_async(user_id, message, conversation_id))

    def get_conversations(self, user_id: str) -> List[dict]:
        """Get all conversations for a user from our database."""
        with Session(engine) as db_session:
            conversations = db_session.exec(
                select(Conversation)
                .where(Conversation.user_id == UUID(user_id))
                .order_by(Conversation.updated_at.desc())
            ).all()
            
            result = []
            for conv in conversations:
                # Count messages
                msg_count = len(db_session.exec(
                    select(Message).where(Message.conversation_id == conv.id)
                ).all())
                
                result.append({
                    "id": conv.id,
                    "title": conv.title,
                    "created_at": conv.created_at.isoformat(),
                    "message_count": msg_count
                })
            
            return result

    def get_conversation_messages(
        self, 
        user_id: str, 
        conversation_id: int
    ) -> Optional[dict]:
        """Get a conversation with all its messages from our database."""
        with Session(engine) as db_session:
            conversation = db_session.exec(
                select(Conversation).where(
                    Conversation.id == conversation_id,
                    Conversation.user_id == UUID(user_id)
                )
            ).first()
            
            if not conversation:
                return None
            
            messages = db_session.exec(
                select(Message)
                .where(Message.conversation_id == conversation_id)
                .order_by(Message.created_at)
            ).all()
            
            return {
                "id": conversation.id,
                "title": conversation.title,
                "created_at": conversation.created_at.isoformat(),
                "updated_at": conversation.updated_at.isoformat(),
                "messages": [
                    {
                        "id": msg.id,
                        "role": msg.role,
                        "content": msg.content,
                        "created_at": msg.created_at.isoformat()
                    }
                    for msg in messages
                ]
            }
