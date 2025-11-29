#!/usr/bin/env python3
"""
Database seeder script with async support - DEBUG VERSION.
Adds detailed error logging to identify issues.

Usage:
    python scripts/seed_debug.py                  # Seed all modules
    python scripts/seed_debug.py --module user    # Seed specific module
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

# MORE VERBOSE LOGGING
logging.basicConfig(
    level=logging.DEBUG,  # Changed to DEBUG
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

settings = get_settings()


# ============================================================================
# SEEDER REGISTRY
# ============================================================================

logger.info("=" * 60)
logger.info("IMPORTING SEEDER FUNCTIONS")
logger.info("=" * 60)

try:
    logger.info("Importing user seeder...")
    from modules.user_management.infrastructure.seeds import seed_users
    logger.info("✓ User seeder imported")
except Exception as e:
    logger.error(f"✗ Failed to import user seeder: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

try:
    logger.info("Importing file seeder...")
    from modules.file_management.infrastructure.seeds import seed_files
    logger.info("✓ File seeder imported")
except Exception as e:
    logger.error(f"✗ Failed to import file seeder: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

SEEDERS = {
    "user": seed_users,
    "file": seed_files,
}

logger.info(f"✓ Registered {len(SEEDERS)} seeders")


# ============================================================================
# MAIN SEEDING LOGIC
# ============================================================================

async def verify_database() -> bool:
    """Verify database connection"""
    logger.info("\nStep 1: Verifying database connection...")
    
    try:
        if not db.is_initialized:
            logger.info("  Initializing database...")
            db.initialize()
            logger.info("  ✓ Database initialized")
        
        async with db.engine.begin() as conn:
            result = await conn.execute(text("SELECT version()"))
            version = result.scalar()
            logger.info(f"  ✓ Connected to PostgreSQL")
            logger.info(f"  Version: {version}")
            return True
    except Exception as e:
        logger.error(f"  ✗ Database connection failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def verify_tables_exist() -> bool:
    """Verify that tables exist (migrations have been run)"""
    logger.info("\nStep 2: Verifying tables exist...")
    
    try:
        if not db.is_initialized:
            db.initialize()
        
        async with db.engine.begin() as conn:
            logger.info(f"  Checking schemas: {settings.MODULE_SCHEMAS}")
            
            for module_name, schema_name in settings.MODULE_SCHEMAS.items():
                logger.info(f"  Checking schema '{schema_name}' for module '{module_name}'...")
                
                result = await conn.execute(text(f"""
                    SELECT table_name
                    FROM information_schema.tables
                    WHERE table_schema = '{schema_name}'
                    ORDER BY table_name
                """))
                tables = [row[0] for row in result.fetchall()]
                
                if not tables:
                    logger.warning(f"  ⚠ No tables found in schema '{schema_name}'")
                    logger.warning("  Run migrations first: python scripts/migrate.py")
                    return False
                
                logger.info(f"  ✓ Schema '{schema_name}' has {len(tables)} tables:")
                for table in tables:
                    logger.info(f"    - {table}")
        
        return True
    except Exception as e:
        logger.error(f"  ✗ Table verification failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def seed_module(module_name: str) -> bool:
    """
    Seed a specific module with detailed error logging.
    """
    if module_name not in SEEDERS:
        logger.error(f"✗ Unknown module: {module_name}")
        logger.info(f"Available modules: {', '.join(SEEDERS.keys())}")
        return False
    
    logger.info(f"\n{'=' * 60}")
    logger.info(f"SEEDING MODULE: {module_name}")
    logger.info("=" * 60)
    
    try:
        if not db.is_initialized:
            logger.info("  Initializing database...")
            db.initialize()
        
        logger.info("  Getting database session...")
        
        # Get async session
        async for session in db.get_session():
            try:
                logger.info(f"  ✓ Session created")
                logger.info(f"  Calling seeder function: {SEEDERS[module_name].__name__}")
                
                # Run seeder
                await SEEDERS[module_name](session)
                
                logger.info("  Committing transaction...")
                await session.commit()
                logger.info(f"  ✓ Transaction committed")
                
                logger.info(f"✓ Module '{module_name}' seeded successfully\n")
                return True
                
            except Exception as e:
                logger.error(f"✗ Error seeding {module_name}: {e}")
                logger.error(f"  Error type: {type(e).__name__}")
                logger.error("  Full traceback:")
                import traceback
                traceback.print_exc()
                
                logger.info("  Rolling back transaction...")
                await session.rollback()
                logger.info("  ✓ Transaction rolled back")
                
                return False
            finally:
                logger.debug("  Breaking from session loop")
                break
                
    except Exception as e:
        logger.error(f"✗ Failed to get session: {e}")
        logger.error("  Full traceback:")
        import traceback
        traceback.print_exc()
        return False


async def seed_all_modules() -> bool:
    """Seed all modules in order"""
    logger.info("\n" + "=" * 60)
    logger.info("SEEDING ALL MODULES")
    logger.info("=" * 60)
    
    success_count = 0
    failed_count = 0
    failed_modules = []
    
    # Seed in order (users first, then files - dependency order)
    for module_name in SEEDERS.keys():
        logger.info(f"\nProcessing module: {module_name}")
        
        if await seed_module(module_name):
            success_count += 1
        else:
            failed_count += 1
            failed_modules.append(module_name)
    
    logger.info("\n" + "=" * 60)
    logger.info("SEEDING SUMMARY")
    logger.info("=" * 60)
    logger.info(f"✓ Successful: {success_count}")
    if failed_count > 0:
        logger.info(f"✗ Failed: {failed_count}")
        logger.info(f"  Failed modules: {', '.join(failed_modules)}")
    logger.info("=" * 60)
    
    return failed_count == 0


async def main():
    """Main seeding function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Database seeder (async) - DEBUG VERSION")
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
    logger.info("DATABASE SEEDER (Async) - DEBUG MODE")
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
        logger.error(f"\n✗ Seeding failed with exception: {e}")
        logger.error("Full traceback:")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        # Clean up
        if db.is_initialized:
            logger.info("\nClosing database connection...")
            await db.close()
            logger.info("✓ Database connection closed")


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)