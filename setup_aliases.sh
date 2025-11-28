#!/bin/bash
################################################################################
# Quick Setup Script for Python Path Aliases
# 
# This script automates the setup of path aliases in your Python project
# to enable clean imports like TypeScript.
################################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print colored messages
print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_header() {
    echo ""
    echo "======================================================================"
    echo "$1"
    echo "======================================================================"
    echo ""
}

# Check if we're in a Python project
check_project() {
    if [ ! -d "src" ]; then
        print_error "No 'src' directory found. Are you in the project root?"
        exit 1
    fi
    print_success "Found src directory"
}

# Create pyproject.toml if it doesn't exist
setup_pyproject() {
    print_header "Setting up pyproject.toml"
    
    if [ -f "pyproject.toml" ]; then
        print_warning "pyproject.toml already exists"
        read -p "Do you want to backup and replace it? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            cp pyproject.toml pyproject.toml.backup
            print_success "Backed up to pyproject.toml.backup"
        else
            print_info "Skipping pyproject.toml creation"
            return
        fi
    fi
    
    print_info "Creating pyproject.toml..."
    
    cat > pyproject.toml << 'EOF'
[build-system]
requires = ["setuptools>=68.0.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "modular-monolith"
version = "1.0.0"
description = "A modular monolith application"
requires-python = ">=3.10"

dependencies = [
    "fastapi>=0.104.0",
    "uvicorn[standard]>=0.24.0",
    "sqlalchemy>=2.0.0",
    "asyncpg>=0.29.0",
    "pydantic>=2.0.0",
    "pydantic-settings>=2.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-asyncio>=0.21.0",
    "black>=23.0.0",
    "ruff>=0.1.0",
]

[tool.setuptools.packages.find]
where = ["src"]

[tool.setuptools.package-dir]
"" = "src"

[tool.black]
line-length = 100
target-version = ["py310", "py311"]

[tool.ruff]
line-length = 100
target-version = "py310"

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]
EOF

    print_success "Created pyproject.toml"
}

# Create setup.py
setup_setup_py() {
    print_header "Setting up setup.py"
    
    if [ -f "setup.py" ]; then
        print_warning "setup.py already exists, skipping"
        return
    fi
    
    print_info "Creating setup.py..."
    
    cat > setup.py << 'EOF'
"""
Setup file for package.
Configuration is in pyproject.toml.
"""
from setuptools import setup

setup()
EOF

    print_success "Created setup.py"
}

# Create VSCode settings
setup_vscode() {
    print_header "Setting up VSCode configuration"
    
    if [ ! -d ".vscode" ]; then
        mkdir .vscode
        print_success "Created .vscode directory"
    fi
    
    if [ -f ".vscode/settings.json" ]; then
        print_warning ".vscode/settings.json already exists"
        read -p "Do you want to backup and replace it? (y/n) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_info "Skipping VSCode settings"
            return
        fi
        cp .vscode/settings.json .vscode/settings.json.backup
        print_success "Backed up to .vscode/settings.json.backup"
    fi
    
    print_info "Creating .vscode/settings.json..."
    
    cat > .vscode/settings.json << 'EOF'
{
  "python.analysis.extraPaths": [
    "${workspaceFolder}/src"
  ],
  "python.autoComplete.extraPaths": [
    "${workspaceFolder}/src"
  ],
  "python.formatting.provider": "black",
  "editor.formatOnSave": true,
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter",
    "editor.codeActionsOnSave": {
      "source.organizeImports": true
    }
  },
  "terminal.integrated.env.linux": {
    "PYTHONPATH": "${workspaceFolder}/src"
  }
}
EOF

    print_success "Created .vscode/settings.json"
}

# Install package in editable mode
install_package() {
    print_header "Installing package in editable mode"
    
    print_info "Running: pip install -e ."
    
    if pip install -e . ; then
        print_success "Package installed successfully"
    else
        print_error "Failed to install package"
        print_info "You may need to activate your virtual environment first"
        exit 1
    fi
}

# Test imports
test_imports() {
    print_header "Testing imports"
    
    print_info "Testing if imports work..."
    
    python3 << 'EOF'
import sys
try:
    # Try to import from modules (without src prefix)
    sys.path.insert(0, 'src')
    
    # Check if we can import
    import modules
    print("✓ Import test passed")
except ImportError as e:
    print(f"✗ Import test failed: {e}")
    sys.exit(1)
EOF

    if [ $? -eq 0 ]; then
        print_success "Import test passed"
    else
        print_warning "Import test failed, but this is OK if you haven't created modules yet"
    fi
}

# Print next steps
print_next_steps() {
    print_header "Setup Complete!"
    
    echo "Your project is now configured for clean imports."
    echo ""
    echo "Next steps:"
    echo ""
    echo "1. Update your imports:"
    echo "   Before: from src.modules.user.models import User"
    echo "   After:  from modules.user.models import User"
    echo ""
    echo "2. You can use the migration script to update all imports automatically:"
    echo "   python3 migrate_imports.py --dry-run"
    echo "   python3 migrate_imports.py"
    echo ""
    echo "3. Reload your IDE/editor for changes to take effect"
    echo ""
    echo "4. Test your application:"
    echo "   python3 main.py"
    echo ""
    print_success "All done! 🎉"
}

# Main execution
main() {
    print_header "Python Path Aliases Setup"
    
    print_info "This script will setup your project for clean imports"
    print_info "similar to TypeScript path mapping"
    echo ""
    
    read -p "Continue? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_info "Setup cancelled"
        exit 0
    fi
    
    # Run setup steps
    check_project
    setup_pyproject
    setup_setup_py
    setup_vscode
    install_package
    test_imports
    print_next_steps
}

# Run main
main