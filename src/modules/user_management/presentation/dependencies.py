from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator, Annotated
from fastapi import Depends

from infrastructure.database.connection import db
from infrastructure.database.session_context import set_current_session, clear_current_session
from modules.user_management.application.services.user_service import UserService
from modules.user_management.application.interfaces.user_service import IUserService
from modules.user_management.infrastructure.persistence.repositories.user_repository import UserRepository


# ============================================================================
# DATABASE SESSION DEPENDENCY
# ============================================================================

async def get_user_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Get database session for user module.
    
    Yields:
        AsyncSession instance
        
    Lifecycle:
    1. Get session from db.get_session()
    2. Set into ContextVar (for UnitOfWork and Repository)
    3. Yield to route/controller
    4. Clear from ContextVar in finally block
    """
    # Get session from database connection pool
    async for session in db.get_session():
        # Set session vào ContextVar
        set_current_session(session)
        
        try:
            # Yield session to controller
            yield session
        finally:
            # Clear session từ ContextVar khi request kết thúc
            clear_current_session()

# ✅ Type annotation cho clean dependency injection
SessionDep = Annotated[AsyncSession, Depends(get_user_db_session)]


# ============================================================================
# SERVICE DEPENDENCIES
# ============================================================================

def get_user_service() -> IUserService:
    """
    Get IUserService instance.
    Returns:
        IUserService instance
    """
    return UserService(UserRepository())


# ✅ Type annotation cho service
UserServiceDep = Annotated[IUserService, Depends(get_user_service)]
