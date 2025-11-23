# Parallel Earth — Repository Architecture Document

**Last Updated**: Architecture Improvements Complete  
**Status**: Foundation established with architecture enforcement, ready for Phase 1 implementation

This document describes the complete repository architecture for **Parallel Earth**, an AI-driven, multi-era Earth simulation. It separates the system into two overarching layers:

1. **Universe Model (Phases 1–7)** — the simulated reality itself
2. **Systems Layer** — the infrastructure supporting realism, safety, debugging, and scale

The architecture is fully modular so that every engine (worldgen, NPCs, economy, ideology, etc.) can evolve independently without breaking other systems. Renderers — Minecraft, Unreal Engine, or a custom client — are thin visualization layers that never own simulation logic.

---

## 0. High-Level Mental Model

The simulation brain is composed of **seven phases**:

### Universe Model (the simulated reality)

1. **Phase 1: The Universe (Time + State)** — The rules of existence. WorldState, ticks, determinism.
2. **Phase 2: History (Truth + Context)** — The memory of the world. Era/country/city truth and signals.
3. **Phase 3: Appearance (Physical World)** — The environment + geography + structures. Terrain, buildings, biomes.
4. **Phase 4: The People (Population)** — NPCs, demographics, roles. Populations and their identities.
5. **Phase 5: Consciousness (AI Minds)** — NPC dialogue, thinking, memory. Cognition, personality, decision-making.
6. **Phase 6: Visualization (Renderer)** — Minecraft / 3D engine — the camera. Thin visualization layer.
7. **Phase 7: The Simulation Orchestrator (THE ACTUAL GAME)** — The system that:
   - Binds all phases together
   - Updates the world each tick
   - Processes actions
   - Evolves the universe
   - Handles consequences
   - Drives timelines
   - Generates the next moment
   
   **The orchestrator is what makes the simulation feel like a living civilization and not just a bunch of disconnected systems.**

### Systems Layer (support infrastructure)

Meta-layer that surrounds all phases, providing cross-cutting concerns:
- Observability / Inspector tools
- Safety and era consistency
- Data ingestion pipelines
- Logging & analytics
- Testing and regression tools
- Performance and scaling utilities
- LLM routing and safety
- Localization and translation

**The Universe Model is the world. The Systems Layer is the machinery supporting it.**

---

## 1. Repository Tree (Top-Level)

```
parallel-earth/
  README.md
  docs/
  backend/
  game-client-minecraft/
  tools/
  tests/
  scripts/
  configs/
```

### README.md

Describes vision, quickstart instructions, and module responsibilities.

### docs/

Long-form documentation stable across development.

```
docs/
  vision/            # Concept bible, core vision
  architecture/      # System architecture, diagrams
  data-specs/        # Schemas for history, worldgen, ideologies, etc.
  api/               # Public API documentation
  era-notes/         # Research on specific eras/regions/cities
```

### tools/

Tooling used during development:

```
tools/
  profilers/
  debug-ui/
  importers/         # Data pipelines for loading history, geography, laws, etc.
  headless_realism_harness.py  # Headless simulation runner for realism validation
```

**`headless_realism_harness.py`** - Scientific instrument for judging realism. Runs simulation without renderer, prints daily summaries, tracks NPC conversations, monitors macro indicators, measures ideological drift, calculates divergence score. Use before Minecraft integration to validate the brain is alive.

### tests/

System-wide tests to ensure determinism and world coherence.

```
tests/
  integration/
  simulation-regression/
```

### scripts/

Helper utilities for developers.

```
scripts/
  run_backend.sh
  run_minecraft_server.sh
  rebuild_world_cache.sh
  setup_database.sh
  test_tick.py
  validate_architecture.py  # Architecture boundary validation
```

**`validate_architecture.py`** - Runs import validation to check for phase engine cross-imports. Treats violations as build errors. Can be integrated into CI/CD.

### configs/

```
configs/
  dev.yaml
  prod.yaml
  secrets.template.yaml
  secrets.yaml
  model-routing.yaml   # cheap vs strong LLM rules
  engine-order.yaml    # Engine priority order and dependency graph
```

