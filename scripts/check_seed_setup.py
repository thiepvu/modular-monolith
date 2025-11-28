#!/usr/bin/env python3
"""
Diagnostic script to check seed setup.
Run this before running seed.py to catch issues early.

Usage:
    python scripts/check_seed_setup.py
"""
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

print("=" * 70)
print("SEED SETUP DIAGNOSTIC")
print("=" * 70)

# ============================================================================
# 1. Check file structure
# ============================================================================
print("\n1. Checking file structure...")
print("-" * 70)

files_to_check = [
    "src/modules/user_management/infrastructure/persistence/models.py",
    "src/modules/user_management/infrastructure/persistence/seeds/seed_users.py",
    "src/modules/file_management/infrastructure/persistence/models.py",
    "src/modules/file_management/infrastructure/persistence/seed_files.py",
    "src/infrastructure/database/connection.py",
    "src/infrastructure/database/base.py",
    "src/config/settings.py",
]

all_exist = True
for file_path in files_to_check:
    full_path = project_root / file_path
    exists = full_path.exists()
    status = "✓" if exists else "✗"
    print(f"  {status} {file_path}")
    if not exists:
        all_exist = False

if not all_exist:
    print("\n✗ Some required files are missing!")
    print("  Make sure you've created all seeder files.")
    sys.exit(1)

print("\n✓ All required files exist")

# ============================================================================
# 2. Check imports
# ============================================================================
print("\n2. Checking imports...")
print("-" * 70)

try:
    print("  Importing settings...")
    from config.settings import get_settings
    settings = get_settings()
    print(f"    ✓ Settings imported")
    print(f"    DATABASE_URL: {settings.DATABASE_URL[:30]}...")
    print(f"    MODULE_SCHEMAS: {settings.MODULE_SCHEMAS}")
except Exception as e:
    print(f"  ✗ Failed to import settings: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

try:
    print("  Importing database connection...")
    from infrastructure.database.connection import db
    print("    ✓ Database connection imported")
except Exception as e:
    print(f"  ✗ Failed to import database connection: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

try:
    print("  Importing base models...")
    from infrastructure.database.base import MODULE_BASES
    print(f"    ✓ Base models imported")
    print(f"    Registered modules: {list(MODULE_BASES.keys())}")
except Exception as e:
    print(f"  ✗ Failed to import base models: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

try:
    print("  Importing user models...")
    from modules.user_management.infrastructure.persistence.models import (
        UserModel, UserProfileModel
    )
    print(f"    ✓ User models imported")
    print(f"    UserModel table: {UserModel.__tablename__}")
    print(f"    UserProfileModel table: {UserProfileModel.__tablename__}")
except Exception as e:
    print(f"  ✗ Failed to import user models: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

try:
    print("  Importing file models...")
    from modules.file_management.infrastructure.persistence.models import FileModel
    print(f"    ✓ File models imported")
    print(f"    FileModel table: {FileModel.__tablename__}")
except Exception as e:
    print(f"  ✗ Failed to import file models: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

try:
    print("  Importing user seeder...")
    from modules.user_management.infrastructure.persistence.seeds import seed_users
    print(f"    ✓ User seeder imported")
    print(f"    Function: {seed_users.__name__}")
    
    # Check signature
    import inspect
    sig = inspect.signature(seed_users)
    print(f"    Signature: {sig}")
    params = list(sig.parameters.keys())
    if len(params) != 1:
        print(f"    ✗ ERROR: seed_users should have 1 parameter, has {len(params)}")
        sys.exit(1)
    print(f"    ✓ Signature correct (accepts session parameter)")
except Exception as e:
    print(f"  ✗ Failed to import user seeder: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

try:
    print("  Importing file seeder...")
    from modules.file_management.infrastructure.persistence.seeds import seed_files
    print(f"    ✓ File seeder imported")
    print(f"    Function: {seed_files.__name__}")
    
    # Check signature
    import inspect
    sig = inspect.signature(seed_files)
    print(f"    Signature: {sig}")
    params = list(sig.parameters.keys())
    if len(params) != 1:
        print(f"    ✗ ERROR: seed_files should have 1 parameter, has {len(params)}")
        sys.exit(1)
    print(f"    ✓ Signature correct (accepts session parameter)")
except Exception as e:
    print(f"  ✗ Failed to import file seeder: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n✓ All imports successful")

# ============================================================================
# 3. Check database connection
# ============================================================================
print("\n3. Checking database connection...")
print("-" * 70)

import asyncio

async def check_db():
    try:
        print("  Initializing database...")
        db.initialize()
        print("  ✓ Database initialized")
        
        print("  Testing connection...")
        from sqlalchemy import text
        async with db.engine.begin() as conn:
            result = await conn.execute(text("SELECT 1"))
            result.scalar()
        print("  ✓ Connection successful")
        
        await db.close()
        print("  ✓ Database closed")
        
        return True
    except Exception as e:
        print(f"  ✗ Database connection failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if not asyncio.run(check_db()):
    print("\n✗ Database connection check failed")
    print("  Make sure PostgreSQL is running and DATABASE_URL is correct")
    sys.exit(1)

print("\n✓ Database connection successful")

# ============================================================================
# 4. Check if migrations have been run
# ============================================================================
print("\n4. Checking if migrations have been run...")
print("-" * 70)

async def check_tables():
    try:
        db.initialize()
        
        from sqlalchemy import text
        async with db.engine.begin() as conn:
            for module_name, schema_name in settings.MODULE_SCHEMAS.items():
                print(f"  Checking schema '{schema_name}'...")
                
                result = await conn.execute(text(f"""
                    SELECT table_name
                    FROM information_schema.tables
                    WHERE table_schema = '{schema_name}'
                    ORDER BY table_name
                """))
                tables = [row[0] for row in result.fetchall()]
                
                if not tables:
                    print(f"    ✗ No tables found in schema '{schema_name}'")
                    print(f"    Run migrations: python scripts/migrate.py")
                    await db.close()
                    return False
                
                print(f"    ✓ Found {len(tables)} tables:")
                for table in tables:
                    print(f"      - {table}")
        
        await db.close()
        return True
        
    except Exception as e:
        print(f"  ✗ Failed to check tables: {e}")
        import traceback
        traceback.print_exc()
        return False

if not asyncio.run(check_tables()):
    print("\n✗ Table check failed")
    sys.exit(1)

print("\n✓ All tables exist")

# ============================================================================
# Summary
# ============================================================================
print("\n" + "=" * 70)
print("DIAGNOSTIC SUMMARY")
print("=" * 70)
print("✓ All files exist")
print("✓ All imports successful")
print("✓ Database connection working")
print("✓ Tables exist")
print("\n✅ Setup looks good! You can run:")
print("   python scripts/seed.py")
print("=" * 70)