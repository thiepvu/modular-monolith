"""User repository implementation"""

from typing import Optional, Dict, Any
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from shared.repositories.base_repository import BaseRepository
from infrastructure.database.session_context import get_current_session

from modules.user_management.domain.entities.user import User
from modules.user_management.domain.value_objects.email import Email
from modules.user_management.domain.repositories.user_repository import IUserRepository

from ..models import UserModel


class UserRepository(BaseRepository[User, UserModel], IUserRepository):
    """User repository implementation"""
    
    def __init__(self):
        """
        Initialize user repository.

        """
        super().__init__(User, UserModel)
    
    @property
    def _session(self) -> AsyncSession:
        """
        Lazy load session from ContextVar.
        
        Session được get mỗi khi property được access,
        đảm bảo session đã được set bởi @with_session decorator.
        
        Returns:
            AsyncSession from ContextVar
            
        Raises:
            RuntimeError: If no session in ContextVar
        """
        return get_current_session()
    
    async def save(self, user: User) -> User:
        """
        Persist a user entity. Delegates to add() for new entities (no id)
        or update() for existing ones.
        """
        if getattr(user, "id", None) is None:
            return await self.add(user)
        return await self.update(user)
    
    async def get_by_email(self, email: str) -> Optional[User]:
        """
        Get user by email.
        
        Args:
            email: User email
            
        Returns:
            User entity if found, None otherwise
        """
        stmt = select(UserModel).where(
            UserModel.email == email.lower(),
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
    
    def _to_entity(self, model: UserModel) -> User:
        """
        Convert ORM model to domain entity.
        
        Args:
            model: User ORM model
            
        Returns:
            User domain entity
        """
        user = User(
            email=Email(model.email),
            username=model.username,
            first_name=model.first_name,
            last_name=model.last_name,
            is_active=model.is_active,
            id=model.id
        )
        
        # Set internal timestamps from model
        user._created_at = model.created_at
        user._updated_at = model.updated_at
        user._is_deleted = model.is_deleted
        
        return user
    
    def _to_model(self, entity: User) -> UserModel:
        """
        Convert domain entity to ORM model.
        
        Args:
            entity: User domain entity
            
        Returns:
            User ORM model
        """
        return UserModel(
            id=entity.id,
            email=entity.email.value,
            username=entity.username,
            first_name=entity.first_name,
            last_name=entity.last_name,
            is_active=entity.is_active,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            is_deleted=entity.is_deleted
        )