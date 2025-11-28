"""
Base SQLAlchemy models and declarative base.
All ORM models should inherit from BaseModel.
Supports multi-schema modular architecture.
"""

from datetime import datetime
from typing import Dict
from sqlalchemy import Column, DateTime, Boolean, MetaData
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
import uuid


class ModuleBase:
    """
    Container for module's declarative base and schema info.
    Each module gets its own Base with associated schema.
    """
    def __init__(self, module_name: str, schema_name: str):
        self.module_name = module_name
        self.schema_name = schema_name
        
        # Create declarative base for this module
        self.Base = declarative_base()
        
        # Set schema for all tables in this module
        self.Base.metadata.schema = schema_name
        
        # Create BaseModel for this module
        self.BaseModel = self._create_base_model()
    
    def _create_base_model(self):
        """Create BaseModel class for this module"""
        
        class BaseModel(self.Base):
            """
            Base model with common fields for all entities.
            Provides: id, created_at, updated_at, is_deleted
            """
            
            __abstract__ = True
            
            id = Column(
                UUID(as_uuid=True),
                primary_key=True,
                default=uuid.uuid4,
                nullable=False,
                comment="Primary key UUID"
            )
            
            created_at = Column(
                DateTime,
                default=datetime.utcnow,
                nullable=False,
                comment="Record creation timestamp"
            )
            
            updated_at = Column(
                DateTime,
                default=datetime.utcnow,
                onupdate=datetime.utcnow,
                nullable=False,
                comment="Record last update timestamp"
            )
            
            is_deleted = Column(
                Boolean,
                default=False,
                nullable=False,
                index=True,
                comment="Soft delete flag"
            )
            
            def __repr__(self) -> str:
                """String representation of model"""
                return f"<{self.__class__.__name__}(id={self.id})>"
            
            def soft_delete(self):
                """Mark record as deleted (soft delete)"""
                self.is_deleted = True
            
            def restore(self):
                """Restore soft-deleted record"""
                self.is_deleted = False
        
        return BaseModel


# Global registry of module bases
MODULE_BASES: Dict[str, ModuleBase] = {}


def register_module_base(module_name: str, schema_name: str) -> ModuleBase:
    """
    Register a module and get its Base and BaseModel.
    
    This function should be called at the top of each module's models.py file.
    
    Args:
        module_name: Name of the module (e.g., "user", "product")
        schema_name: PostgreSQL schema name (e.g., "user_schema", "product_schema")
    
    Returns:
        ModuleBase: Container with Base and BaseModel for defining models
        
    Example:
        # In modules/user/infrastructure/models.py
        from infrastructure.database.base import register_module_base
        
        module_base = register_module_base("user", "user_schema")
        
        # Inherit from BaseModel (has id, timestamps, is_deleted)
        class User(module_base.BaseModel):
            __tablename__ = "users"
            email = Column(String(255), unique=True, nullable=False)
            ...
        
        # Or inherit from Base directly (no common fields)
        class UserSession(module_base.Base):
            __tablename__ = "user_sessions"
            id = Column(Integer, primary_key=True)  # Custom ID
            ...
    """
    if module_name not in MODULE_BASES:
        MODULE_BASES[module_name] = ModuleBase(module_name, schema_name)
    
    return MODULE_BASES[module_name]


def get_module_base(module_name: str) -> ModuleBase:
    """
    Get the ModuleBase for a module.
    
    Args:
        module_name: Name of the module
        
    Returns:
        ModuleBase: The module's base
        
    Raises:
        KeyError: If module not registered
    """
    if module_name not in MODULE_BASES:
        raise KeyError(
            f"Module '{module_name}' not registered. "
            f"Call register_module_base() first."
        )
    return MODULE_BASES[module_name]


def get_combined_metadata() -> MetaData:
    """
    Get combined metadata from all registered modules.
    Used by Alembic for migrations.
    
    Returns:
        MetaData: Combined metadata containing all tables from all modules
    """
    combined = MetaData()
    
    for module_name, module_base in MODULE_BASES.items():
        for table in module_base.Base.metadata.tables.values():
            table.tometadata(combined)
    
    return combined


# ============================================================================
# Backward Compatibility
# ============================================================================

# Default Base for simple projects (single schema, no modules)
Base = declarative_base()


class BaseModel(Base):
    """
    Default BaseModel (single schema).
    
    For multi-schema setup, use register_module_base() instead.
    
    This is kept for backward compatibility or simple projects.
    """
    
    __abstract__ = True
    
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
        comment="Primary key UUID"
    )
    
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        comment="Record creation timestamp"
    )
    
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
        comment="Record last update timestamp"
    )
    
    is_deleted = Column(
        Boolean,
        default=False,
        nullable=False,
        index=True,
        comment="Soft delete flag"
    )
    
    def __repr__(self) -> str:
        """String representation of model"""
        return f"<{self.__class__.__name__}(id={self.id})>"
    
    def soft_delete(self):
        """Mark record as deleted (soft delete)"""
        self.is_deleted = True
    
    def restore(self):
        """Restore soft-deleted record"""
        self.is_deleted = False


# ============================================================================
# Exports
# ============================================================================

__all__ = [
    'Base',
    'BaseModel',
    'ModuleBase',
    'MODULE_BASES',
    'register_module_base',
    'get_module_base',
    'get_combined_metadata',
]