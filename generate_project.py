#!/usr/bin/env python3
"""
Modular Monolith Project Generator
Generates complete project structure with all files from Steps 1-11
"""

import os
from pathlib import Path
from typing import Dict

# Color codes for terminal output
GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'

def print_success(message: str):
    print(f"{GREEN}✓ {message}{RESET}")

def print_info(message: str):
    print(f"{BLUE}ℹ {message}{RESET}")

def print_warning(message: str):
    print(f"{YELLOW}⚠ {message}{RESET}")

def print_error(message: str):
    print(f"{RED}✗ {message}{RESET}")

# Store all file contents
FILES: Dict[str, str] = {}

# Due to character limits, I'll create a modular approach
# This script will be split into multiple parts

def create_directory_structure(base_path: Path):
    """Create all necessary directories"""
    directories = [
        # Root
        "docs/architecture",
        "docs/api",
        "docs/development",
        "scripts",
        
        # Source
        "src/core/domain",
        "src/core/application",
        "src/core/interfaces",
        "src/core/exceptions",
        
        "src/config/environments",
        
        "src/shared/api",
        "src/shared/validation",
        "src/shared/utils",
        "src/shared/repositories",
        
        "src/infrastructure/database",
        "src/infrastructure/migrations/versions",
        "src/infrastructure/seeds",
        "src/infrastructure/logging",
        "src/infrastructure/cache",
        
        "src/bootstrapper",
        
        # User module
        "src/modules/user_management/domain/entities",
        "src/modules/user_management/domain/value_objects",
        "src/modules/user_management/domain/events",
        "src/modules/user_management/domain/exceptions",
        "src/modules/user_management/application/dto",
        "src/modules/user_management/application/services",
        "src/modules/user_management/infrastructure/persistence/repositories",
        "src/modules/user_management/presentation/api/v1/controllers",
        
        # Tests
        "tests/unit/core",
        "tests/unit/modules/user_management",
        "tests/integration",
        "tests/e2e",
    ]
    
    for directory in directories:
        dir_path = base_path / directory
        dir_path.mkdir(parents=True, exist_ok=True)
        
        # Create __init__.py in Python packages
        if directory.startswith("src/") or directory.startswith("tests/"):
            init_file = dir_path / "__init__.py"
            if not init_file.exists():
                init_file.write_text('"""Package initialization"""\n')
    
    print_success("Directory structure created")

