"""
Unit of Work implementation for transaction management.
Ensures atomic operations across multiple repositories.
"""

from typing import Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from core.interfaces.unit_of_work import IUnitOfWork
from infrastructure.database.session_context import get_current_session

logger = logging.getLogger(__name__)


class UnitOfWork(IUnitOfWork):
    """
    Unit of Work implementation with SQLAlchemy.
    Manages transactions and ensures data consistency.
    """
    
    def __init__(self):
        """
        Initialize Unit of Work.

        """
        self._is_committed = False
        self._is_rolled_back = False
    @property
    def _session(self) -> AsyncSession:
        """
        Lazy load session from ContextVar.
        
        Session được get mỗi khi property được access,
        đảm bảo session đã được set bởi @with_session decorator.
        
        Returns:
            AsyncSession from ContextVar
            
        Raises:
            RuntimeError: If no session in ContextVar
            
        Note:
            This is called AFTER repository is created,
            ensuring session is already set by decorator.
        """
        return get_current_session()
        
    async def __aenter__(self) -> "UnitOfWork":
        """
        Enter async context manager.
        
        Returns:
            Self
        """
        logger.debug("Starting Unit of Work transaction")
        return self
    
    async def __aexit__(
        self,
        exc_type: Any,
        exc_val: Any,
        exc_tb: Any
    ) -> None:
        """
        Exit async context manager.
        Commits on success, rolls back on exception.
        
        Args:
            exc_type: Exception type if raised
            exc_val: Exception value if raised
            exc_tb: Exception traceback if raised
        """
        if exc_type is not None:
            logger.warning(
                f"Exception in Unit of Work: {exc_type.__name__}: {exc_val}"
            )
            await self.rollback()
        else:
            if not self._is_committed and not self._is_rolled_back:
                await self.commit()
        
        logger.debug("Unit of Work transaction ended")
    
    async def commit(self) -> None:
        """
        Commit the transaction.
        Saves all changes to the database.
        """
        if self._is_rolled_back:
            logger.warning("Cannot commit - transaction already rolled back")
            return
        
        if self._is_committed:
            logger.warning("Transaction already committed")
            return
        
        try:
            await self._session.commit()
            self._is_committed = True
            logger.debug("Transaction committed successfully")
        except Exception as e:
            logger.error(f"Error committing transaction: {e}", exc_info=True)
            await self.rollback()
            raise
    
    async def rollback(self) -> None:
        """
        Rollback the transaction.
        Discards all changes.
        """
        if self._is_rolled_back:
            logger.warning("Transaction already rolled back")
            return
        
        try:
            await self._session.rollback()
            self._is_rolled_back = True
            logger.debug("Transaction rolled back")
        except Exception as e:
            logger.error(f"Error rolling back transaction: {e}", exc_info=True)
            raise
    
    async def refresh(self, entity: Any) -> None:
        """
        Refresh entity state from database.
        
        Args:
            entity: Entity to refresh
        """
        try:
            await self._session.refresh(entity)
            logger.debug(f"Refreshed entity: {entity.__class__.__name__}")
        except Exception as e:
            logger.error(f"Error refreshing entity: {e}", exc_info=True)
            raise
    
    async def flush(self) -> None:
        """
        Flush pending changes to database without committing.
        Useful for getting auto-generated IDs.
        """
        try:
            await self._session.flush()
            logger.debug("Session flushed")
        except Exception as e:
            logger.error(f"Error flushing session: {e}", exc_info=True)
            raise
    
    @property
    def session(self) -> AsyncSession:
        """
        Get the underlying session.
        
        Returns:
            SQLAlchemy async session
        """
        return self._session