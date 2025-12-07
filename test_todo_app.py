#!/usr/bin/env python3
"""
Comprehensive test script for Phase I Todo Application.
Tests all CRUD operations, validation, and edge cases.
"""

import sys
sys.path.insert(0, 'src')

from todo_app.storage import TaskStorage
from todo_app.operations import TaskOperations
from todo_app.models import Task


def test_task_creation():
    """Test creating tasks with validation."""
    print("\n=== Testing Task Creation ===")
    storage = TaskStorage()
    ops = TaskOperations(storage)

    # Test 1: Create task with title only
    try:
        task1 = ops.create_task("Buy groceries")
        assert task1.id == 1
        assert task1.title == "Buy groceries"
        assert task1.description is None
        assert task1.completed is False
        print("✅ Test 1 passed: Create task with title only")
    except Exception as e:
        print(f"❌ Test 1 failed: {e}")
        return False

    # Test 2: Create task with title and diption
    try:
        task2 = ops.create_task("Call dentist", "Schedule appointment for next week")
        assert task2.id == 2
        assert task2.title == "Call dentist"
        assert task2.description == "Schedule appointment for next week"
        print("✅ Test 2 passed: Create task with title and description")
    except Exception as e:
        print(f"❌ Test 2 failed: {e}")
        return False

    # Test 3: Reject empty title
    try:
        ops.create_task("")
        print("❌ Test 3 failed: Empty title should be rejected")
        return False
    except ValueError as e:
        print(f"✅ Test 3 passed: Empty title rejected - {e}")

    # Test 4: Reject title >200 characters
    try:
        long_title = "a" * 201
        ops.create_task(long_title)
        print("❌ Test 4 failed: Title >200 chars should be rejected")
        return False
    except ValueError as e:
        print(f"✅ Test 4 passed: Long title rejected - {e}")

    # Test 5: Reject description >1000 characters
    try:
        long_desc = "a" * 1001
        ops.create_task("Valid title", long_desc)
        print("❌ Test 5 failed: Description >1000 chars should be rejected")
        return False
    except ValueError as e:
        print(f"✅ Test 5 passed: Long description rejected - {e}")

    return True


def test_task_listing():
    """Test listing tasks."""
    print("\n=== Testing Task Listing ===")
    storage = TaskStorage()
    ops = TaskOperations(storage)

    # Test 1: Empty list
    tasks = ops.list_tasks()
    assert len(tasks) == 0
    print("✅ Test 1 passed: Empty list returns []")

    # Test 2: List with tasks
    ops.create_task("Task 1")
    ops.create_task("Task 2")
    ops.create_task("Task 3")
    tasks = ops.list_tasks()
    assert len(tasks) == 3
    print(f"✅ Test 2 passed: List returns {len(tasks)} tasks")

    return True


def test_task_update():
    """Test updating tasks."""
    print("\n=== Testing Task Update ===")
    storage = TaskStorage()
    ops = TaskOperations(storage)

    task = ops.create_task("Original title", "Original description")

    # Test 1: Update title only
    updated = ops.update_task(task.id, title="New title")
    assert updated.title == "New title"
    assert updated.description == "Original description"
    print("✅ Test 1 passed: Update title only")

    # Test 2: Update description only
    updated = ops.update_task(task.id, description="New description")
    assert updated.title == "New title"
    assert updated.description == "New description"
    print("✅ Test 2 passed: Update description only")

    # Test 3: Update both
    updated = ops.update_task(task.id, title="Final title", description="Final description")
    assert updated.title == "Final title"
    assert updated.description == "Final description"
    print("✅ Test 3 passed: Update both fields")

    # Test 4: Invalid task ID
    result = ops.update_task(999, title="Test")
    assert result is None
    print("✅ Test 4 passed: Invalid ID returns None")

    # Test 5: Reject empty title
    try:
        ops.update_task(task.id, title="")
        print("❌ Test 5 failed: Empty title should be rejected")
        return False
    except ValueError:
        print("✅ Test 5 passed: Empty title rejected in update")

    return True


