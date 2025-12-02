"""
Presentation Layer Dependencies for User Management Module

This module provides FastAPI dependency injection for the user management module.
It bridges the presentation layer with application services and infrastructure components.
"""

from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator

from infrastructure.database.connection import db
from modules.user_management.application.services.user_service import UserService
from modules.user_management.application.interfaces.user_service import IUserService
from modules.user_management.domain.repositories.user_repository import IUserRepository
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
def get_user_service() -> IUserService:
    """
    Return IUserService instance. The DB session is injected via Depends.
    """
    repository: IUserRepository = UserRepository()
    return UserService(repository)



# Example of additional dependencies for complex scenarios

async def get_current_user_id(
    # This would typically extract user ID from JWT token or session
    # For now, this is a placeholder
) -> str:
    """
    Extracts current user ID from authentication context.
    
    Returns:
        str: Current user's unique identifier
        
    Raises:
        HTTPException: If user is not authenticated
    """
    # TODO: Implement actual authentication logic
    # from fastapi import Header, HTTPException
    # Extract from JWT token, session, etc.
    raise NotImplementedError("Authentication not yet implemented")


CurrentUserIdDep = Annotated[str, Depends(get_current_user_id)]


# Example with event bus integration (if you use domain events)
# from core.events.event_bus import EventBus
# from infrastructure.events.in_memory_event_bus import InMemoryEventBus
#
# def get_event_bus() -> EventBus:
#     """Provides event bus for domain events."""
#     return InMemoryEventBus()
#
# EventBusDep = Annotated[EventBus, Depends(get_event_bus)]


# Example with caching layer
# from modules.user_management.infrastructure.caching.user_cache import UserCache
#
# def get_user_cache(session: SessionDep) -> UserCache:
#     """Provides user cache for read optimization."""
#     return UserCache(session)
#
# UserCacheDep = Annotated[UserCache, Depends(get_user_cache)]