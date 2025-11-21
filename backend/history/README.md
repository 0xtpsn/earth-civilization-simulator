# History Engine

The world's recorded timeline, era profiles, and historical data that serves as the "truth backbone" for the simulation.

## Structure

- **`era-profiles/`** — Global era characteristics
  - Social norms per time period
  - Technology levels
  - Dominant beliefs and ideologies
  - Economic systems
  - Political structures

- **`country-profiles/`** — National-level data
  - Regime types by year
  - Laws and legal systems
  - Macro indicators (GDP, population, etc.)
  - Political stability metrics
  - Historical transitions

- **`city-profiles/`** — Local-level data
  - Local economy characteristics
  - Demographics by year
  - Cultural composition
  - Industrial specialization
  - Historical events

- **`event-library/`** — Canonical historical events
  - Wars, crises, inventions
  - Reforms and revolutions
  - Natural disasters
  - Economic shocks
  - With timestamps and locations

- **`signal-extraction/`** — Convert history into forecasting signals
  - Political instability indicators
  - Economic cycle detection
  - Demographic pressure signals
  - Elite competition metrics
  - Structural-demographic theory calculations

- **`loaders/`** — Data ingestion
  - Ingest historical datasets
  - Normalize into DB schemas
  - Validate era constraints
  - Handle data gaps

## Purpose

History is the "truth backbone" the simulation reads from. It provides:
- Constraints on what's possible in each era
- Baseline data for NPC generation
- Patterns for predictive analytics
- Validation for simulation outputs

