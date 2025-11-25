"""
Specification pattern implementation.
Allows building complex queries in a reusable way.
"""

from abc import ABC, abstractmethod
from typing import TypeVar, Generic
from sqlalchemy import Select

T = TypeVar("T")


class Specification(ABC, Generic[T]):
    """
    Base specification interface.
    Specifications encapsulate query logic.
    """
    
    @abstractmethod
    def to_sqlalchemy(self, query: Select) -> Select:
        """
        Convert specification to SQLAlchemy query.
        
        Args:
            query: Base SQLAlchemy query
            
        Returns:
            Modified query with specification applied
        """
        pass
    
    def and_(self, other: "Specification[T]") -> "Specification[T]":
        """
        Combine specifications with AND.
        
        Args:
            other: Other specification
            
        Returns:
            Combined specification
        """
        return AndSpecification(self, other)
    
    def or_(self, other: "Specification[T]") -> "Specification[T]":
        """
        Combine specifications with OR.
        
        Args:
            other: Other specification
            
        Returns:
            Combined specification
        """
        return OrSpecification(self, other)
    
    def not_(self) -> "Specification[T]":
        """
        Negate specification.
        
        Returns:
            Negated specification
        """
        return NotSpecification(self)


class AndSpecification(Specification[T]):
    """AND combination of specifications"""
    
    def __init__(self, left: Specification[T], right: Specification[T]):
        self.left = left
        self.right = right
    
    def to_sqlalchemy(self, query: Select) -> Select:
        query = self.left.to_sqlalchemy(query)
        query = self.right.to_sqlalchemy(query)
        return query


class OrSpecification(Specification[T]):
    """OR combination of specifications"""
    
    def __init__(self, left: Specification[T], right: Specification[T]):
        self.left = left
        self.right = right
    
    def to_sqlalchemy(self, query: Select) -> Select:
        # This is simplified - actual OR logic would be more complex
        # You would need to combine WHERE clauses with OR
        return query


class NotSpecification(Specification[T]):
    """NOT negation of specification"""
    
    def __init__(self, spec: Specification[T]):
        self.spec = spec
    
    def to_sqlalchemy(self, query: Select) -> Select:
        # This is simplified - actual NOT logic would be more complex
        return query


# Example specifications for common use cases
class ActiveEntitySpecification(Specification[T]):
    """Specification for active (non-deleted) entities"""
    
    def __init__(self, model_class):
        self.model_class = model_class
    
    def to_sqlalchemy(self, query: Select) -> Select:
        return query.where(self.model_class.is_deleted == False)


class CreatedAfterSpecification(Specification[T]):
    """Specification for entities created after a date"""
    
    def __init__(self, model_class, date):
        self.model_class = model_class
        self.date = date
    
    def to_sqlalchemy(self, query: Select) -> Select:
        return query.where(self.model_class.created_at >= self.date)