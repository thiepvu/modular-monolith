"""
File seeder function.
To be imported by main seed.py script.
"""
import logging
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ....infrastructure.persistence.models import FileModel
from modules.user_management.infrastructure.persistence.models import UserModel

logger = logging.getLogger(__name__)


async def seed_files(session: AsyncSession):
    """
    Seed file data.
    
    Args:
        session: AsyncSession instance (already created by seed.py)
    """
    logger.info("  Seeding files...")
    
    # Check if files already exist (idempotent)
    result = await session.execute(select(FileModel).limit(1))
    existing = result.scalars().first()
    
    if existing:
        logger.info("    ⚠ Files already exist, skipping...")
        return
    
    # Get first user as owner (must seed users first!)
    user_result = await session.execute(select(UserModel).limit(1))
    owner = user_result.scalars().first()
    
    if not owner:
        logger.warning("    ⚠ No users found! Seed users first.")
        return
    
    # Create files
    files_data = [
        {
            "name": "file1.txt",
            "original_name": "My Document.txt",
            "path": "/files/file1.txt",
            "size": 2048,
            "mime_type": "text/plain",
            "owner_id": owner.id,
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
            "owner_id": owner.id,
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
    
    logger.info(f"    ✓ Created {len(files)} files")