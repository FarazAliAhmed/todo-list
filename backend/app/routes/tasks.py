"""
Task API endpoints for CRUD operations.
Auth temporarily disabled for testing.
"""
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlmodel import Session, select
from app.database import get_session
from app.models.task import Task, utc_now
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.errors import not_found_error


router = APIRouter(prefix="/api", tags=["tasks"])


@router.get("/{user_id}/tasks", response_model=List[TaskResponse])
async def list_tasks(
    user_id: str,
    session: Session = Depends(get_session)
):
    """List all tasks for a user."""
    try:
        user_uuid = UUID(user_id)
    except ValueError:
        return []
    
    statement = select(Task).where(Task.user_id == user_uuid)
    tasks = session.exec(statement).all()
    return tasks


@router.post("/{user_id}/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    user_id: str,
    task_data: TaskCreate,
    session: Session = Depends(get_session)
):
    """Create a new task."""
    try:
        user_uuid = UUID(user_id)
    except ValueError:
        raise not_found_error("User", user_id)
    
    task = Task(
        user_id=user_uuid,
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
    session: Session = Depends(get_session)
):
    """Get a specific task by ID."""
    try:
        user_uuid = UUID(user_id)
    except ValueError:
        raise not_found_error("Task", task_id)
    
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == user_uuid
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
    session: Session = Depends(get_session)
):
    """Update an existing task."""
    try:
        user_uuid = UUID(user_id)
    except ValueError:
        raise not_found_error("Task", task_id)
    
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == user_uuid
    )
    task = session.exec(statement).first()

    if task is None:
        raise not_found_error("Task", task_id)

    if task_data.title is not None:
        task.title = task_data.title
    if task_data.description is not None:
        task.description = task_data.description
    if task_data.completed is not None:
        task.completed = task_data.completed

    task.updated_at = utc_now()
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.delete("/{user_id}/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    user_id: str,
    task_id: int,
    session: Session = Depends(get_session)
):
    """Delete a task."""
    try:
        user_uuid = UUID(user_id)
    except ValueError:
        raise not_found_error("Task", task_id)
    
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == user_uuid
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
    session: Session = Depends(get_session)
):
    """Toggle the completion status of a task."""
    try:
        user_uuid = UUID(user_id)
    except ValueError:
        raise not_found_error("Task", task_id)
    
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == user_uuid
    )
    task = session.exec(statement).first()

    if task is None:
        raise not_found_error("Task", task_id)

    task.completed = not task.completed
    task.updated_at = utc_now()
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
