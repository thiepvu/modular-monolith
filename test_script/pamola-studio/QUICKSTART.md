# Quick Start Guide

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
venv\Scripts\activate
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
