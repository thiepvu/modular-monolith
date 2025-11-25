"""
Query pattern implementation.
Queries represent read operations that don't change state.
"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from pydantic import BaseModel

TResult = TypeVar("TResult")


class Query(BaseModel, ABC):
    """
    Base query.
    Queries are immutable requests for data.
    """
    
    class Config:
        frozen = True  # Make query immutable


class QueryHandler(ABC, Generic[TResult]):
    """
    Base query handler.
    Handles execution of queries.
    """
    
    @abstractmethod
    async def handle(self, query: Query) -> TResult:
        """
        Handle query execution.
        
        Args:
            query: Query to execute
            
        Returns:
            Query result
        """
        pass