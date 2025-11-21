# Architecture Skeleton

## Layering
- Simulation runtime (`backend/simulation-engine/`): tick loop, scheduler, event bus, orchestration policies.
- Engines (`backend/`): NPC, economy, ideologies, world-generation, history, timeline, localization, knowledge.
- Platform (`backend/`): shared contracts, state mgmt, persistence, observability, LLM adapters.
- Data (`data/`): seeds, reference layers, scenario experiments.
- Tests (`tests/`): unit and integration harnesses.

## Core flows (first pass)
- Boot: load scenario seed -> hydrate state -> register engines -> start deterministic tick loop.
- Tick: orchestrator orders engine updates -> engines publish events -> event bus fans out -> state diffs persisted.
- Branch/replay: timeline engine snapshots -> persistence stores checkpoints -> scheduler can fork or rewind.
- Observe: observability layer computes signals -> feeds predictive/ideology/economy engines -> exposes telemetry for UX.

## Next steps
- Define minimal TypeScript or Python package structure under `backend/` with inter-engine interfaces.
- Add schema for seeds and reference data (JSON/Parquet/etc.) plus validation.
- Build a thin CLI to create/run/fork scenarios in headless mode.
- Wire tests for deterministic tick and snapshot/branch lifecycle.

