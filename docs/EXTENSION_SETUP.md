# PostgreSQL Extensions Setup

## Issue

PostGIS and pgvector extensions installed via Homebrew are built for PostgreSQL 17/18, but the project currently uses PostgreSQL 15.

## Solutions

### Option 1: Upgrade PostgreSQL (Recommended)

Upgrade to PostgreSQL 17 or 18 to match the extension versions:

```bash
# Install PostgreSQL 17
brew install postgresql@17

# Start PostgreSQL 17
brew services start postgresql@17

# Migrate database (if needed)
pg_dump -U $(whoami) -d parallel_earth > backup.sql
createdb -U $(whoami) parallel_earth_new
psql -U $(whoami) -d parallel_earth_new < backup.sql

# Update database connection in configs/secrets.yaml
```

### Option 2: Build Extensions from Source for PostgreSQL 15

This is more complex and requires compiling extensions:

```bash
# Install build dependencies
brew install postgis --build-from-source
brew install pgvector --build-from-source

# Link extensions manually
# (Requires matching PostgreSQL version)
```

### Option 3: Use Docker (Alternative)

Run PostgreSQL with extensions in Docker:

```bash
docker run -d \
  --name parallel-earth-db \
  -e POSTGRES_PASSWORD=yourpassword \
  -e POSTGRES_DB=parallel_earth \
  -p 5432:5432 \
  -v parallel_earth_data:/var/lib/postgresql/data \
  pgvector/pgvector:pg17
```

## Current Status

- ✅ PostgreSQL 15 installed and running
- ✅ PostGIS installed (but not compatible with PostgreSQL 15)
- ✅ pgvector installed (but not compatible with PostgreSQL 15)
- ⚠️ Extensions need PostgreSQL 17+ to work

## Recommendation

For Phase 0, the extensions are not critical for the basic tick loop. They can be configured later when implementing:
- NPC memory (pgvector)
- Geospatial features (PostGIS)

The simulation brain can run without these extensions initially.

