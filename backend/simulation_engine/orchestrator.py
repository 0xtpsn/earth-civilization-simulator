"""Orchestrator that coordinates all engines and manages the simulation lifecycle."""

import asyncio
import logging
from typing import Dict, List, Optional

from backend.shared.interfaces import Engine, EventPublisher, EventSubscriber
from backend.shared.types import ScenarioID, Time
from backend.simulation_engine.determinism import set_rng
from backend.simulation_engine.event_bus import EventBus
from backend.simulation_engine.state import WorldState
from backend.simulation_engine.tick import TickScheduler

logger = logging.getLogger(__name__)


class SimulationOrchestrator:
    """
    Master orchestrator for the simulation.
    
    This is Phase 7: The Simulation Orchestrator (THE ACTUAL GAME), part of Phase 1: The Universe.
    
    The orchestrator is THE ACTUAL GAME - the system that:
    - Binds all phases together
    - Updates the world each tick
    - Processes actions
    - Evolves the universe
    - Handles consequences
    - Drives timelines
    - Generates the next moment
    
    The orchestrator is what makes the simulation feel like a living civilization
    and not just a bunch of disconnected systems.
    
    ARCHITECTURE:
    - Belongs in simulation_engine/ (not a separate runtime)
    - Orchestrates all phase engines but doesn't know their internals
    - Engines communicate via EventBus and WorldState, not direct calls
    - Only sequences and validates; never invents content itself
    """

    def __init__(self, seed: int = 42):
        """Initialize the orchestrator.
        
        Args:
            seed: Random seed for deterministic simulation
        """
        self.seed = seed
        self.event_bus = EventBus()
        self.engines: List[Engine] = []
        self.state: Optional[WorldState] = None
        self.scheduler: Optional[TickScheduler] = None
        self._initialized = False

    async def initialize(
        self, scenario_id: ScenarioID, initial_time: Time, location: str
    ) -> None:
        """Initialize the simulation with a scenario.
        
        Args:
            scenario_id: Scenario to load
            initial_time: Starting time
            location: Starting location
        """
        logger.info(f"Initializing simulation: scenario={scenario_id}, time={initial_time}, location={location}")

        # Set up deterministic randomness
        set_rng(self.seed)

        # Create initial world state
        from backend.shared.types import Era, TimelineID
        from uuid import uuid4

        self.state = WorldState(
            current_time=initial_time,
            scenario_id=scenario_id,
            timeline_id=TimelineID(uuid4()),
            era=Era(str(initial_time)[:4] if isinstance(initial_time, str) else str(initial_time.year)),
            current_location=location,
            seed=self.seed,
        )

        # Initialize all engines (respecting dependencies)
        initialized = set()
        remaining = list(self.engines)

        while remaining:
            progress = False
            for engine in list(remaining):
                # Check if dependencies are satisfied
                deps = getattr(engine, "dependencies", [])
                if all(dep in initialized for dep in deps):
                    try:
                        await engine.initialize(self.state)
                        logger.info(f"Initialized engine: {engine.name}")
                        initialized.add(engine.name)
                        remaining.remove(engine)
                        progress = True
                    except Exception as e:
                        logger.error(
                            f"Error initializing engine {engine.name}: {e}", exc_info=True
                        )
                        raise

            if not progress:
                # Circular dependency or missing dependency
                missing = [e.name for e in remaining]
                raise RuntimeError(
                    f"Cannot initialize engines due to unresolved dependencies: {missing}"
                )

        # Set up event bus subscriptions and start event bus
        for engine in self.engines:
            if isinstance(engine, EventSubscriber):
                # Engines can subscribe to events
                # This will be handled by each engine's implementation
                pass

        # Start event bus workers
        await self.event_bus.start()

        self._initialized = True
        logger.info("Simulation initialized successfully")

    def register_engine(self, engine: Engine) -> None:
        """Register an engine with the orchestrator.
        
        Args:
            engine: Engine instance to register
        """
        if engine in self.engines:
            logger.warning(f"Engine {engine.name} already registered")
            return

        self.engines.append(engine)
        logger.info(f"Registered engine: {engine.name}")

    async def start(self, tick_rate: float = 1.0) -> None:
        """Start the simulation.
        
        Args:
            tick_rate: Real-world seconds per tick
        """
        if not self._initialized:
            raise RuntimeError("Simulation not initialized. Call initialize() first.")

        if self.state is None:
            raise RuntimeError("World state not initialized")

        logger.info("Starting simulation...")

        # Sort engines by priority (lower priority = runs first)
        sorted_engines = sorted(self.engines, key=lambda e: getattr(e, "priority", 0))

        # Create tick scheduler
        self.scheduler = TickScheduler(
            engines=sorted_engines,
            state=self.state,
            tick_rate=tick_rate,
        )

        # Start the tick loop
        await self.scheduler.start()

    async def stop(self) -> None:
        """Stop the simulation."""
        logger.info("Stopping simulation...")

        if self.scheduler:
            await self.scheduler.stop()

        # Stop event bus
        await self.event_bus.stop()

        # Shutdown all engines (reverse order)
        for engine in reversed(self.engines):
            try:
                await engine.shutdown()
            except Exception as e:
                logger.error(f"Error shutting down engine {engine.name}: {e}", exc_info=True)

        logger.info("Simulation stopped")

    def pause(self) -> None:
        """Pause the simulation."""
        if self.scheduler:
            self.scheduler.pause()

    def resume(self) -> None:
        """Resume the simulation."""
        if self.scheduler:
            self.scheduler.resume()

    async def fast_forward(self, ticks: int) -> None:
        """Fast-forward the simulation.
        
        Args:
            ticks: Number of ticks to advance
        """
        if self.scheduler:
            await self.scheduler.fast_forward(ticks)

    def get_state(self) -> Optional[WorldState]:
        """Get the current world state."""
        return self.state

    def get_event_bus(self) -> EventBus:
        """Get the event bus."""
        return self.event_bus

