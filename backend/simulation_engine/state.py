"""World state management with compression, incremental updates, and lazy loading."""

import gzip
import json
import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, Optional

from backend.shared.types import AgentID, Era, Location, ScenarioID, Time, TimelineID

logger = logging.getLogger(__name__)


# WorldState schema version - increment when breaking changes occur
WORLD_STATE_VERSION = 1


@dataclass
class WorldState:
    """Canonical world state - everything that can be serialized and restored.
    
    This is a versioned schema. When engine schemas change, increment WORLD_STATE_VERSION
    and implement migration hooks in migrate_state().
    
    Think "database migrations, but for world reality."
    """

    # Schema versioning
    state_version: int = field(default=WORLD_STATE_VERSION)

    # Time and scenario
    current_time: Time
    scenario_id: ScenarioID
    timeline_id: TimelineID
    era: Era

    # Location context
    current_location: Location

    # Engine state storage (each engine can store its state here)
    engine_states: Dict[str, Any] = field(default_factory=dict)

    # Lazy loading support
    _lazy_loaders: Dict[str, Callable] = field(default_factory=dict, repr=False)
    _loaded_partitions: set = field(default_factory=set, repr=False)

    # Metadata
    tick_count: int = 0
    seed: int = 42
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def register_lazy_loader(self, partition: str, loader: Callable) -> None:
        """Register a lazy loader for a partition.
        
        Args:
            partition: Partition identifier (e.g., "npc:region:1", "economy:market:us")
            loader: Async function that loads partition data
        """
        self._lazy_loaders[partition] = loader

    async def get_engine_state(self, engine_name: str, partition: Optional[str] = None) -> Optional[Any]:
        """Get state for a specific engine, with optional lazy loading.
        
        Args:
            engine_name: Name of the engine
            partition: Optional partition identifier for lazy loading
            
        Returns:
            Engine state or None
        """
        if partition:
            # Lazy load partition if needed
            if partition not in self._loaded_partitions:
                loader = self._lazy_loaders.get(partition)
                if loader:
                    logger.debug(f"Lazy loading partition: {partition}")
                    await loader(partition)
                    self._loaded_partitions.add(partition)

        return self.engine_states.get(engine_name)

    def set_engine_state(self, engine_name: str, state: Any) -> None:
        """Set state for a specific engine."""
        self.engine_states[engine_name] = state
        self.updated_at = datetime.now()

    def unload_partition(self, partition: str) -> None:
        """Unload a partition to free memory.
        
        Args:
            partition: Partition identifier
        """
        if partition in self._loaded_partitions:
            # Remove partition data from engine states
            # Engines should implement partition cleanup
            self._loaded_partitions.discard(partition)
            logger.debug(f"Unloaded partition: {partition}")

    def to_dict(self) -> Dict[str, Any]:
        """Convert state to dictionary for serialization."""
        return {
            "state_version": self.state_version,
            "current_time": (
                self.current_time.isoformat()
                if isinstance(self.current_time, datetime)
                else str(self.current_time)
            ),
            "scenario_id": str(self.scenario_id),
            "timeline_id": str(self.timeline_id),
            "era": str(self.era),
            "current_location": str(self.current_location),
            "engine_states": self.engine_states,
            "tick_count": self.tick_count,
            "seed": self.seed,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WorldState":
        """Create state from dictionary with automatic migration.
        
        If the stored state_version is older than current, migrates the state.
        """
        stored_version = data.get("state_version", 0)
        
        # Migrate if needed
        if stored_version < WORLD_STATE_VERSION:
            logger.info(f"Migrating WorldState from version {stored_version} to {WORLD_STATE_VERSION}")
            data = cls.migrate_state(data, stored_version, WORLD_STATE_VERSION)
        
        # Ensure state_version is set after migration
        if "state_version" not in data:
            data["state_version"] = WORLD_STATE_VERSION
        
        return cls(
            state_version=data["state_version"],
            current_time=Time(datetime.fromisoformat(data["current_time"])),
            scenario_id=ScenarioID(data["scenario_id"]),
            timeline_id=TimelineID(data["timeline_id"]),
            era=Era(data["era"]),
            current_location=Location(data["current_location"]),
            engine_states=data.get("engine_states", {}),
            tick_count=data.get("tick_count", 0),
            seed=data.get("seed", 42),
            created_at=datetime.fromisoformat(data.get("created_at", datetime.now().isoformat())),
            updated_at=datetime.fromisoformat(data.get("updated_at", datetime.now().isoformat())),
        )
    
    @staticmethod
    def migrate_state(data: Dict[str, Any], from_version: int, to_version: int) -> Dict[str, Any]:
        """Migrate state from one version to another.
        
        Args:
            data: State dictionary to migrate
            from_version: Source version
            to_version: Target version
            
        Returns:
            Migrated state dictionary
            
        Example migration:
            if from_version == 0 and to_version == 1:
                # Add new field with default value
                data["new_field"] = default_value
                data["state_version"] = 1
        """
        # Apply migrations sequentially
        current = from_version
        while current < to_version:
            next_version = current + 1
            
            # Version 0 -> 1: Add state_version field if missing
            if current == 0 and next_version == 1:
                if "state_version" not in data:
                    data["state_version"] = 1
                current = next_version
                continue
            
            # Add future migrations here:
            # if current == 1 and next_version == 2:
            #     # Migration logic
            #     current = next_version
            #     continue
            
            # If no migration defined, just update version
            data["state_version"] = next_version
            current = next_version
        
        return data

    def create_diff(self, previous_state: "WorldState") -> Dict[str, Any]:
        """Create a diff between this state and a previous state.
        
        Args:
            previous_state: Previous state to compare against
            
        Returns:
            Dictionary containing only changed fields
        """
        diff: Dict[str, Any] = {}

        # Compare top-level fields
        if self.current_time != previous_state.current_time:
            diff["current_time"] = (
                self.current_time.isoformat()
                if isinstance(self.current_time, datetime)
                else str(self.current_time)
            )

        if self.current_location != previous_state.current_location:
            diff["current_location"] = str(self.current_location)

        if self.tick_count != previous_state.tick_count:
            diff["tick_count"] = self.tick_count

        # Compare engine states
        engine_diffs = {}
        for engine_name, current_state in self.engine_states.items():
            previous_state_data = previous_state.engine_states.get(engine_name)

            # Simple comparison - engines can implement custom diffing
            if current_state != previous_state_data:
                engine_diffs[engine_name] = current_state

        if engine_diffs:
            diff["engine_states"] = engine_diffs

        return diff

    def apply_diff(self, diff: Dict[str, Any], base_state: Optional["WorldState"] = None) -> None:
        """Apply a diff to this state (or create from base state).
        
        Args:
            diff: Diff dictionary to apply
            base_state: Base state to apply diff to (if None, uses self)
        """
        target = base_state if base_state else self

        if "current_time" in diff:
            target.current_time = Time(datetime.fromisoformat(diff["current_time"]))

        if "current_location" in diff:
            target.current_location = Location(diff["current_location"])

        if "tick_count" in diff:
            target.tick_count = diff["tick_count"]

        if "engine_states" in diff:
            for engine_name, engine_state in diff["engine_states"].items():
                target.engine_states[engine_name] = engine_state

        target.updated_at = datetime.now()

    def to_compressed(self) -> bytes:
        """Serialize and compress state.
        
        Returns:
            Compressed state as bytes
        """
        data = json.dumps(self.to_dict()).encode("utf-8")
        return gzip.compress(data, compresslevel=6)

    @classmethod
    def from_compressed(cls, data: bytes) -> "WorldState":
        """Create state from compressed data.
        
        Args:
            data: Compressed state bytes
            
        Returns:
            Restored WorldState
        """
        decompressed = gzip.decompress(data)
        state_dict = json.loads(decompressed.decode("utf-8"))
        return cls.from_dict(state_dict)


@dataclass
class StateSnapshot:
    """A snapshot of world state at a specific point in time."""

    state: WorldState
    snapshot_time: datetime
    compressed_data: Optional[bytes] = None

    def __post_init__(self):
        """Compress state data after initialization."""
        if self.compressed_data is None:
            self.compressed_data = self.state.to_compressed()

    @classmethod
    def create(cls, state: WorldState) -> "StateSnapshot":
        """Create a snapshot from a world state.
        
        Args:
            state: World state to snapshot
            
        Returns:
            StateSnapshot instance
        """
        return cls(
            state=state,
            snapshot_time=datetime.now(),
        )

    def restore(self) -> WorldState:
        """Restore the world state from this snapshot.
        
        Returns:
            Restored WorldState
        """
        if self.compressed_data:
            return WorldState.from_compressed(self.compressed_data)
        return self.state
