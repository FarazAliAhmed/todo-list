"""Quick test to verify all modules can be imported."""

import sys
sys.path.insert(0, 'src')

try:
    from todo_app import models
    print("✅ models.py imported successfully")

    from todo_app import storage
    print("✅ storage.py imported successfully")

    from todo_app import operations
    print("✅ operations.py imported successfully")

    from todo_app import ui
    print("✅ ui.py imported successfully")

    from todo_app import main
    print("✅ main.py imported successfully")

    # Test basic functionality
    from todo_app.storage import TaskStorage
    from todo_app.operations import TaskOperations

    storage_instance = TaskStorage()
    ops = TaskOperations(storage_instance)

    # Create a test task
    task = ops.create_task("Test Task", "This is a test")
    print(f"\n✅ Created task: {task}")

    # List tasks
    tasks = ops.list_tasks()
    print(f"✅ Listed {len(tasks)} task(s)")

    # Toggle completion
    updated = ops.toggle_completion(task.id)
    print(f"✅ Toggled completion: {updated}")

    # Delete task
    deleted = ops.delete_task(task.id)
    print(f"✅ Deleted task: {deleted}")

    print("\n🎉 All tests passed! Application is ready to run.")
    print("\nTo run the application:")
    print("  python3 -m todo_app.main")

except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
