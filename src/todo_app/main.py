"""
Main entry point for the todo application.

This module initializes the application components and runs the main loop.
"""

from .storage import TaskStorage
from .operations import TaskOperations
from .ui import ConsoleUI


def main() -> None:
    """Main application entry point."""
    # Display welcome message
    print("\n" + "=" * 50)
    print("  Welcome to Todo Application!")
    print("  Manage your tasks efficiently from the command line")
    print("=" * 50)

    # Initialize components
    storage = TaskStorage()
    operations = TaskOperations(storage)
    ui = ConsoleUI(operations)

    # Main application loop
    try:
        while True:
            ui.display_menu()
            choice = ui.get_user_choice()

            if choice == 1:
                ui.add_task_flow()
            elif choice == 2:
                ui.view_tasks_flow()
            elif choice == 3:
                ui.update_task_flow()
            elif choice == 4:
                ui.delete_task_flow()
            elif choice == 5:
                ui.toggle_completion_flow()
            elif choice == 6:
                print("\n" + "=" * 50)
                print("  Thank you for using Todo Application!")
                print("  Goodbye! 👋")
                print("=" * 50 + "\n")
                break

    except KeyboardInterrupt:
        print("\n\n" + "=" * 50)
        print("  Application interrupted")
        print("  Goodbye! 👋")
        print("=" * 50 + "\n")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        print("Application terminated unexpectedly\n")


if __name__ == "__main__":
    main()
