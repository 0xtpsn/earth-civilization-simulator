# API Module

Interface for any renderer — REST and WebSocket endpoints for clients.

## Structure

- **`rest/`** — REST API endpoints
- **`websocket/`** — Streaming connections
- **`schemas/`** — Shared types

## Design

**Renderer-agnostic** — Minecraft plugin, web UI, or Unreal client all talk to this same API. The backend doesn't care what renders it, only that requests are valid.

## Usage

Minecraft plugin only talks to this folder — it never directly accesses backend modules. This ensures clean separation and allows swapping renderers without backend changes.

