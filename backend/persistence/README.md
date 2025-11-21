# Persistence Module

Database connectors and repositories — keeps storage cleanly decoupled from logic.

## Structure

- **`postgres/`** — Structured data storage
  - World state
  - NPC data
  - Economic data
  - Historical records
  - Relational schemas

- **`vector-db/`** — Embedding storage
  - Memory embeddings
  - Knowledge embeddings
  - Semantic search
  - Similarity queries

- **`cache/`** — Fast access layer
  - Redis or similar
  - Frequently accessed data
  - Session state
  - Performance optimization

- **`migrations/`** — Schema versioning
  - Database migrations
  - Schema evolution
  - Version control
  - Rollback support

## Design

**Decoupled storage** — Logic modules don't know about database details. They use repository interfaces, and this module handles the actual storage implementation.

## Responsibilities

- Store world state
- Persist NPC memory
- Save timeline snapshots
- Cache frequently accessed data
- Handle schema migrations

