"""User repository implementation"""

from typing import Optional, Dict, Any
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from shared.repositories.base_repository import BaseRepository
from modules.user_management.domain.entities.user import User
from modules.user_management.domain.value_objects.email import Email
from modules.user_management.domain.repositories.user_repository import IUserRepository
from ..models import UserModel
from.mappers import to_entity


class UserRepository(BaseRepository[User, UserModel], IUserRepository):
    """User repository implementation"""
    
    def __init__(self, session: AsyncSession):
        """
        Initialize user repository.
        
        Args:
            session: SQLAlchemy async session
        """
        self._to_entity = to_entity
        super().__init__(session, User, UserModel)

    
    async def save(self, user: User) -> User:
        """
        Persist a user entity. Delegates to add() for new entities (no id)
        or update() for existing ones.
        """
        if getattr(user, "id", None) is None:
            return await self.add(user)
        return await self.update(user)
    
    async def get_by_email(self, email: Email) -> Optional[User]:
        """
        Get user by email.
        
        Args:
            email: User Email value object
            
        Returns:
            User entity if found, None otherwise
        """
        stmt = select(UserModel).where(
            UserModel.email == email.value.lower(),
            UserModel.is_deleted == False
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        
        if model is None:
            return None
        
        return self._to_entity(model)
    
    async def get_by_username(self, username: str) -> Optional[User]:
        """
        Get user by username.
        
        Args:
            username: Username
            
        Returns:
            User entity if found, None otherwise
        """
        stmt = select(UserModel).where(
            UserModel.username == username.lower(),
            UserModel.is_deleted == False
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        
        if model is None:
            return None
        
        return self._to_entity(model)
    
    async def count_by_criteria(self, filters: Dict[str, Any]) -> int:
        """
        Count users matching criteria.
        
        Args:
            filters: Filter criteria
            
        Returns:
            Count of matching users
        """
        from sqlalchemy import func
        
        stmt = select(func.count()).select_from(UserModel).where(
            UserModel.is_deleted == False
        )
        
        for field, value in filters.items():
            if hasattr(UserModel, field):
                column = getattr(UserModel, field)
                stmt = stmt.where(column == value)
        
        result = await self._session.execute(stmt)
        return result.scalar_one()
