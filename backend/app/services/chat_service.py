"""
Chat service with OpenAI integration for AI-powered task management.
"""
import json
from typing import Optional, List
from uuid import UUID
from openai import OpenAI
from sqlmodel import Session, select
from app.database import engine
from app.models.conversation import Conversation, Message
from app.services.mcp_tools import MCPTools, TOOL_DEFINITIONS
from datetime import datetime, UTC


def utc_now():
    return datetime.now(UTC)


class ChatService:
    """Service for handling AI chat interactions."""
    
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.mcp_tools = MCPTools()
        self.model = "gpt-4o-mini"  # Cost-effective model
        
        self.system_prompt = """You are a helpful AI assistant for managing todo tasks. 
You help users add, view, update, complete, and delete their tasks through natural conversation.

When users want to:
- Add/create/remember something → use add_task
- See/show/list/view tasks → use list_tasks  
- Mark done/complete/finish → use complete_task
- Delete/remove/cancel → use delete_task
- Change/update/rename/modify → use update_task

Always be friendly and confirm actions. If a task operation fails, explain the error helpfully.
When listing tasks, format them nicely for the user."""

    def _execute_tool(self, user_id: str, tool_name: str, arguments: dict) -> dict:
        """Execute an MCP tool and return the result."""
        if tool_name == "add_task":
            return self.mcp_tools.add_task(
                user_id=user_id,
                title=arguments.get("title"),
                description=arguments.get("description")
            )
        elif tool_name == "list_tasks":
            return self.mcp_tools.list_tasks(
                user_id=user_id,
                status=arguments.get("status", "all")
            )
        elif tool_name == "complete_task":
            return self.mcp_tools.complete_task(
                user_id=user_id,
                task_id=arguments.get("task_id")
            )
        elif tool_name == "delete_task":
            return self.mcp_tools.delete_task(
                user_id=user_id,
                task_id=arguments.get("task_id")
            )
        elif tool_name == "update_task":
            return self.mcp_tools.update_task(
                user_id=user_id,
                task_id=arguments.get("task_id"),
                title=arguments.get("title"),
                description=arguments.get("description")
            )
        else:
            return {"error": f"Unknown tool: {tool_name}", "status": "failed"}

    def _get_or_create_conversation(
        self, 
        session: Session, 
        user_id: UUID, 
        conversation_id: Optional[int]
    ) -> Conversation:
        """Get existing conversation or create a new one."""
        if conversation_id:
            conversation = session.exec(
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
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        return conversation

    def _get_conversation_history(
        self, 
        session: Session, 
        conversation_id: int,
        limit: int = 20
    ) -> List[dict]:
        """Get recent messages from conversation history."""
        messages = session.exec(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.desc())
            .limit(limit)
        ).all()
        
        # Reverse to get chronological order
        messages = list(reversed(messages))
        
        return [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]

    def _save_message(
        self,
        session: Session,
        conversation_id: int,
        user_id: UUID,
        role: str,
        content: str,
        tool_calls: Optional[str] = None
    ) -> Message:
        """Save a message to the database."""
        message = Message(
            conversation_id=conversation_id,
            user_id=user_id,
            role=role,
            content=content,
            tool_calls=tool_calls,
            created_at=utc_now()
        )
        session.add(message)
        session.commit()
        session.refresh(message)
        return message

    def chat(
        self,
        user_id: str,
        message: str,
        conversation_id: Optional[int] = None
    ) -> dict:
        """
        Process a chat message and return AI response.
        
        Args:
            user_id: The user's ID
            message: The user's message
            conversation_id: Optional existing conversation ID
            
        Returns:
            dict with conversation_id, response, and tool_calls
        """
        user_uuid = UUID(user_id)
        tool_calls_made = []
        
        with Session(engine) as session:
            # Get or create conversation
            conversation = self._get_or_create_conversation(
                session, user_uuid, conversation_id
            )
            
            # Get conversation history
            history = self._get_conversation_history(session, conversation.id)
            
            # Save user message
            self._save_message(
                session, conversation.id, user_uuid, "user", message
            )
            
            # Build messages for OpenAI
            messages = [{"role": "system", "content": self.system_prompt}]
            messages.extend(history)
            messages.append({"role": "user", "content": message})
            
            # Call OpenAI with tools
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=TOOL_DEFINITIONS,
                tool_choice="auto"
            )
            
            assistant_message = response.choices[0].message
            
            # Handle tool calls if any
            if assistant_message.tool_calls:
                # Process each tool call
                tool_results = []
                for tool_call in assistant_message.tool_calls:
                    tool_name = tool_call.function.name
                    arguments = json.loads(tool_call.function.arguments)
                    
                    # Execute the tool
                    result = self._execute_tool(user_id, tool_name, arguments)
                    
                    tool_calls_made.append({
                        "tool_name": tool_name,
                        "arguments": arguments,
                        "result": result
                    })
                    
                    tool_results.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "content": json.dumps(result)
                    })
                
                # Add assistant message with tool calls
                messages.append({
                    "role": "assistant",
                    "content": assistant_message.content or "",
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": "function",
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments
                            }
                        }
                        for tc in assistant_message.tool_calls
                    ]
                })
                
                # Add tool results
                messages.extend(tool_results)
                
                # Get final response from OpenAI
                final_response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages
                )
                
                final_content = final_response.choices[0].message.content
            else:
                final_content = assistant_message.content
            
            # Save assistant response
            self._save_message(
                session,
                conversation.id,
                user_uuid,
                "assistant",
                final_content,
                json.dumps(tool_calls_made) if tool_calls_made else None
            )
            
            # Update conversation timestamp
            conversation.updated_at = utc_now()
            session.add(conversation)
            session.commit()
            
            return {
                "conversation_id": conversation.id,
                "response": final_content,
                "tool_calls": tool_calls_made
            }

    def get_conversations(self, user_id: str) -> List[dict]:
        """Get all conversations for a user."""
        with Session(engine) as session:
            conversations = session.exec(
                select(Conversation)
                .where(Conversation.user_id == UUID(user_id))
                .order_by(Conversation.updated_at.desc())
            ).all()
            
            result = []
            for conv in conversations:
                # Count messages
                msg_count = len(session.exec(
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
        """Get a conversation with all its messages."""
        with Session(engine) as session:
            conversation = session.exec(
                select(Conversation).where(
                    Conversation.id == conversation_id,
                    Conversation.user_id == UUID(user_id)
                )
            ).first()
            
            if not conversation:
                return None
            
            messages = session.exec(
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
