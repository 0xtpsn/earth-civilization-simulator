"""
Import validation to enforce architecture boundaries.

This module provides utilities to validate imports and prevent phase engines
from directly importing other phase engines. Treat violations as build errors.

ARCHITECTURE RULE:
==================
Every engine only imports from shared/ + systems/ services, and the orchestrator
is the only place allowed to hold engine references. If you ever see npc importing
economy directly, treat it as a build error.
"""

import ast
import importlib.util
from pathlib import Path
from typing import List, Set, Tuple

from backend.shared.architecture import (
    PHASE_ENGINES,
    SYSTEMS_LAYER,
    SHARED_MODULES,
    UNIVERSE_MODULE,
    is_phase_engine,
    is_systems_layer,
    is_shared_module,
)


class ImportValidator:
    """Validates imports to enforce architecture boundaries."""
    
    def __init__(self, backend_root: Path):
        """Initialize validator.
        
        Args:
            backend_root: Path to backend/ directory
        """
        self.backend_root = backend_root
        self.violations: List[Tuple[str, str, str]] = []  # (file, importing, imported)
    
    def validate_file(self, file_path: Path) -> List[Tuple[str, str, str]]:
        """Validate imports in a single file.
        
        Args:
            file_path: Path to Python file to validate
            
        Returns:
            List of violations: (file, importing_module, imported_module)
        """
        if not file_path.exists() or not file_path.suffix == ".py":
            return []
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                source = f.read()
            
            tree = ast.parse(source, filename=str(file_path))
            violations = []
            
            # Get the module name of the file being validated
            relative_path = file_path.relative_to(self.backend_root)
            importing_module = str(relative_path.with_suffix("")).replace("/", ".")
            
            # Extract base module name
            importing_base = importing_module.split(".")[0]
            
            # Walk AST to find imports
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imported_base = alias.name.split(".")[0]
                        if self._is_violation(importing_base, imported_base):
                            violations.append((str(file_path), importing_base, imported_base))
                
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imported_base = node.module.split(".")[0]
                        if self._is_violation(importing_base, imported_base):
                            violations.append((str(file_path), importing_base, imported_base))
            
            return violations
            
        except Exception as e:
            # Skip files that can't be parsed (might be binary, etc.)
            return []
    
    def _is_violation(self, importing_base: str, imported_base: str) -> bool:
        """Check if an import is a violation.
        
        Args:
            importing_base: Base module name doing the importing
            imported_base: Base module name being imported
            
        Returns:
            True if this is a violation, False otherwise
        """
        # Same module - always allowed
        if importing_base == imported_base:
            return False
        
        # Shared modules can import anything
        if is_shared_module(importing_base):
            return False
        
        # Universe module (Phase 1 + 7) can import anything (it orchestrates)
        if importing_base == UNIVERSE_MODULE:
            return False
        
        # Systems Layer can import anything
        if is_systems_layer(importing_base):
            return False
        
        # Phase engines cannot import other phase engines
        if is_phase_engine(importing_base):
            if is_phase_engine(imported_base):
                return True  # Phase engine importing another phase engine - VIOLATION
        
        # Phase engines can import Systems Layer, shared, persistence
        if is_phase_engine(importing_base):
            if is_systems_layer(imported_base) or is_shared_module(imported_base):
                return False  # Allowed
        
        return False
    
    def validate_directory(self, directory: Path) -> List[Tuple[str, str, str]]:
        """Validate all Python files in a directory.
        
        Args:
            directory: Directory to validate
            
        Returns:
            List of all violations
        """
        all_violations = []
        
        for py_file in directory.rglob("*.py"):
            # Skip __pycache__ and test files for now
            if "__pycache__" in str(py_file) or "test" in py_file.name.lower():
                continue
            
            violations = self.validate_file(py_file)
            all_violations.extend(violations)
        
        return all_violations
    
    def validate_backend(self) -> List[Tuple[str, str, str]]:
        """Validate entire backend directory.
        
        Returns:
            List of all violations
        """
        return self.validate_directory(self.backend_root)


def check_imports(backend_root: Path = None) -> bool:
    """Check imports and report violations.
    
    Args:
        backend_root: Path to backend/ (default: auto-detect)
        
    Returns:
        True if no violations, False otherwise
    """
    if backend_root is None:
        # Auto-detect backend root
        current = Path(__file__).parent
        while current.name != "backend" and current.parent != current:
            current = current.parent
        backend_root = current
    
    validator = ImportValidator(backend_root)
    violations = validator.validate_backend()
    
    if violations:
        print("=" * 80)
        print("ARCHITECTURE VIOLATIONS DETECTED")
        print("=" * 80)
        print()
        
        for file_path, importing, imported in violations:
            print(f"❌ {file_path}")
            print(f"   Phase engine '{importing}' is importing phase engine '{imported}'")
            print(f"   → Use EventBus, WorldState, or Systems Layer services instead")
            print()
        
        print("=" * 80)
        print(f"Total violations: {len(violations)}")
        print("=" * 80)
        return False
    
    print("✅ No architecture violations detected")
    return True


if __name__ == "__main__":
    import sys
    success = check_imports()
    sys.exit(0 if success else 1)

