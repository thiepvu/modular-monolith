"""
Central seed data runner.
Manages seeding data across all modules.
"""

from typing import List, Callable, Awaitable
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from ..database.connection import db

logger = logging.getLogger(__name__)


class SeedRunner:
    """Central seed data runner for all modules"""
    
    def __init__(self):
        self._seeders: List[Callable[[AsyncSession], Awaitable[None]]] = []
    
    def register_seeder(
        self,
        seeder: Callable[[AsyncSession], Awaitable[None]]
    ) -> None:
        """
        Register a seeder function.
        
        Args:
            seeder: Async function that accepts AsyncSession
        """
        self._seeders.append(seeder)
        logger.debug(f"Registered seeder: {seeder.__name__}")
    
    async def run_all(self) -> None:
        """
        Run all registered seeders.
        Each seeder runs in its own transaction.
        """
        if not self._seeders:
            logger.warning("No seeders registered")
            return
        
        logger.info(f"Running {len(self._seeders)} seeders...")
        
        success_count = 0
        failed_count = 0
        
        async for session in db.get_session():
            for seeder in self._seeders:
                try:
                    logger.info(f"Running seeder: {seeder.__name__}")
                    await seeder(session)
                    await session.commit()
                    success_count += 1
                    logger.info(f"✓ Seeder completed: {seeder.__name__}")
                except Exception as e:
                    logger.error(
                        f"✗ Seeder failed: {seeder.__name__} - {e}",
                        exc_info=True
                    )
                    await session.rollback()
                    failed_count += 1
        
        logger.info(
            f"Seeding complete: {success_count} successful, {failed_count} failed"
        )
        
        if failed_count > 0:
            raise RuntimeError(f"{failed_count} seeders failed")


# Example seeder for user module
async def seed_users(session: AsyncSession) -> None:
    """
    Seed initial users.
    This is an example - actual implementation will be in user module.
    """
    from src.modules.user_management.infrastructure.persistence.repositories.user_repository import UserRepository
    from src.modules.user_management.domain.entities.user import User
    
    repository = UserRepository(session)
    
    # Check if users already exist
    count = await repository.count()
    if count > 0:
        logger.info("Users already seeded, skipping...")
        return
    
    # Create sample users
    users_data = [
        {
            "email": "admin@example.com",
            "username": "admin",
            "first_name": "Admin",
            "last_name": "User"
        },
        {
            "email": "john.doe@example.com",
            "username": "johndoe",
            "first_name": "John",
            "last_name": "Doe"
        },
        {
            "email": "jane.smith@example.com",
            "username": "janesmith",
            "first_name": "Jane",
            "last_name": "Smith"
        }
    ]
    
    for user_data in users_data:
        user = User.create(**user_data)
        await repository.add(user)
    
    logger.info(f"✓ Seeded {len(users_data)} users")