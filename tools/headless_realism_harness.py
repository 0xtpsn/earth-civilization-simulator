#!/usr/bin/env python3
"""
Headless Realism Harness - Scientific Instrument for Judging Realism

This CLI tool runs the simulation brain without any renderer and prints:
- Daily world summary
- Top NPC conversations
- Macro indicators
- Ideological drift
- Divergence score

This is how you know the brain is alive before integrating graphics.

ARCHITECTURE:
- Not a phase - it's a tool for validating realism
- Runs the simulation headlessly
- Outputs structured data for analysis
- Can be used for regression testing and scientific validation
"""

import asyncio
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# Add backend to path
backend_root = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_root.parent))

from backend.app.bootstrap import create_orchestrator
from backend.shared.constants import DEFAULT_SEED, DEFAULT_TICK_RATE


class RealismHarness:
    """Headless realism validation harness."""
    
    def __init__(self, scenario_id: str = "test_scenario", days: int = 30):
        """Initialize harness.
        
        Args:
            scenario_id: Scenario to run
            days: Number of days to simulate
        """
        self.scenario_id = scenario_id
        self.days = days
        self.orchestrator = None
        self.metrics: List[Dict[str, Any]] = []
    
    async def run(self):
        """Run the simulation and collect metrics."""
        print("=" * 80)
        print("HEADLESS REALISM HARNESS")
        print("=" * 80)
        print(f"Scenario: {self.scenario_id}")
        print(f"Duration: {self.days} days")
        print(f"Seed: {DEFAULT_SEED}")
        print("=" * 80)
        print()
        
        # Create orchestrator
        self.orchestrator = await create_orchestrator()
        
        # Initialize scenario
        await self.orchestrator.initialize(
            scenario_id=self.scenario_id,
            initial_time=datetime(2025, 1, 1),
            location="Singapore, Singapore"
        )
        
        # Run simulation
        print("Starting simulation...")
        print()
        
        for day in range(1, self.days + 1):
            # Advance one day
            await self.orchestrator.tick()
            
            # Collect metrics
            metrics = await self.collect_daily_metrics(day)
            self.metrics.append(metrics)
            
            # Print daily summary
            self.print_daily_summary(day, metrics)
        
        # Print final summary
        self.print_final_summary()
        
        # Cleanup
        await self.orchestrator.stop()
    
    async def collect_daily_metrics(self, day: int) -> Dict[str, Any]:
        """Collect metrics for a single day.
        
        Args:
            day: Day number
            
        Returns:
            Dictionary of metrics
        """
        state = self.orchestrator.get_state()
        
        metrics = {
            "day": day,
            "tick_count": state.tick_count,
            "current_time": str(state.current_time),
            "location": str(state.current_location),
            "era": str(state.era),
        }
        
        # Get engine-specific metrics
        engine_states = state.engine_states
        
        # NPC metrics (if available)
        if "npc" in engine_states:
            npc_state = engine_states["npc"]
            metrics["npc_count"] = npc_state.get("count", 0) if isinstance(npc_state, dict) else 0
            metrics["top_conversations"] = npc_state.get("top_conversations", []) if isinstance(npc_state, dict) else []
        
        # Economy metrics (if available)
        if "economy" in engine_states:
            economy_state = engine_states["economy"]
            if isinstance(economy_state, dict):
                metrics["gdp"] = economy_state.get("gdp", 0)
                metrics["inflation"] = economy_state.get("inflation", 0)
                metrics["unemployment"] = economy_state.get("unemployment", 0)
        
        # Ideology metrics (if available)
        if "ideologies" in engine_states:
            ideology_state = engine_states["ideologies"]
            if isinstance(ideology_state, dict):
                metrics["ideological_drift"] = ideology_state.get("drift_score", 0)
                metrics["dominant_ideologies"] = ideology_state.get("dominant", [])
        
        # WorldGen metrics (if available)
        if "world_generation" in engine_states:
            worldgen_state = engine_states["world_generation"]
            if isinstance(worldgen_state, dict):
                metrics["chunks_generated"] = worldgen_state.get("chunks_generated", 0)
        
        return metrics
    
    def print_daily_summary(self, day: int, metrics: Dict[str, Any]):
        """Print daily summary.
        
        Args:
            day: Day number
            metrics: Daily metrics
        """
        print(f"📅 Day {day:3d} | {metrics.get('current_time', 'N/A')}")
        print(f"   Location: {metrics.get('location', 'N/A')}")
        print(f"   Era: {metrics.get('era', 'N/A')}")
        
        # NPC summary
        npc_count = metrics.get("npc_count", 0)
        if npc_count > 0:
            print(f"   👥 NPCs: {npc_count}")
            conversations = metrics.get("top_conversations", [])
            if conversations:
                print(f"   💬 Top conversations: {len(conversations)}")
                for i, conv in enumerate(conversations[:3], 1):
                    print(f"      {i}. {conv.get('summary', 'N/A')}")
        
        # Economy summary
        gdp = metrics.get("gdp")
        if gdp is not None:
            print(f"   💰 GDP: {gdp:,.0f}")
            inflation = metrics.get("inflation", 0)
            if inflation:
                print(f"   📈 Inflation: {inflation:.2f}%")
        
        # Ideology summary
        drift = metrics.get("ideological_drift")
        if drift is not None:
            print(f"   🧠 Ideological drift: {drift:.3f}")
            dominant = metrics.get("dominant_ideologies", [])
            if dominant:
                print(f"   🎯 Dominant: {', '.join(dominant[:3])}")
        
        print()
    
    def print_final_summary(self):
        """Print final summary with divergence score."""
        print("=" * 80)
        print("FINAL SUMMARY")
        print("=" * 80)
        print()
        
        # Calculate divergence score (placeholder - implement based on your metrics)
        divergence_score = self.calculate_divergence_score()
        print(f"📊 Divergence Score: {divergence_score:.3f}")
        print("   (Lower = more stable, Higher = more dynamic)")
        print()
        
        # Summary statistics
        if self.metrics:
            npc_counts = [m.get("npc_count", 0) for m in self.metrics if "npc_count" in m]
            if npc_counts:
                print(f"👥 NPCs: min={min(npc_counts)}, max={max(npc_counts)}, avg={sum(npc_counts)/len(npc_counts):.1f}")
            
            gdp_values = [m.get("gdp", 0) for m in self.metrics if "gdp" in m]
            if gdp_values:
                print(f"💰 GDP: min={min(gdp_values):,.0f}, max={max(gdp_values):,.0f}, avg={sum(gdp_values)/len(gdp_values):,.0f}")
            
            drift_values = [m.get("ideological_drift", 0) for m in self.metrics if "ideological_drift" in m]
            if drift_values:
                print(f"🧠 Ideological drift: min={min(drift_values):.3f}, max={max(drift_values):.3f}, avg={sum(drift_values)/len(drift_values):.3f}")
        
        print()
        print("=" * 80)
        print("Simulation complete. The brain is alive! 🧠")
        print("=" * 80)
    
    def calculate_divergence_score(self) -> float:
        """Calculate divergence score (placeholder implementation).
        
        Returns:
            Divergence score (0.0 = stable, 1.0 = highly dynamic)
        """
        if len(self.metrics) < 2:
            return 0.0
        
        # Simple variance-based divergence
        # In a real implementation, this would measure:
        # - How much NPC behavior diverges from baseline
        # - Economic volatility
        # - Ideological shifts
        # - World state changes
        
        variance = 0.0
        count = 0
        
        # Measure variance in key metrics
        for metric_name in ["gdp", "inflation", "ideological_drift"]:
            values = [m.get(metric_name, 0) for m in self.metrics if metric_name in m]
            if len(values) > 1:
                mean = sum(values) / len(values)
                var = sum((v - mean) ** 2 for v in values) / len(values)
                variance += var
                count += 1
        
        if count == 0:
            return 0.0
        
        # Normalize to 0-1 range (simplified)
        divergence = min(1.0, variance / count)
        return divergence


async def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Headless Realism Harness")
    parser.add_argument("--scenario", default="test_scenario", help="Scenario ID")
    parser.add_argument("--days", type=int, default=30, help="Number of days to simulate")
    parser.add_argument("--output", help="Output JSON file for metrics")
    
    args = parser.parse_args()
    
    harness = RealismHarness(scenario_id=args.scenario, days=args.days)
    
    try:
        await harness.run()
        
        # Save metrics if output file specified
        if args.output:
            output_path = Path(args.output)
            with open(output_path, "w") as f:
                json.dump(harness.metrics, f, indent=2, default=str)
            print(f"\nMetrics saved to: {output_path}")
    
    except KeyboardInterrupt:
        print("\n\nSimulation interrupted by user")
        if harness.orchestrator:
            await harness.orchestrator.stop()
    except Exception as e:
        print(f"\n\nError: {e}")
        import traceback
        traceback.print_exc()
        if harness.orchestrator:
            await harness.orchestrator.stop()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())

