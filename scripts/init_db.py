#!/usr/bin/env python3
"""
Initialize database schemas using async DatabaseConnection.
Works with your async-only connection.py
"""
import sys
import asyncio
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import logging
from sqlalchemy import text

# Import from YOUR project - adjust these paths to match your structure
from infrastructure.database.connection import DatabaseConnection 
from config.settings import get_settings

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

settings = get_settings()


async def verify_connection(db: DatabaseConnection) -> bool:
    """Verify database connection works"""
    logger.info("Verifying database connection...")
    
    try:
        async with db.engine.begin() as conn:
            result = await conn.execute(text("SELECT version()"))
            version = result.scalar()
            logger.info(f"✓ Database connection successful")
            logger.info(f"  PostgreSQL version: {version}")
            return True
    except Exception as e:
        logger.error(f"✗ Database connection failed: {e}")
        logger.error("\nTroubleshooting:")
        logger.error("  1. Is PostgreSQL running? → docker-compose ps")
        logger.error("  2. Check DATABASE_URL in .env")
        logger.error("  3. Try: docker-compose up -d")
        return False


async def list_schemas(db: DatabaseConnection) -> list:
    """List all existing schemas in database"""
    logger.info("\nListing existing schemas...")
    
    async with db.engine.begin() as conn:
        result = await conn.execute(text("""
            SELECT schema_name 
            FROM information_schema.schemata 
            WHERE schema_name NOT IN (
                'information_schema', 'pg_catalog', 'pg_toast',
                'pg_temp_1', 'pg_toast_temp_1'
            )
            ORDER BY schema_name
        """))
        
        schemas = [row[0] for row in result.fetchall()]
        
        if schemas:
            logger.info("  Found schemas:")
            for schema in schemas:
                logger.info(f"    - {schema}")
        else:
            logger.info("  No custom schemas found")
        
        return schemas


async def create_schemas(db: DatabaseConnection):
    """Create all module schemas defined in settings"""
    logger.info("\n" + "="*60)
    logger.info("Creating module schemas")
    logger.info("="*60)
    
    async with db.engine.begin() as conn:
        for module_name, schema_name in settings.MODULE_SCHEMAS.items():
            try:
                await conn.execute(
                    text(f"CREATE SCHEMA IF NOT EXISTS {schema_name}")
                )
                logger.info(f"✓ Schema '{schema_name}' ready (module: {module_name})")
            except Exception as e:
                logger.error(f"✗ Failed to create schema '{schema_name}': {e}")
                raise
        
        # Commit happens automatically with begin()
    
    logger.info("✓ All schemas created successfully")


async def verify_all_schemas(db: DatabaseConnection) -> bool:
    """Verify all required schemas exist"""
    logger.info("\n" + "="*60)
    logger.info("Verifying schemas")
    logger.info("="*60)
    
    existing = await list_schemas(db)
    required = set(settings.MODULE_SCHEMAS.values())
    
    missing = required - set(existing)
    
    if missing:
        logger.error(f"✗ Missing schemas: {missing}")
        return False
    
    logger.info("✓ All required schemas verified:")
    for module, schema in settings.MODULE_SCHEMAS.items():
        logger.info(f"  ✓ {module:12} → {schema}")
    
    return True


async def show_database_info(db: DatabaseConnection):
    """Show database information"""
    logger.info("\n" + "="*60)
    logger.info("Database Information")
    logger.info("="*60)
    
    async with db.engine.begin() as conn:
        # Get database size
        result = await conn.execute(text("""
            SELECT pg_size_pretty(pg_database_size(current_database())) as size
        """))
        db_size = result.scalar()
        
        # Get table count per schema
        schema_info = {}
        for schema_name in settings.MODULE_SCHEMAS.values():
            result = await conn.execute(text(f"""
                SELECT COUNT(*)
                FROM information_schema.tables
                WHERE table_schema = '{schema_name}'
            """))
            count = result.scalar()
            schema_info[schema_name] = count
    
    logger.info(f"Database size: {db_size}")
    logger.info("\nTables per schema:")
    for schema, count in schema_info.items():
        logger.info(f"  {schema:20} → {count} tables")


