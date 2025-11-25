"""Session utilities and context managers"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from .connection import db

logger = logging.getLogger(__name__)


@asynccontextmanager
async def get_session_context() -> AsyncGenerator[AsyncSession, None]:
    """
    Context manager for database session outside of FastAPI.
    Useful for background tasks, scripts, etc.
    
    Usage:
        async with get_session_context() as session:
            # Use session
            pass
    
    Yields:
        AsyncSession instance
    """
    async for session in db.get_session():
        yield session