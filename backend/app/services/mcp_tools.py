"""
MCP Tools for task management.
These tools are used by the AI agent to manage tasks.
"""
from typing import Optional, List
from uuid import UUID
from sqlmodel import Session, select
from app.models.task import Task
from app.database import engine
from datetime import datetime, UTC


def utc_now():
    return datetime.now(UTC)


class MCPTools:
    """MCP Tools for task operations."""

    @staticmethod
    def add_task(user_id: str, title: str, description: Optional[str] = None) -> dict:
        """
        Create a new task for the user.
        
        Args:
            user_id: The user's ID
            title: Task title (required)
            description: Task description (optional)
        
        Returns:
            dict with task_id, status, and title
        """
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
                
                return {
                    "task_id": task.id,
                    "status": "created",
                    "title": task.title
                }
        except Exception as e:
            return {"error": str(e), "status": "failed"}

    @staticmethod
    def list_tasks(user_id: str, status: str = "all") -> dict:
        """
        List tasks for the user.
        
        Args:
            user_id: The user's ID
            status: Filter by status - "all", "pending", or "completed"
        
        Returns:
            dict with list of tasks
        """
        try:
            with Session(engine) as session:
                query = select(Task).where(Task.user_id == UUID(user_id))
                
                if status == "pending":
                    query = query.where(Task.completed == False)
                elif status == "completed":
                    query = query.where(Task.completed == True)
                
                query = query.order_by(Task.created_at.desc())
                tasks = session.exec(query).all()
                
                return {
                    "tasks": [
                        {
                            "id": t.id,
                            "title": t.title,
                            "description": t.description,
                            "completed": t.completed,
                            "created_at": t.created_at.isoformat()
                        }
                        for t in tasks
                    ],
                    "count": len(tasks),
                    "status": "success"
                }
        except Exception as e:
            return {"error": str(e), "status": "failed", "tasks": []}

    @staticmethod
    def complete_task(user_id: str, task_id: int) -> dict:
        """
        Mark a task as complete.
        
        Args:
            user_id: The user's ID
            task_id: The task ID to complete
        
        Returns:
            dict with task_id, status, and title
        """
        try:
            with Session(engine) as session:
                task = session.exec(
                    select(Task).where(
                        Task.id == task_id,
                        Task.user_id == UUID(user_id)
                    )
                ).first()
                
                if not task:
                    return {"error": "Task not found", "status": "failed"}
                
                task.completed = True
                task.updated_at = utc_now()
                session.add(task)
                session.commit()
                
                return {
                    "task_id": task.id,
                    "status": "completed",
                    "title": task.title
                }
        except Exception as e:
            return {"error": str(e), "status": "failed"}

    @staticmethod
    def delete_task(user_id: str, task_id: int) -> dict:
        """
        Delete a task.
        
        Args:
            user_id: The user's ID
            task_id: The task ID to delete
        
        Returns:
            dict with task_id, status, and title
        """
        try:
            with Session(engine) as session:
                task = session.exec(
                    select(Task).where(
                        Task.id == task_id,
                        Task.user_id == UUID(user_id)
                    )
                ).first()
                
                if not task:
                    return {"error": "Task not found", "status": "failed"}
                
                title = task.title
                session.delete(task)
                session.commit()
                
                return {
                    "task_id": task_id,
                    "status": "deleted",
                    "title": title
                }
        except Exception as e:
            return {"error": str(e), "status": "failed"}

    @staticmethod
    def update_task(
        user_id: str, 
        task_id: int, 
        title: Optional[str] = None, 
        description: Optional[str] = None
    ) -> dict:
        """
        Update a task's title or description.
        
        Args:
            user_id: The user's ID
            task_id: The task ID to update
            title: New title (optional)
            description: New description (optional)
        
        Returns:
            dict with task_id, status, and title
        """
        try:
            with Session(engine) as session:
                task = session.exec(
                    select(Task).where(
                        Task.id == task_id,
                        Task.user_id == UUID(user_id)
                    )
                ).first()
                
                if not task:
                    return {"error": "Task not found", "status": "failed"}
                
                if title is not None:
                    task.title = title
                if description is not None:
                    task.description = description
                task.updated_at = utc_now()
                
                session.add(task)
                session.commit()
                session.refresh(task)
                
                return {
                    "task_id": task.id,
                    "status": "updated",
                    "title": task.title
                }
        except Exception as e:
            return {"error": str(e), "status": "failed"}


# Tool definitions for OpenAI function calling
TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "Create a new task for the user. Use this when the user wants to add, create, or remember something.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "The title of the task"
                    },
                    "description": {
                        "type": "string",
                        "description": "Optional description of the task"
                    }
                },
                "required": ["title"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_tasks",
            "description": "List the user's tasks. Use this when the user wants to see, show, or view their tasks.",
            "parameters": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "enum": ["all", "pending", "completed"],
                        "description": "Filter tasks by status. Use 'pending' for incomplete tasks, 'completed' for done tasks, 'all' for everything."
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "complete_task",
            "description": "Mark a task as complete. Use this when the user says they finished, completed, or done with a task.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "integer",
                        "description": "The ID of the task to mark as complete"
                    }
                },
                "required": ["task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_task",
            "description": "Delete a task. Use this when the user wants to remove, delete, or cancel a task.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "integer",
                        "description": "The ID of the task to delete"
                    }
                },
                "required": ["task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_task",
            "description": "Update a task's title or description. Use this when the user wants to change, modify, or rename a task.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "integer",
                        "description": "The ID of the task to update"
                    },
                    "title": {
                        "type": "string",
                        "description": "The new title for the task"
                    },
                    "description": {
                        "type": "string",
                        "description": "The new description for the task"
                    }
                },
                "required": ["task_id"]
            }
        }
    }
]
