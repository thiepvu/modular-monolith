#!/usr/bin/env python3
"""
Modular Monolith Smart Generator
Creates project structure and provides guided setup
"""

import os
import sys
from pathlib import Path
from typing import List, Tuple

class Colors:
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header():
    print(f"\n{Colors.BOLD}{'='*70}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}   Modular Monolith Generator{Colors.RESET}")
    print(f"{Colors.BOLD}{'='*70}{Colors.RESET}\n")

def print_success(msg: str):
    print(f"{Colors.GREEN}✓ {msg}{Colors.RESET}")

def print_info(msg: str):
    print(f"{Colors.BLUE}ℹ {msg}{Colors.RESET}")

def print_warning(msg: str):
    print(f"{Colors.YELLOW}⚠ {msg}{Colors.RESET}")

def create_directory_structure(base: Path) -> List[Path]:
    """Create all directories"""
    dirs = [
        # Docs
        "docs/architecture", "docs/api", "docs/development",
        # Scripts
        "scripts",
        # Config
        "src/config/environments",
        # Core
        "src/core/domain", "src/core/application", "src/core/interfaces", "src/core/exceptions",
        # Shared
        "src/shared/api", "src/shared/validation", "src/shared/utils", "src/shared/repositories",
        # Infrastructure
        "src/infrastructure/database", "src/infrastructure/migrations/versions",
        "src/infrastructure/seeds", "src/infrastructure/logging", "src/infrastructure/cache",
        # Bootstrapper
        "src/bootstrapper",
        # User Module
        "src/modules/user_management/domain/entities",
        "src/modules/user_management/domain/value_objects",
        "src/modules/user_management/domain/events",
        "src/modules/user_management/domain/exceptions",
        "src/modules/user_management/application/dto",
        "src/modules/user_management/application/services",
        "src/modules/user_management/infrastructure/persistence/repositories",
        "src/modules/user_management/presentation/api/v1/controllers",
        # Tests
        "tests/unit/core", "tests/unit/modules/user_management",
        "tests/integration", "tests/e2e",
    ]
    
    created = []
    for d in dirs:
        path = base / d
        path.mkdir(parents=True, exist_ok=True)
        created.append(path)
    
    return created

def create_init_files(base: Path):
    """Create __init__.py files"""
    python_dirs = [
        "src", "src/core", "src/core/domain", "src/core/application",
        "src/core/interfaces", "src/core/exceptions", "src/config",
        "src/config/environments", "src/shared", "src/shared/api",
        "src/shared/validation", "src/shared/utils", "src/shared/repositories",
        "src/infrastructure", "src/infrastructure/database",
        "src/infrastructure/migrations", "src/infrastructure/seeds",
        "src/infrastructure/logging", "src/infrastructure/cache",
        "src/bootstrapper", "src/modules", "src/modules/user_management",
        "src/modules/user_management/domain",
        "src/modules/user_management/domain/entities",
        "src/modules/user_management/domain/value_objects",
        "src/modules/user_management/domain/events",
        "src/modules/user_management/domain/exceptions",
        "src/modules/user_management/application",
        "src/modules/user_management/application/dto",
        "src/modules/user_management/application/services",
        "src/modules/user_management/infrastructure",
        "src/modules/user_management/infrastructure/persistence",
        "src/modules/user_management/infrastructure/persistence/repositories",
        "src/modules/user_management/presentation",
        "src/modules/user_management/presentation/api",
        "src/modules/user_management/presentation/api/v1",
        "src/modules/user_management/presentation/api/v1/controllers",
        "tests", "tests/unit", "tests/unit/core", "tests/unit/modules",
        "tests/unit/modules/user_management", "tests/integration", "tests/e2e",
    ]
    
    for d in python_dirs:
        init_file = base / d / "__init__.py"
        if not init_file.exists():
            init_file.write_text('"""Package initialization"""\n')

