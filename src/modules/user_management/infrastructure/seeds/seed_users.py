"""
User seeder function.
To be imported by main seed.py script.
"""
import logging
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ...infrastructure.persistence.models import UserModel, UserProfileModel

logger = logging.getLogger(__name__)


async def seed_users(session: AsyncSession):
    """
    Seed user data.
    
    Args:
        session: AsyncSession instance (already created by seed.py)
    """
    logger.info("  Seeding users...")
    
    # Check if users already exist (idempotent)
    result = await session.execute(select(UserModel).limit(1))
    existing = result.scalars().first()
    
    if existing:
        logger.info("    ⚠ Users already exist, skipping...")
        return
    
    # Create users
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
    
    users = [UserModel(**data) for data in users_data]
    session.add_all(users)
    await session.flush()  # Flush to get IDs
    
    # Create profiles
    profiles_data = [
        {
            "user_id": users[0].id,
            "first_name": "Admin",
            "last_name": "User",
            "phone": "+1234567890"
        },
        {
            "user_id": users[1].id,
            "first_name": "John",
            "last_name": "Doe",
            "phone": "+1234567891"
        },
        {
            "user_id": users[2].id,
            "first_name": "Jane",
            "last_name": "Smith",
            "phone": "+1234567892"
        },
    ]
    
    profiles = [UserProfileModel(**data) for data in profiles_data]
    session.add_all(profiles)
    
    logger.info(f"    ✓ Created {len(users)} users and {len(profiles)} profiles")