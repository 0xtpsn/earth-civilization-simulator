# Simulation Engine

The master orchestrator of time, rules, and systems — the "physics engine for civilization."

## Structure

- **`tick/`** — Time stepping
  - Daily/weekly stepping
  - Fast-forward batching
  - Time dilation
  - Tick scheduling

- **`state/`** — Canonical world state
  - Everything serializable
  - Global state object
  - State snapshots
  - State diffs

- **`rules/`** — Hard constraints
  - Laws and legal systems
  - Physics constraints
  - Capacity limits
  - Era limits
  - Validation rules

- **`event-propagation/`** — Ripple effects
  - How actions ripple across systems
  - Market reactions
  - Political responses
  - Social diffusion
  - Cascading effects

- **`determinism/`** — Reproducibility
  - Seeds and random streams
  - Replay correctness
  - Deterministic execution
  - Branch point tracking

- **`scenarios/`** — Spawn presets
  - "Singapore 2025"
  - "Cleveland 1860"
  - "Jakarta 1998"
  - Scenario definitions
  - Initial state generation

## Responsibilities

- Coordinate all domain engines
- Manage time progression
- Enforce rules and constraints
- Propagate events across systems
- Ensure deterministic execution
- Handle scenario initialization

## Design

This is the "physics engine for civilization" — it doesn't model specific domains (that's what engines do), but rather orchestrates how they interact over time.

