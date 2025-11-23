"""
Phase 2: History (Truth & Context)

Holds era-specific truth, data, and historical signals. This is the truth layer
that other phases read from.

ARCHITECTURE RULES:
- This is a Phase 2 engine
- CAN import: shared/, persistence/, Systems Layer services (llm, knowledge, etc.)
- CANNOT import: Other phase engines (world_generation, npc, economy, etc.)
- MUST communicate with other phases via: EventBus, WorldState
- Phase 3 (WorldGen) reads from this via WorldState or events, not direct imports

KEY PRINCIPLE:
Phase 2 stores truth keyframes and signals (population, laws, tech level, macro
indicators, canon events). It never encodes fixed city layouts or scripted future
events. Everything is data-driven and era-authentic.
"""

# Phase 2 engine - do not import other phase engines directly
# Use EventBus, WorldState, or Systems Layer services for communication

