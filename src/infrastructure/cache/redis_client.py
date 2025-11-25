"""
Redis client for caching.
Optional component - can be used for performance optimization.
"""

from typing import Optional, Any
import json
import logging
from redis import asyncio as aioredis

from ...config.settings import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class RedisClient:
    """
    Redis client for caching operations.
    Provides simple key-value storage with TTL support.
    """
    
    def __init__(self):
        self._client: Optional[aioredis.Redis] = None
    
    async def initialize(self) -> None:
        """Initialize Redis connection"""
        try:
            self._client = await aioredis.from_url(
                f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}",
                password=settings.REDIS_PASSWORD,
                encoding="utf-8",
                decode_responses=True
            )
            await self._client.ping()
            logger.info("✓ Redis connection initialized")
        except Exception as e:
            logger.warning(f"Could not connect to Redis: {e}")
            self._client = None
    
    async def close(self) -> None:
        """Close Redis connection"""
        if self._client:
            await self._client.close()
            logger.info("✓ Redis connection closed")
    
    async def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None
        """
        if not self._client:
            return None
        
        try:
            value = await self._client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.error(f"Error getting from cache: {e}")
            return None
    
    async def set(
        self,
        key: str,
        value: Any,
        ttl: int = 3600
    ) -> bool:
        """
        Set value in cache.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds
            
        Returns:
            True if successful, False otherwise
        """
        if not self._client:
            return False
        
        try:
            serialized = json.dumps(value)
            await self._client.setex(key, ttl, serialized)
            return True
        except Exception as e:
            logger.error(f"Error setting cache: {e}")
            return False
    
    async def delete(self, key: str) -> bool:
        """
        Delete key from cache.
        
        Args:
            key: Cache key
            
        Returns:
            True if deleted, False otherwise
        """
        if not self._client:
            return False
        
        try:
            await self._client.delete(key)
            return True
        except Exception as e:
            logger.error(f"Error deleting from cache: {e}")
            return False
    
    async def exists(self, key: str) -> bool:
        """
        Check if key exists.
        
        Args:
            key: Cache key
            
        Returns:
            True if exists, False otherwise
        """
        if not self._client:
            return False
        
        try:
            return await self._client.exists(key) > 0
        except Exception as e:
            logger.error(f"Error checking cache existence: {e}")
            return False


# Global Redis client instance
redis_client = RedisClient()