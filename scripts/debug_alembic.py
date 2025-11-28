#!/usr/bin/env python3
"""
Script debug Alembic configuration
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

print("=" * 60)
print("Debugging Alembic Configuration")
print("=" * 60)

# Test 1: Import config
print("\n1. Testing config...")
try:
    from src.config import get_settings
    settings = get_settings()
    print(f"   ✓ Config loaded")
    print(f"   Database URL: {settings.DATABASE_URL[:30]}...")
    print(f"   Schemas: {settings.MODULE_SCHEMAS}")
except Exception as e:
    print(f"   ✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 2: Import database
print("\n2. Testing database module...")
try:
    from src.infrastructure.database.base import MODULE_BASES
    print(f"   ✓ Database module loaded")
    print(f"   Registered modules: {list(MODULE_BASES.keys())}")
except Exception as e:
    print(f"   ✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 3: Import models
print("\n3. Testing model imports...")
try:
    from src.modules.user_management.infrastructure.persistence import models as UserModel
    print(f"   ✓ User models loaded")
    from src.modules.file_management.infrastructure.persistence import models as FileModel
    print(f"   ✓ File models loaded")

except Exception as e:
    print(f"   ✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 4: Check metadata
print("\n4. Checking metadata...")
try:
    from sqlalchemy import MetaData
    target_metadata = MetaData()
    
    for module_name, base_obj in MODULE_BASES.items():
        schema = settings.MODULE_SCHEMAS[module_name]
        tables = list(base_obj.Base.metadata.tables.keys())
        print(f"\n   Module: {module_name} (schema: {schema})")
        print(f"   Tables: {tables}")
        
        for table_name in tables:
            table = base_obj.Base.metadata.tables[table_name]
            print(f"     - {table_name}")
            print(f"       Schema: {table.schema}")
            print(f"       Columns: {[c.name for c in table.columns]}")
            
        # Copy to combined metadata
        for table in base_obj.Base.metadata.tables.values():
            table.tometadata(target_metadata)
    
    print(f"\n   Combined metadata tables: {len(target_metadata.tables)}")
    for table_name in target_metadata.tables.keys():
        print(f"     - {table_name}")
        
except Exception as e:
    print(f"   ✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 5: Test Alembic env
print("\n5. Testing Alembic env.py...")
try:
    import importlib.util
    spec = importlib.util.spec_from_file_location("env", "alembic/env.py")
    env_module = importlib.util.module_from_spec(spec)
    print("   ✓ env.py can be loaded")
    print("   Note: Not executing to avoid side effects")
except Exception as e:
    print(f"   ✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("✅ All debug checks passed!")
print("=" * 60)
print("\nIf migration still fails, please share the full error message.")