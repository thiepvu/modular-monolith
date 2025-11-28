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
from sqlalchemy import text

# Import from YOUR project
from infrastructure.database.connection import db
from config.settings import get_settings

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

settings = get_settings()


# ============================================================================
# SEEDER REGISTRY
# ============================================================================

# Import seeder functions from each module
from modules.user_management.infrastructure.persistence.seeds import seed_users
from modules.file_management.infrastructure.persistence.seeds import seed_files

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
    """
    Seed a specific module.
    
    CRITICAL FIX: Pass session directly to seeder function.
    The seeder function expects: async def seed_xxx(session: AsyncSession)
    """
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
                # Run seeder - pass session directly
                await SEEDERS[module_name](session)
                # Commit is done here, not in seeder
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
    
    # Seed in order (users first, then files - dependency order)
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