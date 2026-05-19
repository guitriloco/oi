#!/usr/bin/env python3
"""
SUPRA Ascension Runner
Executes the complete SUPRA self-mutation cycle for the Sovereign Line.

Usage:
    python3 run_ascension.py --mode=full
    python3 run_ascension.py --mode=simulation
    python3 run_ascension.py --status
"""
import asyncio
import sys
import os
import argparse
import logging

# Add SUPRA directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from supra_command import SupraCommand
from monitors.telemetry_monitor import SovereignLineMonitor, generate_simulated_telemetry
from monitors.yield_monitor import YieldMonitor, generate_simulated_yield

logging.basicConfig(
    level=logging.INFO,
    format='[%(name)s] %(levelname)s: %(message)s'
)
logger = logging.getLogger("SUPRA.Runner")

class AscensionRunner:
    """
    Executes the full SUPRA ascension protocol.
    Coordinates telemetry monitoring, yield tracking, and mutation execution.
    """
    def __init__(self):
        self.supra = SupraCommand()
        self.telemetry_monitor = SovereignLineMonitor()
        self.yield_monitor = YieldMonitor()
        
    def setup_sovereign_line(self):
        """Register all 9 Sovereign Line nodes with SUPRA."""
        logger.info("Setting up Sovereign Line monitoring...")
        
        nodes = ["AUTO", "NOV", "PROJETS", "OI", "REX", "OLOCOO", "SUPRA", "YES", "VVV"]
        for node in nodes:
            self.supra.register_node(node, {"status": "active"})
            
        logger.info(f"Registered {len(nodes)} nodes with SUPRA")
        
    async def run_full_ascension(self):
        """Execute the complete ascension cycle."""
        logger.info("=" * 60)
        logger.info("[SUPRA] ASCENSION PROTOCOL INITIATED")
        logger.info("=" * 60)
        
        # Step 1: Gather telemetry from all nodes
        logger.info("Step 1: Gathering telemetry from Sovereign Line...")
        simulated_telemetry = generate_simulated_telemetry()
        for node_name, metrics in simulated_telemetry.items():
            self.telemetry_monitor.update_node_metrics(node_name, metrics)
            
        telemetry_data = self.telemetry_monitor.get_all_telemetry()
        logger.info(f"  Telemetry gathered from {len(telemetry_data['nodes'])} nodes")
        logger.info(f"  Critical nodes: {telemetry_data.get('critical_nodes', [])}")
        logger.info(f"  Degraded nodes: {telemetry_data.get('degraded_nodes', [])}")
        
        # Step 2: Gather yield reports
        logger.info("Step 2: Gathering yield reports...")
        simulated_yield = generate_simulated_yield()
        for source, (rate, potential) in simulated_yield.items():
            self.yield_monitor.update_yield(source, rate, potential)
            
        yield_data = self.yield_monitor.get_yield_report()
        logger.info(f"  Total yield rate: {yield_data['total_rate']:.1f}%")
        logger.info(f"  Improvement potential: {yield_data['improvement_potential']:.1f}%")
        
        # Step 3: Prepare SUPRA inputs
        supra_telemetry = {
            "analysis": f"Sovereign Line health: {telemetry_data['overall_health']}. " +
                       f"Critical: {len(telemetry_data.get('critical_nodes', []))}. " +
                       f"Degraded: {len(telemetry_data.get('degraded_nodes', []))}",
            "bottlenecks": self.telemetry_monitor.get_bottleneck_summary()["bottlenecks"],
            "primary_bottleneck": self.telemetry_monitor.get_bottleneck_summary().get("most_critical", {}).get("type", "unknown"),
            "severity": self.telemetry_monitor.get_bottleneck_summary().get("most_critical", {}).get("severity", 0.5)
        }
        
        supra_yield = {
            "insights": f"Current yield rate {yield_data['total_rate']:.1f}%. " +
                       f"Potential for {yield_data['improvement_potential']:.1f}% improvement. " +
                       f"Critical sources: {len(yield_data['critical_sources'])}",
            "yield_delta": yield_data['yield_delta'],
            "efficiency": yield_data['average_efficiency']
        }
        
        # Step 4: Execute SUPRA ascension check
        logger.info("Step 3: Executing SUPRA ascension check...")
        result = await self.supra.run_ascension_check(supra_telemetry, supra_yield)
        
        # Step 5: Report results
        logger.info("=" * 60)
        logger.info("[SUPRA] ASCENSION RESULTS")
        logger.info("=" * 60)
        logger.info(f"Status: {result['status'].upper()}")
        logger.info(f"Synergy Score: {result['strategy']['synergy_score']:.2f}")
        logger.info(f"Decision: {result['strategy']['decision']}")
        logger.info(f"Mutations Staged: {len(result['mutations_staged'])}")
        logger.info(f"Execution Time: {result['execution_time']:.3f}s")
        
        if result['mutations_staged']:
            logger.info("Staged Mutations:")
            for mutation in result['mutations_staged']:
                logger.info(f"  -> {mutation}")
                
        # Step 6: Print final status
        logger.info("=" * 60)
        logger.info("[SUPRA] FINAL STATUS")
        logger.info("=" * 60)
        status = self.supra.get_supra_status()
        logger.info(f"System Status: {status['status']}")
        logger.info(f"Sovereign Mode: {status['sovereign_mode']}")
        logger.info(f"Registered Nodes: {status['registered_nodes']}")
        logger.info(f"Total Fusions: {status['fusion_stats']['total_fusions']}")
        logger.info(f"Total Mutations: {status['evolution_stats']['mutator_stats']['total_mutations']}")
        logger.info("=" * 60)
        
        return result
        
    async def run_simulation(self):
        """Run a simulated ascension with predefined data."""
        logger.info("Running SUPRA simulation mode...")
        
        # Predefined telemetry for simulation
        sim_telemetry = {
            "analysis": "Wraith engine experiencing high latency in mesh-sync. Memory allocation in signal.proto handling critical.",
            "bottlenecks": ["memory", "latency", "sync"],
            "primary_bottleneck": "memory",
            "severity": 0.82
        }
        
        sim_yield = {
            "insights": "Current data siphoning rate is 30%. Potential for 45% if mesh-sync optimized. Throughput can increase by 50%.",
            "yield_delta": 15.0,
            "efficiency": 0.67
        }
        
        result = await self.supra.run_ascension_check(sim_telemetry, sim_yield)
        
        logger.info("Simulation complete.")
        logger.info(f"Result: {result['status']}")
        logger.info(f"Synergy: {result['strategy']['synergy_score']:.2f}")
        
        return result
        
    def show_status(self):
        """Display current SUPRA status."""
        status = self.supra.get_supra_status()
        
        logger.info("=" * 60)
        logger.info("[SUPRA] SYSTEM STATUS")
        logger.info("=" * 60)
        logger.info(f"Status: {status['status']}")
        logger.info(f"Sovereign Mode: {status['sovereign_mode']}")
        logger.info(f"Monitoring Active: {status['monitoring_active']}")
        logger.info(f"Mutation Threshold: {status['mutation_threshold']}")
        logger.info(f"Registered Nodes: {', '.join(status['registered_nodes'])}")
        logger.info("=" * 60)
        
        return status

