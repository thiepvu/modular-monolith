"""
Database connection for File module.
Automatically connects to file_schema.
"""
from typing import Annotated
from fastapi import Depends
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database.connection import db

from modules.file_management.infrastructure.persistence.repositories.file_repository import FileRepository
from modules.file_management.application.services.file_service import FileService
from modules.file_management.application.services.file_storage_service import FileStorageService
from infrastructure.database.session_context import set_current_session, clear_current_session

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
        # Set session vào ContextVar
        set_current_session(session)
    
    try:
        # Yield session to controller
        yield session
    finally:
        # Clear session từ ContextVar khi request kết thúc
        clear_current_session()


def get_file_service() -> FileService:
        """
        Get file service instance with dependencies.
        
        Args:
            session: Database session
            
        Returns:
            FileService instance
        """
        repository = FileRepository()
        return FileService(repository, FileStorageService())
