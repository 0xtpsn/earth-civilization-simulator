# Data

Source files and experiment fixtures that feed the simulation.

## Structure

- **`seeds/`** — Curated starting states
  - Era/region starting states
  - Agent seeds
  - Scenario definitions
  - Initial world states

- **`reference/`** — Static reference data
  - Historical datasets
  - Lookup tables
  - Geospatial layers
  - Era profiles
  - Country/city data

- **`experiments/`** — Scenario experiments
  - Scenario definitions
  - Model-tuning inputs
  - Test configurations
  - Experiment results

## Usage

This data feeds into:
- **`backend/history/loaders/`** — Historical data import
- **`backend/world-generation/`** — Geography and structure data
- **`backend/simulation_engine/scenarios/`** — Starting states
- **`tools/importers/`** — Data processing
