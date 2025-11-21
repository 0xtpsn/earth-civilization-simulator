# Configs

Central place for configuration files.

## Files

- **`dev.yaml`** — Development environment configuration
- **`prod.yaml`** — Production environment configuration
- **`secrets.template.yaml`** — Template for secrets (API keys, DB credentials)
- **`model-routing.yaml`** — LLM routing rules (cheap vs strong model usage)

## Usage

Configuration files are loaded by the backend at startup. They define:
- Database connections
- API endpoints
- Model provider settings
- Feature flags
- Performance tuning

## Security

Never commit `secrets.yaml` — only commit `secrets.template.yaml` as a reference.

