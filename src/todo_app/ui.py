"""
Console user interface for the todo application.

This module provides the console UI with menu display, user input handling,
and workflow coordination for all task operations.
"""

from typing import Optional
from .models import Task
from .operations import TaskOperations


class ConsoleUI:
    """
    Console user interface for task management.

    Handles all user interaction including menu display, input capture,
    task display, and workflow coordination.
    """

    def __init__(self, operations: TaskOperations) -> None:
        """
        Initialize UI with operations layer.

        Args:
            operations: The operations instance for business logic
        """
        self.operations = operations

    def display_menu(self) -> None:
        """Display the main menu."""
        print("\n" + "=" * 50)
        print("           TODO APPLICATION")
        print("=" * 50)
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Mark Complete/Incomplete")
        print("6. Exit")
        print("=" * 50)

    def get_user_choice(self) -> int:
        """
        Get and validate user menu choice.

        Returns:
            int: Valid menu choice (1-6)
        """
        while True:
            try:
                choice = int(input("\nEnter your choice (1-6): "))
                if 1 <= choice <= 6:
                    return choice
                else:
                    self.display_error("Please enter a number between 1 and 6")
            except ValueError:
                self.display_error("Invalid input. Please enter a number")
            except KeyboardInterrupt:
                print("\n")
                return 6  # Exit on Ctrl+C

    def display_task(self, task: Task) -> None:
        """
        Display a single task with formatting.

        Args:
            task: The task to display
        """
        status = "✓" if task.completed else "○"
        print(f"\n[{status}] ID: {task.id} | {task.title}")
        if task.description:
            print(f"    Description: {task.description}")
        print(f"    Created: {task.created_at.strftime('%Y-%m-%d %I:%M %p')}")

    def display_tasks(self, tasks: list[Task]) -> None:
        """
        Display a list of tasks.

        Args:
            tasks: List of tasks to display
        """
        if not tasks:
            print("\n📝 No tasks found. Your todo list is empty!")
            return

        print(f"\n📋 You have {len(tasks)} task(s):")
        print("-" * 50)
        for task in tasks:
            self.display_task(task)
        print("-" * 50)

    def display_error(self, message: str) -> None:
        """
        Display an error message.

        Args:
            message: The error message to display
        """
        print(f"\n❌ Error: {message}")

    def display_success(self, message: str) -> None:
        """
        Display a success message.

        Args:
            message: The success message to display
        """
        print(f"\n✅ Success: {message}")

    def add_task_flow(self) -> None:
        """Handle the add task workflow."""
        print("\n--- Add New Task ---")
        try:
            title = input("Enter task title: ").strip()
            description = input("Enter description (optional, press Enter to skip): ").strip()
            description = description if description else None

            task = self.operations.create_task(title, description)
            self.display_success(f"Task created successfully! ID: {task.id}")

        except ValueError as e:
            self.display_error(str(e))
        except KeyboardInterrupt:
            print("\n")
            self.display_error("Operation cancelled")
        except Exception as e:
            self.display_error(f"An unexpected error occurred: {e}")

    def view_tasks_flow(self) -> None:
        """Handle the view tasks workflow."""
        try:
            tasks = self.operations.list_tasks()
            self.display_tasks(tasks)
        except Exception as e:
            self.display_error(f"An unexpected error occurred: {e}")

    def update_task_flow(self) -> None:
        """Handle the update task workflow."""
        print("\n--- Update Task ---")
        try:
            # Get task ID
            task_id = self._get_task_id("Enter task ID to update: ")
            if task_id is None:
                return

            # Check if task exists
            task = self.operations.storage.get(task_id)
            if not task:
                self.display_error(f"Task with ID {task_id} not found")
                return

            # Display current task
            print("\nCurrent task details:")
            self.display_task(task)

            # Get new values
            print("\nEnter new values (press Enter to keep current value):")
            new_title = input(f"Title [{task.title}]: ").strip()
            new_description = input(f"Description [{task.description or 'None'}]: ").strip()

            # Prepare update parameters
            title_update = new_title if new_title else None
            desc_update = new_description if new_description else None

            # Check if any changes were made
            if title_update is None and desc_update is None:
                print("\n⚠️  No changes made")
                return

            # Update task
            updated_task = self.operations.update_task(task_id, title_update, desc_update)
            if updated_task:
                self.display_success("Task updated successfully!")
                self.display_task(updated_task)
            else:
                self.display_error(f"Task with ID {task_id} not found")

        except ValueError as e:
            self.display_error(str(e))
        except KeyboardInterrupt:
            print("\n")
            self.display_error("Operation cancelled")
        except Exception as e:
            self.display_error(f"An unexpected error occurred: {e}")

    def delete_task_flow(self) -> None:
        """Handle the delete task workflow."""
        print("\n--- Delete Task ---")
        try:
            # Get task ID
            task_id = self._get_task_id("Enter task ID to delete: ")
            if task_id is None:
                return

            # Check if task exists and display it
            task = self.operations.storage.get(task_id)
            if not task:
                self.display_error(f"Task with ID {task_id} not found")
                return

            print("\nTask to be deleted:")
            self.display_task(task)

            # Confirm deletion
            confirm = input("\nAre you sure you want to delete this task? (y/n): ").strip().lower()
            if confirm != 'y':
                print("\n⚠️  Deletion cancelled")
                return

            # Delete task
            if self.operations.delete_task(task_id):
                self.display_success(f"Task {task_id} deleted successfully!")
            else:
                self.display_error(f"Task with ID {task_id} not found")

        except KeyboardInterrupt:
            print("\n")
            self.display_error("Operation cancelled")
        except Exception as e:
            self.display_error(f"An unexpected error occurred: {e}")

    def toggle_completion_flow(self) -> None:
        """Handle the toggle completion workflow."""
        print("\n--- Mark Complete/Incomplete ---")
        try:
            # Get task ID
            task_id = self._get_task_id("Enter task ID: ")
            if task_id is None:
                return

            # Toggle completion
            task = self.operations.toggle_completion(task_id)
            if task:
                status = "complete" if task.completed else "incomplete"
                self.display_success(f"Task {task_id} marked as {status}!")
                self.display_task(task)
            else:
                self.display_error(f"Task with ID {task_id} not found")

        except KeyboardInterrupt:
            print("\n")
            self.display_error("Operation cancelled")
        except Exception as e:
            self.display_error(f"An unexpected error occurred: {e}")

    def _get_task_id(self, prompt: str) -> Optional[int]:
        """
        Get and validate task ID from user.

        Args:
            prompt: The prompt to display

        Returns:
            Optional[int]: The task ID if valid, None if cancelled
        """
        while True:
            try:
                task_id_str = input(prompt).strip()
                if not task_id_str:
                    return None
                task_id = int(task_id_str)
                if task_id < 1:
                    self.display_error("Task ID must be a positive number")
                    continue
                return task_id
            except ValueError:
                self.display_error("Please enter a valid number")
            except KeyboardInterrupt:
                print("\n")
                return None
