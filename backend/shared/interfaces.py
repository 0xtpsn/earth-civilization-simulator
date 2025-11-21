"""Core interfaces and contracts for the simulation system."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from backend.shared.types import Time


class Engine(ABC):
    """Base interface that all simulation engines must implement."""

    @abstractmethod
    async def initialize(self, state: "WorldState") -> None:
        """Initialize the engine with the current world state."""
        pass

    @abstractmethod
    async def tick(self, state: "WorldState", delta_time: float) -> None:
        """Process one simulation tick.
        
        Args:
            state: The current world state
            delta_time: Time elapsed since last tick (in simulation time units)
        """
        pass

    @abstractmethod
    async def shutdown(self) -> None:
        """Clean up resources when shutting down."""
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the name of this engine."""
        pass


class EventPublisher(ABC):
    """Interface for publishing events to the event bus."""

    @abstractmethod
    async def publish(self, event_type: str, event_data: Dict[str, Any]) -> None:
        """Publish an event to the event bus.
        
        Args:
            event_type: Type/category of the event
            event_data: Event payload
        """
        pass


class EventSubscriber(ABC):
    """Interface for subscribing to events from the event bus."""

    @abstractmethod
    async def handle_event(self, event_type: str, event_data: Dict[str, Any]) -> None:
        """Handle an event from the event bus.
        
        Args:
            event_type: Type/category of the event
            event_data: Event payload
        """
        pass


class StateSnapshot(ABC):
    """Interface for creating and restoring state snapshots."""

    @abstractmethod
    def create_snapshot(self, state: "WorldState") -> Dict[str, Any]:
        """Create a serializable snapshot of the world state."""
        pass

    @abstractmethod
    def restore_snapshot(self, snapshot: Dict[str, Any]) -> "WorldState":
        """Restore world state from a snapshot."""
        pass


class PersistenceAdapter(ABC):
    """Interface for persistence layer adapters."""

    @abstractmethod
    async def save(self, key: str, data: Any) -> None:
        """Save data with the given key."""
        pass

    @abstractmethod
    async def load(self, key: str) -> Optional[Any]:
        """Load data by key."""
        pass

    @abstractmethod
    async def delete(self, key: str) -> None:
        """Delete data by key."""
        pass


# Forward reference for WorldState (defined in state module)
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backend.simulation_engine.state import WorldState