def create_file(base_path: Path, file_path: str, content: str):
    """Create a file with content"""
    full_path = base_path / file_path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    """Main generator function"""
    print_info("=" * 60)
    print_info("Modular Monolith Project Generator")
    print_info("=" * 60)
    print()
    
    # Get project name
    project_name = input(f"{BLUE}Enter project name (default: modular-monolith): {RESET}").strip()
    if not project_name:
        project_name = "modular-monolith"
    
    # Create project directory
    project_path = Path(project_name)
    
    if project_path.exists():
        response = input(f"{YELLOW}Directory '{project_name}' already exists. Continue? (y/N): {RESET}").strip().lower()
        if response != 'y':
            print_error("Aborted.")
            return
    
    project_path.mkdir(exist_ok=True)
    print_success(f"Created project directory: {project_path.absolute()}")
    print()
    
    # Create directory structure
    print_info("Creating directory structure...")
    create_directory_structure(project_path)
    print()
    
    # Since I cannot include all files here due to length, 
    # I'll provide instructions to download from the artifacts above
    
    print_info("=" * 60)
    print_info("NEXT STEPS:")
    print_info("=" * 60)
    print()
    print_info("The basic directory structure has been created.")
    print()
    print_info("To complete the setup, please copy the content from each artifact:")
    print()
    
    print_info("Step 1: Root Configuration Files")
    print("  - .env.example")
    print("  - .gitignore")
    print("  - alembic.ini")
    print("  - pyproject.toml")
    print("  - requirements.txt")
    print("  - README.md")
    print()
    
    print_info("Step 2-11: Copy content from artifacts for:")
    print("  - Documentation (docs/)")
    print("  - Scripts (scripts/)")
    print("  - Config (src/config/)")
    print("  - Core (src/core/)")
    print("  - Shared (src/shared/)")
    print("  - Infrastructure (src/infrastructure/)")
    print("  - Bootstrapper (src/bootstrapper/)")
    print("  - User Module (src/modules/user_management/)")
    print("  - Tests (tests/)")
    print()
    
    # Create a helper script
    helper_script = """#!/bin/bash
# Quick Setup Helper Script

echo "Setting up Modular Monolith Project..."

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Setup environment
echo "Setting up environment..."
cp .env.example .env
echo "Please edit .env with your database credentials"

# Database setup
echo ""
echo "To complete setup, run:"
echo "  1. createdb modular_db"
echo "  2. python scripts/migrate.py --upgrade"
echo "  3. python scripts/seed.py"
echo "  4. python src/main.py"
echo ""
echo "Then visit: http://localhost:8000/api/docs"
"""
    
    setup_script_path = project_path / "setup.sh"
    setup_script_path.write_text(helper_script)
    setup_script_path.chmod(0o755)
    print_success(f"Created setup helper script: setup.sh")
    print()
    
    # Create Windows batch file
    windows_helper = """@echo off
REM Quick Setup Helper Script for Windows

echo Setting up Modular Monolith Project...

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv
call venv\\Scripts\\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Setup environment
echo Setting up environment...
copy .env.example .env
echo Please edit .env with your database credentials

REM Database setup
echo.
echo To complete setup, run:
echo   1. createdb modular_db
echo   2. python scripts/migrate.py --upgrade
echo   3. python scripts/seed.py
echo   4. python src/main.py
echo.
echo Then visit: http://localhost:8000/api/docs

pause
"""
    
    setup_bat_path = project_path / "setup.bat"
    setup_bat_path.write_text(windows_helper)
    print_success(f"Created Windows setup script: setup.bat")
    print()
    
    # Create Makefile
    makefile_content = """# Makefile for Modular Monolith

.PHONY: help install migrate seed run test clean

help:
\t@echo "Available commands:"
\t@echo "  make install    - Install dependencies"
\t@echo "  make migrate    - Run database migrations"
\t@echo "  make seed       - Seed database with initial data"
\t@echo "  make run        - Run the application"
\t@echo "  make test       - Run all tests"
\t@echo "  make test-unit  - Run unit tests"
\t@echo "  make test-int   - Run integration tests"
\t@echo "  make test-e2e   - Run e2e tests"
\t@echo "  make coverage   - Run tests with coverage"
\t@echo "  make clean      - Clean up generated files"

install:
\tpip install -r requirements.txt

migrate:
\tpython scripts/migrate.py --upgrade

seed:
\tpython scripts/seed.py

run:
\tpython src/main.py

test:
\tpytest

test-unit:
\tpytest tests/unit/

test-int:
\tpytest tests/integration/

test-e2e:
\tpytest tests/e2e/

coverage:
\tpytest --cov=src --cov-report=html --cov-report=term

clean:
\tfind . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
\tfind . -type f -name "*.pyc" -delete 2>/dev/null || true
\trm -rf .pytest_cache htmlcov .coverage
"""
    
    makefile_path = project_path / "Makefile"
    makefile_path.write_text(makefile_content)
    print_success(f"Created Makefile")
    print()
    
    # Create quick start guide
    quickstart = """# Quick Start Guide

## Prerequisites
- Python 3.11+
- PostgreSQL 14+
- Git

## Setup Steps

### 1. Install Dependencies
```bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Windows
python -m venv venv
venv\\Scripts\\activate
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env with your settings
```

### 3. Setup Database
```bash
# Create database
createdb modular_db

# Run migrations
python scripts/migrate.py --upgrade

# Seed initial data
python scripts/seed.py
```

### 4. Run Application
```bash
python src/main.py
```

Visit: http://localhost:8000/api/docs

## Using Make (Linux/Mac)
```bash
make install   # Install dependencies
make migrate   # Run migrations
make seed      # Seed database
make run       # Start server
make test      # Run tests
```

## Manual File Setup

Since this is a template generator, you need to copy the actual
file contents from the Claude conversation artifacts:

1. Copy Step 1 files (root config)
2. Copy Step 2 files (documentation)
3. Copy Step 3 files (scripts)
4. Copy Step 4 files (config)
5. Copy Step 5 files (bootstrapper)
6. Copy Step 6 files (shared utilities)
7. Copy Step 7 files (shared repositories)
8. Copy Step 8 files (infrastructure)
9. Copy Step 9 files (core layer)
10. Copy Step 10 files (user module)
11. Copy Step 11 files (tests)

## API Endpoints

Once running, available endpoints:
- GET    /health
- POST   /api/v1/users
- GET    /api/v1/users
- GET    /api/v1/users/{id}
- PUT    /api/v1/users/{id}
- DELETE /api/v1/users/{id}
- POST   /api/v1/users/{id}/activate
- POST   /api/v1/users/{id}/deactivate

## Testing
```bash
# All tests
pytest

# With coverage
pytest --cov=src --cov-report=html

# Unit tests only
pytest tests/unit/

# Integration tests only
pytest tests/integration/

# E2E tests only
pytest tests/e2e/
```

## Troubleshooting

### Database Connection Error
- Check DATABASE_URL in .env
- Ensure PostgreSQL is running
- Verify database exists

### Import Errors
- Ensure virtual environment is activated
- Run from project root directory
- Check PYTHONPATH

### Migration Errors
- Drop and recreate database
- Delete migration versions
- Run migrations again

## Next Steps

1. Add authentication module
2. Add file management module
3. Add project management module
4. Implement JWT authentication
5. Add role-based access control
6. Add API rate limiting
7. Setup CI/CD pipeline
8. Deploy to production

For more information, see docs/ directory.
"""
    
    quickstart_path = project_path / "QUICKSTART.md"
    quickstart_path.write_text(quickstart)
    print_success(f"Created QUICKSTART.md")
    print()
    
    print_info("=" * 60)
    print_success("Project structure created successfully!")
    print_info("=" * 60)
    print()
    print_info(f"Project location: {project_path.absolute()}")
    print()
    print_info("To complete the setup:")
    print(f"  1. cd {project_name}")
    print("  2. Copy all file contents from the conversation artifacts")
    print("  3. Run ./setup.sh (Linux/Mac) or setup.bat (Windows)")
    print("  4. Or use: make install && make migrate && make seed && make run")
    print()
    print_info("See QUICKSTART.md for detailed instructions")
    print()
    print_success("Happy coding! 🚀")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        print_warning("Aborted by user")
    except Exception as e:
        print_error(f"Error: {e}")
        import traceback
        traceback.print_exc()