"""
Data models for the todo application.

This module defines the Task data structure used throughout the application.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Task:
    """
    Represents a todo task.

    Attributes:
        id: Unique identifier for the task
        title: Task title (1-200 characters)
        description: Optional task description (max 1000 characters)
        completed: Completion status (True if complete, False otherwise)
        created_at: Timestamp when task was created
        updated_at: Timestamp when task was last updated
    """
    id: int
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime

    def __str__(self) -> str:
        """Return string representation of task with status indicator."""
        status = "✓" if self.completed else "○"
        return f"[{status}] ID: {self.id} | {self.title}"
