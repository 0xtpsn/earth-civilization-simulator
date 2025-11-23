# Simulation Engine

The master orchestrator of time, rules, and systems — the "physics engine for civilization."

## Structure

- **`tick/`** — Time stepping
- **`state/`** — Canonical world state
- **`rules/`** — Hard constraints
- **`event-propagation/`** — Ripple effects
- **`determinism/`** — Reproducibility
- **`scenarios/`** — Spawn presets

## Responsibilities

- Coordinate all domain engines
- Manage time progression
- Enforce rules and constraints
- Propagate events across systems
- Ensure deterministic execution
- Handle scenario initialization

## Design

This is the "physics engine for civilization" — it doesn't model specific domains (that's what engines do), but rather orchestrates how they interact over time.

