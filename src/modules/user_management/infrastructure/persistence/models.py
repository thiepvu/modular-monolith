"""User SQLAlchemy models"""

from sqlalchemy import Column, String, Boolean

from .....infrastructure.database.base import BaseModel


class UserModel(BaseModel):
    """User ORM model"""
    
    __tablename__ = "users"
    
    email = Column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
        comment="User email address"
    )
    username = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
        comment="Unique username"
    )
    first_name = Column(
        String(100),
        nullable=False,
        comment="User first name"
    )
    last_name = Column(
        String(100),
        nullable=False,
        comment="User last name"
    )
    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
        index=True,
        comment="Whether user is active"
    )
    
    def __repr__(self) -> str:
        return f"<UserModel(id={self.id}, username={self.username})>"