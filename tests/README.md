# Testing Guide

## Test Structure

```
tests/
├── conftest.py              # Shared fixtures
├── unit/                    # Unit tests (no database)
│   ├── core/               # Core domain tests
│   └── modules/            # Module domain tests
├── integration/            # Integration tests (with database)
│   ├── test_user_repository.py
│   └── test_unit_of_work.py
└── e2e/                    # End-to-end tests (full API)
    ├── test_user_api.py
    └── test_health_check.py
```

## Running Tests

### All Tests
```bash
pytest
```

### Unit Tests Only
```bash
pytest tests/unit/
```

### Integration Tests Only
```bash
pytest tests/integration/
```

### E2E Tests Only
```bash
pytest tests/e2e/
```

### Specific Test File
```bash
pytest tests/unit/modules/user_management/test_user_entity.py
```

### Specific Test Function
```bash
pytest tests/unit/modules/user_management/test_user_entity.py::TestUserEntity::test_create_user
```

### With Coverage
```bash
pytest --cov=src --cov-report=html
```

### With Verbose Output
```bash
pytest -v
```

### With Output (print statements)
```bash
pytest -s
```

### Run Tests in Parallel
```bash
pytest -n auto
```

## Test Database Setup

### Create Test Database
```bash
createdb modular_test_db
```

### Run Migrations on Test Database
```bash
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/modular_test_db \
python scripts/migrate.py --upgrade
```

### Drop Test Database
```bash
dropdb modular_test_db
```

## Writing Tests

### Unit Test Example

```python
import pytest
from src.modules.user_management.domain.entities.user import User

def test_create_user():
    """Test user creation"""
    user = User.create(
        email="test@example.com",
        username="testuser",
        first_name="Test",
        last_name="User"
    )
    
    assert user.email.value == "test@example.com"
    assert user.is_active is True
```

### Integration Test Example

```python
import pytest

@pytest.mark.asyncio
async def test_add_user(db_session):
    """Test adding user to database"""
    from src.modules.user_management.infrastructure.persistence.repositories.user_repository import UserRepository
    from src.modules.user_management.domain.entities.user import User
    
    repository = UserRepository(db_session)
    user = User.create(
        email="test@example.com",
        username="testuser",
        first_name="Test",
        last_name="User"
    )
    
    saved_user = await repository.add(user)
    await db_session.commit()
    
    assert saved_user.id is not None
```

### E2E Test Example

```python
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_user_api(client: AsyncClient):
    """Test POST /api/v1/users"""
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "first_name": "Test",
        "last_name": "User"
    }
    
    response = await client.post("/api/v1/users", json=user_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
```

## Test Fixtures

### Database Session Fixture
```python
@pytest.fixture
async def db_session(engine):
    """Create database session for testing"""
    session_factory = async_sessionmaker(bind=engine, class_=AsyncSession)
    
    async with session_factory() as session:
        async with session.begin():
            yield session
            await session.rollback()
```

### HTTP Client Fixture
```python
@pytest.fixture
async def client(db_session):
    """Create test HTTP client"""
    app = create_app()
    
    async def override_get_db():
        yield db_session
    
    app.dependency_overrides[get_db_session] = override_get_db
    
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
```

## Mocking

### Mock Repository Example
```python
from unittest.mock import AsyncMock

@pytest.fixture
def mock_repository():
    """Create mock repository"""
    mock = AsyncMock()
    mock.get_by_id.return_value = User.create(...)
    return mock
```

### Using Mock in Test
```python
@pytest.mark.asyncio
async def test_with_mock(mock_repository):
    """Test with mocked repository"""
    service = UserService(mock_repository)
    
    result = await service.get_user(user_id)
    
    mock_repository.get_by_id.assert_called_once_with(user_id)
```

## Parametrized Tests

```python
@pytest.mark.parametrize("invalid_email", [
    "invalid",
    "invalid@",
    "@example.com",
    "invalid@.com",
])
def test_invalid_emails(invalid_email):
    """Test invalid email formats"""
    with pytest.raises(InvalidEmailException):
        Email(invalid_email)
```

## Test Coverage

### Generate Coverage Report
```bash
pytest --cov=src --cov-report=html
```

