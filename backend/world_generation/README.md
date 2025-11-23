# World Generation

Physical geography, biomes, structures, and era-aware environment reconstruction.

## Structure

- **`earth-geometry/`** — Terrain and elevation
- **`biomes-climate/`** — Environmental systems
- **`hydrology/`** — Water systems
- **`structures/`** — Built environment
- **`chunking/`** — Spatial organization
- **`historicalization/`** — Era-specific layers
- **`exporters/`** — Format conversion

## Output

This module outputs **blueprints**, not final visuals:
- Chunk data structures
- Block/material assignments
- Structure metadata
- Era-specific overlays

Rendering happens in the client layer.

