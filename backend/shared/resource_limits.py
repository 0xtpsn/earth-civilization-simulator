"""Resource limits and quotas for engines and entities."""

import logging
import os
from typing import Dict, Optional

import psutil

logger = logging.getLogger(__name__)


class ResourceLimitExceeded(Exception):
    """Raised when a resource limit is exceeded."""

    pass


class ResourceLimiter:
    """Monitors and enforces resource limits."""

    def __init__(
        self,
        max_memory_mb: Optional[int] = None,
        max_cpu_percent: Optional[float] = None,
        max_npcs: Optional[int] = None,
        max_events_per_tick: Optional[int] = None,
    ):
        """Initialize resource limiter.
        
        Args:
            max_memory_mb: Maximum memory usage in MB
            max_cpu_percent: Maximum CPU usage percentage
            max_npcs: Maximum number of NPCs
            max_events_per_tick: Maximum events per tick
        """
        self.max_memory_mb = max_memory_mb
        self.max_cpu_percent = max_cpu_percent
        self.max_npcs = max_npcs
        self.max_events_per_tick = max_events_per_tick

        self.process = psutil.Process(os.getpid())
        self._current_npcs = 0
        self._current_events_this_tick = 0

    def check_limits(self) -> None:
        """Check if any resource limits are exceeded.
        
        Raises:
            ResourceLimitExceeded: If any limit is exceeded
        """
        # Check memory
        if self.max_memory_mb:
            memory_info = self.process.memory_info()
            memory_mb = memory_info.rss / (1024 * 1024)
            if memory_mb > self.max_memory_mb:
                raise ResourceLimitExceeded(
                    f"Memory limit exceeded: {memory_mb:.2f}MB > {self.max_memory_mb}MB"
                )

        # Check CPU
        if self.max_cpu_percent:
            cpu_percent = self.process.cpu_percent(interval=0.1)
            if cpu_percent > self.max_cpu_percent:
                raise ResourceLimitExceeded(
                    f"CPU limit exceeded: {cpu_percent:.2f}% > {self.max_cpu_percent}%"
                )

        # Check NPC count
        if self.max_npcs and self._current_npcs > self.max_npcs:
            raise ResourceLimitExceeded(
                f"NPC limit exceeded: {self._current_npcs} > {self.max_npcs}"
            )

        # Check events per tick
        if self.max_events_per_tick and self._current_events_this_tick > self.max_events_per_tick:
            raise ResourceLimitExceeded(
                f"Event limit exceeded: {self._current_events_this_tick} > {self.max_events_per_tick}"
            )

    def get_usage(self) -> Dict[str, Any]:
        """Get current resource usage.
        
        Returns:
            Dictionary with resource usage information
        """
        memory_info = self.process.memory_info()
        memory_mb = memory_info.rss / (1024 * 1024)

        return {
            "memory_mb": memory_mb,
            "memory_limit_mb": self.max_memory_mb,
            "cpu_percent": self.process.cpu_percent(interval=0.1),
            "cpu_limit_percent": self.max_cpu_percent,
            "npc_count": self._current_npcs,
            "npc_limit": self.max_npcs,
            "events_this_tick": self._current_events_this_tick,
            "events_limit": self.max_events_per_tick,
        }

    def set_npc_count(self, count: int) -> None:
        """Set current NPC count.
        
        Args:
            count: Number of NPCs
        """
        self._current_npcs = count

    def increment_events(self) -> None:
        """Increment event counter for current tick."""
        self._current_events_this_tick += 1

    def reset_tick_counters(self) -> None:
        """Reset per-tick counters."""
        self._current_events_this_tick = 0

