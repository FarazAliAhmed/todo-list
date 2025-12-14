"""
Integration tests for Phase II Full-Stack Web Application.

Tests all requirements end-to-end with real database operations:
- User authentication flow
- Task CRUD operations with authentication
- User data isolation
- JWT expiration handling
- Error scenarios (invalid data, unauthorized access)

Requirements: All requirements (comprehensive testing)
"""
import os
import pytest
from datetime import datetime, timedelta, UTC
from uuid import uuid4
from fastapi.testclient import TestClient
from jose import jwt
from sqlmodel import Session, create_engine, SQLModel, select
from sqlmodel.pool import StaticPool

from app.main import app
from app.database import get_session
from app.models.user import User
from app.models.task import Task
from app.config import settings


# Create in-memory SQLite database for testing
@pytest.fixture(name="session")
def session_fixture():
    """Create a fresh database session for each test."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    """Create a test client with overridden database session."""
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def create_test_user(session: Session, email: str = "test@example.com") -> User:
    """Helper function to create a test user in the database."""
    user = User(
        id=uuid4(),
        email=email,
        password_hash="hashed_password",
        name="Test User"
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def create_jwt_token(user_id: str, expired: bool = False) -> str:
    """Helper function to create a JWT token for testing."""
    if expired:
        exp = datetime.now(UTC) - timedelta(days=1)
    else:
        exp = datetime.now(UTC) + timedelta(days=settings.jwt_expiration_days)

    payload = {
        "sub": user_id,
        "email": "test@example.com",
        "exp": exp,
        "iat": datetime.now(UTC)
    }

    token = jwt.encode(
        payload,
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm
    )
    return token


# Test 1: User Authentication Flow
class TestAuthentication:
    """Test user authentication and JWT token handling."""

    def test_missing_authentication(self, client: TestClient, session: Session):
        """
        Test that endpoints require authentication.
        Requirements: Requirement 1 (User Authentication), Requirement 7 (RESTful API)
        """
        user = create_test_user(session)
        user_id = str(user.id)

        # Try to access endpoints without authentication
        response = client.get(f"/api/{user_id}/tasks")
        assert response.status_code == 401
        assert "Authentication required" in response.json()["detail"]

        response = client.post(f"/api/{user_id}/tasks", json={"title": "Test"})
        assert response.status_code == 401

    def test_invalid_token(self, client: TestClient, session: Session):
        """
        Test that invalid JWT tokens are rejected.
        Requirements: Requirement 1 (User Authentication)
        """
        user = create_test_user(session)
        user_id = str(user.id)

        # Try with invalid token
        headers = {"Authorization": "Bearer invalid-token"}
        response = client.get(f"/api/{user_id}/tasks", headers=headers)
        assert response.status_code == 401
        assert "Invalid or expired token" in response.json()["detail"]

    def test_expired_token(self, client: TestClient, session: Session):
        """
        Test JWT expiration handling.
        Requirements: Requirement 1 (User Authentication)
        """
        user = create_test_user(session)
        user_id = str(user.id)

        # Create expired token
        expired_token = create_jwt_token(user_id, expired=True)
        headers = {"Authorization": f"Bearer {expired_token}"}

        response = client.get(f"/api/{user_id}/tasks", headers=headers)
        assert response.status_code == 401
        assert "Invalid or expired token" in response.json()["detail"]

    def test_valid_authentication(self, client: TestClient, session: Session):
        """
        Test that valid JWT tokens are accepted.
        Requirements: Requirement 1 (User Authentication)
        """
        user = create_test_user(session)
        user_id = str(user.id)

        # Create valid token
        token = create_jwt_token(user_id)
        headers = {"Authorization": f"Bearer {token}"}

        response = client.get(f"/api/{user_id}/tasks", headers=headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)


# Test 2: Task Creation
class TestTaskCreation:
    """Test task creation with authentication."""

    def test_create_task_authenticated(self, client: TestClient, session: Session):
        """
        Test creating a task with valid authentication.
        Requirements: Requirement 2 (Task Creation via Web Interface)
        """
        user = create_test_user(session)
        user_id = str(user.id)
        token = create_jwt_token(user_id)
        headers = {"Authorization": f"Bearer {token}"}

        task_data = {
            "title": "Buy groceries",
            "description": "Milk, eggs, bread"
        }

        response = client.post(
            f"/api/{user_id}/tasks",
            json=task_data,
            headers=headers
        )

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Buy groceries"
        assert data["description"] == "Milk, eggs, bread"
        assert data["completed"] is False
        assert data["user_id"] == user_id
        assert "id" in data
        assert "created_at" in data

    def test_create_task_without_description(self, client: TestClient, session: Session):
        """
        Test creating a task without description.
        Requirements: Requirement 2 (Task Creation via Web Interface)
        """
        user = create_test_user(session)
        user_id = str(user.id)
        token = create_jwt_token(user_id)
        headers = {"Authorization": f"Bearer {token}"}

        task_data = {"title": "Simple task"}

        response = client.post(
            f"/api/{user_id}/tasks",
            json=task_data,
            headers=headers
        )

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Simple task"
        assert data["description"] is None

    def test_create_task_invalid_data(self, client: TestClient, session: Session):
        """
        Test validation for invalid task data.
        Requirements: Requirement 11 (Error Handling)
        """
        user = create_test_user(session)
        user_id = str(user.id)
        token = create_jwt_token(user_id)
        headers = {"Authorization": f"Bearer {token}"}

        # Empty title
        response = client.post(
            f"/api/{user_id}/tasks",
            json={"title": ""},
            headers=headers
        )
        assert response.status_code == 400  # Custom error handler returns 400

        # Title too long (>200 chars)
        response = client.post(
            f"/api/{user_id}/tasks",
            json={"title": "x" * 201},
            headers=headers
        )
        assert response.status_code == 400  # Custom error handler returns 400

        # Description too long (>1000 chars)
        response = client.post(
            f"/api/{user_id}/tasks",
            json={"title": "Valid", "description": "x" * 1001},
            headers=headers
        )
        assert response.status_code == 400  # Custom error handler returns 400


# Test 3: Task Viewing and User Isolation
class TestTaskViewing:
    """Test task viewing with user data isolation."""

    def test_view_tasks_user_isolation(self, client: TestClient, session: Session):
        """
        Test that users can only see their own tasks.
        Requirements: Requirement 3 (Task Viewing), Requirement 9 (User Data Isolation)
        """
        # Create two users
        user1 = create_test_user(session, "user1@example.com")
        user2 = create_test_user(session, "user2@example.com")

        # Create tasks for user1
        task1 = Task(user_id=user1.id, title="User 1 Task 1", completed=False)
        task2 = Task(user_id=user1.id, title="User 1 Task 2", completed=True)
        session.add(task1)
        session.add(task2)

        # Create tasks for user2
        task3 = Task(user_id=user2.id, title="User 2 Task 1", completed=False)
        session.add(task3)

        session.commit()

        # User1 should only see their tasks
        token1 = create_jwt_token(str(user1.id))
        headers1 = {"Authorization": f"Bearer {token1}"}

        response = client.get(f"/api/{user1.id}/tasks", headers=headers1)
        assert response.status_code == 200
        tasks = response.json()
        assert len(tasks) == 2
        assert all(task["user_id"] == str(user1.id) for task in tasks)

        # User2 should only see their tasks
        token2 = create_jwt_token(str(user2.id))
        headers2 = {"Authorization": f"Bearer {token2}"}

        response = client.get(f"/api/{user2.id}/tasks", headers=headers2)
        assert response.status_code == 200
        tasks = response.json()
        assert len(tasks) == 1
        assert tasks[0]["user_id"] == str(user2.id)

    def test_view_empty_task_list(self, client: TestClient, session: Session):
        """
        Test viewing tasks when user has no tasks.
        Requirements: Requirement 3 (Task Viewing)
        """
        user = create_test_user(session)
        token = create_jwt_token(str(user.id))
        headers = {"Authorization": f"Bearer {token}"}

        response = client.get(f"/api/{user.id}/tasks", headers=headers)
        assert response.status_code == 200
        assert response.json() == []

    def test_get_specific_task(self, client: TestClient, session: Session):
        """
        Test getting a specific task by ID.
        Requirements: Requirement 3 (Task Viewing)
        """
        user = create_test_user(session)
        task = Task(user_id=user.id, title="Test Task", description="Details")
        session.add(task)
        session.commit()
        session.refresh(task)

        token = create_jwt_token(str(user.id))
        headers = {"Authorization": f"Bearer {token}"}

        response = client.get(f"/api/{user.id}/tasks/{task.id}", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == task.id
        assert data["title"] == "Test Task"


# Test 4: Task Update with Ownership Verification
class TestTaskUpdate:
    """Test task updates with ownership verification."""

    def test_update_task_ownership_verification(self, client: TestClient, session: Session):
        """
        Test that users can only update their own tasks.
        Requirements: Requirement 4 (Task Update), Requirement 9 (User Data Isolation)
        """
        # Create two users
        user1 = create_test_user(session, "user1@example.com")
        user2 = create_test_user(session, "user2@example.com")

        # Create task for user1
        task = Task(user_id=user1.id, title="User 1 Task", completed=False)
        session.add(task)
        session.commit()
        session.refresh(task)

        # User2 tries to update user1's task
        token2 = create_jwt_token(str(user2.id))
        headers2 = {"Authorization": f"Bearer {token2}"}

        response = client.put(
            f"/api/{user1.id}/tasks/{task.id}",
            json={"title": "Hacked!"},
            headers=headers2
        )
        # Should get 403 Forbidden because user_id doesn't match token
        assert response.status_code == 403
        assert "Access denied" in response.json()["detail"]

    def test_update_task_success(self, client: TestClient, session: Session):
        """
        Test successful task update.
        Requirements: Requirement 4 (Task Update)
        """
        user = create_test_user(session)
        task = Task(user_id=user.id, title="Original", description="Old desc")
        session.add(task)
        session.commit()
        session.refresh(task)

        token = create_jwt_token(str(user.id))
        headers = {"Authorization": f"Bearer {token}"}

        update_data = {
            "title": "Updated Title",
            "description": "New description"
        }

        response = client.put(
            f"/api/{user.id}/tasks/{task.id}",
            json=update_data,
            headers=headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["description"] == "New description"

    def test_update_nonexistent_task(self, client: TestClient, session: Session):
        """
        Test updating a task that doesn't exist.
        Requirements: Requirement 11 (Error Handling)
        """
        user = create_test_user(session)
        token = create_jwt_token(str(user.id))
        headers = {"Authorization": f"Bearer {token}"}

        response = client.put(
            f"/api/{user.id}/tasks/99999",
            json={"title": "Updated"},
            headers=headers
        )

        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()


# Test 5: Task Deletion with Ownership Verification
class TestTaskDeletion:
    """Test task deletion with ownership verification."""

    def test_delete_task_ownership_verification(self, client: TestClient, session: Session):
        """
        Test that users can only delete their own tasks.
        Requirements: Requirement 5 (Task Deletion), Requirement 9 (User Data Isolation)
        """
        # Create two users
        user1 = create_test_user(session, "user1@example.com")
        user2 = create_test_user(session, "user2@example.com")

        # Create task for user1
        task = Task(user_id=user1.id, title="User 1 Task")
        session.add(task)
        session.commit()
        session.refresh(task)

        # User2 tries to delete user1's task
        token2 = create_jwt_token(str(user2.id))
        headers2 = {"Authorization": f"Bearer {token2}"}

        response = client.delete(
            f"/api/{user1.id}/tasks/{task.id}",
            headers=headers2
        )
        # Should get 403 Forbidden
        assert response.status_code == 403

        # Verify task still exists
        statement = select(Task).where(Task.id == task.id)
        existing_task = session.exec(statement).first()
        assert existing_task is not None

    def test_delete_task_success(self, client: TestClient, session: Session):
        """
        Test successful task deletion.
        Requirements: Requirement 5 (Task Deletion)
        """
        user = create_test_user(session)
        task = Task(user_id=user.id, title="To Delete")
        session.add(task)
        session.commit()
        session.refresh(task)
        task_id = task.id

        token = create_jwt_token(str(user.id))
        headers = {"Authorization": f"Bearer {token}"}

        response = client.delete(
            f"/api/{user.id}/tasks/{task_id}",
            headers=headers
        )

        assert response.status_code == 204

        # Verify task is deleted
        statement = select(Task).where(Task.id == task_id)
        deleted_task = session.exec(statement).first()
        assert deleted_task is None

    def test_delete_nonexistent_task(self, client: TestClient, session: Session):
        """
        Test deleting a task that doesn't exist.
        Requirements: Requirement 11 (Error Handling)
        """
        user = create_test_user(session)
        token = create_jwt_token(str(user.id))
        headers = {"Authorization": f"Bearer {token}"}

        response = client.delete(
            f"/api/{user.id}/tasks/99999",
            headers=headers
        )

        assert response.status_code == 404


# Test 6: Task Completion Toggle
class TestTaskCompletion:
    """Test task completion toggle functionality."""

    def test_toggle_completion(self, client: TestClient, session: Session):
        """
        Test toggling task completion status.
        Requirements: Requirement 6 (Task Completion Toggle)
        """
        user = create_test_user(session)
        task = Task(user_id=user.id, title="Test Task", completed=False)
        session.add(task)
        session.commit()
        session.refresh(task)

        token = create_jwt_token(str(user.id))
        headers = {"Authorization": f"Bearer {token}"}

        # Toggle to completed
        response = client.patch(
            f"/api/{user.id}/tasks/{task.id}/complete",
            headers=headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["completed"] is True

        # Toggle back to incomplete
        response = client.patch(
            f"/api/{user.id}/tasks/{task.id}/complete",
            headers=headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["completed"] is False

    def test_toggle_completion_ownership(self, client: TestClient, session: Session):
        """
        Test that users can only toggle their own tasks.
        Requirements: Requirement 6 (Task Completion Toggle), Requirement 9 (User Data Isolation)
        """
        user1 = create_test_user(session, "user1@example.com")
        user2 = create_test_user(session, "user2@example.com")

        task = Task(user_id=user1.id, title="User 1 Task", completed=False)
        session.add(task)
        session.commit()
        session.refresh(task)

        # User2 tries to toggle user1's task
        token2 = create_jwt_token(str(user2.id))
        headers2 = {"Authorization": f"Bearer {token2}"}

        response = client.patch(
            f"/api/{user1.id}/tasks/{task.id}/complete",
            headers=headers2
        )

        assert response.status_code == 403


# Test 7: Error Scenarios
class TestErrorScenarios:
    """Test various error scenarios and edge cases."""

    def test_invalid_user_id_format(self, client: TestClient, session: Session):
        """
        Test handling of invalid user ID format in URL.
        Requirements: Requirement 11 (Error Handling)
        """
        user = create_test_user(session)
        token = create_jwt_token(str(user.id))
        headers = {"Authorization": f"Bearer {token}"}

        # Invalid UUID format
        response = client.get("/api/not-a-uuid/tasks", headers=headers)
        assert response.status_code == 400
        assert "Invalid user ID format" in response.json()["detail"]

    def test_unauthorized_access_different_user(self, client: TestClient, session: Session):
        """
        Test that authenticated users cannot access other users' resources.
        Requirements: Requirement 9 (User Data Isolation)
        """
        user1 = create_test_user(session, "user1@example.com")
        user2 = create_test_user(session, "user2@example.com")

        # User1 token trying to access user2's tasks
        token1 = create_jwt_token(str(user1.id))
        headers1 = {"Authorization": f"Bearer {token1}"}

        response = client.get(f"/api/{user2.id}/tasks", headers=headers1)
        assert response.status_code == 403
        assert "Access denied" in response.json()["detail"]

    def test_malformed_request_body(self, client: TestClient, session: Session):
        """
        Test handling of malformed request bodies.
        Requirements: Requirement 11 (Error Handling)
        """
        user = create_test_user(session)
        token = create_jwt_token(str(user.id))
        headers = {"Authorization": f"Bearer {token}"}

        # Missing required field
        response = client.post(
            f"/api/{user.id}/tasks",
            json={},
            headers=headers
        )
        assert response.status_code == 400  # Custom error handler returns 400


# Test 8: End-to-End User Flow
class TestEndToEndFlow:
    """Test complete user workflows from start to finish."""

    def test_complete_task_lifecycle(self, client: TestClient, session: Session):
        """
        Test the complete lifecycle of a task: create, view, update, toggle, delete.
        Requirements: All CRUD requirements (2-6)
        """
        user = create_test_user(session)
        token = create_jwt_token(str(user.id))
        headers = {"Authorization": f"Bearer {token}"}

        # 1. Create task
        create_response = client.post(
            f"/api/{user.id}/tasks",
            json={"title": "Complete project", "description": "Finish by Friday"},
            headers=headers
        )
        assert create_response.status_code == 201
        task_id = create_response.json()["id"]

        # 2. View all tasks
        list_response = client.get(f"/api/{user.id}/tasks", headers=headers)
        assert list_response.status_code == 200
        assert len(list_response.json()) == 1

        # 3. Get specific task
        get_response = client.get(f"/api/{user.id}/tasks/{task_id}", headers=headers)
        assert get_response.status_code == 200
        assert get_response.json()["title"] == "Complete project"

        # 4. Update task
        update_response = client.put(
            f"/api/{user.id}/tasks/{task_id}",
            json={"title": "Complete project ASAP"},
            headers=headers
        )
        assert update_response.status_code == 200
        assert update_response.json()["title"] == "Complete project ASAP"

        # 5. Toggle completion
        toggle_response = client.patch(
            f"/api/{user.id}/tasks/{task_id}/complete",
            headers=headers
        )
        assert toggle_response.status_code == 200
        assert toggle_response.json()["completed"] is True

        # 6. Delete task
        delete_response = client.delete(
            f"/api/{user.id}/tasks/{task_id}",
            headers=headers
        )
        assert delete_response.status_code == 204

        # 7. Verify deletion
        list_response = client.get(f"/api/{user.id}/tasks", headers=headers)
        assert list_response.status_code == 200
        assert len(list_response.json()) == 0


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short"])
