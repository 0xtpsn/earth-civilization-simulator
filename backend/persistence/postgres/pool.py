"""PostgreSQL connection pooling and database management."""

import logging
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)


class DatabasePool:
    """Manages PostgreSQL connection pool and sessions."""

    def __init__(
        self,
        connection_string: str,
        pool_size: int = 20,
        max_overflow: int = 10,
        pool_timeout: int = 30,
        pool_recycle: int = 3600,
        echo: bool = False,
    ):
        """Initialize database pool.
        
        Args:
            connection_string: PostgreSQL connection string
            pool_size: Number of connections to maintain
            max_overflow: Maximum overflow connections
            pool_timeout: Seconds to wait for connection
            pool_recycle: Seconds before recycling connection
            echo: Log SQL queries
        """
        self.connection_string = connection_string
        self.engine: Optional[AsyncEngine] = None
        self.session_factory: Optional[sessionmaker] = None
        self.pool_size = pool_size
        self.max_overflow = max_overflow
        self.pool_timeout = pool_timeout
        self.pool_recycle = pool_recycle
        self.echo = echo

    def initialize(self) -> None:
        """Initialize the connection pool."""
        logger.info(f"Initializing database pool: pool_size={self.pool_size}, max_overflow={self.max_overflow}")

        self.engine = create_async_engine(
            self.connection_string,
            pool_size=self.pool_size,
            max_overflow=self.max_overflow,
            pool_timeout=self.pool_timeout,
            pool_recycle=self.pool_recycle,
            pool_pre_ping=True,  # Verify connections before using
            echo=self.echo,
        )

        self.session_factory = sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False,
        )

        logger.info("Database pool initialized")

    async def get_session(self) -> AsyncSession:
        """Get a database session from the pool.
        
        Returns:
            Async database session
            
        Yields:
            Session that will be automatically closed
        """
        if self.session_factory is None:
            raise RuntimeError("Database pool not initialized. Call initialize() first.")

        async with self.session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    async def execute_batch(self, statements: list, batch_size: int = 1000) -> None:
        """Execute batch of statements efficiently.
        
        Args:
            statements: List of SQL statements or ORM operations
            batch_size: Number of statements per batch
        """
        async with self.session_factory() as session:
            for i in range(0, len(statements), batch_size):
                batch = statements[i : i + batch_size]
                for stmt in batch:
                    await session.execute(stmt)
                await session.commit()
                logger.debug(f"Executed batch {i // batch_size + 1}")

    async def close(self) -> None:
        """Close all connections in the pool."""
        if self.engine:
            await self.engine.dispose()
            logger.info("Database pool closed")

    def get_pool_status(self) -> dict:
        """Get current pool status.
        
        Returns:
            Dictionary with pool statistics
        """
        if not self.engine:
            return {"status": "not_initialized"}

        pool = self.engine.pool
        return {
            "size": pool.size(),
            "checked_in": pool.checkedin(),
            "checked_out": pool.checkedout(),
            "overflow": pool.overflow(),
            "invalid": pool.invalid(),
        }

