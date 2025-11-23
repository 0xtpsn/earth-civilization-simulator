"""
Phase 3: Appearance (Physical World Generation)

Generates terrain, structures, cities, biomes, and geography for any era.
This is a blueprint generator, not a renderer.

ARCHITECTURE RULES:
- This is a Phase 3 engine
- CAN import: shared/, persistence/, Systems Layer services (llm, knowledge, etc.)
- CANNOT import: Other phase engines (npc, economy, etc.) directly
- MUST communicate with other phases via: EventBus, WorldState
- Reads truth from Phase 2 (History) via WorldState or events, not direct imports

ANTI-HARDCODING GUARANTEE:
Phase 3 must remain a blueprint generator that reads truth from History (Phase 2)
and writes structured outputs into WorldState. It should never sneak into Phase 1
tick logic beyond being called by the orchestrator.

Phase 1 doesn't "know" buildings; it just knows how to ask the WorldGen engine
to produce era-correct blueprints when needed.

KEY PRINCIPLE:
Uses Phase 2 (History) as conditioning inputs to generate the physical world
on demand, per timeline branch and per user action. Worldgen produces blueprints,
not visuals.
"""

# Phase 3 engine - do not import other phase engines directly
# Use EventBus, WorldState, or Systems Layer services for communication
# Read from Phase 2 (History) via WorldState, not direct imports

