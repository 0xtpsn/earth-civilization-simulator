"""Shared constants used across the backend."""

from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent

# Data directories
DATA_DIR = PROJECT_ROOT / "data"
SEEDS_DIR = DATA_DIR / "seeds"
REFERENCE_DIR = DATA_DIR / "reference"
EXPERIMENTS_DIR = DATA_DIR / "experiments"

# Config directories
CONFIGS_DIR = PROJECT_ROOT / "configs"

# Time constants
TICKS_PER_DAY = 1
TICKS_PER_WEEK = 7
TICKS_PER_MONTH = 30
TICKS_PER_YEAR = 365

# Default values
DEFAULT_SEED = 42
DEFAULT_TICK_RATE = 1.0  # seconds per tick

