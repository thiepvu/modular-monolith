#!/bin/bash
# Quick Setup Helper Script

echo "Setting up Modular Monolith Project..."

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

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
