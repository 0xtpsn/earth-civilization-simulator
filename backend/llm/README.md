# LLM Module

All model usage goes here, nowhere else — centralized AI/LLM integration.

## Structure

- **`providers/`** — Model adapters
- **`prompts/`** — Prompt templates
- **`routing/`** — Model selection
- **`tools/`** — Function calling
- **`safety/`** — Constraints and filters

## Design Principle

**Separation ensures swapability** — You can swap models later without rewriting agents. All LLM usage goes through this module, nowhere else.

## Usage

- NPC dialogue generation
- Leader decision-making
- Structure naming
- Knowledge retrieval assistance
- Translation services

All with era-appropriate constraints and safety checks.

