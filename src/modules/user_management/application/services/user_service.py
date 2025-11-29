"""User application service"""

from typing import List, Optional
from uuid import UUID

from core.interfaces.services import IService
from core.exceptions.base_exceptions import NotFoundException, ConflictException
from ...domain.entities.user import User
from ...infrastructure.persistence.repositories.user_repository import UserRepository
from ..dto.user_dto import (
    UserCreateDTO,
    UserUpdateDTO,
    UserEmailUpdateDTO,
    UserResponseDTO,
    UserListResponseDTO
)
from ..dto.mappers import UserMapper


class UserService(IService):
    """
    User application service.
    Orchestrates user-related use cases.
    """
    
    def __init__(self, user_repository: UserRepository):
        """
        Initialize user service.
        
        Args:
            user_repository: User repository
        """
        self._user_repository = user_repository
        self._mapper = UserMapper()
    
    async def create_user(self, dto: UserCreateDTO) -> UserResponseDTO:
        """
        Create a new user.
        
        Args:
            dto: User creation data
            
        Returns:
            Created user DTO
            
        Raises:
            ConflictException: If user with email or username already exists
        """
        # Check if user with email already exists
        existing = await self._user_repository.get_by_email(dto.email)
        if existing:
            raise ConflictException(f"User with email {dto.email} already exists")
        
        # Check if user with username already exists
        existing = await self._user_repository.get_by_username(dto.username)
        if existing:
            raise ConflictException(f"User with username {dto.username} already exists")
        
        # Create user entity
        user = User.create(
            email=dto.email,
            username=dto.username,
            first_name=dto.first_name,
            last_name=dto.last_name
        )
        
        # Save to repository
        saved_user = await self._user_repository.add(user)
        
        return self._mapper.to_response_dto(saved_user)
    
    async def get_user(self, user_id: UUID) -> UserResponseDTO:
        """
        Get user by ID.
        
        Args:
            user_id: User UUID
            
        Returns:
            User DTO
            
        Raises:
            NotFoundException: If user not found
        """
        user = await self._user_repository.get_by_id(user_id)
        if not user:
            raise NotFoundException("User", user_id)
        
        return self._mapper.to_response_dto(user)
    
    async def get_user_by_email(self, email: str) -> Optional[UserResponseDTO]:
        """
        Get user by email.
        
        Args:
            email: User email
            
        Returns:
            User DTO if found, None otherwise
        """
        user = await self._user_repository.get_by_email(email)
        if not user:
            return None
        
        return self._mapper.to_response_dto(user)
    
    async def get_user_by_username(self, username: str) -> Optional[UserResponseDTO]:
        """
        Get user by username.
        
        Args:
            username: Username
            
        Returns:
            User DTO if found, None otherwise
        """
        user = await self._user_repository.get_by_username(username)
        if not user:
            return None
        
        return self._mapper.to_response_dto(user)
    
    async def update_user(self, user_id: UUID, dto: UserUpdateDTO) -> UserResponseDTO:
        """
        Update user profile.
        
        Args:
            user_id: User UUID
            dto: User update data
            
        Returns:
            Updated user DTO
            
        Raises:
            NotFoundException: If user not found
        """
        user = await self._user_repository.get_by_id(user_id)
        if not user:
            raise NotFoundException("User", user_id)
        
        # Update profile if both fields provided
        if dto.first_name and dto.last_name:
            user.update_profile(dto.first_name, dto.last_name)
        
        # Save changes
        updated_user = await self._user_repository.update(user)
        
        return self._mapper.to_response_dto(updated_user)
    
    async def update_user_email(
        self,
        user_id: UUID,
        dto: UserEmailUpdateDTO
    ) -> UserResponseDTO:
        """
        Update user email.
        
        Args:
            user_id: User UUID
            dto: Email update data
            
        Returns:
            Updated user DTO
            
        Raises:
            NotFoundException: If user not found
            ConflictException: If email already in use
        """
        user = await self._user_repository.get_by_id(user_id)
        if not user:
            raise NotFoundException("User", user_id)
        
        # Check if email already in use
        existing = await self._user_repository.get_by_email(dto.email)
        if existing and existing.id != user_id:
            raise ConflictException(f"Email {dto.email} is already in use")
        
        # Update email
        user.change_email(dto.email)
        
        # Save changes
        updated_user = await self._user_repository.update(user)
        
        return self._mapper.to_response_dto(updated_user)
    
    async def activate_user(self, user_id: UUID) -> UserResponseDTO:
        """
        Activate user account.
        
        Args:
            user_id: User UUID
            
        Returns:
            Updated user DTO
            
        Raises:
            NotFoundException: If user not found
        """
        user = await self._user_repository.get_by_id(user_id)
        if not user:
            raise NotFoundException("User", user_id)
        
        user.activate()
        updated_user = await self._user_repository.update(user)
        
        return self._mapper.to_response_dto(updated_user)
    
    async def deactivate_user(self, user_id: UUID) -> UserResponseDTO:
        """
        Deactivate user account.
        
        Args:
            user_id: User UUID
            
        Returns:
            Updated user DTO
            
        Raises:
            NotFoundException: If user not found
        """
        user = await self._user_repository.get_by_id(user_id)
        if not user:
            raise NotFoundException("User", user_id)
        
        user.deactivate()
        updated_user = await self._user_repository.update(user)
        
        return self._mapper.to_response_dto(updated_user)
    
    async def delete_user(self, user_id: UUID) -> None:
        """
        Delete user (soft delete).
        
        Args:
            user_id: User UUID
            
        Raises:
            NotFoundException: If user not found
        """
        exists = await self._user_repository.exists(user_id)
        if not exists:
            raise NotFoundException("User", user_id)
        
        await self._user_repository.delete(user_id, soft=True)
    
    async def list_users(
        self,
        skip: int = 0,
        limit: int = 100,
        is_active: Optional[bool] = None
    ) -> List[UserListResponseDTO]:
        """
        List all users.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records
            is_active: Filter by active status
            
        Returns:
            List of user DTOs
        """
        if is_active is not None:
            users = await self._user_repository.find_by_criteria(
                filters={"is_active": is_active},
                skip=skip,
                limit=limit
            )
        else:
            users = await self._user_repository.get_all(skip, limit)
        
        return self._mapper.to_list_dtos(users)
    
    async def search_users(
        self,
        search_term: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[UserListResponseDTO]:
        """
        Search users by term.
        
        Args:
            search_term: Search term
            skip: Number of records to skip
            limit: Maximum number of records
            
        Returns:
            List of matching user DTOs
        """
        users = await self._user_repository.search(
            search_term=search_term,
            search_fields=["username", "first_name", "last_name", "email"],
            skip=skip,
            limit=limit
        )
        
        return self._mapper.to_list_dtos(users)
    
    async def count_users(self, is_active: Optional[bool] = None) -> int:
        """
        Count total users.
        
        Args:
            is_active: Filter by active status
            
        Returns:
            Total count
        """
        if is_active is not None:
            return await self._user_repository.count_by_criteria({"is_active": is_active})
        return await self._user_repository.count()