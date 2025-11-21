# NPC Engine

Everything about human agents — autonomous entities with cognition, memory, personality, and social networks.

## Structure

- **`profiles/`** — NPC identity schema and templates
  - Personality traits (Big Five, risk tolerance)
  - Ideology alignment
  - Cultural parameters
  - Demographics (age, occupation, health, wealth)
  - Life history

- **`cognition/`** — Observe → think → act loop
  - Decision policies
  - Goal pursuit algorithms
  - Belief updating
  - Constraint satisfaction

- **`memory/`** — Short/long-term memory store
  - Memory interface
  - Summarization strategies
  - Retrieval mechanisms
  - Forgetting curves

- **`dialogue/`** — Conversation management
  - Intent parsing
  - Emotional tone
  - Cultural communication styles
  - Speech act generation

- **`social-network/`** — Relationship graphs
  - Family, friends, colleagues
  - Gossip/reputation spread
  - Influence networks
  - Social capital

- **`behaviors/`** — Action primitives
  - Work, protest, buy, sell, flee
  - Bribe, invest, negotiate
  - Form relationships, join groups

- **`spawning/`** — Population generation
  - Era/city-appropriate NPCs
  - Demographic distributions
  - Cultural alignment
  - Economic stratification

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

