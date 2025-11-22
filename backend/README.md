# Backend

The simulation brain — the core product that models human civilization across time.

## Module Overview

### Core Orchestration
- **`app/`** — Entry point, dependency injection, service registry, tick scheduler

### Domain Engines
- **`npc/`** — Human agents: cognition, memory, dialogue, social networks, behaviors
- **`world-generation/`** — Geography, biomes, structures, chunk blueprints
- **`history/`** — Era/country/city profiles, event library, signal extraction
- **`ideologies/`** — Belief systems: political, economic, cultural, religious
- **`economy/`** — Markets, production, trade, labor, macro cycles, shocks
- **`money/`** — Financial accounts, wallets, assets, transactions, banking

### Supporting Systems
- **`knowledge/`** — RAG, era-bounded knowledge, retrieval, embeddings
- **`simulation_engine/`** — Tick loop, state management, rules, determinism
- **`timeline/`** — Time travel, branching, snapshots, replay
- **`commands/`** — Player command layer (timejump, spawn, inspect, etc.)
- **`llm/`** — Model providers, prompts, routing, safety
- **`localization/`** — Languages, translation, fairness rules

### Infrastructure
- **`api/`** — REST/WebSocket interface for clients
- **`persistence/`** — Postgres, vector DB, cache, migrations
- **`observability/`** — Logs, metrics, inspector UI
- **`shared/`** — Types, constants, utilities

## Design Principles

1. **Separation of concerns** — Each module owns one domain
2. **No renderer dependencies** — Backend outputs data, not visuals
3. **Deterministic** — Seeded randomness, replayable ticks
4. **Era-authentic** — Knowledge and behaviors respect historical constraints

