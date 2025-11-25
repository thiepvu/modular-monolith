"""Test Unit of Work pattern"""

import pytest

from src.shared.repositories.unit_of_work import UnitOfWork
from src.modules.user_management.domain.entities.user import User
from src.modules.user_management.infrastructure.persistence.repositories.user_repository import UserRepository


class TestUnitOfWork:
    """Test UnitOfWork transaction management"""
    
    @pytest.mark.asyncio
    async def test_commit_transaction(self, db_session):
        """Test successful transaction commit"""
        # Arrange
        repository = UserRepository(db_session)
        user = User.create(
            email="uow@example.com",
            username="uowuser",
            first_name="UoW",
            last_name="User"
        )
        
        # Act
        async with UnitOfWork(db_session) as uow:
            await repository.add(user)
            await uow.commit()
        
        # Assert
        retrieved = await repository.get_by_email("uow@example.com")
        assert retrieved is not None
    
    @pytest.mark.asyncio
    async def test_rollback_transaction(self, db_session):
        """Test transaction rollback on exception"""
        # Arrange
        repository = UserRepository(db_session)
        
        # Act & Assert
        with pytest.raises(Exception):
            async with UnitOfWork(db_session):
                user = User.create(
                    email="rollback@example.com",
                    username="rollbackuser",
                    first_name="Rollback",
                    last_name="User"
                )
                await repository.add(user)
                raise Exception("Force rollback")
        
        # User should not be saved
        retrieved = await repository.get_by_email("rollback@example.com")
        assert retrieved is None