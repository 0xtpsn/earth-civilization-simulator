"""
Phase 5: Consciousness Layer (Systems Layer Service)

This is a Systems Layer service that provides LLM functionality to phase engines.
Phase engines (NPC, WorldGen, etc.) can import and use this service, but this
module should not import phase engines directly.

ARCHITECTURE:
- This is a Systems Layer service, not a phase engine
- Phase engines (npc/, world_generation/, etc.) can import this
- This module should NOT import phase engines directly
- Provides: LLM routing, safety, era-bounded knowledge validation
"""

# Systems Layer service - can be imported by phase engines
# Do not import phase engines from here

