# The 7-Phase Universe Model

This document defines the complete 7-phase architecture of the Parallel Earth simulation.

## Overview

The simulation brain is composed of **seven distinct phases** that work together to create a living civilization:

1. **Phase 1: The Universe (Time + State)** — The rules of existence
2. **Phase 2: History (Truth + Context)** — The memory of the world
3. **Phase 3: Appearance (Physical World)** — The environment + geography + structures
4. **Phase 4: The People (Population)** — NPCs, demographics, roles
5. **Phase 5: Consciousness (AI Minds)** — NPC dialogue, thinking, memory
6. **Phase 6: Visualization (Renderer)** — Minecraft / 3D engine — the camera
7. **Phase 7: The Simulation Orchestrator (THE ACTUAL GAME)** — Binds all phases together

---

## Phase 1: The Universe (Time + State)

**Location**: `backend/simulation_engine/`

**Purpose**: The rules of existence.

**Components**:
- WorldState — Canonical world state
- Tick loop — Deterministic time progression
- Determinism — Seeded RNG for reproducibility
- EventBus — Pub/sub event system
- Rules — Universal constraints, laws, physics

**Key Principle**: This is the foundation. Everything else builds on top of the Universe.

---

## Phase 2: History (Truth + Context)

**Location**: `backend/history/`

**Purpose**: The memory of the world.

**Components**:
- Era profiles — Global structure of each time period
- Country profiles — Political systems, laws, macro indicators
- City profiles — Demographics, cultural traits, economies
- Event library — Wars, crises, inventions, reforms
- Signal extraction — Economic/political cycles

**Key Principle**: Stores truth keyframes and signals. Never encodes fixed city layouts or scripted future events.

---

## Phase 3: Appearance (Physical World)

**Location**: `backend/world_generation/`

**Purpose**: The environment + geography + structures.

**Components**:
- Earth geometry — Terrain and elevation
- Biomes & climate — Environmental systems
- Hydrology — Water systems
- Structures — Procedural/AI-driven city and building generation
- Chunking — Blueprint format for rendering
- Historicalization — Different layouts per era

**Key Principle**: Generates blueprints only, not visuals. Reads from Phase 2 (History) via WorldState or events, never direct imports.

**Anti-Hardcoding Guarantee**: Phase 1 doesn't "know" buildings; it just knows how to ask the WorldGen engine to produce era-correct blueprints when needed.

---

## Phase 4: The People (Population)

**Location**: `backend/npc/`

**Purpose**: NPCs, demographics, roles.

**Components**:
- Profiles — NPC identities, roles, demographics
- Cognition — Decision-making, goal pursuit
- Memory — Persistent records of encounters
- Dialogue — Conversation systems
- Social network — Relationships, affiliations
- Behaviors — Culturally grounded actions
- Spawning — Population generation

**Key Principle**: NPCs observe → think → act. They are autonomous agents with memory, personality, goals, and culturally grounded behavior.

---

## Phase 5: Consciousness (AI Minds)

**Location**: `backend/llm/` (Systems Layer service)

**Purpose**: NPC dialogue, thinking, memory.

**Components**:
- Providers — LLM API integrations (OpenAI, Anthropic)
- Prompts — Era-bounded prompt templates
- Routing — Model selection (cheap vs strong)
- Tools — LLM function calling
- Safety — Anachronism prevention, era consistency

**Key Principle**: Centralized AI usage for cognition, dialogue, memory recall. Ensures era-bounded knowledge and avoids anachronisms.

**Note**: This is a Systems Layer service, not a phase engine. It can be imported by phase engines.

---

## Phase 6: Visualization (Renderer)

**Location**: `game-client-minecraft/` (or any renderer)

**Purpose**: Minecraft / 3D engine — the camera.

**Components**:
- Plugin — Minecraft server plugin
- Bridge — API communication layer
- UI — User interface
- Assets — Textures, models
- Configs — Renderer-specific settings

**Key Principle**: Thin visualization layer. Consumes the API and renders the world, but never owns simulation logic. The renderer is the camera, not the reality.

**Note**: This phase is outside `backend/` because it's a visualization layer, not part of the simulation brain.

---

## Phase 7: The Simulation Orchestrator (THE ACTUAL GAME)

**Location**: `backend/simulation_engine/orchestrator.py`

**Purpose**: The system that binds all phases together.

**Responsibilities**:
- Binds all phases together
- Updates the world each tick
- Processes actions
- Evolves the universe
- Handles consequences
- Drives timelines
- Generates the next moment

**Key Principle**: **The orchestrator is what makes the simulation feel like a living civilization and not just a bunch of disconnected systems.**

**Architecture**:
- Belongs in `simulation_engine/` (not a separate runtime)
- Orchestrates all phase engines but doesn't know their internals
- Sequences execution via Engine interface
- Engines communicate via EventBus and WorldState, not direct calls

---

## Phase Relationships

```
Phase 1 (Universe) ──┐
                     │
Phase 2 (History) ───┼──> Phase 3 (Appearance)
                     │
Phase 4 (People) ────┼──> Phase 5 (Consciousness)
                     │
Phase 6 (Visualization) ──┘
                     │
         Phase 7 (Orchestrator) ──> Binds all phases together
```

**Communication Rules**:
- Phase engines cannot directly import other phase engines
- Phase engines communicate via EventBus, WorldState, or Systems Layer services
- Phase 7 (Orchestrator) can reference all phases for orchestration
- Phase 6 (Visualization) consumes the API, never owns simulation logic

---

## Systems Layer (Meta-Layer)

The Systems Layer surrounds all phases, providing cross-cutting services:

- **LLM** (`backend/llm/`) — Phase 5: Consciousness (Systems Layer service)
- **Knowledge** (`backend/knowledge/`) — RAG, era knowledge (Foundational)
- **Timeline** (`backend/timeline/`) — Time travel, branching (Foundational)
- **Observability** (`backend/observability/`) — Logs, metrics
- **Localization** (`backend/localization/`) — Translation
- **Commands** (`backend/commands/`) — Player interactions
- **API** (`backend/api/`) — Renderer interface
- **Systems** (`backend/systems/`) — Safety, telemetry, pipelines, model routing

**Key Principle**: Systems Layer services can be imported by phase engines, but phase engines cannot import each other.

---

## Summary

The 7-phase architecture ensures:

1. **Clear separation** — Each phase has a distinct purpose
2. **Modular design** — Phases can evolve independently
3. **Clean boundaries** — Phase engines don't directly import each other
4. **Living civilization** — Phase 7 orchestrator binds everything together
5. **Renderer-agnostic** — Phase 6 is just a camera, not the reality

**The orchestrator (Phase 7) is THE ACTUAL GAME** — it's what makes the simulation feel like a living civilization and not just a bunch of disconnected systems.

