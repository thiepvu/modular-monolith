"""Production environment specific settings"""

from pydantic import field_validator
from config.settings import Settings


class ProductionSettings(Settings):
    """Production environment settings"""
    
    DEBUG: bool = False
    ENVIRONMENT: str = "production"
    DB_ECHO: bool = False
    LOG_LEVEL: str = "INFO"
    
    @field_validator("SECRET_KEY")
    @classmethod
    def validate_secret_key(cls, v: str) -> str:
        """Ensure secret key is not default in production"""
        if "change-this" in v.lower():
            raise ValueError("SECRET_KEY must be changed in production!")
        if len(v) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters long!")
        return v
    
    @field_validator("DATABASE_URL")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        """Ensure database URL is not localhost in production"""
        if "localhost" in v or "127.0.0.1" in v:
            raise ValueError("DATABASE_URL should not use localhost in production!")
        return v