**`engine-order.yaml`** - Defines execution order and dependencies for all engines. The orchestrator uses this to determine tick sequencing. When adding new engines (climate, war, disease, tech diffusion), add them here with appropriate priority and dependencies.

---

## 2. backend/ — The Civilization Brain

This is the core of Parallel Earth. Everything inside `backend/` is renderer-agnostic.

```
backend/
  app/
  simulation_engine/
  history/
  world_generation/
  npc/
  llm/
  economy/
  money/
  ideologies/
  knowledge/
  timeline/
  commands/
  localization/
  api/
  persistence/
  observability/
  systems/          # Systems Layer namespace (meta-layer)
  shared/
```

---

## 2.1 app/ — Universe Bootstrap

Responsible for initializing all subsystems and starting the simulation runtime.

```
app/
  main.py
  bootstrap.py
  bootstrap/
  runtime/
```

- **main.py** — Entry point, FastAPI application
- **bootstrap.py** — Dependency wiring, orchestrator creation
- **bootstrap/** — Additional bootstrap utilities
- **runtime/** — Tick scheduler, service registry

---

## 2.2 simulation_engine/ — Phase 1: The Universe + Phase 7: The Simulation Orchestrator

This is the fundamental engine that keeps reality consistent and deterministic. **This is the spine.**

**Phase 1: The Universe (Time + State)** — The rules of existence. WorldState, ticks, determinism.

**Phase 7: The Simulation Orchestrator (THE ACTUAL GAME)** — The system that:
- Binds all phases together
- Updates the world each tick
- Processes actions
- Evolves the universe
- Handles consequences
- Drives timelines
- Generates the next moment

**The orchestrator is what makes the simulation feel like a living civilization and not just a bunch of disconnected systems.**

**Conceptual Ownership**: The Simulation Engine is Phase 1 (The Universe) plus Phase 7 (The Simulation Orchestrator). The orchestrator is not a separate runtime elsewhere; it belongs right here in the simulation core, because it's THE ACTUAL GAME that makes the simulation feel like a living civilization and not just a bunch of disconnected systems.

```
simulation_engine/
  orchestrator.py      # Phase 7: Master coordinator
  tick.py              # Deterministic tick loop
  state.py             # Canonical WorldState
  event_bus.py         # Pub/sub event system
  determinism.py       # Seeded RNG for reproducibility
  tick/                # Time stepping, fast-forward, time dilation
  state/               # State snapshots, state diffs
  rules/               # Universal constraints, laws, physics, capacity limits
  event-propagation/   # Ripple effects, cascading consequences
  scenarios/           # Initial test presets (e.g., "Singapore 2025", "Cleveland 1860")
  determinism/         # Additional determinism utilities
```

### Core Components

**`orchestrator.py` - SimulationOrchestrator (Phase 7: THE ACTUAL GAME)**
- **The system that binds all phases together**
- Master coordinator for the entire simulation
- Manages engine lifecycle (register, initialize, tick, shutdown)
- Coordinates event bus and tick scheduler
- Handles scenario initialization
- Ensures deterministic execution via seeded RNG
- Sequences subsystems per tick and bundles consequences
- Updates the world each tick
- Processes actions
- Evolves the universe
- Handles consequences
- Drives timelines
- Generates the next moment
- **Makes the simulation feel like a living civilization**

**Key Methods**:
```python
async def initialize(scenario_id, initial_time, location)
async def start(tick_rate=1.0)
async def stop()
def register_engine(engine: Engine)
```

**`tick.py` - TickScheduler**
- Manages the deterministic tick loop
- Advances simulation time (default: 1 day per tick)
- Ticks all registered engines in priority order
- Supports pause/resume, fast-forward, time jumping

**Key Features**:
- Deterministic time progression
- Configurable tick rate (real-world seconds per tick)
- Configurable time per tick (simulation time units)
- Engine priority-based execution order

**`state.py` - WorldState**
- Canonical world state object
- Serializable (to_dict/from_dict)
- Engine-specific state storage
- State compression and diffing support
- **Versioned schema** with migration hooks
- Tracks: current_time, tick_count, scenario_id, location, engine_states, state_version

**Key Features**:
- **Schema versioning** (`WORLD_STATE_VERSION`) - think "database migrations, but for world reality"
- **Automatic migration** - `from_dict()` migrates older state versions
- Gzip compression for state snapshots
- Incremental state diffs
- Lazy loading support
- Partition management

**`event_bus.py` - EventBus**
- Pub/sub event system for inter-engine communication
- Async event processing with worker pool
- Backpressure handling (configurable queue size)
- Event history tracking
- Wildcard subscriptions (`*`)

**Key Features**:
- Async queue with configurable size (default: 10,000)
- Multiple worker threads (default: 4)
- Event statistics tracking
- Non-blocking publish with drop-on-full strategy

**`determinism.py` - DeterministicRandom**
- Seeded random number generator wrapper
- Global RNG access via `get_rng()` / `set_rng()`
- Reproducible randomness for deterministic simulation
- State save/restore for replay

**Key Features**:
- Explicit seeding for reproducibility
- Global singleton pattern
- State persistence for branching timelines

---

## 2.3 history/ — Phase 2: Truth & Context

Holds era-specific truth, data, and historical signals. This is the truth layer that other phases read from.

```
history/
  era-profiles/        # Global structure of each time period
  country-profiles/    # Political systems, laws, macro indicators
  city-profiles/       # Demographics, cultural traits, economies
  event-library/       # Wars, crises, inventions, reforms
  signal-extraction/   # Economic/political cycles, patterns
  loaders/             # Import historical datasets cleanly
```

**Key Principle**: Phase 2 stores **truth keyframes and signals** (population, laws, tech level, macro indicators, canon events). It never encodes fixed city layouts or scripted future events. Everything is data-driven and era-authentic.

**Anti-Hardcoding Guarantee**: Nothing in Phase 1 or Phase 2 should ever encode fixed city layouts or scripted future events. Phase 2 is pure truth data.

---

## 2.4 world_generation/ — Phase 3: Physical World Appearance

Generates terrain, structures, cities, biomes, and geography for any era. This is a **blueprint generator**, not a renderer.

```
world_generation/
  earth-geometry/      # Terrain + paleoDEM
  biomes-climate/      # Land classification
  hydrology/           # River and coastline simulation
  structures/          # Procedural/AI-driven city and building generation
  chunking/            # Blueprint format for rendering
  historicalization/  # Different layouts per era
  exporters/           # Finalize world chunks for renderer
```

**Key Principles**:
- **Anti-hardcoding guarantee**: Phase 3 must remain a blueprint generator that reads truth from History (Phase 2) and writes structured outputs into WorldState. It should never sneak into Phase 1 tick logic beyond being called by the orchestrator.
- Phase 1 doesn't "know" buildings; it just knows how to ask the WorldGen engine to produce era-correct blueprints when needed.
- Worldgen produces **blueprints**, not visuals.
- Uses Phase 2 (History) as conditioning inputs to generate the physical world **on demand**, per timeline branch and per user action.
- Phase 3 uses Phase 2 truth keyframes as conditioning inputs to generate the physical world on demand.
- **Strict contract**: WorldGen outputs `ChunkBlueprint` objects (defined in `shared/types.py`). WorldGen never touches renderer formats. Renderer adapters live in `world_generation/exporters/` or in the client.

**Generation Flow**: Phase 2 (truth) → Phase 3 (blueprints) → WorldState → Renderer

**ChunkBlueprint Schema**:
- Defined in `backend/shared/types.py`
- Strict contract: `chunk_id`, `era`, `terrain_heightmap`, `biome_map`, `structures`, `metadata`
- This is the anti-hardcoding firewall: WorldGen outputs blueprints only, never renderer-specific formats

---

## 2.5 npc/ — Phase 4: The People

Defines populations, roles, identities, and behaviors. Autonomous agents that observe → think → act.

```
npc/
  profiles/            # NPC identity schema (personality, ideology, demographics, life history)
  cognition/           # Observe → think → act loop, decision policies, goal pursuit
  memory/              # Short/long-term memory store, summarization, retrieval
  dialogue/            # Conversation management, intent parsing, emotional tone
  social-network/      # Relationship graphs, family/friends/colleagues, influence networks
  behaviors/           # Action primitives (work, protest, buy, sell, flee, etc.)
  spawning/            # Population generation, era/city-appropriate NPCs, demographic distributions
  utils/               # Helper functions
```

**Key Principle**: NPC traits are sampled from era/culture distributions. Everything is AI-generated and emergent, not hardcoded. NPCs use Phase 5 (LLM/Consciousness) for cognition and dialogue, and Knowledge (RAG) for era-appropriate information.

---

## 2.6 llm/ — Phase 5: Consciousness Layer

Centralized AI usage for cognition, dialogue, memory recall. The consciousness layer that Phase 4 (People) uses.

```
llm/
  providers/           # OpenAI, Anthropic, model routing
  prompts/             # Prompt management, templates
  routing/             # Model selection (cheap vs strong LLM rules)
  tools/               # LLM function calling
  safety/              # Era-bounded knowledge validation, anachronism prevention
  rate_limiter.py      # Rate limiting and circuit breakers
```

**Key Principle**: Ensures era-bounded knowledge and avoids anachronisms. Cognition/dialogue is produced through LLM + memory + norms + incentives. This is a **Systems Layer service** that phase engines call into, not a direct dependency.

---

## 2.7 economy/ & money/ — Societal Behavior Engines

### Economy

```
economy/
  macro/               # Macroeconomic cycles
  markets/             # Market dynamics, pricing
  production/          # Production systems
  trade/               # Trade routes, commerce
  labor/               # Labor markets, employment
  shocks/              # Economic shocks, crises
  forecasts/           # Economic forecasting
```

### Money

```
money/
  wallets/             # Individual wallets
  assets/              # Asset types
  transactions/        # Transaction processing
  banking/             # Banking systems
  era-currency/        # Era-appropriate currencies
```

Together, Economy and Money simulate incentives, scarcity, and agent-level finances.

---

## 2.8 ideologies/ — Belief Systems

```
ideologies/
  political/           # Political ideologies
  economic/            # Economic ideologies
  cultural/            # Cultural beliefs
  religious/           # Religious systems
  diffusion/           # How beliefs spread through society
```

Models how beliefs spread and form societal pressure.

---

## 2.9 knowledge/ — RAG + Era Knowledge (Foundational Engine)

**Purpose**: Era-bounded truth layer that NPC minds, worldgen, and history call into. RAG foundation.

**Status**: First-class engine in terms of dependency. Knowledge/RAG feeds History + NPC + WorldGen. It doesn't belong inside NPC or History folders because it serves multiple engines.

```
knowledge/
  corpora/             # Document storage (primary sources, historical summaries, laws, newspapers)
  retrieval/           # Search interface, relevance ranking, context extraction
  embeddings/          # Vector DB connectors (pgvector), embedding generation, similarity search
  era-knowledge/       # Temporal constraints, what is available to be known in each era
  validation/          # Guardrails, prevent future knowledge leakage, anachronism detection
```

**Key Principle**: NPCs use this to "know things" appropriate to their time. Knowledge/RAG feeds History + NPC + WorldGen. It's foundational because it enables era-authentic behavior across multiple phase engines.

---

## 2.10 timeline/ — Time Travel & History Branching (Foundational Engine)

**Purpose**: Makes the Universe deterministic and branchable. Time travel, branching realities, snapshots, replay.

**Status**: First-class engine in terms of dependency. Timeline wraps state saves/replays. It's foundational because it enables deterministic rewinds and alternate realities.

```
timeline/
  event-log/           # Event history for replay
  snapshots/           # State snapshots for time travel
  branching/            # Timeline branching logic
  replay/               # Deterministic replay system
```

**Key Principle**: Timeline wraps state saves/replays. It's foundational because it enables deterministic rewinds and alternate realities. Timeline makes your Universe deterministic and branchable.

---

## 2.11 commands/ — Player Interactions (Systems Layer)

**Purpose**: Player interactions, generalized command layer for any client.

```
commands/
  registry/             # Command registry
  parsers/              # Command parsing
  actions/              # Action execution
  permissions/          # Permission system
```

**Status**: Systems Layer service. Cross-cutting concern for player interactions.

---

## 2.12 localization/ — Language Layer (Systems Layer)

**Purpose**: Language support, translation pipeline, fairness rules.

```
localization/
  languages/            # Language definitions
  translation/          # Translation pipeline
  fairness/             # Fairness rules, bias mitigation
```

Supports English, Chinese initially; manages translation bias.

**Status**: Systems Layer service. Cross-cutting concern for multi-language support.

---

## 2.13 api/ — Renderer Interface (Systems Layer)

**Purpose**: Renderer interface. The only bridge between the brain and visualization.

```
api/
  rest/                 # REST endpoints
  websocket/            # WebSocket protocol
  schemas/              # Request/response schemas
```

**Status**: Systems Layer service. The only bridge between the brain and visualization.

---

## 2.14 persistence/ — Databases & Storage (Infrastructure)

**Purpose**: Databases & storage.

```
persistence/
  postgres/             # PostgreSQL adapter with connection pooling
  cache/                # Redis adapter for fast access
  vector-db/            # Vector storage (via pgvector)
  migrations/           # Database schema versioning (Alembic)
```

**Database Version Note**: 
- **PostGIS 3.5+** supports PostgreSQL 12-18 (e.g., 3.5 requires PG12-17, newer releases cover PG12-18)
- **pgvector** works on PostgreSQL 13-16+ (many installs run it on PG13-16)
- The architecture doesn't depend on exact DB version, as long as PostGIS + pgvector are available
- Keep the stack flexible — don't let infra assumptions lock you later

---

## 2.15 systems/ — Systems Layer Namespace (Meta-Layer)

**Purpose**: Physical namespace for Systems Layer services. Makes the meta-layer explicit in the repo structure.

```
systems/
  safety/               # Era consistency, anachronism prevention
  telemetry/            # Observability, metrics
  pipelines/            # Data ingestion pipelines
  model_router/         # LLM model routing (cheap vs strong)
```

**Status**: Systems Layer meta-layer. Engines call these through interfaces, preventing drift.

**Key Principle**: The Systems Layer namespace makes the meta-layer physical. Engines import from `systems/` for cross-cutting services, not from phase engines.

---

## 2.16 observability/ — Systems Layer Tools

**Purpose**: Logs, metrics, inspector UI for debugging.

```
observability/
  logs/                 # Structured logging
  metrics/              # Prometheus metrics
  inspector/            # Debug inspector UI
```

**Status**: Not a phase — supports all phases. Systems Layer service.

---

## 2.17 shared/ — Universal Helpers

**Purpose**: Universal helpers, types, constants, utilities.

```
shared/
  types/                # Type definitions (AgentID, Time, Location, ChunkBlueprint, etc.)
  constants/            # Constants (DEFAULT_SEED, DEFAULT_TICK_RATE)
  time.py              # Canonical time unit and calendar model
  interfaces.py         # Core interfaces (Engine, EventPublisher, EventSubscriber)
  base_engine.py       # BaseEngine class
  architecture.py      # Architecture boundary enforcement and validation
  import_validator.py  # AST-based import validation
  batch_processor.py   # Batch processing utilities
  task_queue.py        # Async task queue
  resource_limits.py    # Resource monitoring and limits
  utils/                # Shared utilities
```

**Key Components**:
- **`time.py`** - Canonical time model: UTC internally, 1 tick = 1 day, epoch = Jan 1, 1 CE. Localization handled in Phase 6.
- **`types.py`** - Includes `ChunkBlueprint` schema for Phase 3 output contract.
- **`architecture.py`** - Architecture boundary definitions and validation utilities.
- **`import_validator.py`** - AST-based validation to prevent phase engine cross-imports.

---

## 3. game-client-minecraft/ — Phase 6: Visualization (Renderer)

**Phase 6: Visualization (Renderer)** — Minecraft / 3D engine — the camera.

A thin client visualizing the simulation. Handles NPC entity rendering, world block updates, player actions.

This is Phase 6 of the 7-phase architecture. The renderer is the camera that visualizes the simulation brain. It consumes the API and renders the world, but never owns simulation logic.

```
game-client-minecraft/
  plugin/
  bridge/
  ui/
  assets/
  configs/
```

**Status**: Renderer = camera. Backend = reality. The brain is the real product.

---

## 4. System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│              Systems Layer (Meta-Layer)                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ Observability│  │     LLM     │  │ Localization│       │
│  │   Safety     │  │   Routing   │  │ Translation │       │
│  │   Testing    │  │   Pipelines │  │   Metrics   │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ Services all phases
                            ▼
┌─────────────────────────────────────────────────────────────┐
│     Phase 6: Visualization (Renderer) - The Camera          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │  Minecraft   │  │   Web UI    │  │   CLI Tool   │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ REST/WebSocket API
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      API Layer (Systems Layer)              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │   REST API   │  │  WebSocket   │  │   Schemas   │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  Phase 1: Universe + Phase 7: Orchestrator (THE ACTUAL GAME) │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  SimulationOrchestrator  →  TickScheduler          │   │
│  │  WorldState  →  EventBus  →  Determinism          │   │
│  │  (Binds all phases, evolves universe, drives timelines)│   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ Orchestrates all phases
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    Phase Engines                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ Phase 2:     │  │ Phase 3:     │  │ Phase 4:     │       │
│  │  History     │  │  Appearance  │  │  People      │       │
│  │  (Truth)     │  │  (WorldGen)  │  │  (NPCs)      │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ Phase 5:     │  │  Economy/     │  │  Ideologies  │       │
│  │ Consciousness│  │  Money       │  │              │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ Use Systems Layer services
                            │ No direct imports between phases
                            ▼
┌─────────────────────────────────────────────────────────────┐
│         Foundational Engines (Serve Multiple Phases)        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │  Timeline    │  │  Knowledge   │  │  Commands    │       │
│  │ (Branching)  │  │  (RAG/Era)   │  │  (Player)    │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              Infrastructure Layer                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │  Persistence │  │   Cache      │  │   Metrics    │       │
│  │  (Postgres)  │  │   (Redis)    │  │ (Prometheus) │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. Runtime Flow

Every tick:

1. **Universe tick engine advances time** (Phase 1: The Universe)
2. **Simulation orchestrator calls all subsystems** (Phase 7: THE ACTUAL GAME)
3. **NPCs think and act** (Phase 4, using Phase 5 for consciousness)
4. **Economy updates** (Societal behavior)
5. **Ideologies spread** (Societal behavior)
6. **Worldgen updates structures or terrain** (Phase 3, reading from Phase 2)
7. **Timeline records snapshots and events** (Foundational engine)
8. **Renderer clients receive updates** (Phase 6: Visualization - The Camera)

**Renderer = camera. Backend = reality.**

### Boot Sequence

```
1. FastAPI app starts (main.py)
2. Bootstrap creates SimulationOrchestrator with seed
3. Orchestrator initializes:
   - EventBus (starts worker pool)
   - WorldState (from scenario or defaults)
   - DeterministicRandom (with seed)
4. Phase engines registered via bootstrap:
   - Phase 2: History
   - Phase 3: World Generation
   - Phase 4: NPC
   - Phase 5: LLM (consciousness) - Systems Layer service
   - Foundational: Timeline, Knowledge
   - Societal: Economy, Money, Ideologies
5. Orchestrator.initialize() called:
   - Sorts engines by priority/dependencies
   - Calls engine.initialize(state) for each
   - Sets up event subscriptions
6. Orchestrator.start() called:
   - Creates TickScheduler
   - Starts tick loop
```

### Tick Loop Flow

```
1. TickScheduler._tick() called
2. Update simulation time: state.current_time += time_per_tick
3. Increment tick_count
4. For each engine (in priority order):
   a. Call engine.tick(state, delta_time)
   b. Engine may:
      - Read from Phase 2 (History) for truth
      - Generate blueprints (Phase 3) on demand
      - Use Systems Layer services (LLM, Knowledge, etc.)
      - Update its state in state.engine_states
      - Publish events via EventBus
      - Read events from EventBus
5. Log: "Day {tick_count}: {current_time}"
6. Timeline records snapshot (if configured)
7. Sleep for tick_rate seconds
8. Repeat
```

### Event Flow

```
1. Engine publishes event: event_bus.publish(event_type, event_data)
2. Event added to async queue
3. Worker thread picks up event
4. EventBus finds subscribers (by type or wildcard)
5. Subscribers.handle_event() called asynchronously
6. Event statistics updated
```

### Phase Interaction Rules

**Critical Boundaries**:
- **No direct imports between phase engines**: Phase engines never directly import other phase engines. They communicate via:
  - EventBus (pub/sub)
  - WorldState (shared state)
  - Systems Layer services (LLM, Knowledge, etc.)
- **Phase 3 (WorldGen) reads from Phase 2 (History)**: WorldGen uses History as conditioning inputs to generate blueprints on demand.
- **Phase 4 (NPC) uses Phase 5 (LLM)**: NPCs use the LLM layer for consciousness, but LLM is a Systems Layer service, not a direct dependency.
- **Timeline and Knowledge serve multiple phases**: These foundational engines are called by History, NPC, WorldGen, etc., but they're separate modules.

---

## 6. Technology Stack

### Core
- **Language**: Python 3.11+
- **Framework**: FastAPI 0.104+ (async REST/WebSocket)
- **ASGI Server**: Uvicorn

### Data Science
- NumPy, Pandas, SciPy, scikit-learn
- For economic modeling, demographic analysis, signal processing

### AI/LLM
- OpenAI API, Anthropic API
- LangChain for orchestration
- Sentence transformers for embeddings

### Database
- **PostgreSQL 12-18**: Structured data storage (flexible version support)
- **PostGIS 3.5+**: Geospatial extension (supports PG12-18)
- **pgvector**: Vector embeddings extension (works on PG13-16+)
- **SQLAlchemy 2.0+**: Async ORM
- **Alembic**: Database migrations

**Note**: PostGIS and pgvector work across multiple PostgreSQL versions. The architecture doesn't depend on exact DB version, as long as extensions are available. Keep the stack flexible.

### Caching
- **Redis 5.0+**: Fast in-memory cache
- **hiredis**: High-performance Redis client

### Observability
- **structlog**: Structured logging
- **prometheus-client**: Metrics collection

### Development
- **pytest**: Testing framework
- **mypy**: Type checking
- **ruff**: Linting
- **black**: Code formatting

---

## 7. Design Principles

### 1. Modular Separation
Each phase is a dedicated module with clear boundaries. Phase engines don't know about each other directly — they communicate via events and Systems Layer services.

### 2. Renderer-Agnostic
Backend outputs data, not visuals. Any client (Minecraft, web, CLI) can consume the API. The brain is the real product.

### 3. Deterministic Simulation
- Seeded random number generation
- Reproducible tick execution
- Replayable timelines
- Branchable history

### 4. Era-Authentic
- Knowledge bounded by era (no anachronisms)
- NPCs behave according to cultural/historical context
- Economic systems match historical regimes
- Technologies available only in appropriate eras

### 5. AI-Generated, Emergent Content
**Critical**: Nothing is hardcoded. Everything is generated:

- **Phase 1/2**: Never encode fixed city layouts or scripted future events
- **Phase 2**: Stores truth keyframes and signals (population, laws, tech level, macro indicators, canon events)
- **Phase 3**: Generates physical world on demand using Phase 2 as conditioning inputs, per timeline branch and per user action
- **Phase 4+5**: Generate people/minds from era/culture distributions and LLM + memory + norms + incentives
- **Orchestrator**: Only sequences and validates; it never invents content itself

**If you keep that boundary, your world will stay emergent forever.**

### 6. Systems Layer as Meta-Layer
Systems Layer services (LLM, Knowledge, Observability, etc.) surround all phases. No phase engine directly imports another phase engine — only shared interfaces + Systems Layer services.

### 7. Scalable Architecture
- Connection pooling for database
- Caching layer for performance
- Event queue with backpressure
- State compression and diffing
- Batch processing support
- Resource limits and monitoring

### 8. Architecture Enforcement
- **Import validation** - AST-based checker prevents phase engine cross-imports
- **Systems Layer namespace** - Physical `backend/systems/` folder makes meta-layer explicit
- **WorldState versioning** - Schema version + migration hooks for time travel snapshots
- **ChunkBlueprint contract** - Strict schema for Phase 3 output (anti-hardcoding firewall)
- **Engine priority spec** - `configs/engine-order.yaml` defines execution order and dependencies
- **Canonical time model** - UTC internally, localized in Phase 6 (prevents time travel mess)
- **Headless realism harness** - CLI tool for scientific validation before renderer integration

---

## 8. Brain Completion Criteria

The brain is considered "ready to render" when:

- ✅ It can load any place/time snapshot
- ⏳ NPCs behave realistically over weeks of ticks
- ⏳ The economy reacts to actions
- ⏳ Rewinds/branches replicate deterministically
- ⏳ Worldgen builds accurate environments for the era

Then it's ready for visualization.

---

## 9. Current Implementation Status

### ✅ Phase 0 Complete

**Infrastructure**:
- ✅ Folder structure and module organization
- ✅ Python 3.11+ + FastAPI framework locked in
- ✅ Configuration system (dev/prod/secrets)
- ✅ PostgreSQL + Redis running locally
- ✅ Backend boots cleanly
- ✅ Deterministic tick loop working

**Core Components**:
- ✅ SimulationOrchestrator (Phase 1 + Phase 7)
- ✅ TickScheduler
- ✅ EventBus (with backpressure)
- ✅ WorldState (with compression/diffing)
- ✅ DeterministicRandom
- ✅ BaseEngine class
- ✅ Engine interfaces

**Infrastructure**:
- ✅ PostgreSQL connection pooling
- ✅ Redis cache adapter
- ✅ Prometheus metrics collector
- ✅ Rate limiting and circuit breakers
- ✅ Batch processing utilities
- ✅ Task queue
- ✅ Resource limits

**Architecture Enforcement**:
- ✅ Systems Layer namespace (`backend/systems/`)
- ✅ WorldState versioning with migration hooks
- ✅ Canonical time model (`backend/shared/time.py`)
- ✅ ChunkBlueprint schema (`backend/shared/types.py`)
- ✅ Engine priority order spec (`configs/engine-order.yaml`)
- ✅ Import validation (`backend/shared/import_validator.py`, `scripts/validate_architecture.py`)
- ✅ Headless realism harness (`tools/headless_realism_harness.py`)

### ⏳ Phase 1 (Next)

**Phase Engines** (structure defined, implementation pending):
- ⏳ Phase 2: History engine
- ⏳ Phase 3: World generation engine
- ⏳ Phase 4: NPC engine
- ⏳ Phase 5: LLM/Consciousness layer (Systems Layer service)
- ⏳ Economy engine
- ⏳ Money engine
- ⏳ Ideology engine

**Foundational Engines**:
- ⏳ Timeline branching implementation
- ⏳ Knowledge RAG system

**Systems Layer**:
- ⏳ Command system
- ⏳ Localization system
- ⏳ Enhanced observability

---

## 10. Guiding Philosophy

The architecture ensures:

- **Zero hardcoding** of buildings or societal behavior
- **Everything is emergent**, driven by history and AI
- **The world runs independently** of graphics
- **Time travel is deterministic**
- **Any renderer can be swapped in**
- **Modules never depend on renderer**
- **The brain is the real product**

---

## 11. Future Considerations

### Horizontal Scaling
- Distributed state management
- Multi-instance coordination
- Sharding strategies

### Performance Optimization
- Lazy loading for large simulations
- Geographic partitioning
- On-demand world generation

### Advanced Features
- Real-time multiplayer support
- Advanced time travel UI
- Scenario marketplace
- Historical data import

---

## Conclusion

The architecture is designed to be:
- **Modular**: Clear phase separation
- **Scalable**: Infrastructure ready for growth
- **Deterministic**: Reproducible and branchable
- **Era-Authentic**: Historical accuracy built-in
- **Renderer-Agnostic**: Any client can consume the API
- **AI-Generated**: Nothing hardcoded, everything emergent

Phase 0 has established a solid foundation. The simulation brain is alive, the tick loop is the spine, and phase engines can now be added incrementally without breaking the system or introducing hardcoding risks.

**The current Phase 0 foundation is not just compatible with the vision — it's the right launchpad for Phase 1 and onward without hardcoding risk.**
