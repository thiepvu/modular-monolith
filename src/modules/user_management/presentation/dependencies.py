from typing import  Annotated
from fastapi import Depends

from modules.user_management.application.services.user_service import UserService
from modules.user_management.application.interfaces.user_service import IUserService
from modules.user_management.infrastructure.persistence.repositories.user_repository import UserRepository

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
