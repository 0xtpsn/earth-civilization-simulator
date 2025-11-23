"""
Societal Behavior Engine: Ideologies

Belief systems and how they spread.

ARCHITECTURE RULES:
- This is a societal behavior engine (not a numbered phase, but follows same rules)
- CAN import: shared/, persistence/, Systems Layer services
- CANNOT import: Other phase engines directly
- MUST communicate with other phases via: EventBus, WorldState
"""

# Societal behavior engine - do not import other phase engines directly
# Use EventBus, WorldState, or Systems Layer services for communication

