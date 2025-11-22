# Parallel Earth Simulator

A simulation that recreates Earth across all eras — past, present, and plausible futures. Built to model human civilization through dynamic cultures, economies, ideologies, geography, and agent-based populations, enabling users to explore alternate histories, evolving societies, and branching timelines shaped by their actions.

## Project Structure

This is a mono-repo with two main components:

- **`backend/`** — The simulation brain (the real product)
- **`game-client-minecraft/`** — Minecraft plugin for testing/visualization (disposable renderer)

## Technology Stack

- **Language**: Python 3.11+
- **Framework**: FastAPI (async REST/WebSocket API)
- **Data Science**: pandas, numpy, scipy, scikit-learn
- **AI/LLM**: OpenAI, Anthropic, LangChain
- **Vector DB**: pgvector (PostgreSQL extension)
- **Database**: PostgreSQL + SQLAlchemy
- **Caching**: Redis
- **Package Management**: setuptools (pyproject.toml)

## Quick Start

### Prerequisites

- Python 3.11 or higher
- PostgreSQL (for structured data)
- Redis (for caching)
- PostgreSQL with PostGIS and pgvector extensions

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd earth-simulator

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"

# Set up configuration
cp configs/secrets.template.yaml configs/secrets.yaml
# Edit configs/secrets.yaml with your credentials
```

### Running the Backend

```bash
# Development mode
python -m backend.app.main

# Or use the script
./scripts/run_backend.sh

# The API will be available at http://localhost:8000
# API docs at http://localhost:8000/docs
```

### Running Tests

```bash
pytest
pytest --cov=backend  # With coverage
```

## Architecture Overview

### Backend Modules

- **`app/`** — Entry point, bootstrap, and runtime orchestration
- **`npc/`** — Autonomous human agents with cognition, memory, and social networks
- **`world-generation/`** — Geography, biomes, structures, and era-aware environments
- **`history/`** — Era profiles, country/city data, event library, and signal extraction
- **`ideologies/`** — Political, economic, cultural, and religious belief systems
- **`economy/`** — Macro/micro economics, markets, production, trade, labor
- **`money/`** — Financial accounts, wallets, assets, transactions, banking
- **`knowledge/`** — RAG foundation, era-bounded knowledge, retrieval systems
- **`simulation_engine/`** — Master orchestrator: tick loop, state, rules, determinism
- **`commands/`** — Player/auditor command layer (decoupled from client)
- **`llm/`** — Model providers, prompts, routing, safety constraints
- **`timeline/`** — Time travel, branching realities, snapshots, replay
- **`localization/`** — Language support, translation pipeline, fairness rules
- **`api/`** — REST/WebSocket interface for any renderer
- **`persistence/`** — Database connectors, vector DB, cache, migrations
- **`observability/`** — Logs, metrics, inspector UI for debugging
- **`shared/`** — Core types, constants, shared utilities

### Client

- **`game-client-minecraft/`** — Paper/Spigot plugin for rendering simulation in Minecraft

### Tooling

- **`tools/`** — Dev tooling (profilers, debug UI, importers)
- **`scripts/`** — Utility scripts for running/maintaining the project
- **`configs/`** — Configuration files (dev, prod, secrets, model routing)
- **`tests/`** — Integration and regression tests
- **`docs/`** — Design documentation, data specs, API docs

## Philosophy

- **Modular separation** — Each domain is a dedicated module
- **Renderer-agnostic** — Backend doesn't care what renders it (Minecraft, Unreal, web)
- **Deterministic simulation** — Replayable, branchable timelines
- **Era-authentic** — NPCs, knowledge, and systems respect historical constraints

## Development Status

✅ Infrastructure complete  
✅ Python project structure initialized  
⏳ Implementation in progress

## Documentation

- [Architecture](docs/architecture/) - System design and architecture
- [API Documentation](docs/api/) - REST and WebSocket API specs
- [Data Specifications](docs/data-specs/) - Data schemas and formats

## License

MIT License - see [LICENSE](LICENSE) file.
