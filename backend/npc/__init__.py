"""
Phase 4: People (NPCs)

Defines populations, roles, identities, and behaviors. Autonomous agents that
observe → think → act.

ARCHITECTURE RULES:
- This is a Phase 4 engine
- CAN import: shared/, persistence/, Systems Layer services (llm, knowledge, etc.)
- CANNOT import: Other phase engines (history, world_generation, economy, etc.) directly
- MUST communicate with other phases via: EventBus, WorldState
- Uses Phase 5 (LLM/Consciousness) via Systems Layer service, not direct dependency

KEY PRINCIPLE:
NPC traits are sampled from era/culture distributions. Everything is AI-generated
and emergent, not hardcoded. NPCs use Phase 5 (LLM/Consciousness) for cognition
and dialogue, and Knowledge (RAG) for era-appropriate information.
"""

# Phase 4 engine - do not import other phase engines directly
# Use EventBus, WorldState, or Systems Layer services for communication
# Use llm/ (Phase 5) as a Systems Layer service, not a direct dependency

