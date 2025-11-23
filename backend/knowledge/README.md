# Knowledge Engine

RAG foundation and "what agents know" — the library of reality for the simulation.

## Structure

- **`corpora/`** — Document storage
- **`retrieval/`** — Search and ranking
- **`embeddings/`** — Vector representations
- **`era-knowledge/`** — Temporal constraints
- **`validation/`** — Guardrails

## Purpose

This is the "library of reality" for the simulation:
- NPCs query this for era-appropriate knowledge
- LLMs use this for context
- Players can access historical information
- System validates that knowledge matches era

## Key Constraint

**No anachronisms** — A 1300 CE scholar cannot know about 2025 technology. The validation layer enforces era-appropriate knowledge boundaries.

