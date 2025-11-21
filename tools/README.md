# Tools

Development tooling, not part of runtime — utilities for debugging, profiling, and data import.

## Structure

- **`profilers/`** — Performance profiling tools
  - Simulation performance profilers
  - Memory usage analyzers
  - Tick time measurements
  - Bottleneck detection

- **`debug-ui/`** — Simulation inspector UI
  - Internal admin panel
  - Pause/step controls
  - Agent state viewer
  - World state inspector
  - Timeline browser
  - Connects to `backend/observability/`

- **`importers/`** — One-off dataset import tools
  - Historical data importers
  - Geography data loaders
  - Event library builders
  - Reference data processors

## Usage

These tools are for development and debugging, not part of the production simulation runtime. They help developers:
- Profile performance
- Debug simulation behavior
- Import historical datasets
- Inspect world state

