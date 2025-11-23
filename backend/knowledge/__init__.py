"""
Foundational Engine: Knowledge (RAG + Era Knowledge)

This is a foundational engine that serves multiple phases (History, NPC, WorldGen).
It provides era-bounded knowledge retrieval and validation.

ARCHITECTURE:
- Foundational engine (serves multiple phases)
- Phase engines can import and use this
- This module should NOT import phase engines directly
- Provides: RAG, era knowledge validation, semantic search
"""

# Foundational engine - can be imported by phase engines
# Do not import phase engines from here

