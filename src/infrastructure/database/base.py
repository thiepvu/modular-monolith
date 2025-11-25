"""
Base SQLAlchemy models and declarative base.
All ORM models should inherit from BaseModel.
"""

from datetime import datetime
from sqlalchemy import Column, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
import uuid

# Declarative base for all models
Base = declarative_base()


class BaseModel(Base):
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