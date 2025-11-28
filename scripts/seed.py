#!/usr/bin/env python3
"""
Database seeder script with async support.
Seeds sample data for all modules using async DatabaseConnection.

Usage:
    python scripts/seed.py                  # Seed all modules
    python scripts/seed.py --module user    # Seed specific module
    python scripts/seed.py --module file    # Seed specific module
    python scripts/seed.py --list           # List available modules
"""
import sys
import asyncio
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

import logging
from sqlalchemy import text, select
from sqlalchemy.ext.asyncio import AsyncSession

# Import from YOUR project
from src.infrastructure.database.connection import db
from src.config.settings import get_settings

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

settings = get_settings()


# ============================================================================
# SEEDER FUNCTIONS (Async)
# ============================================================================

async def seed_users(session: AsyncSession):
    """
    Seed user data.
    """
    from src.modules.user_management.infrastructure.persistence.models import (
        UserModel, 
        UserProfileModel
    )
    
    logger.info("  Seeding users...")
    
    # Check if users already exist
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
            "hashed_password": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYBq.dIhuHu",  # "password"
            "is_active": True,
            "is_superuser": True
        },
        {
            "email": "user1@example.com",
            "username": "user1",
            "hashed_password": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYBq.dIhuHu",
            "is_active": True,
            "is_superuser": False
        },
        {
            "email": "user2@example.com",
            "username": "user2",
            "hashed_password": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYBq.dIhuHu",
            "is_active": True,
            "is_superuser": False
        },
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


async def seed_files(session: AsyncSession):
    """
    Seed file data.
    """
    from src.modules.file_management.infrastructure.persistence.models import FileModel
    from src.modules.user_management.infrastructure.persistence.models import UserModel
    
    logger.info("  Seeding files...")
    
    # Check if files already exist
    result = await session.execute(select(FileModel).limit(1))
    existing = result.scalars().first()
    
    if existing:
        logger.info("    ⚠ Files already exist, skipping...")
        return
    
    # Get first user as owner
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


# ============================================================================
# SEEDER REGISTRY
# ============================================================================

SEEDERS = {
    "user": seed_users,
    "file": seed_files,
}


# ============================================================================
# MAIN SEEDING LOGIC
# ============================================================================

async def verify_database() -> bool:
    """Verify database connection"""
    logger.info("Step 1: Verifying database connection...")
    
    if not db.is_initialized:
        db.initialize()
    
    try:
        async with db.engine.begin() as conn:
            result = await conn.execute(text("SELECT version()"))
            version = result.scalar()
            logger.info(f"  ✓ Connected to PostgreSQL")
            logger.info(f"  Version: {version}")
            return True
    except Exception as e:
        logger.error(f"  ✗ Database connection failed: {e}")
        return False


async def verify_tables_exist() -> bool:
    """Verify that tables exist (migrations have been run)"""
    logger.info("\nStep 2: Verifying tables exist...")
    
    if not db.is_initialized:
        db.initialize()
    
    try:
        async with db.engine.begin() as conn:
            for schema_name in settings.MODULE_SCHEMAS.values():
                result = await conn.execute(text(f"""
                    SELECT COUNT(*)
                    FROM information_schema.tables
                    WHERE table_schema = '{schema_name}'
                """))
                count = result.scalar()
                
                if count == 0:
                    logger.warning(f"  ⚠ No tables found in schema '{schema_name}'")
                    logger.warning("  Run migrations first: python scripts/migrate.py")
                    return False
                
                logger.info(f"  ✓ Schema '{schema_name}' has {count} tables")
        
        return True
    except Exception as e:
        logger.error(f"  ✗ Table verification failed: {e}")
        return False


async def seed_module(module_name: str) -> bool:
    """Seed a specific module"""
    if module_name not in SEEDERS:
        logger.error(f"✗ Unknown module: {module_name}")
        logger.info(f"Available modules: {', '.join(SEEDERS.keys())}")
        return False
    
    logger.info(f"\nSeeding module: {module_name}")
    logger.info("─" * 60)
    
    if not db.is_initialized:
        db.initialize()
    
    try:
        # Get async session
        async for session in db.get_session():
            try:
                # Run seeder
                await SEEDERS[module_name](session)
                await session.commit()
                logger.info(f"✓ Module '{module_name}' seeded successfully\n")
                return True
            except Exception as e:
                await session.rollback()
                logger.error(f"✗ Error seeding {module_name}: {e}")
                import traceback
                traceback.print_exc()
                return False
            finally:
                # CRITICAL: Break after first iteration
                break
    except Exception as e:
        logger.error(f"✗ Failed to get session: {e}")
        return False


async def seed_all_modules() -> bool:
    """Seed all modules in order"""
    logger.info("\n" + "=" * 60)
    logger.info("SEEDING ALL MODULES")
    logger.info("=" * 60)
    
    success_count = 0
    failed_count = 0
    
    # Seed in order (users first, then files)
    for module_name in SEEDERS.keys():
        if await seed_module(module_name):
            success_count += 1
        else:
            failed_count += 1
    
    logger.info("=" * 60)
    logger.info("SEEDING SUMMARY")
    logger.info("=" * 60)
    logger.info(f"✓ Successful: {success_count}")
    if failed_count > 0:
        logger.info(f"✗ Failed: {failed_count}")
    logger.info("=" * 60)
    
    return failed_count == 0


async def main():
    """Main seeding function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Database seeder (async)")
    parser.add_argument(
        "--module",
        type=str,
        help="Seed specific module",
        choices=list(SEEDERS.keys())
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available modules"
    )
    args = parser.parse_args()
    
    logger.info("=" * 60)
    logger.info("DATABASE SEEDER (Async)")
    logger.info("=" * 60)
    
    # List modules
    if args.list:
        logger.info("\nAvailable modules:")
        for module in SEEDERS.keys():
            logger.info(f"  - {module}")
        return 0
    
    try:
        # Pre-checks
        logger.info("\nRunning pre-checks...")
        logger.info("─" * 60)
        
        if not await verify_database():
            logger.error("\n✗ Database check failed")
            return 1
        
        if not await verify_tables_exist():
            logger.error("\n✗ Tables check failed")
            logger.error("Run migrations first: python scripts/migrate.py")
            return 1
        
        logger.info("\n✓ All pre-checks passed")
        
        # Seed
        if args.module:
            success = await seed_module(args.module)
        else:
            success = await seed_all_modules()
        
        if success:
            logger.info(f"\n✅ SEEDING COMPLETED SUCCESSFULLY!")
            return 0
        else:
            logger.error(f"\n✗ SEEDING FAILED")
            return 1
            
    except Exception as e:
        logger.error(f"\n✗ Seeding failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        # Clean up
        if db.is_initialized:
            await db.close()


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)