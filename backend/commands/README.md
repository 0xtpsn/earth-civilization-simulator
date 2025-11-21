# Commands Module

All player/auditor commands, decoupled from client — the command layer that any renderer can use.

## Structure

- **`registry/`** — Command definitions
  - List of all supported commands
  - `/timejump` — Jump to different time
  - `/spawn` — Spawn NPCs or items
  - `/sleep` — Fast-forward time
  - `/inspect` — View world state
  - Command metadata

- **`parsers/`** — Input parsing
  - Parse client input into structured actions
  - Handle different input formats
  - Validate command syntax
  - Extract parameters

- **`actions/`** — Command execution
  - Actual effects injected into simulation
  - Integration with simulation engine
  - Side effects handling
  - Result generation

- **`permissions/`** — Access control
  - What's allowed in what mode
  - God mode vs survival mode
  - Role-based permissions
  - Era-appropriate restrictions

## Design Philosophy

**Decoupled from client** — Minecraft, web UI, or Unreal all call into this same command layer. The backend doesn't care how commands are invoked, only that they're valid and authorized.

## Example Commands

- `/timejump 1860-01-01 Cleveland` — Jump to specific time/place
- `/spawn npc merchant --culture japanese --era 1860` — Spawn NPC
- `/sleep 1 month` — Fast-forward time
- `/inspect economy` — View economic state
- `/inspect npc <id>` — View NPC details

