# History Engine

The world's recorded timeline, era profiles, and historical data that serves as the "truth backbone" for the simulation.

## Structure

- **`era-profiles/`** — Global era characteristics
- **`country-profiles/`** — National-level data
- **`city-profiles/`** — Local-level data
- **`event-library/`** — Canonical historical events
- **`signal-extraction/`** — Convert history into forecasting signals
- **`loaders/`** — Data ingestion

## Purpose

History is the "truth backbone" the simulation reads from. It provides:
- Constraints on what's possible in each era
- Baseline data for NPC generation
- Patterns for predictive analytics
- Validation for simulation outputs

