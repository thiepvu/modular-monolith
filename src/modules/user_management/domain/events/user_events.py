"""User domain events"""

from typing import Dict, Any, Optional
from uuid import UUID

from .....core.domain.events import DomainEvent


class UserCreatedEvent(DomainEvent):
    """User created domain event"""
    
    def __init__(self, user_id: UUID, email: str):
        """
        Initialize user created event.
        
        Args:
            user_id: User UUID
            email: User email address
        """
        super().__init__()
        self.user_id = user_id
        self.email = email
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary"""
        data = super().to_dict()
        data.update({
            "user_id": str(self.user_id),
            "email": self.email
        })
        return data


class UserUpdatedEvent(DomainEvent):
    """User updated domain event"""
    
    def __init__(self, user_id: UUID, changes: Optional[Dict[str, Any]] = None):
        """
        Initialize user updated event.
        
        Args:
            user_id: User UUID
            changes: Dictionary of changes made
        """
        super().__init__()
        self.user_id = user_id
        self.changes = changes or {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary"""
        data = super().to_dict()
        data.update({
            "user_id": str(self.user_id),
            "changes": self.changes
        })
        return data


class UserActivatedEvent(DomainEvent):
    """User activated domain event"""
    
    def __init__(self, user_id: UUID):
        """
        Initialize user activated event.
        
        Args:
            user_id: User UUID
        """
        super().__init__()
        self.user_id = user_id
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary"""
        data = super().to_dict()
        data.update({"user_id": str(self.user_id)})
        return data


class UserDeactivatedEvent(DomainEvent):
    """User deactivated domain event"""
    
    def __init__(self, user_id: UUID):
        """
        Initialize user deactivated event.
        
        Args:
            user_id: User UUID
        """
        super().__init__()
        self.user_id = user_id
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary"""
        data = super().to_dict()
        data.update({"user_id": str(self.user_id)})
        return data