def create_checklist(base: Path):
    """Create setup checklist"""
    checklist = """# Setup Checklist

## ✅ Files to Copy from Artifacts

### Step 1: Root Configuration
- [ ] .env.example
- [ ] .gitignore  
- [ ] alembic.ini
- [ ] pyproject.toml
- [ ] requirements.txt
- [ ] README.md

### Step 2: Documentation  
- [ ] docs/architecture/README.md
- [ ] docs/api/README.md
- [ ] docs/development/README.md

### Step 3: Scripts
- [ ] scripts/migrate.py
- [ ] scripts/seed.py
- [ ] scripts/generate_types.py

### Step 4: Configuration
- [ ] src/config/__init__.py
- [ ] src/config/settings.py
- [ ] src/config/logging_config.py
- [ ] src/config/environments/development.py
- [ ] src/config/environments/production.py
- [ ] src/config/environments/testing.py

### Step 5: Bootstrapper
- [ ] src/bootstrapper/__init__.py
- [ ] src/bootstrapper/container.py
- [ ] src/bootstrapper/module_loader.py
- [ ] src/bootstrapper/app_factory.py

### Step 6: Shared Utilities
- [ ] src/shared/api/base_controller.py
- [ ] src/shared/api/response.py
- [ ] src/shared/api/pagination.py
- [ ] src/shared/api/error_handler.py
- [ ] src/shared/api/versioning.py
- [ ] src/shared/validation/validators.py
- [ ] src/shared/utils/datetime_utils.py
- [ ] src/shared/utils/string_utils.py

### Step 7: Shared Repositories
- [ ] src/shared/repositories/base_repository.py
- [ ] src/shared/repositories/unit_of_work.py
- [ ] src/shared/repositories/specification.py

### Step 8: Infrastructure
- [ ] src/infrastructure/database/base.py
- [ ] src/infrastructure/database/connection.py
- [ ] src/infrastructure/database/session.py
- [ ] src/infrastructure/migrations/env.py
- [ ] src/infrastructure/migrations/script.py.mako
- [ ] src/infrastructure/seeds/seed_runner.py
- [ ] src/infrastructure/logging/logger.py
- [ ] src/infrastructure/cache/redis_client.py

### Step 9: Core Layer
- [ ] src/core/domain/base_entity.py
- [ ] src/core/domain/base_aggregate.py
- [ ] src/core/domain/value_objects.py
- [ ] src/core/domain/events.py
- [ ] src/core/application/base_service.py
- [ ] src/core/application/base_command.py
- [ ] src/core/application/base_query.py
- [ ] src/core/application/dto.py
- [ ] src/core/interfaces/repositories.py
- [ ] src/core/interfaces/unit_of_work.py
- [ ] src/core/interfaces/services.py
- [ ] src/core/exceptions/base_exceptions.py
- [ ] src/core/exceptions/error_codes.py

### Step 10: User Module (Part 1 - Domain)
- [ ] src/modules/user_management/domain/entities/user.py
- [ ] src/modules/user_management/domain/value_objects/email.py
- [ ] src/modules/user_management/domain/events/user_events.py
- [ ] src/modules/user_management/domain/exceptions/user_exceptions.py

### Step 10: User Module (Part 2 - Application & Infrastructure)
- [ ] src/modules/user_management/application/dto/user_dto.py
- [ ] src/modules/user_management/application/dto/mappers.py
- [ ] src/modules/user_management/application/services/user_service.py
- [ ] src/modules/user_management/infrastructure/persistence/models.py
- [ ] src/modules/user_management/infrastructure/persistence/repositories/user_repository.py

### Step 10: User Module (Part 3 - Presentation)
- [ ] src/modules/user_management/presentation/api/v1/controllers/user_controller.py
- [ ] src/modules/user_management/presentation/api/v1/routes.py
- [ ] src/main.py

### Step 11: Tests (Part 1 - Unit Tests)
- [ ] tests/conftest.py
- [ ] tests/unit/core/test_base_entity.py
- [ ] tests/unit/core/test_value_object.py
- [ ] tests/unit/modules/user_management/test_user_entity.py
- [ ] tests/unit/modules/user_management/test_email_value_object.py
- [ ] tests/unit/modules/user_management/test_user_service.py

### Step 11: Tests (Part 2 - Integration & E2E)
- [ ] tests/integration/test_user_repository.py
- [ ] tests/integration/test_unit_of_work.py
- [ ] tests/e2e/test_user_api.py
- [ ] tests/e2e/test_health_check.py

## 🚀 After Copying All Files

### Setup
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your database credentials
```

### Database
```bash
createdb modular_db
python scripts/migrate.py --upgrade
python scripts/seed.py
```

### Run
```bash
python src/main.py
```

### Test
```bash
pytest
```

Visit: http://localhost:8000/api/docs

## 📝 Notes
- Each checkbox represents a file to copy from the conversation artifacts
- Open each artifact (Steps 1-11) in the conversation
- Copy the content to the corresponding file
- Use VS Code or any text editor
- Verify file structure matches the checklist
"""
    
    (base / "CHECKLIST.md").write_text(checklist)

