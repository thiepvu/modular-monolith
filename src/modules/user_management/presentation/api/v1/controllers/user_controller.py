"""User API controller"""

from uuid import UUID
from typing import Optional
from fastapi import Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.user_management.infrastructure.database import get_user_db_session
from src.shared.api.base_controller import BaseController
from src.shared.api.response import ApiResponse
from src.shared.api.pagination import PaginationParams, PaginatedResponse
from src.shared.repositories.unit_of_work import UnitOfWork
from src.modules.user_management.infrastructure.persistence.repositories.user_repository import UserRepository
from src.modules.user_management.application.services.user_service import UserService
from src.modules.user_management.application.dto.user_dto import (
    UserCreateDTO,
    UserUpdateDTO,
    UserEmailUpdateDTO,
    UserResponseDTO,
    UserListResponseDTO
)


class UserController(BaseController):
    """User API controller"""
    
    def __init__(self):
        super().__init__()
    
    def _get_service(self, session: AsyncSession) -> UserService:
        """
        Get user service instance with dependencies.
        
        Args:
            session: Database session
            
        Returns:
            UserService instance
        """
        repository = UserRepository(session)
        return UserService(repository)
    
    async def create_user(
        self,
        dto: UserCreateDTO,
        session: AsyncSession = Depends(get_user_db_session)
    ) -> ApiResponse[UserResponseDTO]:
        """
        Create a new user.
        
        Args:
            dto: User creation data
            session: Database session
            
        Returns:
            Created user response
        """
        async with UnitOfWork(session):
            service = self._get_service(session)
            user = await service.create_user(dto)
            return self.created(user, "User created successfully")
    
    async def get_user(
        self,
        user_id: UUID,
        session: AsyncSession = Depends(get_user_db_session)
    ) -> ApiResponse[UserResponseDTO]:
        """
        Get user by ID.
        
        Args:
            user_id: User UUID
            session: Database session
            
        Returns:
            User response
        """
        service = self._get_service(session)
        user = await service.get_user(user_id)
        return self.success(user)
    
    async def get_user_by_email(
        self,
        email: str,
        session: AsyncSession = Depends(get_user_db_session)
    ) -> ApiResponse[UserResponseDTO]:
        """
        Get user by email.
        
        Args:
            email: User email
            session: Database session
            
        Returns:
            User response
        """
        service = self._get_service(session)
        user = await service.get_user_by_email(email)
        
        if not user:
            self.error("User not found", status_code=status.HTTP_404_NOT_FOUND)
        
        return self.success(user)
    
    async def get_user_by_username(
        self,
        username: str,
        session: AsyncSession = Depends(get_user_db_session)
    ) -> ApiResponse[UserResponseDTO]:
        """
        Get user by username.
        
        Args:
            username: Username
            session: Database session
            
        Returns:
            User response
        """
        service = self._get_service(session)
        user = await service.get_user_by_username(username)
        
        if not user:
            self.error("User not found", status_code=status.HTTP_404_NOT_FOUND)
        
        return self.success(user)
    
    async def update_user(
        self,
        user_id: UUID,
        dto: UserUpdateDTO,
        session: AsyncSession = Depends(get_user_db_session)
    ) -> ApiResponse[UserResponseDTO]:
        """
        Update user profile.
        
        Args:
            user_id: User UUID
            dto: User update data
            session: Database session
            
        Returns:
            Updated user response
        """
        async with UnitOfWork(session):
            service = self._get_service(session)
            user = await service.update_user(user_id, dto)
            return self.success(user, "User updated successfully")
    
    async def update_user_email(
        self,
        user_id: UUID,
        dto: UserEmailUpdateDTO,
        session: AsyncSession = Depends(get_user_db_session)
    ) -> ApiResponse[UserResponseDTO]:
        """
        Update user email.
        
        Args:
            user_id: User UUID
            dto: Email update data
            session: Database session
            
        Returns:
            Updated user response
        """
        async with UnitOfWork(session):
            service = self._get_service(session)
            user = await service.update_user_email(user_id, dto)
            return self.success(user, "Email updated successfully")
    
    async def activate_user(
        self,
        user_id: UUID,
        session: AsyncSession = Depends(get_user_db_session)
    ) -> ApiResponse[UserResponseDTO]:
        """
        Activate user account.
        
        Args:
            user_id: User UUID
            session: Database session
            
        Returns:
            Updated user response
        """
        async with UnitOfWork(session):
            service = self._get_service(session)
            user = await service.activate_user(user_id)
            return self.success(user, "User activated successfully")
    
    async def deactivate_user(
        self,
        user_id: UUID,
        session: AsyncSession = Depends(get_user_db_session)
    ) -> ApiResponse[UserResponseDTO]:
        """
        Deactivate user account.
        
        Args:
            user_id: User UUID
            session: Database session
            
        Returns:
            Updated user response
        """
        async with UnitOfWork(session):
            service = self._get_service(session)
            user = await service.deactivate_user(user_id)
            return self.success(user, "User deactivated successfully")
    
    async def delete_user(
        self,
        user_id: UUID,
        session: AsyncSession = Depends(get_user_db_session)
    ) -> ApiResponse:
        """
        Delete user (soft delete).
        
        Args:
            user_id: User UUID
            session: Database session
            
        Returns:
            Success response
        """
        async with UnitOfWork(session):
            service = self._get_service(session)
            await service.delete_user(user_id)
            return self.no_content("User deleted successfully")
    
    async def list_users(
        self,
        params: PaginationParams = Depends(),
        is_active: Optional[bool] = Query(None, description="Filter by active status"),
        search: Optional[str] = Query(None, description="Search term"),
        session: AsyncSession = Depends(get_user_db_session)
    ) -> ApiResponse[PaginatedResponse[UserListResponseDTO]]:
        """
        List all users with pagination.
        
        Args:
            params: Pagination parameters
            is_active: Filter by active status
            search: Search term
            session: Database session
            
        Returns:
            Paginated user list response
        """
        service = self._get_service(session)
        
        # Search if search term provided
        if search:
            users = await service.search_users(
                search_term=search,
                skip=params.skip,
                limit=params.limit
            )
            total = len(users)  # Simplified - should count from query
        else:
            users = await service.list_users(
                skip=params.skip,
                limit=params.limit,
                is_active=is_active
            )
            total = await service.count_users(is_active=is_active)
        
        return self.paginated(users, total, params)