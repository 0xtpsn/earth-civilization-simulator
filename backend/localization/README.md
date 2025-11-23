# Localization Module

Language and translation logic — handles multilingual support and translation fairness.

## Structure

- **`languages/`** — Supported languages
- **`translation/`** — Translation pipeline
- **`fairness/`** — Translation balancing

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

