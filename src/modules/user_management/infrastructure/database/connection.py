"""
Database connection for User module.
Automatically connects to user_schema.
"""
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database.connection import db

async def get_user_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency for User module database session.
    
    This automatically connects to the correct schema (user_schema)
    based on the module's configuration.
    
    Usage in User module routers:
        @router.get("/users")
        async def get_users(session: AsyncSession = Depends(get_user_db_session)):
            # This session is configured for user_schema
            result = await session.execute(select(UserModel))
            return result.scalars().all()
    
    Yields:
        AsyncSession instance configured for user_schema
    """
    async for session in db.get_session():
        yield session