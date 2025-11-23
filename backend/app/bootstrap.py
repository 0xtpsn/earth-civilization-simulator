"""Bootstrap and dependency injection for the application.

ARCHITECTURE NOTES:
===================

This module registers phase engines with the orchestrator. When implementing
phase engines, follow these rules:

1. Phase engines (history, world_generation, npc, etc.) should NOT directly
   import each other. They communicate via:
   - EventBus (pub/sub events)
   - WorldState (shared state)
   - Systems Layer services (llm, knowledge, etc.)

2. Systems Layer services (llm, knowledge, timeline, etc.) can be used by
   phase engines but are registered separately.

3. Engine registration order matters for dependencies. The orchestrator will
   resolve dependencies automatically.

4. Phase 3 (WorldGen) reads from Phase 2 (History) via WorldState or events,
   not direct imports.

5. Phase 4 (NPC) uses Phase 5 (LLM) as a Systems Layer service, not a
   direct dependency.

Example engine registration:
    from backend.history import HistoryEngine  # Phase 2
    from backend.world_generation import WorldGenEngine  # Phase 3
    from backend.npc import NPCEngine  # Phase 4
    
    orchestrator.register_engine(HistoryEngine())  # Registers first
    orchestrator.register_engine(WorldGenEngine())  # Can read from History via WorldState
    orchestrator.register_engine(NPCEngine())  # Uses LLM service, not direct import
"""

import logging
from typing import List

from backend.shared.base_engine import BaseEngine
from backend.shared.interfaces import Engine
from backend.simulation_engine.event_bus import EventBus
from backend.simulation_engine.orchestrator import SimulationOrchestrator

logger = logging.getLogger(__name__)


def create_orchestrator(seed: int = 42) -> SimulationOrchestrator:
    """Create and configure the simulation orchestrator.
    
    This function registers all phase engines with the orchestrator.
    
    ARCHITECTURE:
    - Phase 1 + Phase 7 are in simulation_engine/ (orchestrator itself)
    - Phase 2: History (truth layer)
    - Phase 3: World Generation (blueprint generator, reads from Phase 2)
    - Phase 4: NPC (uses Phase 5 LLM as Systems Layer service)
    - Phase 5: LLM/Consciousness (Systems Layer service)
    - Foundational: Timeline, Knowledge (serve multiple phases)
    - Societal: Economy, Money, Ideologies
    
    Args:
        seed: Random seed for deterministic simulation
        
    Returns:
        Configured orchestrator instance
    """
    orchestrator = SimulationOrchestrator(seed=seed)

    # Register engines here as they are implemented
    # IMPORTANT: Phase engines should NOT import each other directly.
    # They communicate via EventBus, WorldState, or Systems Layer services.
    
    # Example registration order (when engines are implemented):
    # 
    # # Phase 2: History (truth layer - no dependencies on other phases)
    # from backend.history import HistoryEngine
    # orchestrator.register_engine(HistoryEngine())
    # 
    # # Phase 3: World Generation (reads from Phase 2 via WorldState, not direct import)
    # from backend.world_generation import WorldGenEngine
    # orchestrator.register_engine(WorldGenEngine())
    # 
    # # Foundational: Timeline (serves all phases)
    # from backend.timeline import TimelineEngine
    # orchestrator.register_engine(TimelineEngine())
    # 
    # # Foundational: Knowledge (serves History, NPC, WorldGen)
    # from backend.knowledge import KnowledgeEngine
    # orchestrator.register_engine(KnowledgeEngine())
    # 
    # # Phase 4: NPC (uses Phase 5 LLM as Systems Layer service)
    # from backend.npc import NPCEngine
    # orchestrator.register_engine(NPCEngine())
    # 
    # # Societal behavior engines
    # from backend.economy import EconomyEngine
    # from backend.money import MoneyEngine
    # from backend.ideologies import IdeologyEngine
    # orchestrator.register_engine(EconomyEngine())
    # orchestrator.register_engine(MoneyEngine())
    # orchestrator.register_engine(IdeologyEngine())

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
