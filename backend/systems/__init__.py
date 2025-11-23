"""
Systems Layer - Meta-Layer Services

This namespace contains cross-cutting services that surround all phases.
Phase engines can import from systems/, but phase engines cannot import each other.

ARCHITECTURE:
- This is the Systems Layer meta-layer
- Can be imported by phase engines
- Should not import phase engines directly
- Provides cross-cutting services: safety, telemetry, pipelines, model routing

STRUCTURE:
- systems/safety/ - Era consistency, anachronism prevention
- systems/telemetry/ - Observability, metrics (may move from observability/)
- systems/pipelines/ - Data ingestion pipelines
- systems/model_router/ - LLM model routing (may move from llm/routing/)
"""

# Systems Layer meta-layer - can be imported by phase engines
# Do not import phase engines from here

