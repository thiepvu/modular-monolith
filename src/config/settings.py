"""
Application settings management.
Uses pydantic-settings for environment variable validation.
"""
from functools import lru_cache
from typing import List, Optional
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Application
    APP_NAME: str = Field(default="Modular Monolith API", description="Application name")
    APP_VERSION: str = Field(default="1.0.0", description="Application version")
    DEBUG: bool = Field(default=False, description="Debug mode")
    TESTING: bool = Field(default=False, description="Testing mode")
    ENVIRONMENT: str = Field(default="development", description="Environment name")
    
    # API Configuration
    API_V1_PREFIX: str = Field(default="/api/v1", description="API v1 prefix")
    API_V2_PREFIX: str = Field(default="/api/v2", description="API v2 prefix")
    
    # System
    SERVER_URL: Optional[str] = None

    # Database
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/modular_db",
        description="Database connection URL"
    )
    DB_POOL_SIZE: int = Field(default=10, ge=1, le=100, description="Database pool size")
    DB_MAX_OVERFLOW: int = Field(default=20, ge=0, le=100, description="Database max overflow")
    DB_ECHO: bool = Field(default=False, description="Echo SQL queries")
    
    # CORS
    CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:3000"],
        description="Allowed CORS origins"
    )
    CORS_CREDENTIALS: bool = Field(default=True, description="Allow credentials")
    CORS_METHODS: List[str] = Field(default=["*"], description="Allowed methods")
    CORS_HEADERS: List[str] = Field(default=["*"], description="Allowed headers")
    
    # Security
    SECRET_KEY: str = Field(
        default="change-this-secret-key-in-production",
        description="Secret key for JWT encoding"
    )
    ALGORITHM: str = Field(default="HS256", description="JWT algorithm")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=30,
        ge=1,
        description="Access token expiration in minutes"
    )
    
    # Logging
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")
    LOG_FORMAT: str = Field(default="json", description="Log format (json or text)")
    
    # Redis
    REDIS_USERNAME: Optional[str] = None
    REDIS_PASSWORD: Optional[str] = None
    REDIS_HOST: Optional[str] = None
    REDIS_PORT: Optional[str] = None
    REDIS_DB0: Optional[str] = None
    
    # File Upload
    MAX_UPLOAD_SIZE: int = Field(
        default=10485760,
        ge=1,
        description="Max upload size in bytes (default 10MB)"
    )
    ALLOWED_EXTENSIONS: List[str] = Field(
        default=["pdf", "doc", "docx", "xls", "xlsx", "png", "jpg", "jpeg"],
        description="Allowed file extensions"
    )
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )
   
    @field_validator("ENVIRONMENT")
    @classmethod
    def validate_environment(cls, v: str) -> str:
        """Validate environment value"""
        allowed = ["development", "testing", "staging", "production"]
        if v not in allowed:
            raise ValueError(f"ENVIRONMENT must be one of {allowed}")
        return v
    
    @field_validator("LOG_LEVEL")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level"""
        allowed = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        v_upper = v.upper()
        if v_upper not in allowed:
            raise ValueError(f"LOG_LEVEL must be one of {allowed}")
        return v_upper
    
    @property
    def is_development(self) -> bool:
        """Check if running in development mode"""
        return self.ENVIRONMENT == "development"
    
    @property
    def is_production(self) -> bool:
        """Check if running in production mode"""
        return self.ENVIRONMENT == "production"
    
    @property
    def is_testing(self) -> bool:
        """Check if running in testing mode"""
        return self.TESTING or self.ENVIRONMENT == "testing"


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    Using lru_cache ensures settings are loaded only once.
    """
    return Settings()