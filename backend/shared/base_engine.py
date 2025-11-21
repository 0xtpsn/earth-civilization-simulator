"""Base engine class that all engines should inherit from with priority support."""

import logging
from typing import Any, Optional

from backend.shared.interfaces import Engine, EventPublisher, EventSubscriber
from backend.simulation_engine.event_bus import EventBus

logger = logging.getLogger(__name__)


class BaseEngine(Engine, EventPublisher):
    """Base class for all simulation engines.
    
    Provides common functionality:
    - Engine lifecycle (initialize, tick, shutdown)
    - Event publishing
    - Event subscription support
    - State management helpers
    - Priority and dependency support
    """

    def __init__(
        self,
        name: str,
        event_bus: Optional[EventBus] = None,
        priority: int = 0,
        weight: float = 1.0,
        dependencies: Optional[list[str]] = None,
    ):
        """Initialize the base engine.
        
        Args:
            name: Name of the engine
            event_bus: Event bus instance (will be set during initialization)
            priority: Engine priority (lower = higher priority, runs first)
            weight: Processing weight (affects time allocation)
            dependencies: List of engine names that must run before this one
        """
        self._name = name
        self._event_bus = event_bus
        self._initialized = False
        self.priority = priority
        self.weight = weight
        self.dependencies = dependencies or []

    @property
    def name(self) -> str:
        """Return the name of this engine."""
        return self._name

    async def initialize(self, state: Any) -> None:
        """Initialize the engine with the current world state.
        
        Args:
            state: The current world state
        """
        if self._initialized:
            logger.warning(f"Engine {self.name} already initialized")
            return

        logger.info(f"Initializing engine: {self.name}")
        await self._on_initialize(state)
        self._initialized = True

    async def tick(self, state: Any, delta_time: float) -> None:
        """Process one simulation tick.
        
        Args:
            state: The current world state
            delta_time: Time elapsed since last tick
        """
        if not self._initialized:
            raise RuntimeError(f"Engine {self.name} not initialized")

        await self._on_tick(state, delta_time)

    async def shutdown(self) -> None:
        """Clean up resources when shutting down."""
        if not self._initialized:
            return

        logger.info(f"Shutting down engine: {self.name}")
        await self._on_shutdown()
        self._initialized = False

    async def publish(self, event_type: str, event_data: dict[str, Any]) -> None:
        """Publish an event to the event bus.
        
        Args:
            event_type: Type/category of the event
            event_data: Event payload
        """
        if self._event_bus is None:
            logger.warning(
                f"Event bus not set for {self.name}, cannot publish event: {event_type}"
            )
            return

        await self._event_bus.publish(event_type, event_data)

    def set_event_bus(self, event_bus: EventBus) -> None:
        """Set the event bus for this engine.
        
        Args:
            event_bus: Event bus instance
        """
        self._event_bus = event_bus

    # Methods to be overridden by subclasses

    async def _on_initialize(self, state: Any) -> None:
        """Called during initialization. Override in subclasses."""
        pass

    async def _on_tick(self, state: Any, delta_time: float) -> None:
        """Called each tick. Override in subclasses."""
        pass

    async def _on_shutdown(self) -> None:
        """Called during shutdown. Override in subclasses."""
        pass
