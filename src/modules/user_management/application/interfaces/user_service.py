from __future__ import annotations

from abc import abstractmethod
from typing import List, Optional
from uuid import UUID

from core.interfaces.services import IService
from ..dto.user_dto import (
    UserCreateDTO,
    UserUpdateDTO,
    UserEmailUpdateDTO,
    UserResponseDTO,
    UserListResponseDTO,
)

class IUserService(IService):
    """Application service interface for user use-cases."""

    @abstractmethod
    async def create_user(self, dto: UserCreateDTO) -> UserResponseDTO:
        raise NotImplementedError

    @abstractmethod
    async def get_user(self, user_id: UUID) -> UserResponseDTO:
        raise NotImplementedError

    @abstractmethod
    async def get_user_by_email(self, email: str) -> Optional[UserResponseDTO]:
        raise NotImplementedError

    @abstractmethod
    async def get_user_by_username(self, username: str) -> Optional[UserResponseDTO]:
        raise NotImplementedError

    @abstractmethod
    async def update_user(self, user_id: UUID, dto: UserUpdateDTO) -> UserResponseDTO:
        raise NotImplementedError

    @abstractmethod
    async def update_user_email(self, user_id: UUID, dto: UserEmailUpdateDTO) -> UserResponseDTO:
        raise NotImplementedError

    @abstractmethod
    async def activate_user(self, user_id: UUID) -> UserResponseDTO:
        raise NotImplementedError

    @abstractmethod
    async def deactivate_user(self, user_id: UUID) -> UserResponseDTO:
        raise NotImplementedError

    @abstractmethod
    async def delete_user(self, user_id: UUID) -> None:
        raise NotImplementedError

    @abstractmethod
    async def list_users(
        self, skip: int = 0, limit: int = 100, is_active: Optional[bool] = None
    ) -> List[UserListResponseDTO]:
        raise NotImplementedError

    @abstractmethod
    async def search_users(self, search_term: str, skip: int = 0, limit: int = 100) -> List[UserListResponseDTO]:
        raise NotImplementedError

    @abstractmethod
    async def count_users(self, is_active: Optional[bool] = None) -> int:
        raise NotImplementedError
    
    @abstractmethod
    async def user_exists(self, user_id: UUID) -> bool:
        """
        Check if user exists.
        
        Args:
            user_id: User UUID
            
        Returns:
            True if user exists and is active, False otherwise
        """
        pass