"""
Command pattern implementation.
Commands represent actions that change state.
"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Any
from pydantic import BaseModel

TResult = TypeVar("TResult")


class Command(BaseModel, ABC):
    """
    Base command.
    Commands are immutable requests to perform an action.
    """
    
    class Config:
        frozen = True  # Make command immutable


class CommandHandler(ABC, Generic[TResult]):
    """
    Base command handler.
    Handles execution of commands.
    """
    
    @abstractmethod
    async def handle(self, command: Command) -> TResult:
        """
        Handle command execution.
        
        Args:
            command: Command to execute
            
        Returns:
            Command execution result
        """
        pass