from uuid import UUID
from typing import List
import logging

from modules.user_management.application.interfaces.user_service import IUserService

logger = logging.getLogger(__name__)


class FileServiceFacade:
    """
    Facade for cross-module dependencies.
    
    Benefits:
    - Isolates FileService from UserService
    - Single point of change for user-related operations
    - FileService doesn't need to know about User module
    - Easy to mock for testing
    """
    
    def __init__(self, user_service: IUserService):
        """
        Initialize facade with user service.
        
        Args:
            user_service: User service instance (injected)
        """
        self._user_service = user_service
        logger.debug("FileServiceFacade initialized")
    
    async def check_owner_exists(self, owner_id: UUID) -> bool:
        """
        Check if owner user exists and is active.
        
        Args:
            owner_id: User UUID
            
        Returns:
            True if user exists and is active, False otherwise
        """
        try:
            exists = await self._user_service.user_exists(owner_id)
            logger.debug(f"Owner check: {owner_id} exists={exists}")
            return exists
        except Exception as e:
            logger.error(f"Error checking owner existence: {e}", exc_info=True)
            return False
    
    async def check_user_exists(self, user_id: UUID) -> bool:
        """
        Check if user exists and is active.
        
        Args:
            user_id: User UUID
            
        Returns:
            True if user exists and is active, False otherwise
        """
        try:
            exists = await self._user_service.user_exists(user_id)
            logger.debug(f"User check: {user_id} exists={exists}")
            return exists
        except Exception as e:
            logger.error(f"Error checking user existence: {e}", exc_info=True)
            return False
    
    async def validate_users_exist(self, user_ids: List[UUID]) -> bool:
        """
        Validate that all users in list exist.
        
        Args:
            user_ids: List of user UUIDs
            
        Returns:
            True if all users exist, False otherwise
        """
        try:
            users = await self._user_service.get_users_by_ids(user_ids)
            exists = len(users) == len(user_ids)
            logger.debug(f"Batch user check: {len(user_ids)} users, all exist={exists}")
            return exists
        except Exception as e:
            logger.error(f"Error validating users: {e}", exc_info=True)
            return False