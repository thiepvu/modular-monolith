"""Core interfaces (ports)"""

from .repositories import IRepository
from .unit_of_work import IUnitOfWork
from .services import IService

__all__ = ["IRepository", "IUnitOfWork", "IService"]