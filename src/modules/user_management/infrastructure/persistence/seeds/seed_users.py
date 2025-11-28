"""
User seeder using async database connection.
Works with multi-schema BaseModel architecture.
"""
import asyncio
import logging
from sqlalchemy import select

# Import database connection
from src.infrastructure.database.connection import db

# Import models
from src.modules.user_management.infrastructure.persistence.models import (
    UserModel, 
    UserProfileModel
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def seed_users():
    """
    Seed user data using async database connection.
    
    This function demonstrates proper async db context management
    with multi-schema BaseModel.
    """
    logger.info("Seeding users...")
    
    # Ensure database is initialized
    if not db.is_initialized:
        db.initialize()
    
    # Get async session using context manager
    async for session in db.get_session():
        try:
            # Check if users already exist (idempotent seeding)
            result = await session.execute(select(UserModel).limit(1))
            existing_user = result.scalars().first()
            
            if existing_user:
                logger.info("  ⚠ Users already exist, skipping...")
                break
            
            # Create users
            # BaseModel auto-adds: id, created_at, updated_at, is_deleted
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
            
            # Flush to get IDs before creating profiles
            await session.flush()
            
            logger.info(f"  Created {len(users)} users, generating profiles...")
            
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
            
            # Commit transaction
            await session.commit()
            
            logger.info(f"  ✓ Created {len(users)} users and {len(profiles)} profiles")
            
        except Exception as e:
            # Rollback on error
            await session.rollback()
            logger.error(f"  ✗ Error seeding users: {e}")
            import traceback
            traceback.print_exc()
            raise
        
        # CRITICAL: Break after first iteration
        break


async def main():
    """Main function to run seeder"""
    try:
        await seed_users()
        logger.info("✅ User seeding completed successfully")
    except Exception as e:
        logger.error(f"✗ User seeding failed: {e}")
        raise
    finally:
        # Clean up
        if db.is_initialized:
            await db.close()


if __name__ == "__main__":
    asyncio.run(main())