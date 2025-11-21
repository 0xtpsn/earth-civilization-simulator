# Shared Module

Tiny shared abstractions and core types — universal utilities used across modules.

## Structure

- **`types/`** — Core type definitions
  - Base types (Time, Location, ID, etc.)
  - Common interfaces
  - Type utilities

- **`constants/`** — Shared constants
  - Configuration constants
  - Magic numbers
  - Default values

- **`utils/`** — Utility functions
  - Common helpers
  - Math utilities
  - String manipulation
  - Date/time helpers

## Design Principle

**Only universal small stuff** — Don't let this become a junk drawer. Only put things here that are truly shared across multiple modules and are too small to warrant their own module.

## Guidelines

- If it's used by 2+ modules → consider shared
- If it's domain-specific → keep in domain module
- If it's large → consider its own module
- Keep it minimal and focused

