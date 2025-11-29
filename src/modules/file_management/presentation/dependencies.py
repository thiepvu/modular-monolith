"""
Database connection for File module.
Automatically connects to file_schema.
"""
from typing import Annotated
from fastapi import Depends
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database.connection import db

async def get_file_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency for File module database session.
    
    This automatically connects to the correct schema (file_schema)
    based on the module's configuration.
    
    Usage in File module routers:
        @router.get("/files")
        async def get_files(session: AsyncSession = Depends(get_file_db_session)):
            # This session is configured for file_schema
            result = await session.execute(select(FileModel))
            return result.scalars().all()
    
    Yields:
        AsyncSession instance configured for file_schema
    """
    async for session in db.get_session():
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_file_db_session)]