### View Coverage Report
```bash
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

### Coverage Configuration (pyproject.toml)
```toml
[tool.coverage.run]
source = ["src"]
omit = [
    "*/tests/*",
    "*/__pycache__/*",
    "*/venv/*",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
]
```

## Best Practices

### 1. Test Naming
- Use descriptive names: `test_create_user_with_invalid_email`
- Follow pattern: `test_<what>_<condition>_<expected_result>`

### 2. AAA Pattern
```python
def test_example():
    # Arrange - Setup test data
    user = User.create(...)
    
    # Act - Execute the code under test
    result = user.full_name
    
    # Assert - Verify the result
    assert result == "Test User"
```

### 3. One Assertion Per Test
```python
# Good
def test_user_email():
    user = User.create(email="test@example.com", ...)
    assert user.email.value == "test@example.com"

def test_user_is_active():
    user = User.create(...)
    assert user.is_active is True

# Avoid
def test_user_properties():
    user = User.create(...)
    assert user.email.value == "test@example.com"
    assert user.is_active is True
    assert user.full_name == "Test User"
```

### 4. Test Independence
- Each test should be independent
- Don't rely on order of execution
- Clean up after tests (fixtures handle this)

### 5. Use Fixtures
```python
@pytest.fixture
def sample_user():
    """Reusable test user"""
    return User.create(
        email="test@example.com",
        username="testuser",
        first_name="Test",
        last_name="User"
    )

def test_with_fixture(sample_user):
    assert sample_user.email.value == "test@example.com"
```

### 6. Test Edge Cases
- Empty inputs
- Null values
- Boundary conditions
- Invalid data
- Concurrent access

### 7. Don't Test Framework Code
- Don't test SQLAlchemy, FastAPI, etc.
- Test YOUR business logic

## Continuous Integration

### GitHub Actions Example
```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:14
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      
      - name: Run tests
        run: |
          pytest --cov=src --cov-report=xml
        env:
          DATABASE_URL: postgresql+asyncpg://postgres:postgres@localhost:5432/test_db
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

## Performance Testing

### Using pytest-benchmark
```python
def test_user_creation_performance(benchmark):
    """Test user creation performance"""
    
    def create_user():
        return User.create(
            email="perf@example.com",
            username="perfuser",
            first_name="Perf",
            last_name="User"
        )
    
    result = benchmark(create_user)
    assert result is not None
```

## Test Data Factories

### Using factory_boy
```python
import factory
from src.modules.user_management.domain.entities.user import User

class UserFactory(factory.Factory):
    class Meta:
        model = User
    
    email = factory.Sequence(lambda n: f"user{n}@example.com")
    username = factory.Sequence(lambda n: f"user{n}")
    first_name = "Test"
    last_name = "User"

# Usage
user = UserFactory()
```

## Common Issues

### 1. Async Test Not Running
```python
# Missing decorator
@pytest.mark.asyncio  # Add this!
async def test_async_function():
    result = await some_async_function()
    assert result is not None
```

### 2. Database Already Exists
```bash
# Drop and recreate
dropdb modular_test_db
createdb modular_test_db
```

### 3. Import Errors
```bash
# Make sure you're in project root
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### 4. Fixture Not Found
```python
# Make sure conftest.py is in correct location
# tests/conftest.py for global fixtures
# tests/unit/conftest.py for unit test fixtures
```

## Useful Commands

### Run Only Failed Tests
```bash
pytest --lf
```

### Run Tests Modified Since Last Commit
```bash
pytest --picked
```

### Show Test Duration
```bash
pytest --durations=10
```

### Stop on First Failure
```bash
pytest -x
```

### Run Tests Matching Pattern
```bash
pytest -k "user"  # Run tests with "user" in name
```

### Generate Test Report
```bash
pytest --html=report.html --self-contained-html
```

## Summary

✅ **Unit Tests**: Fast, no external dependencies
✅ **Integration Tests**: Test with real database
✅ **E2E Tests**: Test full API endpoints
✅ **Fixtures**: Reusable test setup
✅ **Mocking**: Isolate units under test
✅ **Coverage**: Ensure code is tested
✅ **CI/CD**: Automated testing pipeline