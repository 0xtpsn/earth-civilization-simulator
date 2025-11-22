#!/usr/bin/env python3
"""Test script to verify tick loop shows day counter."""

import asyncio
import logging
import sys
from datetime import datetime

from backend.app.bootstrap import create_orchestrator
from backend.shared.types import Location, ScenarioID, Time

# Configure logging to see INFO messages
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

async def main():
    """Test the tick loop."""
    print("Starting tick loop test...")
    
    orchestrator = create_orchestrator(seed=42)
    
    await orchestrator.initialize(
        scenario_id=ScenarioID("test"),
        initial_time=Time(datetime(2025, 1, 1)),
        location=Location("Cleveland, USA"),
    )
    
    print("Simulation initialized. Starting tick loop for 5 ticks...")
    
    # Start tick loop in background
    tick_task = asyncio.create_task(orchestrator.start(tick_rate=0.5))
    
    # Wait for a few ticks
    await asyncio.sleep(3)
    
    # Stop the simulation
    await orchestrator.stop()
    tick_task.cancel()
    
    try:
        await tick_task
    except asyncio.CancelledError:
        pass
    
    print("\n✅ Tick loop test completed!")
    print("You should have seen 'Day 1:', 'Day 2:', etc. in the logs above.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nTest interrupted")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

