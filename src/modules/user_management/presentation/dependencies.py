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
from modules.user_management.infrastructure.persistence.repositories.user_repository import UserRepository
from modules.user_management.infrastructure.persistence.unit_of_work import UserUnitOfWork


# Database Session Dependency
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


SessionDep = Annotated[AsyncSession, Depends(get_user_db_session)]


# Repository Dependencies
def get_user_repository(
    session: SessionDep,
) -> UserRepository:
    """
    Provides UserRepository instance with database session.
    
    Args:
        session: Database session from dependency injection
        
    Returns:
        UserRepository: Configured repository instance
    """
    return UserRepository(session)


UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]


# Unit of Work Dependency
def get_user_uow(
    session: SessionDep,
) -> UserUnitOfWork:
    """
    Provides Unit of Work pattern implementation for user management.
    
    Args:
        session: Database session from dependency injection
        
    Returns:
        UserUnitOfWork: Unit of work instance for transaction management
    """
    return UserUnitOfWork(session)


UserUnitOfWorkDep = Annotated[UserUnitOfWork, Depends(get_user_uow)]


# Service Dependencies
def get_user_service(
    uow: UserUnitOfWorkDep,
) -> UserService:
    """
    Provides UserService instance with all required dependencies.
    
    Args:
        uow: Unit of work for transaction management
        
    Returns:
        UserService: Configured application service
    """
    return UserService(uow)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]


# Alternative: Direct service with repository (if not using UoW)
def get_user_service_with_repo(
    repository: UserRepositoryDep,
) -> UserService:
    """
    Alternative service provider using repository directly.
    Use this if you want to bypass Unit of Work pattern for simple operations.
    
    Args:
        repository: User repository instance
        
    Returns:
        UserService: Configured application service
    """
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
# from src.core.events.event_bus import EventBus
# from src.infrastructure.events.in_memory_event_bus import InMemoryEventBus
#
# def get_event_bus() -> EventBus:
#     """Provides event bus for domain events."""
#     return InMemoryEventBus()
#
# EventBusDep = Annotated[EventBus, Depends(get_event_bus)]


# Example with caching layer
# from src.modules.user_management.infrastructure.caching.user_cache import UserCache
#
# def get_user_cache(session: SessionDep) -> UserCache:
#     """Provides user cache for read optimization."""
#     return UserCache(session)
#
# UserCacheDep = Annotated[UserCache, Depends(get_user_cache)]