# Architecture Rules & Enforcement

This document defines the architectural boundaries that must be enforced in the codebase.

## Core Principle

**Phase engines must NEVER directly import other phase engines.** They communicate via:
- EventBus (pub/sub events)
- WorldState (shared state)
- Systems Layer services (LLM, Knowledge, etc.)

## Phase Model (7 Phases)

### Phase 1: The Universe (Time + State) (`backend/simulation_engine/`)
- **The rules of existence**
- WorldState, ticks, determinism
- **Phase 7: Orchestrator** is also here (sequences all phases)

### Phase 2: History (Truth + Context) (`backend/history/`)
- **The memory of the world**
- Truth & context layer
- Stores truth keyframes and signals
- **Never encodes fixed city layouts or scripted events**

### Phase 3: Appearance (Physical World) (`backend/world_generation/`)
- **The environment + geography + structures**
- Physical world blueprint generator
- **Reads from Phase 2 (History) via WorldState or events, NOT direct imports**
- Generates blueprints on demand, per timeline branch
- **Anti-hardcoding guarantee**: Never sneaks into Phase 1 tick logic

### Phase 4: The People (Population) (`backend/npc/`)
- **NPCs, demographics, roles**
- Populations and their identities
- Uses Phase 5 (LLM) as Systems Layer service
- Uses Knowledge (RAG) for era-appropriate information

### Phase 5: Consciousness (AI Minds) (`backend/llm/`)
- **NPC dialogue, thinking, memory**
- **Systems Layer service** (not a phase engine)
- Can be imported by phase engines
- Provides LLM routing, safety, era-bounded knowledge

### Phase 6: Visualization (Renderer) (`game-client-minecraft/` or any renderer)
- **Minecraft / 3D engine — the camera**
- Thin visualization layers (not in backend/)
- Renderer clients consume API and render the world

### Phase 7: The Simulation Orchestrator (THE ACTUAL GAME) (`backend/simulation_engine/orchestrator.py`)
- **The system that binds all phases together**
- Updates the world each tick
- Processes actions
- Evolves the universe
- Handles consequences
- Drives timelines
- Generates the next moment
- **Makes the simulation feel like a living civilization and not just a bunch of disconnected systems**

## Systems Layer (Meta-Layer)

Services that surround all phases:
- `llm/` - LLM routing, safety (Phase 5)
- `knowledge/` - RAG, era knowledge (Foundational)
- `timeline/` - Time travel, branching (Foundational)
- `observability/` - Logs, metrics
- `localization/` - Translation
- `commands/` - Player interactions
- `api/` - Renderer interface

**These can be imported by phase engines.**

## Foundational Engines

- **Timeline** - Makes Universe deterministic and branchable
- **Knowledge** - Era-bounded truth layer for NPC minds and worldgen

These serve multiple phases but are separate modules.

## Import Rules

### ✅ Allowed Imports

**Phase engines can import:**
- `backend.shared.*` - Shared utilities
- `backend.persistence.*` - Persistence layer
- `backend.llm.*` - Systems Layer service
- `backend.knowledge.*` - Foundational engine
- `backend.timeline.*` - Foundational engine
- `backend.observability.*` - Systems Layer service
- `backend.localization.*` - Systems Layer service
- `backend.commands.*` - Systems Layer service
- `backend.api.*` - Systems Layer service
- `backend.simulation_engine.*` - Phase 1 + Phase 7 (orchestration)

### ❌ Forbidden Imports

**Phase engines CANNOT import:**
- `backend.history.*` from other phase engines
- `backend.world_generation.*` from other phase engines
- `backend.npc.*` from other phase engines
- `backend.economy.*` from other phase engines
- `backend.money.*` from other phase engines
- `backend.ideologies.*` from other phase engines

**Exception**: Phase 1 + Phase 7 (`simulation_engine/`) can import phase engines for orchestration, but phase engines cannot import each other.

## Communication Patterns

### Pattern 1: EventBus (Pub/Sub)
```python
# Phase engine publishes event
await self.publish("economy.price_change", {"product": "wheat", "price": 10.5})

# Another phase engine subscribes
event_bus.subscribe("economy.price_change", self.handle_price_change)
```

### Pattern 2: WorldState (Shared State)
```python
# Phase 2 (History) writes truth data
state.set_engine_state("history", {"population": 1000, "tech_level": 5})

# Phase 3 (WorldGen) reads truth data
history_data = state.get_engine_state("history")
# Generate blueprints based on history_data
```

### Pattern 3: Systems Layer Services
```python
# Phase 4 (NPC) uses Phase 5 (LLM) as Systems Layer service
from backend.llm.providers import get_llm_provider
response = await get_llm_provider().generate_dialogue(context)
```

## Validation

See `backend/shared/architecture.py` for validation utilities.

## Example Violations

### ❌ BAD: Direct import between phase engines
```python
# In backend/npc/cognition.py
from backend.economy.markets import get_market_price  # VIOLATION!
```

### ✅ GOOD: Use EventBus
```python
# In backend/npc/cognition.py
# Subscribe to economy events
event_bus.subscribe("economy.price_update", self.handle_price_update)

# Or publish request
await self.publish("npc.price_query", {"product": "wheat"})
```

### ✅ GOOD: Use WorldState
```python
# In backend/world_generation/structures.py
# Read from Phase 2 (History) via WorldState
history_data = state.get_engine_state("history")
population = history_data.get("population", 0)
# Generate structures based on population
```

### ✅ GOOD: Use Systems Layer service
```python
# In backend/npc/dialogue.py
from backend.llm.providers import get_llm_provider  # OK - Systems Layer
response = await get_llm_provider().generate(context)
```

## Enforcement

1. **Code Review**: Check imports in phase engine modules
2. **Linting**: Add custom lint rule to detect violations (future)
3. **Documentation**: Each phase engine `__init__.py` documents boundaries
4. **Architecture Module**: `backend/shared/architecture.py` provides validation

## Benefits

- **Modularity**: Phase engines can evolve independently
- **Testability**: Each phase can be tested in isolation
- **Scalability**: Easy to add new phases without breaking existing ones
- **AI-Emergent**: Prevents hardcoding by enforcing clean boundaries
- **Maintainability**: Clear separation of concerns