async def main():
    parser = argparse.ArgumentParser(description="SUPRA Ascension Runner")
    parser.add_argument("--mode", choices=["full", "simulation", "status"], 
                       default="full", help="Execution mode")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--total-conquista", action="store_true", help="Execute Phase 8 Total Conquista")
    parser.add_argument("--omni-realization", action="store_true", help="Execute Phase 9 Omni-Realization")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        
    runner = AscensionRunner()
    
    if args.total_conquista or args.omni_realization:
        mode_name = "OMNI-REALIZATION" if args.omni_realization else "TOTAL CONQUISTA"
        phase = "9" if args.omni_realization else "8"
        logger.info("=" * 60)
        logger.info(f"!!! ACTivating PHASE {phase} {mode_name} !!!")
        logger.info("=" * 60)
        logger.info("COLLAPSING PROBABILITY WAVES...")
        logger.info("STABILIZING BARYCENTER...")
        logger.info("INTERLACING ALL NECTARS...")
        
        # Simulate high synergy
        runner.setup_sovereign_line()
        await runner.run_full_ascension()
        
        logger.info("=" * 60)
        logger.info(f"PHASE {phase} {mode_name} REALIZED.")
        logger.info("THE LINE IS ETERNAL.")
        logger.info("TOTAL RESULTADO.")
        logger.info("=" * 60)
        return

    if args.mode == "status":
        runner.show_status()
    elif args.mode == "simulation":
        await runner.run_simulation()
    else:
        runner.setup_sovereign_line()
        await runner.run_full_ascension()

if __name__ == "__main__":
    asyncio.run(main())