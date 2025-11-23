"""Core type definitions used across the backend."""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, NewType, Optional
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


@dataclass
class ChunkBlueprint:
    """
    ChunkBlueprint schema - strict contract for Phase 3 (WorldGen) output.
    
    This is the anti-hardcoding firewall: WorldGen outputs blueprints only,
    never renderer-specific formats. Renderer adapters live in
    world_generation/exporters/ or in the client.
    
    ARCHITECTURE:
    - Phase 3 (WorldGen) outputs ChunkBlueprint objects
    - Renderers consume ChunkBlueprint and convert to their format
    - WorldGen never touches renderer formats directly
    """
    
    # Chunk identification
    chunk_id: ChunkID  # (x, y, z) coordinates
    era: Era  # Era this blueprint represents
    
    # Terrain data
    terrain_heightmap: Optional[List[List[float]]] = None  # Height values per block
    biome_map: Optional[List[List[str]]] = None  # Biome IDs per block
    
    # Structure data (buildings, roads, etc.)
    structures: List[Dict[str, Any]] = None  # List of structure definitions
    
    # Metadata
    metadata: Dict[str, Any] = None  # Additional metadata (LOD, generation params, etc.)
    
    def __post_init__(self):
        """Initialize default values."""
        if self.structures is None:
            self.structures = []
        if self.metadata is None:
            self.metadata = {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize blueprint to dictionary."""
        return {
            "chunk_id": self.chunk_id,
            "era": str(self.era),
            "terrain_heightmap": self.terrain_heightmap,
            "biome_map": self.biome_map,
            "structures": self.structures,
            "metadata": self.metadata,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ChunkBlueprint":
        """Deserialize blueprint from dictionary."""
        return cls(
            chunk_id=ChunkID(tuple(data["chunk_id"])),
            era=Era(data["era"]),
            terrain_heightmap=data.get("terrain_heightmap"),
            biome_map=data.get("biome_map"),
            structures=data.get("structures", []),
            metadata=data.get("metadata", {}),
        )

