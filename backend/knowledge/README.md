# Knowledge Engine

RAG foundation and "what agents know" — the library of reality for the simulation.

## Structure

- **`corpora/`** — Document storage
  - Primary sources
  - Historical summaries
  - Laws and legal texts
  - Newspapers and periodicals
  - Era-appropriate documents

- **`retrieval/`** — Search and ranking
  - Search interface for NPC/LLM
  - Relevance ranking
  - Context extraction
  - Query processing

- **`embeddings/`** — Vector representations
  - Vector DB connectors
  - Embedding generation
  - Similarity search
  - Semantic indexing

- **`era-knowledge/`** — Temporal constraints
  - What is available to be known in each era
  - Anachronism prevention
  - Knowledge availability windows
  - Historical information limits

- **`validation/`** — Guardrails
  - Prevent future knowledge leakage
  - Era-bounded knowledge checks
  - Anachronism detection
  - Source verification

## Purpose

This is the "library of reality" for the simulation:
- NPCs query this for era-appropriate knowledge
- LLMs use this for context
- Players can access historical information
- System validates that knowledge matches era

## Key Constraint

**No anachronisms** — A 1300 CE scholar cannot know about 2025 technology. The validation layer enforces era-appropriate knowledge boundaries.

