# Observability Module

Debugging the simulation — logs, metrics, and inspector tools.

## Structure

- **`logs/`** — Structured logging
- **`metrics/`** — Performance and behavior metrics
- **`inspector/`** — Internal admin panel

## Purpose

This is how you:
- **Prove realism** — Show that simulation produces believable behavior
- **Find bugs** — Debug why something isn't working
- **Monitor performance** — Track system health
- **Analyze behavior** — Understand simulation dynamics

## Usage

The inspector UI (in `tools/debug-ui/`) connects to this module to provide a debugging interface for developers and researchers.

