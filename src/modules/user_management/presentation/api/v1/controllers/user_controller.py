from uuid import UUID
from typing import Optional
from fastapi import status

from shared.api.base_controller import BaseController
from shared.api.response import ApiResponse
from shared.api.pagination import PaginationParams, PaginatedResponse
from shared.repositories.unit_of_work import UnitOfWork

from modules.user_management.presentation.dependencies import UserServiceDep
from modules.user_management.application.dto.user_dto import (
    UserCreateDTO,
    UserUpdateDTO,
    UserEmailUpdateDTO,
    UserResponseDTO,
    UserListResponseDTO
)


class UserController(BaseController):
    """
    User API controller.
    """
    
    def __init__(self):
        super().__init__()
    
    # ========================================================================
    # WRITE OPERATIONS - với UnitOfWork
    # ========================================================================
    
    async def create_user(
        self,
        dto: UserCreateDTO,
        user_service: UserServiceDep
    ) -> ApiResponse[UserResponseDTO]:
        """
        Create a new user.
        
        Args:
            dto: User creation data
            user_service: User service (auto-injected)
            
        Returns:
            Created user response
        """
        # UnitOfWork get session từ ContextVar
        async with UnitOfWork():
            user = await user_service.create_user(dto)
            # UnitOfWork auto commit khi exit context
            return self.created(user, "User created successfully")
    
    async def update_user(
        self,
        user_id: UUID,
        dto: UserUpdateDTO,
        user_service: UserServiceDep
    ) -> ApiResponse[UserResponseDTO]:
        """
        Update user profile.
        
        Args:
            user_id: User UUID
            dto: User update data
            user_service: User service
            
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
        user_service: UserServiceDep
    ) -> ApiResponse[UserResponseDTO]:
        """
        Update user email.
        
        Args:
            user_id: User UUID
            dto: Email update data
            user_service: User service
            
        Returns:
            Updated user response
        """
        async with UnitOfWork():
            user = await user_service.update_user_email(user_id, dto)
            return self.success(user, "Email updated successfully")
    
    async def activate_user(
        self,
        user_id: UUID,
        user_service: UserServiceDep
    ) -> ApiResponse[UserResponseDTO]:
        """
        Activate user account.
        
        Args:
            user_id: User UUID
            user_service: User service
            
        Returns:
            Updated user response
        """
        async with UnitOfWork():
            user = await user_service.activate_user(user_id)
            return self.success(user, "User activated successfully")
    
    async def deactivate_user(
        self,
        user_id: UUID,
        user_service: UserServiceDep
    ) -> ApiResponse[UserResponseDTO]:
        """
        Deactivate user account.
        
        Args:
            user_id: User UUID
            user_service: User service
            
        Returns:
            Updated user response
        """
        async with UnitOfWork():
            user = await user_service.deactivate_user(user_id)
            return self.success(user, "User deactivated successfully")
    
    async def delete_user(
        self,
        user_id: UUID,
        user_service: UserServiceDep
    ) -> ApiResponse:
        """
        Delete user (soft delete).
        
        Args:
            user_id: User UUID
            user_service: User service
            
        Returns:
            Success response
        """
        async with UnitOfWork():
            await user_service.delete_user(user_id)
            return self.no_content("User deleted successfully")
    
    # ========================================================================
    # READ OPERATIONS - No need UnitOfWork
    # ========================================================================
    
    async def get_user(
        self,
        user_id: UUID,
        user_service: UserServiceDep
    ) -> ApiResponse[UserResponseDTO]:
        """
        Get user by ID.
        
        Args:
            user_id: User UUID
            session: Database session (triggers ContextVar set)
            user_service: User service
            
        Returns:
            User response
            
        Note:
            Read-only operation, KHÔNG cần UnitOfWork.
            Session vẫn cần để repository có thể query.
        """
        user = await user_service.get_user(user_id)
        return self.success(user)
    
    async def get_user_by_email(
        self,
        email: str,
        user_service: UserServiceDep
    ) -> ApiResponse[UserResponseDTO]:
        """
        Get user by email.
        
        Args:
            email: User email
            user_service: User service
            
        Returns:
            User response
        """
        user = await user_service.get_user_by_email(email)
        
        if not user:
            return self.error("User not found", status_code=status.HTTP_404_NOT_FOUND)
        
        return self.success(user)
    
    async def get_user_by_username(
        self,
        username: str,
        user_service: UserServiceDep
    ) -> ApiResponse[UserResponseDTO]:
        """
        Get user by username.
        
        Args:
            username: Username
            session: Database session
            user_service: User service
            
        Returns:
            User response
        """
        user = await user_service.get_user_by_username(username)
        
        if not user:
            return self.error("User not found", status_code=status.HTTP_404_NOT_FOUND)
        
        return self.success(user)
    
    async def list_users(
        self,
        params: PaginationParams,
        is_active: Optional[bool],
        search: Optional[str],
        user_service: UserServiceDep
    ) -> ApiResponse[PaginatedResponse[UserListResponseDTO]]:
        """
        List all users with pagination.
        
        Args:
            params: Pagination parameters
            is_active: Filter by active status
            search: Search term
            user_service: User service
            
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

