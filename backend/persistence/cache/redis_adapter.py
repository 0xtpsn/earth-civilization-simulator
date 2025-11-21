"""Redis caching adapter with TTL and invalidation support."""

import json
import logging
from typing import Any, Optional, Pattern

import redis.asyncio as redis
from redis.asyncio import Redis

from backend.shared.interfaces import PersistenceAdapter

logger = logging.getLogger(__name__)


class RedisCache(PersistenceAdapter):
    """Redis-based caching adapter with TTL and pattern invalidation."""

    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
        password: Optional[str] = None,
        default_ttl: Optional[int] = None,  # Default TTL in seconds
    ):
        """Initialize Redis cache.
        
        Args:
            host: Redis host
            port: Redis port
            db: Redis database number
            password: Redis password
            default_ttl: Default TTL for cached items (None = no expiration)
        """
        self.host = host
        self.port = port
        self.db = db
        self.password = password
        self.default_ttl = default_ttl
        self.client: Optional[Redis] = None
        self._connected = False

    async def connect(self) -> None:
        """Connect to Redis."""
        if self._connected:
            return

        self.client = redis.Redis(
            host=self.host,
            port=self.port,
            db=self.db,
            password=self.password,
            decode_responses=True,
        )

        # Test connection
        await self.client.ping()
        self._connected = True
        logger.info(f"Connected to Redis at {self.host}:{self.port}")

    async def disconnect(self) -> None:
        """Disconnect from Redis."""
        if self.client:
            await self.client.close()
            self._connected = False
            logger.info("Disconnected from Redis")

    async def save(self, key: str, data: Any, ttl: Optional[int] = None) -> None:
        """Save data with the given key.
        
        Args:
            key: Cache key
            data: Data to cache (must be JSON serializable)
            ttl: Time to live in seconds (uses default_ttl if None)
        """
        if not self._connected:
            await self.connect()

        try:
            serialized = json.dumps(data)
            ttl_to_use = ttl if ttl is not None else self.default_ttl

            if ttl_to_use:
                await self.client.setex(key, ttl_to_use, serialized)
            else:
                await self.client.set(key, serialized)

            logger.debug(f"Cached data for key: {key} (TTL: {ttl_to_use})")
        except Exception as e:
            logger.error(f"Error caching data for key {key}: {e}", exc_info=True)
            raise

    async def load(self, key: str) -> Optional[Any]:
        """Load data by key.
        
        Args:
            key: Cache key
            
        Returns:
            Cached data or None if not found/expired
        """
        if not self._connected:
            await self.connect()

        try:
            serialized = await self.client.get(key)
            if serialized is None:
                return None

            return json.loads(serialized)
        except Exception as e:
            logger.error(f"Error loading cached data for key {key}: {e}", exc_info=True)
            return None

    async def delete(self, key: str) -> None:
        """Delete data by key.
        
        Args:
            key: Cache key
        """
        if not self._connected:
            await self.connect()

        try:
            await self.client.delete(key)
            logger.debug(f"Deleted cache key: {key}")
        except Exception as e:
            logger.error(f"Error deleting cache key {key}: {e}", exc_info=True)

    async def invalidate_pattern(self, pattern: str) -> int:
        """Invalidate all keys matching a pattern.
        
        Args:
            pattern: Redis key pattern (e.g., "npc:*", "economy:*")
            
        Returns:
            Number of keys deleted
        """
        if not self._connected:
            await self.connect()

        try:
            keys = []
            async for key in self.client.scan_iter(match=pattern):
                keys.append(key)

            if keys:
                deleted = await self.client.delete(*keys)
                logger.info(f"Invalidated {deleted} keys matching pattern: {pattern}")
                return deleted
            return 0
        except Exception as e:
            logger.error(f"Error invalidating pattern {pattern}: {e}", exc_info=True)
            return 0

    async def exists(self, key: str) -> bool:
        """Check if a key exists.
        
        Args:
            key: Cache key
            
        Returns:
            True if key exists, False otherwise
        """
        if not self._connected:
            await self.connect()

        return bool(await self.client.exists(key))

    async def get_ttl(self, key: str) -> Optional[int]:
        """Get remaining TTL for a key.
        
        Args:
            key: Cache key
            
        Returns:
            TTL in seconds, -1 if no expiration, None if key doesn't exist
        """
        if not self._connected:
            await self.connect()

        ttl = await self.client.ttl(key)
        return ttl if ttl >= 0 else None

    async def clear_all(self) -> None:
        """Clear all cached data (use with caution!)."""
        if not self._connected:
            await self.connect()

        await self.client.flushdb()
        logger.warning("Cleared all cache data")

