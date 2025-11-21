# App

The backend entry point that wires every module together.

## Structure

- **`main.py` / `main.ts`** — Server executable entry point
- **`bootstrap/`** — Startup order, dependency injection, service initialization
- **`runtime/`** — Tick scheduler, service registry, lifecycle management

## Responsibilities

- Initialize all modules in correct order
- Wire dependencies between modules
- Start the tick loop
- Handle graceful shutdown
- Register services for dependency injection

## Boot Sequence

1. Load configuration
2. Initialize persistence layer
3. Load shared types and constants
4. Initialize simulation engine
5. Register all domain engines
6. Start API server
7. Begin tick loop

