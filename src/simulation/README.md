# Simulation
Runtime coordination of the engines.

- `orchestrator/` — deterministic tick loop, engine ordering, inter-engine contracts.
- `scheduler/` — job queueing, time dilation/fast-forward, era switching.
- `event_bus/` — pub/sub for domain events, cross-engine messaging, audit hooks.
