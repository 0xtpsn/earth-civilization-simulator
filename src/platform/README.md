# Platform
Shared infrastructure used by all engines.

- `core/` — types, contracts, error handling, configuration loading.
- `state/` — state container, diffing, deterministic randomness, seeding.
- `persistence/` — snapshot storage, logs, checkpoints, timeline branching metadata.
- `analytics/` — signals, metrics, forecasting utilities, structural-demographic calculators.
- `ai_adapters/` — pluggable external models (e.g., LLM/NLP) behind capability-safe interfaces.
