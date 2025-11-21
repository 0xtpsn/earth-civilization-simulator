# API Module

Interface for any renderer — REST and WebSocket endpoints for clients.

## Structure

- **`rest/`** — REST API endpoints
  - `GET /snapshot?time=<date>&place=<location>` — Get world state
  - `GET /chunk?x=<x>&y=<y>&z=<z>&time=<date>` — Get chunk blueprint
  - `POST /command` — Execute player command
  - `GET /npc/<id>` — Get NPC details
  - Standard REST patterns

- **`websocket/`** — Streaming connections
  - Real-time tick updates
  - NPC dialogue events
  - World state changes
  - Event streaming

- **`schemas/`** — Shared types
  - Request/response types
  - Data transfer objects
  - Validation schemas
  - API contracts

## Design

**Renderer-agnostic** — Minecraft plugin, web UI, or Unreal client all talk to this same API. The backend doesn't care what renders it, only that requests are valid.

## Usage

Minecraft plugin only talks to this folder — it never directly accesses backend modules. This ensures clean separation and allows swapping renderers without backend changes.

