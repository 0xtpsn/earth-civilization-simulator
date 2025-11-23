# Persistence Module

Database connectors and repositories — keeps storage cleanly decoupled from logic.

## Structure

- **`postgres/`** — Structured data storage
- **`vector-db/`** — Embedding storage (via pgvector)
- **`cache/`** — Fast access layer
- **`migrations/`** — Schema versioning

## Design

**Decoupled storage** — Logic modules don't know about database details. They use repository interfaces, and this module handles the actual storage implementation.

## Responsibilities

- Store world state
- Persist NPC memory
- Save timeline snapshots
- Cache frequently accessed data
- Handle schema migrations

