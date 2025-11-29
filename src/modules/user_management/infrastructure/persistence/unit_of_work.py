"""
Unit of Work Pattern Implementation for User Management Module

This module implements the Unit of Work pattern to manage transactions
and coordinate repositories within the user management bounded context.
"""

from typing import Optional
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession

from shared.repositories.unit_of_work import UnitOfWork
from modules.user_management.infrastructure.persistence.repositories.user_repository import UserRepository
# from modules.user_management.infrastructure.persistence.repositories.role_repository import RoleRepository
# from modules.user_management.infrastructure.persistence.repositories.permission_repository import PermissionRepository


class UserUnitOfWork(UnitOfWork):
    """
    Unit of Work for User Management module.
    
    Coordinates all repositories and manages database transactions
    for the user management bounded context.
    
    Attributes:
        users: Repository for user aggregate operations
        roles: Repository for role entity operations  
        permissions: Repository for permission entity operations
    """
    
    def __init__(self, session: AsyncSession):
        """
        Initialize Unit of Work with database session.
        
        Args:
            session: SQLAlchemy async session for database operations
        """
        super().__init__(session)
        
        # Initialize repositories - lazy loading for better performance
        self._users: Optional[UserRepository] = None
        self._roles: Optional[RoleRepository] = None
        self._permissions: Optional[PermissionRepository] = None
    
    @property
    def users(self) -> UserRepository:
        """
        Lazy-loaded user repository.
        
        Returns:
            UserRepository: Repository for user operations
        """
        if self._users is None:
            self._users = UserRepository(self._session)
        return self._users
    
    # @property
    # def roles(self) -> RoleRepository:
    #     """
    #     Lazy-loaded role repository.
        
    #     Returns:
    #         RoleRepository: Repository for role operations
    #     """
    #     if self._roles is None:
    #         self._roles = RoleRepository(self._session)
    #     return self._roles
    
    # @property
    # def permissions(self) -> PermissionRepository:
    #     """
    #     Lazy-loaded permission repository.
        
    #     Returns:
    #         PermissionRepository: Repository for permission operations
    #     """
    #     if self._permissions is None:
    #         self._permissions = PermissionRepository(self._session)
    #     return self._permissions
    
    # async def commit(self) -> None:
    #     """
    #     Commit all pending changes to the database.
        
    #     Raises:
    #         Exception: If commit fails, rolls back transaction
    #     """
    #     try:
    #         await self._session.commit()
    #     except Exception as e:
    #         await self.rollback()
    #         raise
    
    async def rollback(self) -> None:
        """
        Rollback all pending changes in the current transaction.
        """
        await self._session.rollback()
    
    async def refresh(self, instance) -> None:
        """
        Refresh an instance from the database.
        
        Args:
            instance: The entity instance to refresh
        """
        await self._session.refresh(instance)
    
    async def flush(self) -> None:
        """
        Flush pending changes without committing.
        Useful for getting auto-generated IDs before commit.
        """
        await self._session.flush()
    
    @asynccontextmanager
    async def transaction(self):
        """
        Context manager for explicit transaction handling.
        
        Usage:
            async with uow.transaction():
                await uow.users.add(user)
                await uow.roles.add(role)
                # Automatically commits on success, rolls back on error
        
        Yields:
            self: The unit of work instance
            
        Raises:
            Exception: Re-raises any exception after rollback
        """
        try:
            yield self
            await self.commit()
        except Exception as e:
            await self.rollback()
            raise
    
    async def __aenter__(self):
        """Async context manager entry."""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Async context manager exit.
        Commits on success, rolls back on exception.
        """
        if exc_type is not None:
            await self.rollback()
        else:
            await self.commit()


# Example of specialized Unit of Work for read-only operations
class UserReadOnlyUnitOfWork:
    """
    Read-only Unit of Work for optimized query operations.
    Does not support commits or transactions.
    """
    
    def __init__(self, session: AsyncSession):
        """
        Initialize read-only Unit of Work.
        
        Args:
            session: SQLAlchemy async session
        """
        self._session = session
        self._users: Optional[UserRepository] = None
        # self._roles: Optional[RoleRepository] = None
    
    @property
    def users(self) -> UserRepository:
        """Lazy-loaded user repository for read operations."""
        if self._users is None:
            self._users = UserRepository(self._session)
        return self._users
    
    # @property
    # def roles(self) -> RoleRepository:
    #     """Lazy-loaded role repository for read operations."""
    #     if self._roles is None:
    #         self._roles = RoleRepository(self._session)
    #     return self._roles


# Example factory function for creating UoW instances
def create_user_unit_of_work(session: AsyncSession) -> UserUnitOfWork:
    """
    Factory function to create UserUnitOfWork instances.
    
    Args:
        session: Database session
        
    Returns:
        UserUnitOfWork: Configured unit of work instance
    """
    return UserUnitOfWork(session)


# Example of how to use in application service:
"""
class UserService:
    def __init__(self, uow: UserUnitOfWork):
        self._uow = uow
    
    async def create_user_with_role(
        self, 
        user_data: CreateUserDTO,
        role_id: str
    ) -> UserDTO:
        # Using transaction context manager
        async with self._uow.transaction():
            # Create user
            user = User.create(
                email=user_data.email,
                username=user_data.username,
                password_hash=hash_password(user_data.password)
            )
            await self._uow.users.add(user)
            await self._uow.flush()  # Get user ID
            
            # Assign role
            role = await self._uow.roles.get_by_id(role_id)
            if not role:
                raise ValueError("Role not found")
            
            user.assign_role(role)
            
            # Transaction commits automatically on success
            # Rolls back automatically on exception
        
        return UserDTO.from_entity(user)
"""