"""
Main entry point for the Parallel Earth Simulator backend.

This module initializes all components and starts the simulation server.
"""

import asyncio
import logging
from datetime import datetime

import uvicorn
from fastapi import FastAPI

from backend.app.bootstrap import create_orchestrator
from backend.shared.constants import DEFAULT_SEED, DEFAULT_TICK_RATE
from backend.shared.types import Location, ScenarioID, Time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Global orchestrator instance
_orchestrator = None


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="Parallel Earth Simulator API",
        description="API for the Parallel Earth simulation engine",
        version="0.1.0",
    )

    @app.get("/health")
    async def health_check():
        """Health check endpoint."""
        return {"status": "healthy", "version": "0.1.0"}

    @app.get("/simulation/state")
    async def get_state():
        """Get current simulation state."""
        global _orchestrator
        if _orchestrator is None:
            return {"error": "Simulation not initialized"}
        state = _orchestrator.get_state()
        if state:
            return state.to_dict()
        return {"error": "No state available"}

    @app.post("/simulation/start")
    async def start_simulation(
        scenario_id: str = "default",
        initial_time: str = None,
        location: str = "Cleveland, USA",
        seed: int = DEFAULT_SEED,
    ):
        """Start a new simulation."""
        global _orchestrator

        if initial_time is None:
            initial_time = datetime.now().isoformat()

        try:
            orchestrator = create_orchestrator(seed=seed)
            _orchestrator = orchestrator

            await orchestrator.initialize(
                scenario_id=ScenarioID(scenario_id),
                initial_time=Time(datetime.fromisoformat(initial_time)),
                location=Location(location),
            )

            # Start simulation in background
            asyncio.create_task(orchestrator.start(tick_rate=DEFAULT_TICK_RATE))

            return {
                "status": "started",
                "scenario_id": scenario_id,
                "initial_time": initial_time,
                "location": location,
            }
        except Exception as e:
            logger.error(f"Error starting simulation: {e}", exc_info=True)
            return {"error": str(e)}

    @app.post("/simulation/stop")
    async def stop_simulation():
        """Stop the simulation."""
        global _orchestrator
        if _orchestrator:
            await _orchestrator.stop()
            return {"status": "stopped"}
        return {"error": "No simulation running"}

    return app


def main():
    """Main entry point."""
    logger.info("Starting Parallel Earth Simulator Backend...")

    app = create_app()

    # Run the server
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
    )


if __name__ == "__main__":
    main()

