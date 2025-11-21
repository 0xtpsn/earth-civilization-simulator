# Minecraft Client

Paper/Spigot plugin for rendering the simulation in Minecraft — a disposable tester client.

## Structure

- **`plugin/`** — Core plugin code
  - `npc-renderer/` — Spawn/display NPCs by backend instructions
  - `world-renderer/` — Place blocks from chunk blueprints
  - `player-hooks/` — Capture player actions and send to backend
  - `time-controls/` — In-game commands mapped to backend commands

- **`bridge/`** — Networking to backend
  - WebSocket client
  - REST client
  - Retry/queue logic
  - Connection management

- **`ui/`** — Minecraft UI components
  - Chat menus
  - Simple overlays
  - Dialogue popups (as far as Minecraft allows)
  - HUD elements

- **`assets/`** — Resource pack assets (optional)
  - Skins for era-appropriate NPCs
  - Sounds
  - Textures
  - Custom models

- **`configs/`** — Plugin configuration
  - Connection settings
  - Render toggles
  - Performance settings
  - Backend API endpoints

## Design Philosophy

**Minecraft is disposable** — This is just one way to visualize the simulation. The backend doesn't care what renders it. You can swap this for Unreal, web UI, or any other renderer without changing the backend.

## Responsibilities

- Render world chunks as Minecraft blocks
- Display NPCs as entities
- Capture player actions
- Send commands to backend
- Display UI elements
- Handle networking

## Key Constraint

**Never directly access backend modules** — Only talk to `backend/api/`. This ensures clean separation and allows swapping renderers.