async def main():
    """Main initialization function"""
    logger.info("="*60)
    logger.info("DATABASE INITIALIZATION")
    logger.info("="*60)
    
    # Extract database info from URL (safely)
    db_info = settings.DATABASE_URL.split('@')[-1] if '@' in settings.DATABASE_URL else 'configured'
    logger.info(f"Target: {db_info}")
    logger.info(f"Modules: {', '.join(settings.MODULE_SCHEMAS.keys())}")
    logger.info(f"Schemas: {len(settings.MODULE_SCHEMAS)}")
    logger.info("="*60)
    
    # Create database connection instance
    db = DatabaseConnection()
    
    try:
        # Step 1: Initialize connection
        logger.info("\nStep 1: Initializing database connection...")
        db.initialize()
        logger.info("✓ Connection initialized")
        
        # Step 2: Verify connection works
        logger.info("\nStep 2: Testing connection...")
        if not await verify_connection(db):
            logger.error("\n✗ Cannot connect to database. Aborting.")
            sys.exit(1)
        
        # Step 3: Show existing schemas
        logger.info("\nStep 3: Checking existing schemas...")
        await list_schemas(db)
        
        # Step 4: Create required schemas
        logger.info("\nStep 4: Creating schemas...")
        await create_schemas(db)
        
        # Step 5: Verify all schemas created
        logger.info("\nStep 5: Final verification...")
        if not await verify_all_schemas(db):
            logger.error("\n✗ Schema verification failed")
            sys.exit(1)
        
        # Step 6: Show database info
        try:
            await show_database_info(db)
        except Exception as e:
            logger.warning(f"Could not retrieve database info: {e}")
        
        # Success!
        logger.info("\n" + "="*60)
        logger.info("✅ DATABASE INITIALIZATION COMPLETE!")
        logger.info("="*60)
        
        logger.info("\n📋 Next Steps:")
        logger.info("─" * 60)
        logger.info("\n1️⃣  Create initial migration:")
        logger.info("   python scripts/migrate.py --create 'initial migration'")
        
        logger.info("\n2️⃣  Run migrations:")
        logger.info("   python scripts/migrate.py")
        
        logger.info("\n3️⃣  Seed database:")
        logger.info("   python scripts/seed.py")
        
        logger.info("\n4️⃣  Start application:")
        logger.info("   uvicorn main:app --reload")
        
        logger.info("\n" + "="*60)
        
        return 0
        
    except KeyboardInterrupt:
        logger.info("\n\n⚠️  Interrupted by user")
        return 1
        
    except Exception as e:
        logger.error(f"\n✗ Initialization failed: {e}")
        logger.error("\nFull error:")
        import traceback
        traceback.print_exc()
        
        logger.error("\n" + "="*60)
        logger.error("TROUBLESHOOTING TIPS:")
        logger.error("="*60)
        logger.error("1. Check PostgreSQL is running:")
        logger.error("   docker-compose ps")
        logger.error("\n2. Verify DATABASE_URL in .env:")
        logger.error("   Should be: postgresql+asyncpg://user:pass@host:port/dbname")
        logger.error("\n3. Check database exists:")
        logger.error("   psql -U postgres -l")
        logger.error("\n4. Try recreating containers:")
        logger.error("   docker-compose down && docker-compose up -d")
        logger.error("="*60)
        
        return 1
        
    finally:
        # Always clean up connection
        if db.is_initialized:
            logger.info("\nCleaning up...")
            await db.close()
            logger.info("✓ Connection closed")


if __name__ == "__main__":
    # Run async main and exit with proper code
    exit_code = asyncio.run(main())
    sys.exit(exit_code)