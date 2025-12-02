"""
Presentation Layer Dependencies for User Management Module

This module provides FastAPI dependency injection for the user management module.
It bridges the presentation layer with application services and infrastructure components.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator

from infrastructure.database.connection import db
from modules.user_management.application.services.user_service import UserService
from modules.user_management.infrastructure.persistence.repositories import UserRepository
from infrastructure.database.session_context import set_current_session, clear_current_session

# Database Session Dependency
async def get_user_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Get database session for user module.
    
    This dependency provides a session that will be used by UnitOfWork
    in the controller layer.
    
    Yields:
        AsyncSession instance
        
    Note:
        Session được tạo nhưng KHÔNG được commit/rollback ở đây.
        UnitOfWork trong controller sẽ handle transaction management.
    """
    # Get session directly from db.get_session()
    # This is already an async generator that yields AsyncSession
    async for session in db.get_session():
        # Set session vào ContextVar
        set_current_session(session)
    
    try:
        # Yield session to controller
        yield session
    finally:
        # Clear session từ ContextVar khi request kết thúc
        clear_current_session()

# make the service provider async and explicitly return IUserService
def get_user_service() -> UserService:
    """
    Return IUserService instance. The DB session is injected via Depends.
    """
    return UserService(UserRepository())
