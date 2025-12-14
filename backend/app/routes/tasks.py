"""
Task API endpoints for CRUD operations.
All endpoints require JWT authentication and enforce user ownership.
"""
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlmodel import Session, select
from app.database import get_session
from app.middleware.auth import get_current_user, validate_user_id
from app.models.user import User
from app.models.task import Task, utc_now
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.errors import not_found_error


router = APIRouter(prefix="/api", tags=["tasks"])


@router.get("/{user_id}/tasks", response_model=List[TaskResponse])
async def list_tasks(
    user_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    List all tasks for the authenticated user.

    Requirements: Requirement 3 (Task Viewing via Web Interface)
    - Returns only tasks belonging to the authenticated user
    - Requires valid JWT authentication
    """
    # Validate user can only access their own tasks
    validate_user_id(current_user, user_id)

    # Query tasks for this user
    statement = select(Task).where(Task.user_id == current_user.id)
    tasks = session.exec(statement).all()

    return tasks


@router.post("/{user_id}/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    user_id: str,
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Create a new task for the authenticated user.

    Requirements: Requirement 2 (Task Creation via Web Interface)
    - Creates task associated with authenticated user
    - Validates title length (1-200 chars)
    - Validates description length (max 1000 chars)
    """
    # Validate user can only create tasks for themselves
    validate_user_id(current_user, user_id)

    # Create new task
    task = Task(
        user_id=current_user.id,
        title=task_data.title,
        description=task_data.description,
        completed=False
    )

    session.add(task)
    session.commit()
    session.refresh(task)

    return task


@router.get("/{user_id}/tasks/{task_id}", response_model=TaskResponse)
async def get_task(
    user_id: str,
    task_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get a specific task by ID.

    Requirements: Requirement 3 (Task Viewing via Web Interface)
    - Returns task only if it belongs to authenticated user
    - Returns 404 if task doesn't exist
    - Returns 403 if task belongs to another user
    """
    # Validate user can only access their own tasks
    validate_user_id(current_user, user_id)

    # Query task with user ownership check
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == current_user.id
    )
    task = session.exec(statement).first()

    if task is None:
        raise not_found_error("Task", task_id)

    return task


@router.put("/{user_id}/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    user_id: str,
    task_id: int,
    task_data: TaskUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update an existing task.

    Requirements: Requirement 4 (Task Update via Web Interface)
    - Updates task only if it belongs to authenticated user
    - Validates title length (1-200 chars) if provided
    - Validates description length (max 1000 chars) if provided
    - Returns 404 if task doesn't exist
    - Returns 403 if task belongs to another user
    """
    # Validate user can only update their own tasks
    validate_user_id(current_user, user_id)

    # Query task with user ownership check
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == current_user.id
    )
    task = session.exec(statement).first()

    if task is None:
        raise not_found_error("Task", task_id)

    # Update fields if provided
    if task_data.title is not None:
        task.title = task_data.title
    if task_data.description is not None:
        task.description = task_data.description
    if task_data.completed is not None:
        task.completed = task_data.completed

    # Update timestamp
    task.updated_at = utc_now()

    session.add(task)
    session.commit()
    session.refresh(task)

    return task


@router.delete("/{user_id}/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    user_id: str,
    task_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Delete a task.

    Requirements: Requirement 5 (Task Deletion via Web Interface)
    - Deletes task only if it belongs to authenticated user
    - Returns 404 if task doesn't exist
    - Returns 403 if task belongs to another user
    """
    # Validate user can only delete their own tasks
    validate_user_id(current_user, user_id)

    # Query task with user ownership check
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == current_user.id
    )
    task = session.exec(statement).first()

    if task is None:
        raise not_found_error("Task", task_id)

    session.delete(task)
    session.commit()

    return None


@router.patch("/{user_id}/tasks/{task_id}/complete", response_model=TaskResponse)
async def toggle_complete(
    user_id: str,
    task_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Toggle the completion status of a task.

    Requirements: Requirement 6 (Task Completion Toggle via Web Interface)
    - Toggles completion status only if task belongs to authenticated user
    - Returns 404 if task doesn't exist
    - Returns 403 if task belongs to another user
    """
    # Validate user can only toggle their own tasks
    validate_user_id(current_user, user_id)

    # Query task with user ownership check
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == current_user.id
    )
    task = session.exec(statement).first()

    if task is None:
        raise not_found_error("Task", task_id)

    # Toggle completion status
    task.completed = not task.completed
    task.updated_at = utc_now()

    session.add(task)
    session.commit()
    session.refresh(task)

    return task
