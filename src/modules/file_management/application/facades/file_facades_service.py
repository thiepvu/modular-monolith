"""File application service"""

from uuid import UUID


from modules.user_management.application.interfaces.user_service import IUserService
from modules.user_management.application.services.user_service import UserService
from modules.user_management.infrastructure.persistence.repositories.user_repository import UserRepository

class FileServiceFacade:

    def _get_service(self) -> IUserService:
        """Get user service instance"""
        repository = UserRepository()
        return UserService(repository)
    
    async def check_owner_exists(
        self,
        owner_id: UUID
    ) -> bool:
        # Validate owner exists
        return await self._get_service().user_exists(owner_id)

