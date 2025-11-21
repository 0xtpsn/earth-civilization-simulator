"""Metrics collection using Prometheus."""

import logging
import time
from contextlib import asynccontextmanager
from typing import Dict, Optional

from prometheus_client import Counter, Gauge, Histogram, Info

logger = logging.getLogger(__name__)

# Simulation metrics
tick_duration = Histogram(
    "simulation_tick_duration_seconds",
    "Time taken per simulation tick",
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0],
)

engine_latency = Histogram(
    "simulation_engine_latency_seconds",
    "Time taken per engine tick",
    ["engine"],
    buckets=[0.01, 0.05, 0.1, 0.5, 1.0, 2.0, 5.0],
)

tick_count = Counter("simulation_ticks_total", "Total number of simulation ticks")

# Entity metrics
npc_count = Gauge("simulation_npc_count", "Current number of NPCs")
event_count = Counter("simulation_events_total", "Total number of events", ["event_type"])

# Performance metrics
memory_usage = Gauge("simulation_memory_usage_bytes", "Memory usage in bytes")
cpu_usage = Gauge("simulation_cpu_usage_percent", "CPU usage percentage")

# Business metrics
economy_gdp = Gauge("simulation_economy_gdp", "Current GDP value")
economy_inflation = Gauge("simulation_economy_inflation", "Current inflation rate")

# System info
system_info = Info("simulation_system", "System information")


class MetricsCollector:
    """Collects and exposes metrics for the simulation."""

    def __init__(self):
        """Initialize metrics collector."""
        self._start_time = time.time()

    @asynccontextmanager
    async def measure_tick(self):
        """Context manager to measure tick duration."""
        start = time.time()
        try:
            yield
        finally:
            duration = time.time() - start
            tick_duration.observe(duration)
            tick_count.inc()

    @asynccontextmanager
    async def measure_engine(self, engine_name: str):
        """Context manager to measure engine latency.
        
        Args:
            engine_name: Name of the engine
        """
        start = time.time()
        try:
            yield
        finally:
            duration = time.time() - start
            engine_latency.labels(engine=engine_name).observe(duration)

    def record_event(self, event_type: str) -> None:
        """Record an event.
        
        Args:
            event_type: Type of event
        """
        event_count.labels(event_type=event_type).inc()

    def set_npc_count(self, count: int) -> None:
        """Set current NPC count.
        
        Args:
            count: Number of NPCs
        """
        npc_count.set(count)

    def set_economy_metrics(self, gdp: Optional[float] = None, inflation: Optional[float] = None) -> None:
        """Set economy metrics.
        
        Args:
            gdp: GDP value
            inflation: Inflation rate
        """
        if gdp is not None:
            economy_gdp.set(gdp)
        if inflation is not None:
            economy_inflation.set(inflation)

    def update_system_info(self, info: Dict[str, str]) -> None:
        """Update system information.
        
        Args:
            info: Dictionary of system information
        """
        system_info.info(info)

    def get_uptime(self) -> float:
        """Get system uptime in seconds.
        
        Returns:
            Uptime in seconds
        """
        return time.time() - self._start_time


# Global metrics collector instance
_metrics_collector: Optional[MetricsCollector] = None


def get_metrics_collector() -> MetricsCollector:
    """Get the global metrics collector instance.
    
    Returns:
        MetricsCollector instance
    """
    global _metrics_collector
    if _metrics_collector is None:
        _metrics_collector = MetricsCollector()
    return _metrics_collector

