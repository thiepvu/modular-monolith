# project_files.py
"""
All project file contents
Due to size, this will need to be split or you can use the artifacts directly
"""

# This is a template showing the structure
# You'll need to copy content from each artifact (Steps 1-11)

FILES = {
    # ==================== ROOT FILES (Step 1) ====================
    ".env.example": """APP_NAME=Modular Monolith API
APP_VERSION=1.0.0
DEBUG=True
TESTING=False
ENVIRONMENT=development

DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/modular_db
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20

API_V1_PREFIX=/api/v1
API_V2_PREFIX=/api/v2

CORS_ORIGINS=["http://localhost:3000"]

LOG_LEVEL=INFO
LOG_FORMAT=json

SECRET_KEY=change-this-in-production
""",

    ".gitignore": """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
dist/
*.egg-info/
.venv
venv/
ENV/

# IDE
.idea/
.vscode/
*.swp

# Environment
.env

# Database
*.db
*.sqlite

# Logs
*.log

# Testing
.pytest_cache/
.coverage
htmlcov/
""",

    "requirements.txt": """fastapi==0.109.0
uvicorn[standard]==0.27.0
pydantic==2.5.3
pydantic-settings==2.1.0
sqlalchemy==2.0.25
asyncpg==0.29.0
alembic==1.13.1
psycopg2-binary==2.9.9
email-validator==2.1.0
python-multipart==0.0.6
python-json-logger==2.0.7
pytest==7.4.4
pytest-asyncio==0.23.3
pytest-cov==4.1.0
httpx==0.26.0
""",

    "README.md": """# Modular Monolith with Clean Architecture

Production-ready FastAPI application with Clean Architecture and DDD.

## Quick Start

```bash
# Setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env

# Database
createdb modular_db
python scripts/migrate.py --upgrade
python scripts/seed.py

# Run
python src/main.py
```

Visit: http://localhost:8000/api/docs

## Documentation

See `docs/` for detailed documentation.
""",

    # ==================== IMPORTANT NOTE ====================
    # Due to character limits, I cannot include all 100+ files here.
    # Please use the following approach:
    
    # RECOMMENDED APPROACH:
    # Run the generator script which will create the structure,
    # then copy content from artifacts (Steps 1-11) to each file.
    
    # The generator creates all directories and empty files.
    # You then fill them with content from the conversation artifacts.
}

# To use this:
# 1. Save both generate_project.py and project_files.py
# 2. Run: python generate_project.py
# 3. Copy content from artifacts to fill in the files
# 4. Or manually add all file contents to this FILES dict