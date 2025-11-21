"""Task queue for long-running async operations."""

import asyncio
import logging
from enum import Enum
from typing import Any, Callable, Dict, Optional
from uuid import UUID, uuid4

logger = logging.getLogger(__name__)


class TaskStatus(Enum):
    """Task status."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Task:
    """Represents a queued task."""

    def __init__(
        self,
        task_id: UUID,
        func: Callable,
        args: tuple,
        kwargs: dict,
        priority: int = 0,
    ):
        """Initialize task.
        
        Args:
            task_id: Unique task identifier
            func: Async function to execute
            args: Function arguments
            kwargs: Function keyword arguments
            priority: Task priority (lower = higher priority)
        """
        self.task_id = task_id
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.priority = priority
        self.status = TaskStatus.PENDING
        self.result: Optional[Any] = None
        self.error: Optional[Exception] = None
        self.created_at = asyncio.get_event_loop().time()
        self.completed_at: Optional[float] = None


class TaskQueue:
    """Async task queue for background jobs."""

    def __init__(self, max_workers: int = 4, max_queue_size: int = 1000):
        """Initialize task queue.
        
        Args:
            max_workers: Maximum concurrent workers
            max_queue_size: Maximum queue size
        """
        self.max_workers = max_workers
        self.max_queue_size = max_queue_size
        self._queue: asyncio.PriorityQueue = asyncio.PriorityQueue(maxsize=max_queue_size)
        self._tasks: Dict[UUID, Task] = {}
        self._workers: list[asyncio.Task] = []
        self._running = False

    async def start(self) -> None:
        """Start the task queue workers."""
        if self._running:
            return

        self._running = True
        for i in range(self.max_workers):
            worker = asyncio.create_task(self._worker(f"worker-{i}"))
            self._workers.append(worker)
        logger.info(f"Task queue started with {self.max_workers} workers")

    async def stop(self) -> None:
        """Stop the task queue workers."""
        self._running = False

        # Wait for queue to drain
        await self._queue.join()

        # Cancel workers
        for worker in self._workers:
            worker.cancel()

        await asyncio.gather(*self._workers, return_exceptions=True)
        self._workers.clear()
        logger.info("Task queue stopped")

    async def _worker(self, name: str) -> None:
        """Worker coroutine that processes tasks."""
        logger.debug(f"Task queue worker {name} started")

        while self._running:
            try:
                # Get task from queue
                try:
                    priority, task = await asyncio.wait_for(
                        self._queue.get(), timeout=1.0
                    )
                except asyncio.TimeoutError:
                    continue

                # Execute task
                task.status = TaskStatus.RUNNING
                try:
                    result = await task.func(*task.args, **task.kwargs)
                    task.result = result
                    task.status = TaskStatus.COMPLETED
                    logger.debug(f"Task {task.task_id} completed")
                except Exception as e:
                    task.error = e
                    task.status = TaskStatus.FAILED
                    logger.error(f"Task {task.task_id} failed: {e}", exc_info=True)
                finally:
                    task.completed_at = asyncio.get_event_loop().time()
                    self._queue.task_done()

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in task queue worker {name}: {e}", exc_info=True)

        logger.debug(f"Task queue worker {name} stopped")

    async def enqueue(
        self,
        func: Callable,
        *args,
        priority: int = 0,
        **kwargs,
    ) -> UUID:
        """Enqueue a task for execution.
        
        Args:
            func: Async function to execute
            *args: Function arguments
            priority: Task priority (lower = higher priority)
            **kwargs: Function keyword arguments
            
        Returns:
            Task ID
        """
        task_id = uuid4()
        task = Task(task_id, func, args, kwargs, priority)

        try:
            await self._queue.put((priority, task))
            self._tasks[task_id] = task
            logger.debug(f"Enqueued task {task_id} with priority {priority}")
            return task_id
        except asyncio.QueueFull:
            logger.error("Task queue is full")
            raise

    async def get_status(self, task_id: UUID) -> Optional[Dict[str, Any]]:
        """Get task status.
        
        Args:
            task_id: Task identifier
            
        Returns:
            Task status dictionary or None if not found
        """
        task = self._tasks.get(task_id)
        if not task:
            return None

        return {
            "task_id": str(task.task_id),
            "status": task.status.value,
            "priority": task.priority,
            "created_at": task.created_at,
            "completed_at": task.completed_at,
            "has_result": task.result is not None,
            "has_error": task.error is not None,
        }

    async def get_result(self, task_id: UUID, timeout: Optional[float] = None) -> Any:
        """Wait for task to complete and get result.
        
        Args:
            task_id: Task identifier
            timeout: Maximum time to wait (None = wait forever)
            
        Returns:
            Task result
            
        Raises:
            TimeoutError: If timeout exceeded
            Exception: If task failed
        """
        task = self._tasks.get(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")

        start_time = asyncio.get_event_loop().time()
        while task.status in (TaskStatus.PENDING, TaskStatus.RUNNING):
            if timeout:
                elapsed = asyncio.get_event_loop().time() - start_time
                if elapsed > timeout:
                    raise asyncio.TimeoutError(f"Task {task_id} timed out")

            await asyncio.sleep(0.1)

        if task.status == TaskStatus.COMPLETED:
            return task.result
        elif task.status == TaskStatus.FAILED:
            raise task.error or Exception(f"Task {task_id} failed")
        else:
            raise Exception(f"Task {task_id} in unexpected status: {task.status}")

    def get_queue_size(self) -> int:
        """Get current queue size.
        
        Returns:
            Number of tasks in queue
        """
        return self._queue.qsize()

