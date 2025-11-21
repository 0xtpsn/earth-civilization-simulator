# World Generation

Physical geography, biomes, structures, and era-aware environment reconstruction.

## Structure

- **`earth-geometry/`** — Terrain and elevation
  - DEM/paleoDEM loaders
  - Heightmap logic
  - Tectonic keyframes
  - Historical terrain reconstruction

- **`biomes-climate/`** — Environmental systems
  - Biome assignment rules
  - Climate models per era
  - Vegetation patterns
  - Seasonal variations

- **`hydrology/`** — Water systems
  - Rivers and watersheds
  - Lakes and coastlines
  - Derived from terrain data
  - Historical waterway changes

- **`structures/`** — Built environment
  - City growth algorithms
  - Roads and infrastructure
  - Farms and agriculture
  - Landmarks per culture/era
  - Building styles by period

- **`chunking/`** — Spatial organization
  - Chunk blueprint format
  - Streaming rules
  - LOD (level of detail) management

- **`historicalization/`** — Era-specific layers
  - Swap structure layers by year
  - 1860 Cleveland vs 2025 Cleveland
  - Progressive development over time

- **`exporters/`** — Format conversion
  - Convert chunk blueprints to Minecraft blocks
  - Future: Unreal meshes, other formats
  - Renderer-agnostic output

## Output

This module outputs **blueprints**, not final visuals:
- Chunk data structures
- Block/material assignments
- Structure metadata
- Era-specific overlays

Rendering happens in the client layer.

