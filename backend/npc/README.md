# NPC Engine

Everything about human agents — autonomous entities with cognition, memory, personality, and social networks.

## Structure

- **`profiles/`** — NPC identity schema and templates
- **`cognition/`** — Observe → think → act loop
- **`memory/`** — Short/long-term memory store
- **`dialogue/`** — Conversation management
- **`social-network/`** — Relationship graphs
- **`behaviors/`** — Action primitives
- **`spawning/`** — Population generation
- **`utils/`** — Helper functions shared within NPC module

## Key Features

- **Autonomous agents** — NPCs make decisions based on personality, goals, and context
- **Cultural grounding** — Behavior reflects era and cultural norms
- **Persistent memory** — NPCs remember interactions with player and others
- **Social dynamics** — Relationships and reputation affect behavior

## Design Constraints

- This module should **never** know about Minecraft or rendering
- NPCs are pure data/logic entities
- All visual representation happens in client layer

