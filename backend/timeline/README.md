# Timeline Engine

Time travel, branching realities, snapshots, and replay — makes "go back and change history" real.

## Structure

- **`event-log/`** — Append-only action/event sourcing
  - All actions recorded
  - Immutable log
  - Event replay capability
  - Chronological ordering

- **`snapshots/`** — Periodic frozen world states
  - Full state captures
  - Compressed storage
  - Snapshot intervals
  - State restoration

- **`branching/`** — Forked timelines
  - New seeds for branches
  - Divergence markers
  - Branch metadata
  - Timeline comparison

- **`replay/`** — Reconstruction
  - Reconstruct any date from log + snapshot
  - Fast-forward through history
  - State restoration
  - Deterministic replay

## Features

### Time Travel
- Jump to past or future dates
- Restore player state (wealth, injuries, legal status, reputation)
- Reset NPC memory appropriately
- Butterfly effect simulation

### Branching Timelines
- Each revisit creates a new branch
- Compare outcomes across branches
- Learn how different actions lead to different futures

### Replay
- Reconstruct any moment in history
- Fast-forward through time
- Step through events
- Debug simulation behavior

## Integration

Works closely with:
- **`simulation_engine/`** — For state snapshots
- **`persistence/`** — For storage
- **`npc/`** — For memory reset on time travel