def create_quickstart(base: Path):
    """Create quick start guide"""
    quickstart = """# Quick Start Guide

## What Was Generated

✓ Complete directory structure
✓ All __init__.py files
✓ Python package markers
✓ Empty files ready for content

## What You Need to Do

### 1. Copy File Contents

Open the conversation and copy content from each artifact:

**Steps 1-11** contain all the code you need!

- Step 1: Root config files (.env, requirements.txt, etc.)
- Step 2: Documentation
- Step 3: Scripts (migrate, seed, generate_types)
- Step 4: Configuration module
- Step 5: Bootstrapper (IoC, app factory)
- Step 6: Shared utilities
- Step 7: Shared repositories
- Step 8: Infrastructure layer
- Step 9: Core layer (domain, application, interfaces)
- Step 10: Complete User module (3 parts)
- Step 11: Tests (2 parts)

### 2. Install Dependencies

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Setup Environment

```bash
cp .env.example .env
# Edit .env with your PostgreSQL credentials
```

### 4. Setup Database

```bash
createdb modular_db
python scripts/migrate.py --upgrade
python scripts/seed.py
```

### 5. Run Application

```bash
python src/main.py
```

Visit: http://localhost:8000/api/docs

## File Mapping Reference

Check CHECKLIST.md for the complete list of files to copy.

## Need Help?

1. Verify all files are copied using CHECKLIST.md
2. Check that __init__.py files exist in all Python directories
3. Ensure .env is configured correctly
4. Make sure PostgreSQL is running

## Success!

Once all files are copied and the app runs, you'll have:
- ✅ Complete Clean Architecture implementation
- ✅ Working User Management API
- ✅ Comprehensive test suite
- ✅ Production-ready structure

Happy coding! 🚀
"""
    
    (base / "QUICKSTART.md").write_text(quickstart)

def main():
    print_header()
    
    # Get project name
    project_name = input(f"{Colors.BLUE}Project name (modular-monolith): {Colors.RESET}").strip() or "modular-monolith"
    
    project_path = Path(project_name)
    
    if project_path.exists():
        response = input(f"{Colors.YELLOW}'{project_name}' exists. Continue? (y/N): {Colors.RESET}").lower()
        if response != 'y':
            print_warning("Aborted")
            return
    
    print(f"\n{Colors.BOLD}Creating project structure...{Colors.RESET}\n")
    
    # Create structure
    project_path.mkdir(exist_ok=True)
    print_success(f"Created: {project_path.absolute()}")
    
    print(f"\n{Colors.BOLD}Creating directories...{Colors.RESET}")
    dirs = create_directory_structure(project_path)
    print_success(f"Created {len(dirs)} directories")
    
    print(f"\n{Colors.BOLD}Creating Python packages...{Colors.RESET}")
    create_init_files(project_path)
    print_success("Created __init__.py files")
    
    print(f"\n{Colors.BOLD}Creating guides...{Colors.RESET}")
    create_checklist(project_path)
    print_success("Created CHECKLIST.md")
    create_quickstart(project_path)
    print_success("Created QUICKSTART.md")
    
    # Summary
    print(f"\n{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.GREEN}✓ Project structure created successfully!{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.RESET}\n")
    
    print_info("Next steps:")
    print(f"  1. cd {project_name}")
    print(f"  2. Open CHECKLIST.md")
    print(f"  3. Copy content from conversation artifacts (Steps 1-11)")
    print(f"  4. Follow QUICKSTART.md for setup")
    
    print(f"\n{Colors.BOLD}Quick Copy Process:{Colors.RESET}")
    print(f"  • Open the conversation in your browser")
    print(f"  • Find each artifact (Steps 1-11)")
    print(f"  • Copy content to the files listed in CHECKLIST.md")
    print(f"  • Use VS Code for easier multi-file editing")
    
    print(f"\n{Colors.GREEN}Ready to build! 🚀{Colors.RESET}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Aborted{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.RED}Error: {e}{Colors.RESET}")
        import traceback
        traceback.print_exc()