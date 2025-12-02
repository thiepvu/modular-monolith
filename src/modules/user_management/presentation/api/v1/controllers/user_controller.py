"""User API controller"""

from uuid import UUID
from typing import Optional
from fastapi import Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from shared.api.base_controller import BaseController
from shared.api.response import ApiResponse
from shared.api.pagination import PaginationParams, PaginatedResponse
from shared.repositories.unit_of_work import UnitOfWork

from modules.user_management.application.interfaces.user_service import IUserService

from modules.user_management.application.dto.user_dto import (
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
    
    async def create_user(
        self,
        dto: UserCreateDTO,
        user_service: IUserService 
    ) -> ApiResponse[UserResponseDTO]:
        """
        Create a new user.
        
        Args:
            dto: User creation data
            
        Returns:
            Created user response
        """
        async with UnitOfWork():
            user = await user_service.create_user(dto)
            return self.created(user, "User created successfully")
    
    async def get_user(
        self,
        user_id: UUID,
        user_service: IUserService 
    ) -> ApiResponse[UserResponseDTO]:
        """
        Get user by ID.
        
        Args:
            user_id: User UUID
            session: Database session
            
        Returns:
            User response
        """
        user = await user_service.get_user(user_id)
        return self.success(user)
    
    async def get_user_by_email(
        self,
        email: str,
        user_service: IUserService 
    ) -> ApiResponse[UserResponseDTO]:
        """
        Get user by email.
        
        Args:
            email: User email
            session: Database session
            
        Returns:
            User response
        """
        user = await user_service.get_user_by_email(email)
        
        if not user:
            self.error("User not found", status_code=status.HTTP_404_NOT_FOUND)
        
        return self.success(user)
    
    async def get_user_by_username(
        self,
        username: str,
        user_service: IUserService 
    ) -> ApiResponse[UserResponseDTO]:
        """
        Get user by username.
        
        Args:
            username: Username
            session: Database session
            
        Returns:
            User response
        """
        user = await user_service.get_user_by_username(username)
        
        if not user:
            self.error("User not found", status_code=status.HTTP_404_NOT_FOUND)
        
        return self.success(user)
    
    async def update_user(
        self,
        user_id: UUID,
        dto: UserUpdateDTO,
        user_service: IUserService 
    ) -> ApiResponse[UserResponseDTO]:
        """
        Update user profile.
        
        Args:
            user_id: User UUID
            dto: User update data
            
        Returns:
            Updated user response
        """
        async with UnitOfWork():
            user = await user_service.update_user(user_id, dto)
            return self.success(user, "User updated successfully")
    
    async def update_user_email(
        self,
        user_id: UUID,
        dto: UserEmailUpdateDTO,
        user_service: IUserService 
    ) -> ApiResponse[UserResponseDTO]:
        """
        Update user email.
        
        Args:
            user_id: User UUID
            dto: Email update data
            
        Returns:
            Updated user response
        """
        async with UnitOfWork():
            user = await user_service.update_user_email(user_id, dto)
            return self.success(user, "Email updated successfully")
    
    async def activate_user(
        self,
        user_id: UUID,
        user_service: IUserService 
    ) -> ApiResponse[UserResponseDTO]:
        """
        Activate user account.
        
        Args:
            user_id: User UUID
            
        Returns:
            Updated user response
        """
        async with UnitOfWork():
            user = await user_service.activate_user(user_id)
            return self.success(user, "User activated successfully")
    
    async def deactivate_user(
        self,
        user_id: UUID,
        user_service: IUserService 
    ) -> ApiResponse[UserResponseDTO]:
        """
        Deactivate user account.
        
        Args:
            user_id: User UUID
            
        Returns:
            Updated user response
        """
        async with UnitOfWork():
            user = await user_service.deactivate_user(user_id)
            return self.success(user, "User deactivated successfully")
    
    async def delete_user(
        self,
        user_id: UUID,
        user_service: IUserService 
    ) -> ApiResponse:
        """
        Delete user (soft delete).
        
        Args:
            user_id: User UUID
            
        Returns:
            Success response
        """
        async with UnitOfWork():
            await user_service.delete_user(user_id)
            return self.no_content("User deleted successfully")
    
    async def list_users(
        self,
        params: PaginationParams = Depends(),
        is_active: Optional[bool] = Query(None, description="Filter by active status"),
        search: Optional[str] = Query(None, description="Search term"),
        user_service: IUserService = None,
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
        
        # Search if search term provided
        if search:
            users = await user_service.search_users(
                search_term=search,
                skip=params.skip,
                limit=params.limit
            )
            total = len(users)  # Simplified - should count from query
        else:
            users = await user_service.list_users(
                skip=params.skip,
                limit=params.limit,
                is_active=is_active
            )
            total = await user_service.count_users(is_active=is_active)
        
        return self.paginated(users, total, params)