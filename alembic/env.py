"""
Alembic migration environment configuration.
This file is used by Alembic to configure migrations.
Works with multi-schema MODULE_BASES architecture.
"""

from logging.config import fileConfig
from sqlalchemy import pool, MetaData, create_engine, text
from sqlalchemy.engine import Connection
from alembic import context
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

# Import MODULE_BASES registry
from src.infrastructure.database.base import MODULE_BASES

# Import all module models to register them in MODULE_BASES
# This is CRUCIAL - importing models registers them
try:
    from src.modules.user_management.infrastructure.persistence import models as UserModel
    print("✓ Loaded user_management models")
except ImportError as e:
    print(f"⚠ Could not import user_management models: {e}")

try:
    from src.modules.file_management.infrastructure.persistence import models as FileModel
    print("✓ Loaded file_management models")
except ImportError as e:
    print(f"⚠ Could not import file_management models: {e}")

# Add more modules as needed:
# try:
#     from src.modules.project_management.infrastructure.persistence import models as ProjectModel
#     print("✓ Loaded project_management models")
# except ImportError as e:
#     print(f"⚠ Could not import project_management models: {e}")

# Alembic Config object
config = context.config

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Combine metadata from all registered modules
target_metadata = MetaData()

print(f"\nRegistered modules: {list(MODULE_BASES.keys())}")

for module_name, module_base in MODULE_BASES.items():
    tables = list(module_base.Base.metadata.tables.keys())
    print(f"  {module_name}: {len(tables)} tables - {tables}")
    
    # Copy tables to target_metadata
    for table in module_base.Base.metadata.tables.values():
        table.tometadata(target_metadata)

print(f"Total tables in target_metadata: {len(target_metadata.tables)}\n")


def get_url() -> str:
    """
    Get database URL from settings.
    Converts async URL to sync if needed.
    """
    from src.config.settings import get_settings
    settings = get_settings()
    
    url = settings.DATABASE_URL
    
    # Convert async URL to sync for Alembic
    if "postgresql+asyncpg://" in url:
        url = url.replace("postgresql+asyncpg://", "postgresql://")
        print(f"Converted async URL to sync for Alembic")
    
    return url


def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.
    This configures the context with just a URL and not an Engine.
    """
    url = get_url()
    
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
        include_schemas=True,  # Important for multi-schema
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode using sync engine.
    
    This uses a sync (non-async) SQLAlchemy engine which is simpler
    and avoids event loop conflicts.
    """
    url = get_url()
    
    # Create sync engine
    connectable = create_engine(
        url,
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        # Create schemas if they don't exist
        for module_name, module_base in MODULE_BASES.items():
            schema_name = module_base.schema_name
            print(f"Creating schema if not exists: {schema_name}")
            
            connection.execute(
                text(f"CREATE SCHEMA IF NOT EXISTS {schema_name}")
            )
        
        connection.commit()
        
        # Configure and run migrations
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
            include_schemas=True,
        )

        with context.begin_transaction():
            context.run_migrations()
    
    connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()