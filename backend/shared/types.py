"""Core type definitions used across the backend."""

from datetime import datetime
from typing import NewType
from uuid import UUID

# Type aliases for domain concepts
Time = NewType("Time", datetime)
Location = NewType("Location", str)  # Format: "City, Country" or coordinates
AgentID = NewType("AgentID", UUID)
TimelineID = NewType("TimelineID", UUID)
ScenarioID = NewType("ScenarioID", str)
Era = NewType("Era", str)  # Format: "YYYY" or "YYYY-MM-DD"

# Economic types
Currency = NewType("Currency", str)
Price = NewType("Price", float)
Quantity = NewType("Quantity", float)

# Geographic types
Latitude = NewType("Latitude", float)
Longitude = NewType("Longitude", float)
ChunkID = NewType("ChunkID", tuple[int, int, int])  # (x, y, z) coordinates

