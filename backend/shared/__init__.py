"""Shared utilities, types, and interfaces."""

from backend.shared.base_engine import BaseEngine
from backend.shared.batch_processor import BatchProcessor
from backend.shared.constants import (
    CONFIGS_DIR,
    DATA_DIR,
    DEFAULT_SEED,
    DEFAULT_TICK_RATE,
    EXPERIMENTS_DIR,
    PROJECT_ROOT,
    REFERENCE_DIR,
    SEEDS_DIR,
    TICKS_PER_DAY,
    TICKS_PER_MONTH,
    TICKS_PER_WEEK,
    TICKS_PER_YEAR,
)
from backend.shared.interfaces import (
    Engine,
    EventPublisher,
    EventSubscriber,
    PersistenceAdapter,
    StateSnapshot,
)
from backend.shared.resource_limits import ResourceLimitExceeded, ResourceLimiter
from backend.shared.task_queue import Task, TaskQueue, TaskStatus
from backend.shared.types import (
    AgentID,
    ChunkID,
    Currency,
    Era,
    Latitude,
    Location,
    Longitude,
    Price,
    Quantity,
    ScenarioID,
    Time,
    TimelineID,
)

__all__ = [
    # Base classes
    "BaseEngine",
    # Constants
    "PROJECT_ROOT",
    "DATA_DIR",
    "SEEDS_DIR",
    "REFERENCE_DIR",
    "EXPERIMENTS_DIR",
    "CONFIGS_DIR",
    "TICKS_PER_DAY",
    "TICKS_PER_WEEK",
    "TICKS_PER_MONTH",
    "TICKS_PER_YEAR",
    "DEFAULT_SEED",
    "DEFAULT_TICK_RATE",
    # Types
    "Time",
    "Location",
    "AgentID",
    "TimelineID",
    "ScenarioID",
    "Era",
    "Currency",
    "Price",
    "Quantity",
    "Latitude",
    "Longitude",
    "ChunkID",
    # Interfaces
    "Engine",
    "EventPublisher",
    "EventSubscriber",
    "StateSnapshot",
    "PersistenceAdapter",
    # Utilities
    "BatchProcessor",
    "TaskQueue",
    "Task",
    "TaskStatus",
    "ResourceLimiter",
    "ResourceLimitExceeded",
]
