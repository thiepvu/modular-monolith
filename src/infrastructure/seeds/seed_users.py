"""
Central seed data runner.
Manages seeding data across all modules.
"""

from typing import List, Callable, Awaitable
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from ..database.connection import db

logger = logging.getLogger(__name__)

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