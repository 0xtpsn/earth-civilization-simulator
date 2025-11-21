# LLM Module

All model usage goes here, nowhere else — centralized AI/LLM integration.

## Structure

- **`providers/`** — Model adapters
  - OpenAI adapter
  - Local model adapters
  - Anthropic, etc.
  - Unified interface

- **`prompts/`** — Prompt templates
  - Per-task templates
  - Dialogue prompts
  - Leader decision prompts
  - Structure naming prompts
  - Era-appropriate prompts

- **`routing/`** — Model selection
  - Choose cheap vs strong models per call type
  - Cost optimization
  - Quality vs speed tradeoffs
  - Model routing rules

- **`tools/`** — Function calling
  - Function calling schemas
  - Agent query interfaces
  - Tool definitions
  - Capability exposure

- **`safety/`** — Constraints and filters
  - Era-bounded constraints
  - Toxicity filters
  - Hallucination checks
  - Anachronism prevention
  - Content moderation

## Design Principle

**Separation ensures swapability** — You can swap models later without rewriting agents. All LLM usage goes through this module, nowhere else.

## Usage

- NPC dialogue generation
- Leader decision-making
- Structure naming
- Knowledge retrieval assistance
- Translation services

All with era-appropriate constraints and safety checks.

