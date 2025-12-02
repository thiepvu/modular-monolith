"""
Session Context Management with ContextVar

Provides session management using ContextVar for async-safe, request-scoped sessions.
"""

from contextvars import ContextVar
from typing import Optional, Callable
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

# ContextVar that holds the current AsyncSession for the request
_CURRENT_SESSION: ContextVar[Optional[AsyncSession]] = ContextVar(
    "current_db_session", 
    default=None
)


def get_current_session() -> AsyncSession:
    """
    Return the AsyncSession bound to the current request context.
    
    This function is called by repositories to get the current session
    from the context without it being passed explicitly.
    
    Returns:
        AsyncSession: The current session from context
        
    Raises:
        RuntimeError: If called outside of an active session context
                     (i.e., outside of UnitOfWork context manager)
    """
    session = _CURRENT_SESSION.get()
    if session is None:
        raise RuntimeError(
            "No current DB session in context. "
            "Make sure you're calling this within a UnitOfWork context manager."
        )
    return session


def set_current_session(session: AsyncSession) -> None:
    """
    Set the current session in context.
    
    This is called by UnitOfWork when entering the context.
    
    Args:
        session: The AsyncSession to set in context
    """
    _CURRENT_SESSION.set(session)


def clear_current_session() -> None:
    """
    Clear the current session from context.
    
    This is called by UnitOfWork when exiting the context.
    """
    _CURRENT_SESSION.set(None)


# Optional: Session factory holder (if you need to store it globally)
_session_factory: Optional[async_sessionmaker[AsyncSession]] = None


def configure_session_factory(factory: async_sessionmaker[AsyncSession]) -> None:
    """
    Configure the global session factory.
    
    This should be called during application startup.
    
    Args:
        factory: The session factory to use
    """
    global _session_factory
    _session_factory = factory


def get_session_factory() -> async_sessionmaker[AsyncSession]:
    """
    Get the configured session factory.
    
    Returns:
        The session factory
        
    Raises:
        RuntimeError: If factory has not been configured
    """
    if _session_factory is None:
        raise RuntimeError(
            "Session factory not configured. "
            "Call configure_session_factory() during application startup."
        )
    return _session_factory
