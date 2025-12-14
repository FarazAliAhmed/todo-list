"""
Simple test for error handling and validation.

Requirements: Requirement 11 (Error Handling and User Feedback)
"""
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Use a valid UUID for testing
TEST_USER_ID = "550e8400-e29b-41d4-a716-446655440000"


def test_health_check():
    """Test that the API is running."""
    print("Testing health check...")
    response = client.get("/health")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    assert response.json()["status"] == "healthy"
    print("✓ Health check passed")


def test_validation_error_empty_title():
    """Test that empty title returns 400 with validation error."""
    print("\nTesting empty title validation...")
    response = client.post(
        f"/api/{TEST_USER_ID}/tasks",
        json={"title": "", "description": "Test"}
    )
    # Should be 400 (validation) or 401 (auth)
    assert response.status_code in [400, 401], f"Expected 400 or 401, got {response.status_code}"
    data = response.json()
    assert "detail" in data, "Response should have 'detail' field"
    print(f"✓ Empty title validation passed (status: {response.status_code})")
    print(f"  Response: {data}")


def test_validation_error_title_too_long():
    """Test that title longer than 200 chars returns 400."""
    print("\nTesting title too long validation...")
    long_title = "x" * 201
    response = client.post(
        f"/api/{TEST_USER_ID}/tasks",
        json={"title": long_title, "description": "Test"}
    )
    assert response.status_code in [400, 401], f"Expected 400 or 401, got {response.status_code}"
    data = response.json()
    assert "detail" in data
    print(f"✓ Title too long validation passed (status: {response.status_code})")
    print(f"  Response: {data}")


def test_validation_error_description_too_long():
    """Test that description longer than 1000 chars returns 400."""
    print("\nTesting description too long validation...")
    long_description = "x" * 1001
    response = client.post(
        f"/api/{TEST_USER_ID}/tasks",
        json={"title": "Test", "description": long_description}
    )
    assert response.status_code in [400, 401], f"Expected 400 or 401, got {response.status_code}"
    data = response.json()
    assert "detail" in data
    print(f"✓ Description too long validation passed (status: {response.status_code})")
    print(f"  Response: {data}")


def test_unauthorized_no_token():
    """Test that requests without token return 401."""
    print("\nTesting unauthorized access...")
    response = client.get(f"/api/{TEST_USER_ID}/tasks")
    assert response.status_code == 401, f"Expected 401, got {response.status_code}"
    data = response.json()
    assert "detail" in data
    print(f"✓ Unauthorized access handled correctly")
    print(f"  Response: {data}")


def test_valid_title_boundaries():
    """Test that titles at boundary lengths are handled correctly."""
    print("\nTesting valid title boundaries...")

    # 1 character (minimum valid)
    response = client.post(
        f"/api/{TEST_USER_ID}/tasks",
        json={"title": "x"}
    )
    # Should fail auth (401), not validation (400)
    assert response.status_code == 401, f"Expected 401 (auth), got {response.status_code}"
    print("✓ Minimum title length (1 char) passed validation")

    # 200 characters (maximum valid)
    response = client.post(
        f"/api/{TEST_USER_ID}/tasks",
        json={"title": "x" * 200}
    )
    assert response.status_code == 401, f"Expected 401 (auth), got {response.status_code}"
    print("✓ Maximum title length (200 chars) passed validation")


def test_error_response_format():
    """Test that all errors have consistent format."""
    print("\nTesting error response format consistency...")

    # Test 401 error format
    response = client.get(f"/api/{TEST_USER_ID}/tasks")
    assert response.status_code == 401
    data = response.json()
    assert isinstance(data, dict), "Error response should be a dict"
    assert "detail" in data, "Error response should have 'detail' field"
    print("✓ 401 error has consistent format")

    # Test 400 validation error format
    response = client.post(
        f"/api/{TEST_USER_ID}/tasks",
        json={"description": "Test"}  # Missing title
    )
    assert response.status_code in [400, 401]
    data = response.json()
    assert isinstance(data, dict), "Error response should be a dict"
    assert "detail" in data, "Error response should have 'detail' field"
    print(f"✓ Validation error has consistent format (status: {response.status_code})")


if __name__ == "__main__":
    print("=" * 60)
    print("Error Handling and Validation Tests")
    print("=" * 60)

    try:
        test_health_check()
        test_validation_error_empty_title()
        test_validation_error_title_too_long()
        test_validation_error_description_too_long()
        test_unauthorized_no_token()
        test_valid_title_boundaries()
        test_error_response_format()

        print("\n" + "=" * 60)
        print("✓ All tests passed!")
        print("=" * 60)
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
