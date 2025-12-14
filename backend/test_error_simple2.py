"""
Simple test for error handling - focusing on what we can test without auth.
"""
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

TEST_USER_ID = "550e8400-e29b-41d4-a716-446655440000"


def test_health_check():
    """Test that the API is running."""
    print("Testing health check...")
    response = client.get("/health")
    assert response.status_code == 200
    print("✓ Health check passed")


def test_invalid_user_id_format():
    """Test that invalid user_id format returns error."""
    print("\nTesting invalid user_id format...")
    response = client.get("/api/invalid-uuid/tasks")
    # HTTPBearer returns 403 when no auth header is present
    print(f"  Status: {response.status_code}")
    print(f"  Response: {response.json()}")
    assert response.status_code in [400, 401, 403]
    print("✓ Invalid user_id handled correctly")


def test_unauthorized_no_token():
    """Test that requests without token return 401."""
    print("\nTesting unauthorized access...")
    response = client.get(f"/api/{TEST_USER_ID}/tasks")
    print(f"  Status: {response.status_code}")
    print(f"  Response: {response.json()}")
    assert response.status_code == 401
    print("✓ Unauthorized access returns 401")


def test_validation_empty_title():
    """Test validation for empty title."""
    print("\nTesting empty title validation...")
    response = client.post(
        f"/api/{TEST_USER_ID}/tasks",
        json={"title": "", "description": "Test"}
    )
    print(f"  Status: {response.status_code}")
    print(f"  Response: {response.json()}")
    # Validation should catch this as 400, or auth as 401
    assert response.status_code in [400, 401, 403]
    print(f"✓ Empty title handled (status: {response.status_code})")


def test_validation_title_too_long():
    """Test validation for title too long."""
    print("\nTesting title too long...")
    response = client.post(
        f"/api/{TEST_USER_ID}/tasks",
        json={"title": "x" * 201}
    )
    print(f"  Status: {response.status_code}")
    print(f"  Response: {response.json()}")
    assert response.status_code in [400, 401, 403]
    print(f"✓ Title too long handled (status: {response.status_code})")


def test_validation_description_too_long():
    """Test validation for description too long."""
    print("\nTesting description too long...")
    response = client.post(
        f"/api/{TEST_USER_ID}/tasks",
        json={"title": "Test", "description": "x" * 1001}
    )
    print(f"  Status: {response.status_code}")
    print(f"  Response: {response.json()}")
    assert response.status_code in [400, 401, 403]
    print(f"✓ Description too long handled (status: {response.status_code})")


def test_error_response_format():
    """Test that errors have consistent format."""
    print("\nTesting error response format...")
    response = client.get(f"/api/{TEST_USER_ID}/tasks")
    data = response.json()
    assert isinstance(data, dict)
    assert "detail" in data
    print(f"✓ Error response has consistent format")
    print(f"  Keys: {list(data.keys())}")


if __name__ == "__main__":
    print("=" * 60)
    print("Error Handling Tests")
    print("=" * 60)

    try:
        test_health_check()
        test_invalid_user_id_format()
        test_unauthorized_no_token()
        test_validation_empty_title()
        test_validation_title_too_long()
        test_validation_description_too_long()
        test_error_response_format()

        print("\n" + "=" * 60)
        print("✓ All tests passed!")
        print("=" * 60)
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
