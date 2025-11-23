"""
Phase 1: The Universe (Time + State) + Phase 7: The Simulation Orchestrator (THE ACTUAL GAME)

This is the fundamental engine that keeps reality consistent and deterministic.
This is the spine of the simulation.

ARCHITECTURE:
- Phase 1 (The Universe): The rules of existence. WorldState, ticks, determinism.
- Phase 7 (The Simulation Orchestrator): THE ACTUAL GAME. The system that:
  * Binds all phases together
  * Updates the world each tick
  * Processes actions
  * Evolves the universe
  * Handles consequences
  * Drives timelines
  * Generates the next moment
  * Makes the simulation feel like a living civilization

The orchestrator belongs here in the simulation core, not as a separate runtime.
It orchestrates all phase engines but doesn't know their internals.
Engines communicate via EventBus and WorldState, not direct calls.

KEY COMPONENTS:
- SimulationOrchestrator: Master coordinator (Phase 7) - THE ACTUAL GAME
- TickScheduler: Deterministic tick loop
- WorldState: Canonical state
- EventBus: Pub/sub event system
- DeterministicRandom: Seeded RNG for reproducibility
"""

# Phase 1 + Phase 7 - the spine of the simulation
