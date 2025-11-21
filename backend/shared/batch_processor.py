"""Batch processing utilities for efficient bulk operations."""

import asyncio
import logging
from typing import Any, Callable, List, TypeVar

logger = logging.getLogger(__name__)

T = TypeVar("T")
R = TypeVar("R")


class BatchProcessor:
    """Utility for processing items in batches."""

    @staticmethod
    async def process_batch(
        items: List[T],
        processor: Callable[[List[T]], Any],
        batch_size: int = 100,
        max_concurrent: int = 4,
    ) -> List[Any]:
        """Process items in batches with optional concurrency.
        
        Args:
            items: List of items to process
            processor: Async function that processes a batch
            batch_size: Number of items per batch
            max_concurrent: Maximum concurrent batches
            
        Returns:
            List of results from all batches
        """
        semaphore = asyncio.Semaphore(max_concurrent)
        results = []

        async def process_with_semaphore(batch: List[T]) -> Any:
            async with semaphore:
                return await processor(batch)

        batches = [items[i : i + batch_size] for i in range(0, len(items), batch_size)]
        tasks = [process_with_semaphore(batch) for batch in batches]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Filter out exceptions
        valid_results = [r for r in results if not isinstance(r, Exception)]
        errors = [r for r in results if isinstance(r, Exception)]

        if errors:
            logger.warning(f"Encountered {len(errors)} errors during batch processing")

        return valid_results

    @staticmethod
    async def process_parallel(
        items: List[T],
        processor: Callable[[T], R],
        max_concurrent: int = 10,
    ) -> List[R]:
        """Process items in parallel with concurrency limit.
        
        Args:
            items: List of items to process
            processor: Async function that processes a single item
            max_concurrent: Maximum concurrent operations
            
        Returns:
            List of results
        """
        semaphore = asyncio.Semaphore(max_concurrent)

        async def process_with_semaphore(item: T) -> R:
            async with semaphore:
                return await processor(item)

        tasks = [process_with_semaphore(item) for item in items]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Filter out exceptions
        valid_results = [r for r in results if not isinstance(r, Exception)]
        errors = [r for r in results if isinstance(r, Exception)]

        if errors:
            logger.warning(f"Encountered {len(errors)} errors during parallel processing")

        return valid_results

    @staticmethod
    def chunk_list(items: List[T], chunk_size: int) -> List[List[T]]:
        """Split a list into chunks.
        
        Args:
            items: List to chunk
            chunk_size: Size of each chunk
            
        Returns:
            List of chunks
        """
        return [items[i : i + chunk_size] for i in range(0, len(items), chunk_size)]

