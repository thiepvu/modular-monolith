#!/usr/bin/env python3
"""
Complete Modular Monolith Project Generator
Generates ALL files from Steps 1-11 in one script
"""

import os
from pathlib import Path
from typing import Dict

# Terminal colors
class Colors:
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_step(step: int, message: str):
    print(f"\n{Colors.BOLD}{Colors.BLUE}Step {step}: {message}{Colors.RESET}")

def print_success(message: str):
    print(f"{Colors.GREEN}✓ {message}{Colors.RESET}")

def print_info(message: str):
    print(f"{Colors.BLUE}ℹ {message}{Colors.RESET}")

def print_warning(message: str):
    print(f"{Colors.YELLOW}⚠ {message}{Colors.RESET}")

def create_file(base_path: Path, file_path: str, content: str):
    """Create a file with content"""
    full_path = base_path / file_path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print_success(f"Created: {file_path}")

def generate_project():
    """Main generation function"""
    
    print(f"\n{Colors.BOLD}{'='*70}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}   Modular Monolith with Clean Architecture - Project Generator{Colors.RESET}")
    print(f"{Colors.BOLD}{'='*70}{Colors.RESET}\n")
    
    # Get project name
    project_name = input(f"{Colors.BLUE}Enter project name (default: modular-monolith): {Colors.RESET}").strip()
    if not project_name:
        project_name = "modular-monolith"
    
    project_path = Path(project_name)
    
    if project_path.exists():
        response = input(f"{Colors.YELLOW}Directory '{project_name}' exists. Continue? (y/N): {Colors.RESET}").lower()
        if response != 'y':
            print_warning("Aborted.")
            return
    
    project_path.mkdir(exist_ok=True)
    print_success(f"Project directory: {project_path.absolute()}\n")
    
    # Import file contents
    from project_files import FILES
    
    # Create all files
    total = len(FILES)
    for idx, (file_path, content) in enumerate(FILES.items(), 1):
        create_file(project_path, file_path, content)
        if idx % 10 == 0:
            print_info(f"Progress: {idx}/{total} files created...")
    
    # Create __init__.py files
    print_step(0, "Creating Python package markers")
    init_dirs = [
        "src", "src/core", "src/core/domain", "src/core/application", 
        "src/core/interfaces", "src/core/exceptions",
        "src/config", "src/config/environments",
        "src/shared", "src/shared/api", "src/shared/validation", 
        "src/shared/utils", "src/shared/repositories",
        "src/infrastructure", "src/infrastructure/database",
        "src/infrastructure/migrations", "src/infrastructure/seeds",
        "src/infrastructure/logging", "src/infrastructure/cache",
        "src/bootstrapper", "src/modules",
        "src/modules/user_management",
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
        "tests", "tests/unit", "tests/unit/core",
        "tests/unit/modules", "tests/unit/modules/user_management",
        "tests/integration", "tests/e2e",
    ]
    
    for dir_path in init_dirs:
        init_file = project_path / dir_path / "__init__.py"
        if not init_file.exists():
            init_file.parent.mkdir(parents=True, exist_ok=True)
            init_file.write_text('"""Package initialization"""\n')
    
    # Create migrations directory
    migrations_dir = project_path / "src/infrastructure/migrations/versions"
    migrations_dir.mkdir(parents=True, exist_ok=True)
    (migrations_dir / ".gitkeep").write_text("")
    
    print(f"\n{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.GREEN}✓ Project generated successfully!{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.RESET}\n")
    
    print_info("Next steps:")
    print(f"  1. cd {project_name}")
    print(f"  2. python -m venv venv")
    print(f"  3. source venv/bin/activate  # Windows: venv\\Scripts\\activate")
    print(f"  4. pip install -r requirements.txt")
    print(f"  5. cp .env.example .env")
    print(f"  6. # Edit .env with your database credentials")
    print(f"  7. createdb modular_db")
    print(f"  8. python scripts/migrate.py --upgrade")
    print(f"  9. python scripts/seed.py")
    print(f" 10. python src/main.py")
    print(f"\nThen visit: http://localhost:8000/api/docs")
    print(f"\n{Colors.GREEN}Happy coding! 🚀{Colors.RESET}\n")

if __name__ == "__main__":
    try:
        generate_project()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Aborted by user{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.RED}Error: {e}{Colors.RESET}")
        import traceback
        traceback.print_exc()