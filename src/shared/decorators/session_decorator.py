from functools import wraps
from typing import  Callable

from infrastructure.database.connection import db
from infrastructure.database.session_context import (
    set_current_session,
    clear_current_session,

)

# ============================================================================
# DECORATOR: Auto Session Injection
# ============================================================================

def with_session(func: Callable) -> Callable:
    """
    Decorator với automatic commit.
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        async for session in db.get_session():
            set_current_session(session)
            
            try:
                # Call function
                result = await func(*args, **kwargs)
                
                # Auto commit on success
                await session.commit()
                
                return result
            
            except Exception as e:
                # Auto rollback on error
                await session.rollback()
                raise
            
            finally:
                # Clear context
                clear_current_session()
    
    return wrapper
