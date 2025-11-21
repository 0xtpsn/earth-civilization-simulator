"""Deterministic randomness and seeding for reproducible simulations."""

import random
from typing import Optional


class DeterministicRandom:
    """Wrapper around Python's random module with explicit seeding."""

    def __init__(self, seed: Optional[int] = None):
        """Initialize with a seed.
        
        Args:
            seed: Random seed (None uses system time)
        """
        self._seed = seed
        self._rng = random.Random(seed)
        if seed is not None:
            random.seed(seed)

    @property
    def seed(self) -> Optional[int]:
        """Get the current seed."""
        return self._seed

    def random(self) -> float:
        """Generate a random float in [0.0, 1.0)."""
        return self._rng.random()

    def randint(self, a: int, b: int) -> int:
        """Generate a random integer in [a, b]."""
        return self._rng.randint(a, b)

    def choice(self, seq):
        """Choose a random element from a sequence."""
        return self._rng.choice(seq)

    def choices(self, population, weights=None, *, cum_weights=None, k=1):
        """Return a k sized list of population elements chosen with replacement."""
        return self._rng.choices(population, weights, cum_weights=cum_weights, k=k)

    def shuffle(self, x):
        """Shuffle sequence x in place."""
        self._rng.shuffle(x)

    def gauss(self, mu: float, sigma: float) -> float:
        """Generate a random float from a Gaussian distribution."""
        return self._rng.gauss(mu, sigma)

    def uniform(self, a: float, b: float) -> float:
        """Generate a random float uniformly in [a, b)."""
        return self._rng.uniform(a, b)

    def getstate(self):
        """Get the internal state of the random number generator."""
        return self._rng.getstate()

    def setstate(self, state):
        """Set the internal state of the random number generator."""
        self._rng.setstate(state)


# Global deterministic random instance (will be initialized by simulation engine)
_deterministic_rng: Optional[DeterministicRandom] = None


def get_rng() -> DeterministicRandom:
    """Get the global deterministic random number generator."""
    global _deterministic_rng
    if _deterministic_rng is None:
        raise RuntimeError("Deterministic RNG not initialized. Call set_rng() first.")
    return _deterministic_rng


def set_rng(seed: int) -> DeterministicRandom:
    """Set the global deterministic random number generator.
    
    Args:
        seed: Random seed
        
    Returns:
        The initialized RNG instance
    """
    global _deterministic_rng
    _deterministic_rng = DeterministicRandom(seed)
    return _deterministic_rng

