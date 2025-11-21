# Localization Module

Language and translation logic — handles multilingual support and translation fairness.

## Structure

- **`languages/`** — Supported languages
  - English (interface language)
  - Chinese (interface language)
  - NPC native languages (all eras)
  - Language metadata

- **`translation/`** — Translation pipeline
  - Real-time NPC ↔ player translation
  - AI-powered translation
  - Context-aware translation
  - Cultural nuance preservation

- **`fairness/`** — Translation balancing
  - "Translation ON/OFF advantage" rules
  - Fairness mechanics
  - Difficulty scaling
  - Authenticity vs accessibility tradeoffs

## Key Features

- **NPCs always speak native era language** — A 1860 Japanese merchant speaks Japanese
- **Player receives translated version** — If translation is ON
- **Translation can be toggled** — For authenticity challenge
- **Fairness rules** — Balance advantage/disadvantage of translation

## Design Philosophy

Language is both a barrier and a design tool:
- **With translation ON**: More accessible, but loses immersive challenge
- **With translation OFF**: More authentic, but requires language learning or interpretation

The fairness layer ensures neither mode is unfairly advantaged.

