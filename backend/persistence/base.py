"""Base persistence adapter interfaces."""

from abc import ABC, abstractmethod
from typing import Any, Optional

from backend.shared.interfaces import PersistenceAdapter


class InMemoryPersistence(PersistenceAdapter):
    """Simple in-memory persistence adapter for testing/development."""

    def __init__(self):
        """Initialize in-memory storage."""
        self._storage: dict[str, Any] = {}

    async def save(self, key: str, data: Any) -> None:
        """Save data with the given key."""
        self._storage[key] = data

    async def load(self, key: str) -> Optional[Any]:
        """Load data by key."""
        return self._storage.get(key)

    async def delete(self, key: str) -> None:
        """Delete data by key."""
        if key in self._storage:
            del self._storage[key]

    def clear(self) -> None:
        """Clear all stored data."""
        self._storage.clear()

