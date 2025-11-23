#!/usr/bin/env python3
"""
Architecture validation script.

Runs import validation to check for phase engine cross-imports.
Treat violations as build errors.
"""

import sys
from pathlib import Path

# Add backend to path
backend_root = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_root.parent))

from backend.shared.import_validator import check_imports


if __name__ == "__main__":
    backend_path = Path(__file__).parent.parent / "backend"
    success = check_imports(backend_path)
    sys.exit(0 if success else 1)

