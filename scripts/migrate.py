#!/usr/bin/env python3
"""
Alternative migration script with async support and better error handling.
Works with multi-schema MODULE_BASES architecture.

Usage:
    python scripts/migrate.py --create "message"  # Create migration
    python scripts/migrate.py                     # Upgrade to head
    python scripts/migrate.py --downgrade -1     # Downgrade one revision
    python scripts/migrate.py --current          # Show current
    python scripts/migrate.py --history          # Show history
"""
import sys
import os
import asyncio
from pathlib import Path

# Ensure we're in the right directory and add to path
project_root = Path(__file__).resolve().parent.parent
os.chdir(project_root)
sys.path.insert(0, str(project_root))

import logging
from sqlalchemy import text

# Import from YOUR project
from src.infrastructure.database.connection import DatabaseConnection
from src.infrastructure.database.base import MODULE_BASES
from src.config.settings import get_settings

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

settings = get_settings()

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


async def verify_database_connection() -> bool:
    """Verify database connection before migration"""
    logger.info("Step 1: Verifying database connection...")
    
    db = DatabaseConnection()
    try:
        db.initialize()
        
        async with db.engine.begin() as conn:
            result = await conn.execute(text("SELECT version()"))
            version = result.scalar()
            logger.info(f"  ✓ Connected to PostgreSQL")
            logger.info(f"  Version: {version}")
            return True
    except Exception as e:
        logger.error(f"  ✗ Database connection failed: {e}")
        logger.error("\n  Troubleshooting:")
        logger.error("  - Is PostgreSQL running? → docker-compose ps")
        logger.error("  - Check DATABASE_URL in .env")
        logger.error("  - Try: docker-compose up -d")
        return False
    finally:
        if db.is_initialized:
            await db.close()


async def verify_schemas_exist() -> bool:
    """Ensure all required schemas exist"""
    logger.info("\nStep 2: Verifying schemas exist...")
    
    db = DatabaseConnection()
    try:
        db.initialize()
        
        async with db.engine.begin() as conn:
            # Get schemas from MODULE_BASES
            for module_name, module_base in MODULE_BASES.items():
                schema_name = module_base.schema_name
                
                result = await conn.execute(text(f"""
                    SELECT schema_name 
                    FROM information_schema.schemata 
                    WHERE schema_name = '{schema_name}'
                """))
                exists = result.fetchone()
                
                if not exists:
                    logger.warning(f"  ⚠ Schema '{schema_name}' not found, creating...")
                    await conn.execute(text(f"CREATE SCHEMA {schema_name}"))
                    logger.info(f"  ✓ Created schema '{schema_name}'")
                else:
                    logger.info(f"  ✓ Schema '{schema_name}' exists")
        
        return True
    except Exception as e:
        logger.error(f"  ✗ Schema verification failed: {e}")
        return False
    finally:
        if db.is_initialized:
            await db.close()


def verify_models_loaded() -> bool:
    """Verify all models are loaded"""
    logger.info("\nStep 3: Verifying models are loaded...")
    
    try:
        # Import all models - ADJUST THESE IMPORTS TO YOUR PROJECT
        from src.modules.user_management.infrastructure.persistence import models as UserModel
        logger.info("  ✓ User management models loaded")
        
        from src.modules.file_management.infrastructure.persistence import models as FileModel
        logger.info("  ✓ File management models loaded")
        
        # Add more modules as you create them:
        # from src.modules.project_management.infrastructure.persistence import models as ProjectModel
        # logger.info("  ✓ Project management models loaded")
        
        return True
    except ImportError as e:
        logger.error(f"  ✗ Failed to import models: {e}")
        logger.error("\n  Troubleshooting:")
        logger.error("  - Check that model files exist")
        logger.error("  - Verify import paths in this script")
        logger.error("  - Make sure models call register_module_base()")
        return False


