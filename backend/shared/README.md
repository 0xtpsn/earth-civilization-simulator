# Shared Module

Universal helpers, types, constants, and utilities used across all modules.

## Architecture Boundaries

This module can be imported by:
- ✅ All phase engines
- ✅ Systems Layer services
- ✅ Infrastructure modules
- ✅ Phase 1 + Phase 7 (simulation_engine)

## Key Files

- **`interfaces.py`** - Core interfaces (Engine, EventPublisher, EventSubscriber)
- **`base_engine.py`** - BaseEngine class for all engines
- **`types.py`** - Type definitions (AgentID, Time, Location, etc.)
- **`constants.py`** - Constants (DEFAULT_SEED, DEFAULT_TICK_RATE)
- **`architecture.py`** - Architecture boundary enforcement and documentation
- **`batch_processor.py`** - Batch processing utilities
- **`task_queue.py`** - Async task queue
- **`resource_limits.py`** - Resource monitoring and limits

## Architecture Rules

See `architecture.py` for detailed architecture boundary documentation.

**Key Rule**: Phase engines cannot directly import other phase engines. They must use:
- EventBus (pub/sub)
- WorldState (shared state)
- Systems Layer services

