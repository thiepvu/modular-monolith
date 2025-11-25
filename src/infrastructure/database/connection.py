"""
Database connection management.
Handles async database connections and session lifecycle.
"""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    create_async_engine,
    async_sessionmaker
)
from sqlalchemy.pool import NullPool, QueuePool
import logging

from ...config.settings import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class DatabaseConnection:
    """
    Database connection manager.
    Manages engine and session factory lifecycle.
    """
    
    def __init__(self):
        self._engine: AsyncEngine = None
        self._session_factory: async_sessionmaker = None
    
    def initialize(self) -> None:
        """
        Initialize database engine and session factory.
        Should be called during application startup.
        """
        if self._engine is not None:
            logger.warning("Database already initialized")
            return
        
        logger.info("Initializing database connection...")
        logger.debug(f"Database URL: {settings.DATABASE_URL.split('@')[1] if '@' in settings.DATABASE_URL else 'masked'}")
        
        # Create engine with appropriate settings
        engine_kwargs = {
            "echo": settings.DB_ECHO,
            "pool_pre_ping": True,  # Verify connections before using
            "future": True,
        }
        
        # Use NullPool for testing, QueuePool for production
        if settings.is_testing:
            engine_kwargs["poolclass"] = NullPool
            logger.debug("Using NullPool for testing")
        else:
            engine_kwargs["poolclass"] = QueuePool
            engine_kwargs["pool_size"] = settings.DB_POOL_SIZE
            engine_kwargs["max_overflow"] = settings.DB_MAX_OVERFLOW
            engine_kwargs["pool_timeout"] = 30
            engine_kwargs["pool_recycle"] = 3600
            logger.debug(
                f"Using QueuePool (size={settings.DB_POOL_SIZE}, "
                f"overflow={settings.DB_MAX_OVERFLOW})"
            )
        
        self._engine = create_async_engine(
            settings.DATABASE_URL,
            **engine_kwargs
        )
        
        # Create session factory
        self._session_factory = async_sessionmaker(
            bind=self._engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False,
        )
        
        logger.info("✓ Database connection initialized")
    
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """
        Get database session.
        Should be used with async context manager.
        
        Yields:
            AsyncSession instance
            
        Raises:
            RuntimeError: If database not initialized
        """
        if self._session_factory is None:
            raise RuntimeError(
                "Database not initialized. Call initialize() first."
            )
        
        async with self._session_factory() as session:
            try:
                yield session
            except Exception as e:
                logger.error(f"Database session error: {e}", exc_info=True)
                await session.rollback()
                raise
            finally:
                await session.close()
    
    async def close(self) -> None:
        """
        Close database connection.
        Should be called during application shutdown.
        """
        if self._engine is None:
            logger.warning("Database not initialized, nothing to close")
            return
        
        logger.info("Closing database connection...")
        await self._engine.dispose()
        self._engine = None
        self._session_factory = None
        logger.info("✓ Database connection closed")
    
    @property
    def engine(self) -> AsyncEngine:
        """Get database engine"""
        if self._engine is None:
            raise RuntimeError("Database not initialized")
        return self._engine
    
    @property
    def is_initialized(self) -> bool:
        """Check if database is initialized"""
        return self._engine is not None


# Global database connection instance
db = DatabaseConnection()


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency for database session.
    
    Usage:
        @router.get("/")
        async def endpoint(session: AsyncSession = Depends(get_db_session)):
            ...
    
    Yields:
        AsyncSession instance
    """
    async for session in db.get_session():
        yield session