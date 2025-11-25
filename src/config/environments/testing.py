"""Testing environment specific settings"""

from ..settings import Settings


class TestingSettings(Settings):
    """Testing environment settings"""
    
    DEBUG: bool = True
    TESTING: bool = True
    ENVIRONMENT: str = "testing"
    DB_ECHO: bool = False
    LOG_LEVEL: str = "WARNING"
    
    # Use test database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/modular_test_db"
    
    # Disable external services in tests
    REDIS_HOST: str = "localhost"