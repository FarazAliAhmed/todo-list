"""
Business logic layer for the todo application.

This module provides task operations with validation and error handling.
"""

from datetime import datetime
from typing import List, Optional
from .models import Task
from .storage import TaskStorage


class TaskOperations:
    """
    Business logic for task operations.

    Provides validated CRUD operations for tasks, coordinating with
    the storage layer and enforcing business rules.
    """

    def __init__(self, storage: TaskStorage) -> None:
        """
        Initialize operations with storage.

        Args:
            storage: The storage instance to use for persistence
        """
        self.storage = storage

    def create_task(self, title: str, description: Optional[str] = None) -> Task:
        """
        Create a new task with validation.

        Args:
            title: Task title (required, 1-200 characters)
            description: Optional task description (max 1000 characters)

        Returns:
            Task: The created task

        Raises:
            ValueError: If validation fails
        """
        # Validate title
        if not title or not title.strip():
            raise ValueError("Title cannot be empty")

        title = title.strip()
        if len(title) > 200:
            raise ValueError("Title must be 200 characters or less")

        # Validate description
        if description:
            description = description.strip()
            if len(description) > 1000:
                raise ValueError("Description must be 1000 characters or less")
            # Set to None if empty after stripping
            description = description if description else None

        # Create task
        now = datetime.now()
        task = Task(
            id=self.storage.generate_id(),
            title=title,
            description=description,
            completed=False,
            created_at=now,
            updated_at=now
        )

        return self.storage.add(task)

    def list_tasks(self) -> List[Task]:
        """
        List all tasks.

        Returns:
            List[Task]: List of all tasks
        """
        return self.storage.get_all()

    def update_task(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None
    ) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: The ID of the task to update
            title: New title (optional, keeps current if None)
            description: New description (optional, keeps current if None)

        Returns:
            Optional[Task]: The updated task if found, None otherwise

        Raises:
            ValueError: If validation fails
        """
        # Get existing task
        task = self.storage.get(task_id)
        if not task:
            return None

        # Validate and update title if provided
        if title is not None:
            title = title.strip()
            if not title:
                raise ValueError("Title cannot be empty")
            if len(title) > 200:
                raise ValueError("Title must be 200 characters or less")
            task.title = title

        # Validate and update description if provided
        if description is not None:
            description = description.strip()
            if len(description) > 1000:
                raise ValueError("Description must be 1000 characters or less")
            task.description = description if description else None

        # Update timestamp
        task.updated_at = datetime.now()

        return self.storage.update(task_id, task)

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task.

        Args:
            task_id: The ID of the task to delete

        Returns:
            bool: True if task was deleted, False if not found
        """
        return self.storage.delete(task_id)

    def toggle_completion(self, task_id: int) -> Optional[Task]:
        """
        Toggle the completion status of a task.

        Args:
            task_id: The ID of the task to toggle

        Returns:
            Optional[Task]: The updated task if found, None otherwise
        """
        task = self.storage.get(task_id)
        if not task:
            return None

        task.completed = not task.completed
        task.updated_at = datetime.now()

        return self.storage.update(task_id, task)
