"""Base service class for application services"""

from abc import ABC
import logging


class BaseService(ABC):
    """
    Base application service.
    Services orchestrate domain logic and coordinate use cases.
    """
    
    def __init__(self):
        """Initialize service with logger"""
        self._logger = logging.getLogger(self.__class__.__name__)
    
    @property
    def logger(self) -> logging.Logger:
        """Get service logger"""
        return self._logger