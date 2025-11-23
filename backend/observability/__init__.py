"""
Systems Layer: Observability

Logs, metrics, inspector UI for debugging.

ARCHITECTURE:
- This is a Systems Layer service, not a phase engine
- Can be imported by phase engines
- Should not import phase engines directly
- Supports all phases with cross-cutting observability concerns
"""

# Systems Layer service - can be imported by phase engines
# Do not import phase engines from here

