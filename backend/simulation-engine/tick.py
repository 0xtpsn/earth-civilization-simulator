"""Tick loop and time management for the simulation."""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import List, Optional

from backend.shared.interfaces import Engine
from backend.shared.types import Time
from backend.simulation_engine.state import WorldState

logger = logging.getLogger(__name__)


class TickScheduler:
    """Manages the simulation tick loop and time progression."""

    def __init__(
        self,
        engines: List[Engine],
        state: WorldState,
        tick_rate: float = 1.0,  # seconds per tick
        time_per_tick: timedelta = timedelta(days=1),  # 1 day per tick
    ):
        """Initialize the tick scheduler.
        
        Args:
            engines: List of engines to tick
            state: World state
            tick_rate: Real-world seconds per tick (controls simulation speed)
            time_per_tick: Simulation time that passes per tick
        """
        self.engines = engines
        self.state = state
        self.tick_rate = tick_rate
        self.time_per_tick = time_per_tick
        self._running = False
        self._paused = False

    async def start(self) -> None:
        """Start the tick loop."""
        self._running = True
        logger.info("Starting tick scheduler...")

        while self._running:
            if not self._paused:
                await self._tick()
            await asyncio.sleep(self.tick_rate)

    async def stop(self) -> None:
        """Stop the tick loop."""
        self._running = False
        logger.info("Stopping tick scheduler...")

    def pause(self) -> None:
        """Pause the simulation."""
        self._paused = True
        logger.info("Simulation paused")

    def resume(self) -> None:
        """Resume the simulation."""
        self._paused = False
        logger.info("Simulation resumed")

    async def _tick(self) -> None:
        """Execute one simulation tick."""
        try:
            # Update simulation time
            if isinstance(self.state.current_time, datetime):
                self.state.current_time = Time(self.state.current_time + self.time_per_tick)
            else:
                # If it's a string, parse it first
                current = datetime.fromisoformat(str(self.state.current_time))
                self.state.current_time = Time(current + self.time_per_tick)

            self.state.tick_count += 1

            # Tick all engines in order
            for engine in self.engines:
                try:
                    delta_time = self.time_per_tick.total_seconds()
                    await engine.tick(self.state, delta_time)
                except Exception as e:
                    logger.error(f"Error ticking engine {engine.name}: {e}", exc_info=True)

            logger.debug(f"Tick {self.state.tick_count} completed at {self.state.current_time}")

        except Exception as e:
            logger.error(f"Error in tick loop: {e}", exc_info=True)

    async def fast_forward(self, ticks: int) -> None:
        """Fast-forward the simulation by N ticks without real-time delay.
        
        Args:
            ticks: Number of ticks to advance
        """
        logger.info(f"Fast-forwarding {ticks} ticks...")
        original_rate = self.tick_rate
        self.tick_rate = 0.0  # No delay

        for _ in range(ticks):
            await self._tick()

        self.tick_rate = original_rate
        logger.info(f"Fast-forward complete. Current time: {self.state.current_time}")

    async def jump_to_time(self, target_time: Time) -> None:
        """Jump simulation to a specific time (used for time travel).
        
        Args:
            target_time: Target time to jump to
        """
        logger.info(f"Jumping to time: {target_time}")
        self.state.current_time = target_time
        # TODO: Restore state from snapshot if available

