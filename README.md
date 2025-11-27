# Modular Monolith with Clean Architecture

A production-ready FastAPI application implementing Clean Architecture principles with Domain-Driven Design (DDD) in a modular monolith structure.

## 🏗️ Architecture

This project follows **Clean Architecture** with clear separation of concerns:

- **Domain Layer**: Pure business logic (entities, value objects, domain events)
- **Application Layer**: Use cases, DTOs, services
- **Infrastructure Layer**: Database, external services, ORM
- **Presentation Layer**: API controllers, routes, schemas

### Bounded Contexts (Modules)

- User Management
- File Management
- Project Management
- Notification System

## ✨ Features

- ✅ Clean Architecture with DDD
- ✅ Modular Monolith structure
- ✅ Async/Await throughout
- ✅ PostgreSQL with SQLAlchemy
- ✅ Automatic module discovery
- ✅ OpenAPI documentation
- ✅ Type safety with Pydantic
- ✅ Repository pattern
- ✅ Unit of Work pattern
- ✅ Domain events
- ✅ Soft deletes
- ✅ Pagination
- ✅ Error handling
- ✅ Logging (JSON format)
- ✅ API versioning
- ✅ IoC Container

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 14+
- Redis (optional)

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd modular-monolith

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Or with poetry
poetry install

# Copy environment file
cp .env.example .env

# Edit .env with your configuration
nano .env
```

### Database Setup

```bash
# Create database
docker compose -f docker-compose.postgresql.yml up --build -d

# Create migrations
python3 scripts/migrate.py --create "init"

# Run migrations
python3 scripts/migrate.py --upgrade

# Seed initial data
python3 scripts/seed.py
```

### Running the Application

```bash
# Development mode
python3 src/main.py

# Or Run with Python module
python3 -m src.main

# Or with uvicorn
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Access the Application

- **API Documentation**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc
- **Health Check**: http://localhost:8000/health

## 📁 Project Structure

```
.
├── src/
│   ├── core/                  # Shared kernel
│   ├── modules/               # Bounded contexts
│   ├── infrastructure/        # Database, logging
│   ├── shared/                # Shared utilities
│   ├── bootstrapper/          # IoC, app factory
│   ├── config/                # Configuration
│   └── main.py               # Entry point
├── tests/                    # Tests
├── scripts/                  # Utility scripts
├── docs/                     # Documentation
└── alembic.ini              # Alembic config
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific module
pytest tests/unit/modules/user_management/

# Run integration tests
pytest tests/integration/
```

## 📚 Documentation

- [Architecture Guide](docs/architecture/README.md)
- [API Documentation](docs/api/README.md)
- [Development Guide](docs/development/README.md)

## 🛠️ Development

### Code Formatting

```bash
# Format code
black src tests

# Sort imports
isort src tests

# Type checking
mypy src
```

### Creating a New Module

See [Development Guide](docs/development/creating-modules.md) for detailed instructions.

### Database Migrations

```bash
# Create migration
python scripts/migrate.py --create "Description"

# Apply migrations
python scripts/migrate.py --upgrade

# Rollback
python scripts/migrate.py --downgrade -1
```

## 🔒 Security

- Change `SECRET_KEY` in production
- Use environment variables for sensitive data
- Enable HTTPS
- Implement authentication/authorization
- Keep dependencies updated

## 📊 API Standards

### Response Format

**Success:**
```json
{
  "success": true,
  "data": { ... },
  "message": "Success message",
  "timestamp": "2024-01-01T00:00:00"
}
```

**Error:**
```json
{
  "success": false,
  "error": {
    "code": "NOT_FOUND",
    "message": "Resource not found",
    "details": {}
  },
  "timestamp": "2024-01-01T00:00:00"
}
```

### Endpoints

- `GET /api/v1/resource` - List (paginated)
- `GET /api/v1/resource/{id}` - Get single
- `POST /api/v1/resource` - Create
- `PUT /api/v1/resource/{id}` - Update
- `DELETE /api/v1/resource/{id}` - Delete

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📝 License

MIT License - see LICENSE file for details

## 👥 Authors

- Your Name - Initial work

## 🙏 Acknowledgments

- FastAPI
- SQLAlchemy
- Clean Architecture by Robert C. Martin
- Domain-Driven Design by Eric Evans
