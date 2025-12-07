# Design Document - Phase I: Todo Console App

## Overview

This document outlines the technical design for a command-line todo application with in-memory storage. The application follows clean architecture principles with clear separation of concerns, making it maintainable and ready for evolution into subsequent phases.

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Console Interface                     │
│                         (UI Layer)                       │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                  Operations Layer                        │
│            (Business Logic / CRUD Operations)            │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                   Storage Layer                          │
│              (In-Memory Data Management)                 │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                    Data Models                           │
│                  (Task Structure)                        │
└─────────────────────────────────────────────────────────┘
```

### Design Principles

1. **Separation of Concerns**: Each module has a single, well-defined responsibility
2. **Dependency Inversion**: High-level modules don't depend on low-level modules
3. **Single Responsibility**: Each class/function does one thing well
4. **Open/Closed**: Open for extension, closed for modification

## Components and Interfaces

### 1. Data Models (`models.py`)

**Purpose**: Define the structure of a Task

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Task:
    """Represents a todo task."""
    id: int
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime
```

**Responsibilities**:
- Define Task data structure
- Provide immutable task representation
- Include metadata (timestamps)

### 2. Storage Layer (`storage.py`)

**Purpose**: Manage in-memory task storage

```python
class TaskStorage:
    """In-memory storage for tasks."""

    def __init__(self):
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def add(self, task: Task) -> Task
    def get(self, task_id: int) -> Optional[Task]
    def get_all(self) -> List[Task]
    def update(self, task_id: int, task: Task) -> Optional[Task]
    def delete(self, task_id: int) -> bool
    def exists(self, task_id: int) -> bool
```

**Responsibilities**:
- Store tasks in memory (dictionary)
- Generate unique task IDs
- Provide CRUD operations
- Maintain data integrity

**Data Structure**: Dictionary with task ID as key, Task object as value

### 3. Operations Layer (`operations.py`)

**Purpose**: Implement business logic for task operations

```python
class TaskOperations:
    """Business logic for task operations."""

    def __init__(self, storage: TaskStorage):
        self.storage = storage

    def create_task(self, title: str, description: Optional[str] = None) -> Task
    def list_tasks(self) -> List[Task]
    def update_task(self, task_id: int, title: Optional[str] = None,
                   description: Optional[str] = None) -> Optional[Task]
    def delete_task(self, task_id: int) -> bool
    def toggle_completion(self, task_id: int) -> Optional[Task*Responsibilities**:
- Validate inputs
- Coordinate with storage layer
- Handle business rules
- Return appropriate results or errors

**Validation Rules**:
- Title must not be empty
- Title length: 1-200 characters
- Description length: max 1000 characters (if provided)
- Task ID must exist for update/delete/toggle operations

### 4. UI Layer (`ui.py`)

**Purpose**: Handle user interaction and display

```python
class ConsoleUI:
    """Console user interface."""

    def __init__(self, operations: TaskOperations):
        self.operations = operations

    def display_menu(self) -> None
    def get_user_choice(self) -> int
    def add_task_flow(self) -> None
    def view_tasks_flow(self) -> None
    def update_task_flow(self) -> None
    def delete_task_flow(self) -> None
    def toggle_completion_flow(self) -> None
    def display_task(self, task: Task) -> None
    def display_tasks(self, tasks: List[Task]) -> None
    def display_error(self, message: str) -> None
    def display_success(self, message: str) -> None
```

**Responsibilities**:
- Display menu and prompts
- Capture user input
- Format and display tasks
- Show error and success messages
- Coordinate user workflows

**Display Format**:
```
=== Todo Application ===
1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Mark Complete/Incomplete
6. Exit

Task Display:
[✓] ID: 1 | Buy groceries
    Description: Milk, eggs, bread
    Created: 2025-12-04 10:30 AM

[○] ID: 2 | Call dentist
    Created: 2025-12-04 11:15 AM
```

### 5. Main Entry Point (`main.py`)

**Purpose**: Application initialization and main loop

```python
def main():
    """Main application entry point."""
    storage = TaskStorage()
    operations = TaskOperations(storage)
    ui = ConsoleUI(operations)

    while True:
        ui.display_menu()
        choice = ui.get_user_choice()

        if choice == 6:  # Exit
            break

        # Handle menu choices
```

**Responsibilities**:
- Initialize components
- Run main application loop
- Handle graceful shutdown

## Data Models

### Task Model

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | int | Yes | Unique identifier (auto-generated) |
| title | str | Yes | Task title (1-200 chars) |
| description | Optional[str] | No | Task description (max 1000 chars) |
| completed | bool | Yes | Completion status (default: False) |
| created_at | datetime | Yes | Creation timestamp |
| updated_at | datetime | Yes | Last update timestamp |

### Storage Structure

```python
{
    1: Task(id=1, title="Buy groceries", description="Milk, eggs",
            completed=False, created_at=..., updated_at=...),
    2: Task(id=2, title="Call dentist", description=None,
            completed=True, created_at=..., updated_at=...),
    ...
}
```

## Error Handling

### Error Categories

1. **Validation Errors**
   - Empty title
   - Title too long (>200 chars)
   - Description too long (>1000 chars)

2. **Not Found Errors**
   - Invalid task ID
   - Task doesn't exist

3. **Input Errors**
   - Invalid menu choice
   - Non-numeric input for ID
   - Invalid input format

### Error Handling Strategy

```python
# In Operations Layer
def create_task(self, title: str, description: Optional[str] = None) -> Task:
    if not title or not title.strip():
        raise ValueError("Title cannot be empty")

    if len(title) > 200:
        raise ValueError("Title must be 200 characters or less")

    if description and len(description) > 1000:
        raise ValueError("Description must be 1000 characters or less")

    # Create task...

