"""Development environment specific settings"""

from ..settings import Settings


class DevelopmentSettings(Settings):
    """Development environment settings"""
    
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    DB_ECHO: bool = True
    LOG_LEVEL: str = "DEBUG"
    
    # Override for local development
    CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:8080",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8080"
    ]