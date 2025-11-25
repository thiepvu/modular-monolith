"""
Domain events represent something important that happened in the domain.
"""

from abc import ABC
from datetime import datetime
from typing import Any, Dict
from uuid import UUID, uuid4


class DomainEvent(ABC):
    """
    Base domain event.
    Domain events are immutable records of something that happened.
    """
    
    def __init__(self):
        """Initialize domain event with ID and timestamp"""
        self.event_id: UUID = uuid4()
        self.occurred_at: datetime = datetime.utcnow()
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert event to dictionary.
        Useful for serialization and logging.
        
        Returns:
            Dictionary representation of event
        """
        return {
            "event_id": str(self.event_id),
            "event_type": self.__class__.__name__,
            "occurred_at": self.occurred_at.isoformat(),
        }
    
    def __repr__(self) -> str:
        """String representation"""
        return f"<{self.__class__.__name__}(id={self.event_id})>"