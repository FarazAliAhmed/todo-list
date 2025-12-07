# Claude Code Instructions - Evolution of Todo

## Project Overview

This is a spec-driven development project building a todo application that evolves through 5 phases. Currently working on **Phase I: Console Application**.

## Current Phase: Phase I - Console Application

**Objective**: Build a command-line todo application with in-memory storage.

**Technology Stack**:
- Python 3.13+
- UV (package manager)
- No external dependencies for core functionality

## Specification Structure

All specifications are located in `.kiro/specs/phase1-console-app/`:
- `requirements.md` - User stories and acceptance criteria (EARS format)
- `design.md` - Architecture and implementation design
- `tasks.md` - Implementation task breakdown

## Development Guidelines

### Code Style
- Follow PEP 8 Python style guide
- Use type hints for function signatures
- Write docstrings for all classes and functions
- Keep functions under 50 lines when possible

### Project Structure
```
src/
└── todo_app/
    ├── __init__.py
    ├── main.py           # Entry point
    ├── models.py         # Task data model
    ├── storage.py        # In-memory storage
    ├── ui.py             # Console UI
    └── operations.py     # CRUD operations
```

### Implementation Principles

1. **Separation of Concerns**
   - Models: Data structures only
   - Storage: Data management logic
   - Operations: Business logic
   - UI: User interaction and display

2. **Error Handling**
   - Validate all user inputs
   - Provide clear, helpful error messages
   - Never crash - handle exceptions gracefully

3. **User Experience**
   - Clear menu options
   - Confirmation messages for actions
   - Visual indicators for task status
   - Intuitive command flow

### Testing Approach
- Manual testing through console interaction
- Test all CRUD operations
- Test error cases (invalid IDs, empty inputs)
- Test edge cases (empty list, single task, many tasks)

## How to Use This Project

### Reading Specifications
Always read the relevant spec before implementing:
```
@.kiro/specs/phase1-console-app/requirements.md
@.kiro/specs/phase1-console-app/design.md
@.kiro/specs/phase1-console-app/tasks.md
```

### Implementation Workflow
1. Read the requirements document
2. Review the design document
3. Follow the tasks document step-by-step
4. Implement one task at a time
5. Test after each task completion

### Running the Application
```bash
# Setup (using UV)
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .

# Run
python -m todo_app.main
```

## Key Features to Implement

### 1. Add Task
- Prompt for title (required)
- Prompt for description (optional)
- Generate unique ID
- Display confirmation

### 2. View Tasks
- Display all tasks in formatted list
- Show ID, title, description, status
- Handle empty list gracefully
- Use visual indicators (✓ for complete, ○ for incomplete)

### 3. Update Task
- Prompt for task ID
- Allow updating title and/or description
- Validate ID exists
- Display confirmation

### 4. Delete Task
- Prompt for task ID
- Validate ID exists
- Remove from list
- Display confirmation

### 5. Mark Complete/Incomplete
- Prompt for task ID
- Toggle completion status
- Display confirmation

### 6. Exit
- Graceful shutdown
- Optional: Display summary before exit

## Common Patterns

### Menu Display
```python
def display_menu():
    print("\n=== Todo Application ===")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Mark Complete/Incomplete")
    print("6. Exit")
```

### Input Validation
```python
def get_valid_id(prompt: str) -> int:
    while True:
        try:
            task_id = int(input(prompt))
            return task_id
        except ValueError:
            print("Error: Please enter a valid number")
```

### Task Display
```python
def display_task(task: Task):
    status = "✓" if task.completed else "○"
    print(f"[{status}] ID: {task.id} | {task.title}")
    if task.description:
        print(f"    Description: {task.description}")
```

## Next Steps After Phase I

Once Phase I is complete:
1. Create GitHub repository
2. Push code with all specs
3. Create README.md with setup instructions
4. Test thoroughly
5. Prepare for Phase II (Full-Stack Web App)

## Questions to Ask

When implementing, consider:
- Does this match the specification?
- Is the code clean and readable?
- Are errors handled gracefully?
- Is the user experience intuitive?
- Are all acceptance criteria met?

## Resources

- **Specifications**: `.kiro/specs/phase1-console-app/`
- **Constitution**: `CONSTITUTION.md`
- **Hackathon Guide**: `Hackathon II - Todo Spec-Driven Development.md`
