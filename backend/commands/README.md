# Commands Module

All player/auditor commands, decoupled from client — the command layer that any renderer can use.

## Structure

- **`registry/`** — Command definitions
- **`parsers/`** — Input parsing
- **`actions/`** — Command execution
- **`permissions/`** — Access control

## Design Philosophy

**Decoupled from client** — Minecraft, web UI, or Unreal all call into this same command layer. The backend doesn't care how commands are invoked, only that they're valid and authorized.

## Example Commands

- `/timejump 1860-01-01 Cleveland` — Jump to specific time/place
- `/spawn npc merchant --culture japanese --era 1860` — Spawn NPC
- `/sleep 1 month` — Fast-forward time
- `/inspect economy` — View economic state
- `/inspect npc <id>` — View NPC details

