"""
Test script to verify SQLModel models are correctly defined.
This doesn't require a database connection.
"""
import sys
from pathlib import Path
from uuid import uuid4
from datetime import datetime, UTC

# Add app directory to path
sys.path.append(str(Path(__file__).parent))

from app.models import User, Task


def test_user_model():
    """Test User model instantiation."""
    print("Testing User model...")

    user = User(
        id=uuid4(),
        email="test@example.com",
        password_hash="hashed_password",
        name="Test User",
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC)
    )

    assert user.email == "test@example.com"
    assert user.name == "Test User"
    print("✓ User model works correctly")
    return True


def test_task_model():
    """Test Task model instantiation."""
    print("Testing Task model...")

    user_id = uuid4()
    task = Task(
        user_id=user_id,
        title="Test Task",
        description="This is a test task",
        completed=False,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC)
    )

    assert task.title == "Test Task"
    assert task.description == "This is a test task"
    assert task.completed is False
    assert task.user_id == user_id
    print("✓ Task model works correctly")
    return True


def test_model_relationships():
    """Test that model relationships are defined."""
    print("Testing model relationships...")

    # Check that User has tasks relationship
    assert hasattr(User, 'tasks')

    # Check that Task has user relationship
    assert hasattr(Task, 'user')

    print("✓ Model relationships are defined")
    return True


if __name__ == "__main__":
    try:
        test_user_model()
        test_task_model()
        test_model_relationships()
        print("\n✓ All model tests passed!")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Model test failed: {e}")
        sys.exit(1)