def verify_metadata() -> bool:
    """Verify metadata is properly configured"""
    logger.info("\nStep 4: Verifying metadata...")
    
    try:
        if not MODULE_BASES:
            logger.error("  ✗ No modules registered in MODULE_BASES")
            logger.error("  Make sure your models.py files call register_module_base()")
            return False
        
        from sqlalchemy import MetaData
        
        target_metadata = MetaData()
        total_tables = 0
        
        for module_name, module_base in MODULE_BASES.items():
            tables = list(module_base.Base.metadata.tables.keys())
            total_tables += len(tables)
            logger.info(f"  ✓ {module_name} ({module_base.schema_name}): {len(tables)} tables")
            
            # Show table names
            if tables:
                logger.info(f"    Tables: {', '.join(tables)}")
            
            # Copy to combined metadata
            for table in module_base.Base.metadata.tables.values():
                table.tometadata(target_metadata)
        
        logger.info(f"  ✓ Total: {total_tables} tables in metadata")
        
        if total_tables == 0:
            logger.warning("  ⚠ No tables found in metadata")
            logger.warning("  Make sure your models inherit from module_base.BaseModel")
        
        return total_tables > 0
        
    except Exception as e:
        logger.error(f"  ✗ Metadata error: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_alembic_command(args):
    """Run Alembic command"""
    logger.info("\nStep 5: Running Alembic migration...")
    logger.info("=" * 60)
    
    try:
        from alembic.config import Config
        from alembic import command
        
        # Create Alembic config
        alembic_cfg = Config("alembic.ini")
        
        # Note: Alembic uses ASYNC operations via env.py
        
        if args.create:
            logger.info(f"Creating migration: {args.create}")
            command.revision(
                alembic_cfg,
                message=args.create,
                autogenerate=True
            )
            logger.info(f"{Colors.OKGREEN}✓ Migration created successfully{Colors.ENDC}")
            
        elif args.downgrade:
            logger.info(f"Downgrading to: {args.downgrade}")
            command.downgrade(alembic_cfg, args.downgrade)
            logger.info(f"{Colors.OKGREEN}✓ Downgrade completed{Colors.ENDC}")
            
        elif args.current:
            logger.info("Current revision:")
            command.current(alembic_cfg)
            
        elif args.history:
            logger.info("Migration history:")
            command.history(alembic_cfg)
            
        else:  # Default: upgrade
            logger.info("Upgrading to head...")
            command.upgrade(alembic_cfg, "head")
            logger.info(f"{Colors.OKGREEN}✓ Upgrade completed{Colors.ENDC}")
        
        return True
        
    except Exception as e:
        logger.error(f"\n{Colors.FAIL}✗ Alembic error: {e}{Colors.ENDC}")
        logger.error("\nFull error details:")
        import traceback
        traceback.print_exc()
        
        logger.error("\n" + "=" * 60)
        logger.error("TROUBLESHOOTING TIPS:")
        logger.error("=" * 60)
        logger.error("1. Check that models.py files call register_module_base()")
        logger.error("2. Verify alembic/env.py imports MODULE_BASES correctly")
        logger.error("3. Check that alembic/env.py imports all model files")
        logger.error("4. Ensure models are registered BEFORE env.py runs")
        logger.error("5. Check alembic/script.py.mako exists")
        
        return False


async def main():
    """Main function with async pre-checks"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Migration script with async support and multi-schema"
    )
    parser.add_argument(
        "--create", 
        type=str, 
        help="Create new migration with message"
    )
    parser.add_argument(
        "--upgrade", 
        action="store_true", 
        help="Upgrade to head (default)"
    )
    parser.add_argument(
        "--downgrade", 
        type=str, 
        help="Downgrade to revision"
    )
    parser.add_argument(
        "--current", 
        action="store_true", 
        help="Show current revision"
    )
    parser.add_argument(
        "--history", 
        action="store_true", 
        help="Show migration history"
    )
    args = parser.parse_args()
    
    # Print header
    logger.info("=" * 60)
    logger.info("MIGRATION SCRIPT (Multi-Schema Support)")
    logger.info("=" * 60)
    logger.info(f"Working directory: {os.getcwd()}")
    logger.info(f"Python path: {sys.path[0]}")
    logger.info("=" * 60)
    
    # Run async pre-checks
    try:
        # Check 1: Database connection
        if not await verify_database_connection():
            logger.error("\n✗ Database connection check failed")
            return 1
        
        # Check 2: Schemas
        if not await verify_schemas_exist():
            logger.error("\n✗ Schema verification failed")
            return 1
        
        # Check 3: Models (sync)
        if not verify_models_loaded():
            logger.error("\n✗ Model import check failed")
            return 1
        
        # Check 4: Metadata (sync)
        if not verify_metadata():
            logger.error("\n✗ Metadata verification failed")
            return 1
        
        # All checks passed, run Alembic
        logger.info(f"\n{Colors.OKGREEN}✓ All pre-checks passed!{Colors.ENDC}")
        
        if not run_alembic_command(args):
            return 1
        
        # Success!
        logger.info("\n" + "=" * 60)
        logger.info(f"{Colors.OKGREEN}✅ Migration completed successfully!{Colors.ENDC}")
        logger.info("=" * 60)
        
        return 0
        
    except Exception as e:
        logger.error(f"\n{Colors.FAIL}✗ Migration failed: {e}{Colors.ENDC}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)