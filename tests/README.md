# Tests

Global tests that span multiple modules.

## Structure

- **`integration/`** — Cross-module integration tests
  - Backend + agents + economy + timeline tests
  - End-to-end scenario tests
  - Multi-engine interaction tests

- **`simulation-regression/`** — Regression tests
  - Replay old seeds to ensure updates don't break realism
  - Deterministic replay tests
  - Behavior consistency checks

- **`unit/`** — Unit tests for individual modules
  - Module-specific tests
  - Isolated component tests

## Testing Philosophy

- **Deterministic** — All tests should be reproducible
- **Realistic** — Integration tests should validate simulation realism
- **Fast** — Unit tests should run quickly
- **Comprehensive** — Cover critical paths and edge cases
