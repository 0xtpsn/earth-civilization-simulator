"""Bootstrap and dependency injection for the application."""

import logging
from typing import List

from backend.shared.base_engine import BaseEngine
from backend.shared.interfaces import Engine
from backend.simulation_engine.event_bus import EventBus
from backend.simulation_engine.orchestrator import SimulationOrchestrator

logger = logging.getLogger(__name__)


def create_orchestrator(seed: int = 42) -> SimulationOrchestrator:
    """Create and configure the simulation orchestrator.
    
    Args:
        seed: Random seed for deterministic simulation
        
    Returns:
        Configured orchestrator instance
    """
    orchestrator = SimulationOrchestrator(seed=seed)

    # Register engines here as they are implemented
    # Example:
    # orchestrator.register_engine(SomeEngine())
    # orchestrator.register_engine(AnotherEngine())

    return orchestrator


def register_engines(orchestrator: SimulationOrchestrator, engines: List[Engine]) -> None:
    """Register multiple engines with the orchestrator.
    
    Args:
        orchestrator: Orchestrator instance
        engines: List of engine instances to register
    """
    for engine in engines:
        orchestrator.register_engine(engine)
        # Set event bus for engines that need it
        if isinstance(engine, BaseEngine):
            engine.set_event_bus(orchestrator.get_event_bus())

