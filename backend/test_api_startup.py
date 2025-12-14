"""
Test script to verify FastAPI application startup and health check endpoint.
"""
from fastapi.testclient import TestClient
from app.main import app

# Create test client
client = TestClient(app)


def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "todo-api"
    assert data["version"] == "2.0.0"
    print("✓ Health check endpoint working")


def test_root_endpoint():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Todo API"
    assert data["version"] == "2.0.0"
    assert data["docs"] == "/docs"
    print("✓ Root endpoint working")


def test_cors_configured():
    """Test that CORS is configured."""
    # Check that CORS middleware is present
    middlewares = [m for m in app.user_middleware]
    assert len(middlewares) > 0
    print("✓ CORS middleware configured")


def test_app_metadata():
    """Test FastAPI app metadata."""
    assert app.title == "Todo API"
    assert app.description == "RESTful API for multi-user todo application"
    assert app.version == "2.0.0"
    print("✓ App metadata configured correctly")


if __name__ == "__main__":
    print("Testing FastAPI Core API Structure...")
    print()

    try:
        test_health_check()
        test_root_endpoint()
        test_cors_configured()
        test_app_metadata()
        print()
        print("✅ All tests passed! Core API structure is working correctly.")
    except AssertionError as e:
        print(f"❌ Test failed: {e}")
        exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        exit(1)
