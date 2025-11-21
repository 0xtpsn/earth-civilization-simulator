# Observability Module

Debugging the simulation — logs, metrics, and inspector tools.

## Structure

- **`logs/`** — Structured logging
  - Simulation event logs
  - Error tracking
  - Debug information
  - Audit trails

- **`metrics/`** — Performance and behavior metrics
  - Economy statistics
  - Political indicators
  - NPC behavior stats
  - System performance
  - Realism metrics

- **`inspector/`** — Internal admin panel
  - Pause/step simulation
  - View agent states
  - Inspect world state
  - Debug tools
  - State visualization

## Purpose

This is how you:
- **Prove realism** — Show that simulation produces believable behavior
- **Find bugs** — Debug why something isn't working
- **Monitor performance** — Track system health
- **Analyze behavior** — Understand simulation dynamics

## Usage

The inspector UI (in `tools/debug-ui/`) connects to this module to provide a debugging interface for developers and researchers.

