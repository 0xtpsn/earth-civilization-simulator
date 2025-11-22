#!/bin/bash
# Database setup script for Parallel Earth Simulator
# Installs required PostgreSQL extensions: PostGIS and pgvector
#
# NOTE: PostGIS and pgvector require PostgreSQL 17+.
# If using PostgreSQL 15, extensions will not be available.
# See docs/EXTENSION_SETUP.md for upgrade instructions.

set -e

DB_NAME="${DB_NAME:-parallel_earth}"
DB_USER="${DB_USER:-$(whoami)}"

# Detect PostgreSQL installation
if [ -f "/opt/homebrew/opt/postgresql@15/bin/psql" ]; then
    PSQL_BIN="/opt/homebrew/opt/postgresql@15/bin/psql"
    PG_ISREADY="/opt/homebrew/opt/postgresql@15/bin/pg_isready"
    PG_VERSION="15"
elif [ -f "/opt/homebrew/opt/postgresql@17/bin/psql" ]; then
    PSQL_BIN="/opt/homebrew/opt/postgresql@17/bin/psql"
    PG_ISREADY="/opt/homebrew/opt/postgresql@17/bin/pg_isready"
    PG_VERSION="17"
elif [ -f "/opt/homebrew/opt/postgresql@18/bin/psql" ]; then
    PSQL_BIN="/opt/homebrew/opt/postgresql@18/bin/psql"
    PG_ISREADY="/opt/homebrew/opt/postgresql@18/bin/pg_isready"
    PG_VERSION="18"
elif command -v psql > /dev/null 2>&1; then
    PSQL_BIN="psql"
    PG_ISREADY="pg_isready"
    PG_VERSION=$($PSQL_BIN --version | grep -oE '[0-9]+' | head -1)
else
    echo "❌ PostgreSQL not found. Please install PostgreSQL first."
    exit 1
fi

PG_MAJOR_VERSION=$(echo "$PG_VERSION" | cut -d. -f1)

echo "Setting up database: $DB_NAME"
echo "User: $DB_USER"
echo "PostgreSQL version: $PG_VERSION"
echo ""

# Check if PostgreSQL is running
if ! $PG_ISREADY -U "$DB_USER" > /dev/null 2>&1; then
    echo "❌ PostgreSQL is not running. Please start it first:"
    echo "   brew services start postgresql@$PG_MAJOR_VERSION"
    exit 1
fi

echo "✅ PostgreSQL is running"
echo ""

# Create database if it doesn't exist
echo "Creating database if it doesn't exist..."
$PSQL_BIN -U "$DB_USER" -d postgres -c "SELECT 1 FROM pg_database WHERE datname = '$DB_NAME'" | grep -q 1 || \
    $PSQL_BIN -U "$DB_USER" -d postgres -c "CREATE DATABASE $DB_NAME;"
echo "✅ Database ready"
echo ""

# Check if extensions are available (require PostgreSQL 17+)
if [ "$PG_MAJOR_VERSION" -lt 17 ]; then
    echo "⚠️  WARNING: PostgreSQL $PG_VERSION detected."
    echo "   PostGIS and pgvector require PostgreSQL 17+."
    echo "   Extensions will not be installed."
    echo ""
    echo "   To enable extensions, upgrade PostgreSQL:"
    echo "   brew install postgresql@17"
    echo "   brew services start postgresql@17"
    echo "   See docs/EXTENSION_SETUP.md for details"
    echo ""
    exit 0
fi

# Install PostGIS extension
echo "Installing PostGIS extension..."
$PSQL_BIN -U "$DB_USER" -d "$DB_NAME" -c "CREATE EXTENSION IF NOT EXISTS postgis;" 2>&1 | grep -v "already exists" || true
POSTGIS_VERSION=$($PSQL_BIN -U "$DB_USER" -d "$DB_NAME" -t -c "SELECT PostGIS_version();" 2>&1 | xargs)
if [ -n "$POSTGIS_VERSION" ] && [ "$POSTGIS_VERSION" != "ERROR" ]; then
    echo "✅ PostGIS installed: $POSTGIS_VERSION"
else
    echo "⚠️  PostGIS installation failed. Check manually."
fi
echo ""

# Install pgvector extension
echo "Installing pgvector extension..."
$PSQL_BIN -U "$DB_USER" -d "$DB_NAME" -c "CREATE EXTENSION IF NOT EXISTS vector;" 2>&1 | grep -v "already exists" || true
VECTOR_VERSION=$($PSQL_BIN -U "$DB_USER" -d "$DB_NAME" -t -c "SELECT extversion FROM pg_extension WHERE extname = 'vector';" 2>&1 | xargs)
if [ -n "$VECTOR_VERSION" ] && [ "$VECTOR_VERSION" != "ERROR" ]; then
    echo "✅ pgvector installed: version $VECTOR_VERSION"
else
    echo "⚠️  pgvector installation failed. Check manually."
fi
echo ""

# Verify extensions
echo "Verifying installed extensions..."
$PSQL_BIN -U "$DB_USER" -d "$DB_NAME" -c "SELECT extname, extversion FROM pg_extension WHERE extname IN ('postgis', 'vector') ORDER BY extname;" 2>&1
echo ""

echo "✅ Database setup complete!"
echo ""
echo "Extensions installed:"
echo "  - PostGIS: Geospatial support for lat/long + time indexing"
echo "  - pgvector: Vector embeddings for NPC memory and knowledge RAG"

