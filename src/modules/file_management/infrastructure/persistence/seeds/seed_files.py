"""
File seeder using async database connection.
Works with multi-schema BaseModel architecture.
"""
import asyncio
import logging
from uuid import UUID
from sqlalchemy import select

# Import database connection
from src.infrastructure.database.connection import db

# Import models
from src.modules.file_management.infrastructure.persistence.models import FileModel
from src.modules.user_management.infrastructure.persistence.models import UserModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def seed_files():
    """
    Seed file data using async database connection.
    
    This function demonstrates proper async db context management
    with multi-schema BaseModel.
    """
    logger.info("Seeding files...")
    
    # Ensure database is initialized
    if not db.is_initialized:
        db.initialize()
    
    # Get async session using context manager
    async for session in db.get_session():
        try:
            # Check if files already exist (idempotent seeding)
            result = await session.execute(select(FileModel).limit(1))
            existing_file = result.scalars().first()
            
            if existing_file:
                logger.info("  ⚠ Files already exist, skipping...")
                break
            
            # Get first user as owner (must seed users first!)
            user_result = await session.execute(select(UserModel).limit(1))
            owner = user_result.scalars().first()
            
            if not owner:
                logger.warning("  ⚠ No users found! Please seed users first.")
                logger.warning("  Run: python scripts/seed_users.py")
                break
            
            logger.info(f"  Using user {owner.email} as file owner")
            
            # Create files
            # BaseModel auto-adds: id, created_at, updated_at, is_deleted
            files_data = [
                {
                    "name": "file1.txt",
                    "original_name": "My Document.txt",
                    "path": "/files/file1.txt",
                    "size": 2048,
                    "mime_type": "text/plain",
                    "owner_id": owner.id,  # Use actual user ID
                    "description": "A sample text document.",
                    "is_public": True,
                    "download_count": 0,
                    "shared_with": []
                },
                {
                    "name": "image1.png",
                    "original_name": "Picture.png",
                    "path": "/files/image1.png",
                    "size": 4096,
                    "mime_type": "image/png",
                    "owner_id": owner.id,  # Use actual user ID
                    "description": "A sample image file.",
                    "is_public": False,
                    "download_count": 0,
                    "shared_with": []
                },
                {
                    "name": "document1.pdf",
                    "original_name": "Report.pdf",
                    "path": "/files/document1.pdf",
                    "size": 8192,
                    "mime_type": "application/pdf",
                    "owner_id": owner.id,
                    "description": "A sample PDF document.",
                    "is_public": False,
                    "download_count": 5,
                    "shared_with": []
                },
            ]
            
            files = [FileModel(**data) for data in files_data]
            session.add_all(files)
            
            # Commit transaction
            await session.commit()
            
            logger.info(f"  ✓ Created {len(files)} files")
            
        except Exception as e:
            # Rollback on error
            await session.rollback()
            logger.error(f"  ✗ Error seeding files: {e}")
            import traceback
            traceback.print_exc()
            raise
        
        # CRITICAL: Break after first iteration
        break


async def main():
    """Main function to run seeder"""
    try:
        await seed_files()
        logger.info("✅ File seeding completed successfully")
    except Exception as e:
        logger.error(f"✗ File seeding failed: {e}")
        raise
    finally:
        # Clean up
        if db.is_initialized:
            await db.close()


if __name__ == "__main__":
    asyncio.run(main())