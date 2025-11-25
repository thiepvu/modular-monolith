"""Unit of Work interface"""

from abc import ABC, abstractmethod
from typing import Any


class IUnitOfWork(ABC):
    """
    Unit of Work interface for transaction management.
    Ensures atomic operations across multiple repositories.
    """
    
    @abstractmethod
    async def __aenter__(self) -> "IUnitOfWork":
        """
        Enter async context.
        
        Returns:
            Self
        """
        pass
    
    @abstractmethod
    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """
        Exit async context.
        
        Args:
            exc_type: Exception type if raised
            exc_val: Exception value if raised
            exc_tb: Exception traceback if raised
        """
        pass
    
    @abstractmethod
    async def commit(self) -> None:
        """
        Commit transaction.
        Saves all changes to the database.
        """
        pass
    
    @abstractmethod
    async def rollback(self) -> None:
        """
        Rollback transaction.
        Discards all changes.
        """
        pass
    
    @abstractmethod
    async def refresh(self, entity: Any) -> None:
        """
        Refresh entity state from database.
        
        Args:
            entity: Entity to refresh
        """
        pass