# Setup Guide - Phase I Todo Application

## Prerequisites

- Python 3.13 or higher
- UV package manager (optional but recommended)

## Installation Steps

### Step 1: Verify Python Version

```bash
python3 --version
# Should show Python 3.13.x or higher
```

### Step 2: Install UV (Optional)

UV is the recommended package manager for this project:

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Verify installation
uv --version
```

### Step 3: Set Up Virtual Environment

#### Using UV (Recommended):
```bash
# Create virtual environment
uv venv

# Activate virtual environment
# macOS/Linux:
source .venv/bin/activate

# Windows:
.venv\Scripts\activate
```

#### Using Standard Python:
```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
# macOS/Linux:
source .venv/bin/activate

# Windows:
.venv\Scripts\activate
```

### Step 4: Install the Package

```bash
# Using UV:
uv pip install -e .

# Using pip:
pip install -e .
```

## Running the Application

### Method 1: Using Python Module
```bash
python3 -m todo_app.main
```

### Method 2: Using Installed Script (after installation)
```bash
todo
```

### Method 3: Direct Execution
```bash
python3 src/todo_app/main.py
```

## Testing

### Run Comprehensive Tests
```bash
python3 test_todo_app.py
```

### Run Quick Import Test
```bash
python3 test_import.py
```

## Troubleshooting

### Issue: "No module named 'todo_app'"

**Solution**: Make sure you're in the project root directory and have installed the package:
```bash
pip install -e .
```

Or add the src directory to your Python path:
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
```

### Issue: "Python version too old"

**Solution**: Install Python 3.13 or higher:
```bash
# macOS (using Homebrew)
brew install python@3.13

# Ubuntu/Debian
sudo apt update
sudo apt install python3.13

# Windows
# Download from python.org
```

### Issue: UV not found

**Solution**: UV is optional. You can use standard pip instead:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Project Structure

```
evolution-of-todo/
├── .kiro/
│   └── specs/
│       └── phase1-console-app/
│           ├── requirements.md
│           ├── design.md
│           └── tasks.md
├── src/
│   └── todo_app/
│       ├── __init__.py
│       ├── main.py
│       ├── models.py
│       ├── storage.py
│       ├── operations.py
│       └── ui.py
├── pyproject.toml
├── README.md
├── CONSTITUTION.md
├── CLAUDE.md
├── SETUP.md (this file)
└── test_todo_app.py
```

## Next Steps

1. Run the tests to verify everything works
2. Try the application
3. Review the code and specifications
4. Prepare for GitHub submission

## Support

For issues or questions:
1. Check the specifications in `.kiro/specs/phase1-console-app/`
2. Review the CONSTITUTION.md for project principles
3. Check the CLAUDE.md for implementation guidelines