# In UI Layer
def add_task_flow(self):
    try:
        title = input("Enter task title: ").strip()
        description = input("Enter description (optional): ").strip() or None

        task = self.operations.create_task(title, description)
        self.display_success(f"Task created successfully! ID: {task.id}")
    except ValueError as e:
        self.display_error(str(e))
    except Exception as e:
        self.display_error(f"An unexpected error occurred: {e}")
```

### Error Messages

| Error Type | User-Friendly Message |
|------------|----------------------|
| Empty title | "Error: Task title cannot be empty" |
| Title too long | "Error: Title must be 200 characters or less" |
| Description too long | "Error: Description must be 1000 characters or less" |
| Invalid task ID | "Error: Task with ID {id} not found" |
| Invalid menu choice | "Error: Please enter a number between 1 and 6" |
| Invalid ID input | "Error: Please enter a valid task ID (number)" |

## User Interface Flow

### Main Menu Flow

```
Start
  │
  ▼
Display Menu
  │
  ▼
Get User Choice
  │
  ├─→ 1: Add Task Flow
  ├─→ 2: View Tasks Flow
  ├─→ 3: Update Task Flow
  ├─→ 4: Delete Task Flow
  ├─→ 5: Toggle Completion Flow
  └─→ 6: Exit
       │
       ▼
     End
```

### Add Task Flow

```
1. Prompt for title
2. Validate title (not empty, ≤200 chars)
3. Prompt for description (optional)
4. Validate description (≤1000 chars if provided)
5. Create task
6. Display success message with task ID
7. Return to main menu
```

### View Tasks Flow

```
1. Retrieve all tasks
2. If empty: Display "No tasks found"
3. If not empty: Display formatted task list
   - Show ID, title, description, status
   - Use visual indicators (✓/○)
4. Return to main menu
```

### Update Task Flow

```
1. Prompt for task ID
2. Validate ID exists
3. Display current task details
4. Prompt for new title (press Enter to keep current)
5. Prompt for new description (press Enter to keep current)
6. Validate inputs
7. Update task
8. Display success message
9. Return to main menu
```

### Delete Task Flow

```
1. Prompt for task ID
2. Validate ID exists
3. Display task to be deleted
4. Confirm deletion (optional)
5. Delete task
6. Display success message
7. Return to main menu
```

### Toggle Completion Flow

```
1. Prompt for task ID
2. Validate ID exists
3. Toggle completion status
4. Display success message with new status
5. Return to main menu
```

## Testing Strategy

### Manual Testing Approach

**Test Categories**:

1. **Happy Path Tests**
   - Add task with title only
   - Add task with title and description
   - View tasks (empty and populated)
   - Update task title
   - Update task description
   - Delete task
   - Mark task complete
   - Mark task incomplete

2. **Validation Tests**
   - Empty title rejection
   - Title length validation (201 chars)
   - Description length validation (1001 chars)
   - Invalid task ID handling
   - Non-numeric ID input

3. **Edge Cases**
   - Empty task list operations
   - Single task operations
   - Multiple tasks with same title
   - Update without changes
   - Toggle completion multiple times

4. **User Experience Tests**
   - Menu navigation
   - Error message clarity
   - Success message confirmation
   - Visual indicators display
   - Graceful exit

### Test Checklist

```markdown
- [ ] Add task with valid title
- [ ] Add task with title and description
- [ ] Reject empty title
- [ ] Reject title >200 characters
- [ ] Reject description >1000 characters
- [ ] View empty task list
- [ ] View populated task list
- [ ] Update task title
- [ ] Update task description
- [ ] Update with invalid ID
- [ ] Delete existing task
- [ ] Delete with invalid ID
- [ ] Mark task complete
- [ ] Mark task incomplete
- [ ] Toggle completion multiple times
- [ ] Invalid menu choice handling
- [ ] Non-numeric ID input handling
- [ ] Exit application gracefully
```

## Implementation Notes

### Python Version and Dependencies

- **Python**: 3.13+
- **Standard Library Only**: No external dependencies
- **Type Hints**: Use throughout for clarity
- **Dataclasses**: For Task model

### Code Style

- **PEP 8**: Follow Python style guide
- **Type Hints**: All function signatures
- **Docstrings**: All classes and public methods
- **Line Length**: Max 88 characters (Black formatter standard)

### Project Structure

```
src/
└── todo_app/
    ├── __init__.py          # Package initialization
    ├── main.py              # Entry point (50 lines)
    ├── models.py            # Task model (30 lines)
    ├── storage.py           # Storage layer (80 lines)
    ├── operations.py        # Business logic (120 lines)
    └── ui.py                # Console UI (200 lines)
```

### Package Setup

```python
# pyproject.toml
[project]
name = "todo-app"
version = "0.1.0"
description = "Phase I: Console Todo Application"
requires-python = ">=3.13"

[project.scripts]
todo = "todo_app.main:main"
```

## Future Considerations

### Phase II Preparation

This design facilitates evolution to Phase II:

1. **Storage Layer**: Can be replaced with database implementation
2. **Operations Layer**: Business logic remains unchanged
3. **Models**: Can be extended with SQLModel
4. **UI Layer**: Can be replaced with REST API

### Extensibility Points

- Storage interface can support multiple backends
- Operations layer is storage-agnostic
- Models can be extended with additional fields
- UI can be swapped without affecting business logic

## Summary

This design provides:
- ✅ Clean separation of concerns
- ✅ Easy to test and maintain
- ✅ Ready for Phase II evolution
- ✅ Follows Python best practices
- ✅ Meets all Phase I requirements
- ✅ Clear error handling
- ✅ Intuitive user experience
