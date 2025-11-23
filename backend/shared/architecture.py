"""
Architecture boundary enforcement and documentation.

This module defines the architectural boundaries and provides utilities
to enforce them. It documents the phase model and Systems Layer separation.

ARCHITECTURE RULES:
==================

1. Phase Engines (Phase 2-5) must NEVER directly import other phase engines.
   They communicate via:
   - EventBus (pub/sub)
   - WorldState (shared state)
   - Systems Layer services (LLM, Knowledge, etc.)

2. Systems Layer services (LLM, Knowledge, Observability, etc.) can be
   imported by phase engines, but phase engines cannot import each other.

3. Phase 1 (Universe) + Phase 7 (Orchestrator) are in simulation_engine/.
   The orchestrator sequences all phases but doesn't know their internals.

4. Foundational engines (Timeline, Knowledge) serve multiple phases but
   are separate modules, not inside phase folders.

5. Phase 3 (WorldGen) reads from Phase 2 (History) but only through
   WorldState or events, never direct imports.

PHASE MODEL (7 PHASES):
========================

Phase 1: The Universe (Time + State) - simulation_engine/
  - The rules of existence
  - WorldState, ticks, determinism

Phase 2: History (Truth + Context) - history/
  - The memory of the world
  - Truth & context layer

Phase 3: Appearance (Physical World) - world_generation/
  - The environment + geography + structures
  - Physical world blueprints

Phase 4: The People (Population) - npc/
  - NPCs, demographics, roles
  - Populations and their identities

Phase 5: Consciousness (AI Minds) - llm/
  - NPC dialogue, thinking, memory
  - AI/cognition (Systems Layer service)

Phase 6: Visualization (Renderer) - game-client-minecraft/ (or any renderer)
  - Minecraft / 3D engine — the camera
  - Thin visualization layer (not in backend/)

Phase 7: The Simulation Orchestrator (THE ACTUAL GAME) - simulation_engine/orchestrator.py
  - Binds all phases together
  - Updates the world each tick
  - Processes actions
  - Evolves the universe
  - Handles consequences
  - Drives timelines
  - Generates the next moment
  - Makes the simulation feel like a living civilization

SYSTEMS LAYER (Meta-Layer):
===========================

Services that surround all phases:
- llm/ - LLM routing, safety, era-bounded knowledge
- knowledge/ - RAG, era knowledge validation
- observability/ - Logs, metrics, inspector
- localization/ - Translation, language support
- commands/ - Player interactions
- api/ - Renderer interface

These can be imported by phase engines, but phase engines cannot import each other.
"""

from typing import List, Set

# Phase engine module names (for validation)
PHASE_ENGINES: Set[str] = {
    "history",           # Phase 2
    "world_generation",  # Phase 3
    "npc",               # Phase 4
    "economy",           # Societal behavior
    "money",             # Societal behavior
    "ideologies",        # Societal behavior
}

# Systems Layer module names (can be imported by phase engines)
SYSTEMS_LAYER: Set[str] = {
    "systems",           # Systems Layer namespace (meta-layer)
    "llm",               # Phase 5: Consciousness (Systems Layer service)
    "knowledge",         # Foundational: RAG/Era knowledge
    "timeline",          # Foundational: Time travel
    "observability",     # Logs, metrics
    "localization",      # Translation
    "commands",          # Player interactions
    "api",               # Renderer interface
}

# Shared modules (can be imported by anyone)
SHARED_MODULES: Set[str] = {
    "shared",
    "persistence",
}

# Phase 1 + Phase 7 (Universe + Orchestrator)
UNIVERSE_MODULE: str = "simulation_engine"


def is_phase_engine(module_name: str) -> bool:
    """Check if a module is a phase engine."""
    return module_name in PHASE_ENGINES


def is_systems_layer(module_name: str) -> bool:
    """Check if a module is a Systems Layer service."""
    return module_name in SYSTEMS_LAYER


def is_shared_module(module_name: str) -> bool:
    """Check if a module is a shared utility."""
    return module_name in SHARED_MODULES


def validate_import(allowed_modules: List[str], importing_module: str) -> bool:
    """
    Validate that a module is allowed to import from the given modules.
    
    Args:
        allowed_modules: List of module names being imported
        importing_module: Name of the module doing the importing
        
    Returns:
        True if import is allowed, False otherwise
        
    Raises:
        ValueError: If a phase engine tries to import another phase engine
    """
    importing_base = importing_module.split(".")[0] if "." in importing_module else importing_module
    
    # Extract base module names from allowed_modules
    importing_bases = set()
    for mod in allowed_modules:
        base = mod.split(".")[0] if "." in mod else mod
        importing_bases.add(base)
    
    # Phase engines cannot import other phase engines
    if is_phase_engine(importing_base):
        for mod_base in importing_bases:
            if is_phase_engine(mod_base) and mod_base != importing_base:
                raise ValueError(
                    f"ARCHITECTURE VIOLATION: Phase engine '{importing_base}' "
                    f"cannot directly import phase engine '{mod_base}'. "
                    f"Use EventBus, WorldState, or Systems Layer services instead."
                )
    
    return True


# Architecture documentation constants
ARCHITECTURE_DOC = """
ARCHITECTURE BOUNDARIES:
=======================

Phase engines (history, world_generation, npc, economy, money, ideologies):
  - CAN import: shared/, persistence/, Systems Layer services
  - CANNOT import: Other phase engines directly
  - MUST communicate via: EventBus, WorldState, Systems Layer services

Systems Layer (llm, knowledge, timeline, observability, localization, commands, api):
  - CAN be imported by phase engines
  - Provide cross-cutting services to all phases

Phase 1 + Phase 7 (simulation_engine):
  - Orchestrates all phases
  - Does not know phase engine internals
  - Sequences execution via Engine interface

Foundational engines (timeline, knowledge):
  - Serve multiple phases
  - Separate modules, not inside phase folders
  - First-class in orchestration order
"""