def test_task_deletion():
    """Test deleting tasks."""
    print("\n=== Testing Task Deletion ===")
    storage = TaskStorage()
    ops = TaskOperations(storage)

    task1 = ops.create_task("Task 1")
    task2 = ops.create_task("Task 2")

    # Test 1: Delete existing task
    result = ops.delete_task(task1.id)
    assert result is True
    assert len(ops.list_tasks()) == 1
    print("✅ Test 1 passed: Delete existing task")

    # Test 2: Delete non-existent task
    result = ops.delete_task(999)
    assert result is False
    print("✅ Test 2 passed: Delete non-existent task returns False")

    # Test 3: Delete last task
    result = ops.delete_task(task2.id)
    assert result is True
    assert len(ops.list_tasks()) == 0
    print("✅ Test 3 passed: Delete last task")

    return True


def test_task_completion():
    """Test toggling task completion."""
    print("\n=== Testing Task Completion ===")
    storage = TaskStorage()
    ops = TaskOperations(storage)

    task = ops.create_task("Test task")

    # Test 1: Mark as complete
    updated = ops.toggle_completion(task.id)
    assert updated.completed is True
    print("✅ Test 1 passed: Mark task as complete")

    # Test 2: Mark as incomplete
    updated = ops.toggle_completion(task.id)
    assert updated.completed is False
    print("✅ Test 2 passed: Mark task as incomplete")

    # Test 3: Toggle multiple times
    for i in range(5):
        updated = ops.toggle_completion(task.id)
    assert updated.completed is True  # Odd number of toggles
    print("✅ Test 3 passed: Toggle multiple times")

    # Test 4: Invalid task ID
    result = ops.toggle_completion(999)
    assert result is None
    print("✅ Test 4 passed: Invalid ID returns None")

    return True


def test_storage_layer():
    """Test storage layer directly."""
    print("\n=== Testing Storage Layer ===")
    storage = TaskStorage()

    # Test ID generation
    id1 = storage.generate_id()
    id2 = storage.generate_id()
    assert id1 == 1
    assert id2 == 2
    print("✅ ID generation works correctly")

    # Test exists method
    from datetime import datetime
    task = Task(id=1, title="Test", description=None, completed=False,
                created_at=datetime.now(), updated_at=datetime.now())
    storage.add(task)
    assert storage.exists(1) is True
    assert storage.exists(999) is False
    print("✅ Exists method works correctly")

    return True


def test_edge_cases():
    """Test edge cases."""
    print("\n=== Testing Edge Cases ===")
    storage = TaskStorage()
    ops = TaskOperations(storage)

    # Test 1: Whitespace-only title
    try:
        ops.create_task("   ")
        print("❌ Test 1 failed: Whitespace-only title should be rejected")
        return False
    except ValueError:
        print("✅ Test 1 passed: Whitespace-only title rejected")

    # Test 2: Title with leading/trailing whitespace
    task = ops.create_task("  Test Task  ")
    assert task.title == "Test Task"
    print("✅ Test 2 passed: Whitespace trimmed from title")

    # Test 3: Empty description becomes None
    task = ops.create_task("Task", "   ")
    assert task.description is None
    print("✅ Test 3 passed: Empty description becomes None")

    # Test 4: Update with no changes
    task = ops.create_task("Task")
    updated = ops.update_task(task.id)
    assert updated.title == "Task"
    print("✅ Test 4 passed: Update with no changes preserves data")

    return True


def run_all_tests():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("  PHASE I TODO APPLICATION - COMPREHENSIVE TEST SUITE")
    print("=" * 60)

    tests = [
        ("Task Creation", test_task_creation),
        ("Task Listing", test_task_listing),
        ("Task Update", test_task_update),
        ("Task Deletion", test_task_deletion),
        ("Task Completion", test_task_completion),
        ("Storage Layer", test_storage_layer),
        ("Edge Cases", test_edge_cases),
    ]

    passed = 0
    failed = 0

    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
                print(f"\n❌ {test_name} test suite failed")
        except Exception as e:
            failed += 1
            print(f"\n❌ {test_name} test suite crashed: {e}")
            import traceback
            traceback.print_exc()

    print("\n" + "=" * 60)
    print(f"  TEST RESULTS: {passed} passed, {failed} failed")
    print("=" * 60)

    if failed == 0:
        print("\n🎉 All tests passed! Application is ready for submission.")
        print("\nTo run the application:")
        print("  python3 -m todo_app.main")
        return True
    else:
        print(f"\n⚠️  {failed} test suite(s) failed. Please review and fix.")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
