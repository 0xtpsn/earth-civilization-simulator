"""Event bus for pub/sub communication between engines with queue and backpressure."""

import asyncio
import logging
from collections import defaultdict
from typing import Any, Callable, Dict, List, Optional

logger = logging.getLogger(__name__)


class EventBus:
    """Pub/sub event bus for inter-engine communication with queue and backpressure."""

    def __init__(
        self,
        max_queue_size: int = 10000,
        max_history: int = 1000,
        worker_count: int = 4,
        backpressure_strategy: str = "drop",  # "drop", "block", "log"
    ):
        """Initialize the event bus.
        
        Args:
            max_queue_size: Maximum events in queue before backpressure
            max_history: Maximum events to keep in history
            worker_count: Number of async workers processing events
            backpressure_strategy: What to do when queue is full ("drop", "block", "log")
        """
        self._subscribers: Dict[str, List[Callable]] = defaultdict(list)
        self._event_history: List[Dict[str, Any]] = []
        self._max_history = max_history
        self._max_queue_size = max_queue_size
        self._queue: asyncio.Queue = asyncio.Queue(maxsize=max_queue_size)
        self._worker_count = worker_count
        self._workers: List[asyncio.Task] = []
        self._backpressure_strategy = backpressure_strategy
        self._running = False
        self._stats = {
            "published": 0,
            "processed": 0,
            "dropped": 0,
            "errors": 0,
        }

    async def start(self) -> None:
        """Start the event bus workers."""
        if self._running:
            return

        self._running = True
        for i in range(self._worker_count):
            worker = asyncio.create_task(self._worker(f"worker-{i}"))
            self._workers.append(worker)
        logger.info(f"Event bus started with {self._worker_count} workers")

    async def stop(self) -> None:
        """Stop the event bus workers."""
        self._running = False

        # Wait for queue to drain
        await self._queue.join()

        # Cancel workers
        for worker in self._workers:
            worker.cancel()

        await asyncio.gather(*self._workers, return_exceptions=True)
        self._workers.clear()
        logger.info("Event bus stopped")

    async def _worker(self, name: str) -> None:
        """Worker coroutine that processes events from the queue."""
        logger.debug(f"Event bus worker {name} started")

        while self._running:
            try:
                # Get event from queue (with timeout to check _running)
                try:
                    event_type, event_data = await asyncio.wait_for(
                        self._queue.get(), timeout=1.0
                    )
                except asyncio.TimeoutError:
                    continue

                # Process event
                await self._process_event(event_type, event_data)
                self._queue.task_done()
                self._stats["processed"] += 1

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in event bus worker {name}: {e}", exc_info=True)
                self._stats["errors"] += 1
                self._queue.task_done()

        logger.debug(f"Event bus worker {name} stopped")

    async def _process_event(self, event_type: str, event_data: Dict[str, Any]) -> None:
        """Process a single event by notifying all subscribers."""
        # Store in history
        event = {
            "type": event_type,
            "data": event_data,
            "timestamp": asyncio.get_event_loop().time(),
        }

        self._event_history.append(event)
        if len(self._event_history) > self._max_history:
            self._event_history.pop(0)

        # Notify subscribers
        subscribers = self._subscribers.get(event_type, [])
        subscribers_all = self._subscribers.get("*", [])  # Wildcard subscribers

        # Call all subscribers
        for handler in subscribers + subscribers_all:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(event_type, event_data)
                else:
                    handler(event_type, event_data)
            except Exception as e:
                logger.error(f"Error in event handler for {event_type}: {e}", exc_info=True)

    async def publish(self, event_type: str, event_data: Dict[str, Any]) -> bool:
        """Publish an event to all subscribers (non-blocking with backpressure).
        
        Args:
            event_type: Type/category of the event (e.g., "npc.action", "economy.price_change")
            event_data: Event payload
            
        Returns:
            True if event was queued, False if dropped due to backpressure
        """
        self._stats["published"] += 1

        try:
            # Try to put event in queue (non-blocking)
            self._queue.put_nowait((event_type, event_data))
            return True

        except asyncio.QueueFull:
            # Handle backpressure
            self._stats["dropped"] += 1

            if self._backpressure_strategy == "drop":
                logger.warning(f"Event queue full, dropping event: {event_type}")
                return False

            elif self._backpressure_strategy == "block":
                # Block until space available (with timeout)
                try:
                    await asyncio.wait_for(
                        self._queue.put((event_type, event_data)), timeout=5.0
                    )
                    return True
                except asyncio.TimeoutError:
                    logger.error(f"Timeout waiting for queue space: {event_type}")
                    return False

            elif self._backpressure_strategy == "log":
                logger.warning(f"Event queue full, logging event: {event_type}")
                # Still drop, but log the event data
                return False

            return False

    def publish_sync(self, event_type: str, event_data: Dict[str, Any]) -> None:
        """Publish an event synchronously (for immediate processing).
        
        Args:
            event_type: Type/category of the event
            event_data: Event payload
        """
        # Process immediately without queue
        asyncio.create_task(self._process_event(event_type, event_data))

    def subscribe(self, event_type: str, handler: Callable) -> None:
        """Subscribe to events of a specific type.
        
        Args:
            event_type: Event type to subscribe to (use "*" for all events)
            handler: Callable that takes (event_type, event_data) as arguments
        """
        self._subscribers[event_type].append(handler)
        logger.debug(f"Subscribed {handler.__name__} to {event_type}")

    def unsubscribe(self, event_type: str, handler: Callable) -> None:
        """Unsubscribe from events.
        
        Args:
            event_type: Event type to unsubscribe from
            handler: Handler to remove
        """
        if handler in self._subscribers[event_type]:
            self._subscribers[event_type].remove(handler)
            logger.debug(f"Unsubscribed {handler.__name__} from {event_type}")

    def get_event_history(
        self, event_type: Optional[str] = None, limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Get recent event history.
        
        Args:
            event_type: Filter by event type (None for all)
            limit: Maximum number of events to return
            
        Returns:
            List of recent events
        """
        events = self._event_history
        if event_type:
            events = [e for e in events if e["type"] == event_type]
        return events[-limit:]

    def get_stats(self) -> Dict[str, Any]:
        """Get event bus statistics.
        
        Returns:
            Dictionary with statistics
        """
        return {
            **self._stats,
            "queue_size": self._queue.qsize(),
            "queue_max": self._max_queue_size,
            "subscribers": {k: len(v) for k, v in self._subscribers.items()},
            "history_size": len(self._event_history),
        }
