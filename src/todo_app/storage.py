"""
Storage layer for the todo application.

This module provides in-memory storage for tasks with CRUD operations.
"""

from typing import Dict, List, Optional
from .models import Task


class TaskStorage:
    """
    In-memory storage for tasks.

    Manages task storage using a dictionary with task IDs as keys.
    Provides CRUD operations and maintains data integrity during the session.
    """

    def __init__(self) -> None:
        """Initialize empty task storage and ID counter."""
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def generate_id(self) -> int:
        """
        Generate a unique task ID.

        Returns:
            int: The next available task ID
        """
        task_id = self._next_id
        self._next_id += 1
        return task_id

    def add(self, task: Task) -> Task:
        """
        Add a task to storage.

        Args:
            task: The task to add

        Returns:
            Task: The added task
        """
        self._tasks[task.id] = task
        return task

    def get(self, task_id: int) -> Optional[Task]:
        """
        Retrieve a task by ID.

        Args:
            task_id: The ID of the task to retrieve

        Returns:
            Optional[Task]: The task if found, None otherwise
        """
        return self._tasks.get(task_id)

    def get_all(self) -> List[Task]:
        """
        Retrieve all tasks.

        Returns:
            List[Task]: List of all tasks in storage
        """
        return list(self._tasks.values())

    def update(self, task_id: int, task: Task) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: The ID of the task to update
            task: The updated task object

        Returns:
            Optional[Task]: The updated task if found, None otherwise
        """
        if task_id in self._tasks:
            self._tasks[task_id] = task
            return task
        return None

    def delete(self, task_id: int) -> bool:
        """
        Delete a task from storage.

        Args:
            task_id: The ID of the task to delete

        Returns:
            bool: True if task was deleted, False if not found
        """
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def exists(self, task_id: int) -> bool:
        """
        Check if a task exists in storage.

        Args:
            task_id: The ID of the task to check

        Returns:
            bool: True if task exists, False otherwise
        """
        return task_id in self._tasks
