"""
SUPRA Command - Production Command Overlord (CTO.NEW v3.0)
Multi-Model Fusion and Self-Mutation Master Node.
"""
import asyncio
import time
from typing import Dict, Any, List, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SUPRA.Command")

# Import local modules
from intelligence_fusion_v3 import IntelligenceFusionV3
from mutation_loop import MutationLoop

class SupraCommand:
    """
    Production-ready Command Overlord (SUPRA).
    Manages multi-model fusion and self-mutation for the Sovereign Line.
    """
    def __init__(self):
        self.fusion = IntelligenceFusionV3()
        self.evolution = MutationLoop()
        self.sovereign_mode = True
        self.monitoring_active = False
        self.node_registry = {}
        print("[SUPRA] Production Module Initialized.")
        print("[SUPRA] Sovereign Mode: ABSOLUTE")
        print("[SUPRA] Mutation Threshold: 0.75")

    def register_node(self, node_name: str, telemetry_source: Dict[str, Any]):
        """Register a node for SUPRA monitoring."""
        self.node_registry[node_name] = telemetry_source
        self.evolution.register_node(node_name)
        print(f"[SUPRA] Node registered: {node_name}")

    async def run_ascension_check(self, telemetry: Dict[str, Any], yield_report: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main ascension check - runs the full SUPRA decision cycle.
        
        Args:
            telemetry: Telemetry data from all nodes
            yield_report: Yield analysis from YES node
        """
        print(f"[SUPRA] Initiating Strategic Ascension Check...")
        start_time = time.time()
        
        # 1. Prepare multi-model inputs
        inputs = {
            "claude": {
                "analysis": telemetry.get("analysis", ""),
                "type": "strategic",
                "bottlenecks": telemetry.get("bottlenecks", [])
            },
            "gemini": {
                "insights": yield_report.get("insights", ""),
                "type": "yield",
                "yield_delta": yield_report.get("yield_delta", 0)
            },
            "local": {
                "telemetry_score": self._calculate_telemetry_score(telemetry),
                "primary_bottleneck": telemetry.get("primary_bottleneck", "unknown"),
                "severity": telemetry.get("severity", 0.5)
            }
        }
        
        # 2. Fuse Strategic Inputs via IntelligenceFusion
        strategy = self.fusion.fuse_multi_model(inputs)
        print(f"[SUPRA] Strategy Fusion Complete. Synergy: {strategy['synergy_score']:.2f}")
        print(f"[SUPRA] Decision: {strategy['decision']}")
        
        # 3. Trigger Evolution if threshold met
        result = {
            "strategy": strategy,
            "mutations_staged": [],
            "execution_time": 0,
            "status": "stable"
        }
        
        if strategy['mutation_required']:
            print("[SUPRA] System-wide Mutation Required. Engaging Evolution Engine...")
            
            # Get telemetry data for mutation targets
            all_node_telemetry = self._prepare_node_telemetry(telemetry)
            
            # Execute evolution on all bottlenecked nodes
            evolved_nodes = await self.evolution.scan_and_evolve(all_node_telemetry)
            result["mutations_staged"] = evolved_nodes
            result["status"] = "evolved"
            
            print(f"[SUPRA] Evolution complete. {len(evolved_nodes)} nodes mutated.")
        else:
            print("[SUPRA] Current architecture stable. No mutation needed.")
            
        result["execution_time"] = time.time() - start_time
        return result

    async def execute_supra_command(self, command: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a direct SUPRA command.
        
        Commands:
        - supra --ascend --mutate=ALL
        - supra --status
        - supra --fuse --models=claude,gemini
        """
        print(f"[SUPRA] Executing command: {command}")
        
        if "ascend" in command:
            return await self.run_ascension_check(
                params.get("telemetry", {}),
                params.get("yield_report", {})
            )
        elif "status" in command:
            return self.get_supra_status()
        elif "fuse" in command:
            return self._execute_fusion(params.get("inputs", {}))
        else:
            return {"error": f"Unknown command: {command}"}

    def get_supra_status(self) -> Dict[str, Any]:
        """Get current SUPRA system status."""
        return {
            "status": "OPERATIONAL",
            "sovereign_mode": self.sovereign_mode,
            "monitoring_active": self.monitoring_active,
            "registered_nodes": list(self.node_registry.keys()),
            "mutation_threshold": 0.75,
            "fusion_stats": self.fusion.get_fusion_report(),
            "evolution_stats": self.evolution.get_evolution_report()
        }

    def _calculate_telemetry_score(self, telemetry: Dict[str, Any]) -> float:
        """Calculate overall telemetry health score."""
        if not telemetry:
            return 0.5
            
        # Simple average of available metrics
        score = telemetry.get("severity", 0.5)
        return 1.0 - score  # Invert so higher = healthier

    def _prepare_node_telemetry(self, telemetry: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """Prepare node-specific telemetry for evolution."""
        result = {}
        bottleneck_nodes = ["AUTO", "OI", "OLOCOO"]
        
        if "bottlenecks" in telemetry:
            bottlenecks = telemetry["bottlenecks"]
            if isinstance(bottlenecks, list):
                for node in bottleneck_nodes:
                    result[node] = {
                        "node": node,
                        "bottleneck": bottlenecks[0] if bottlenecks else "generic",
                        "severity": telemetry.get("severity", 0.7)
                    }
            elif isinstance(bottlenecks, dict):
                for node, data in bottlenecks.items():
                    result[node] = data
        else:
            for node in bottleneck_nodes:
                result[node] = {
                    "node": node,
                    "bottleneck": telemetry.get("primary_bottleneck", "generic"),
                    "severity": telemetry.get("severity", 0.7)
                }
                
        return result

    def _execute_fusion(self, inputs: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Execute direct fusion without evolution."""
        return self.fusion.fuse_multi_model(inputs)

# === Standalone Execution ===
if __name__ == "__main__":
    # Simulated run with CTO.NEW production scenario
    supra = SupraCommand()
    
    # Register the 9-node Sovereign Line
    nodes = ["AUTO", "NOV", "PROJETS", "OI", "REX", "OLOCOO", "SUPRA", "YES", "VVV"]
    for node in nodes:
        supra.register_node(node, {"status": "active"})
    
    # Simulated telemetry from the Sovereign Line
    dummy_telemetry = {
        "analysis": "Wraith engine is experiencing latency in mesh-sync operations. Memory allocation in signal.proto handling is high.",
        "bottlenecks": ["memory", "latency"],
        "primary_bottleneck": "memory",
        "severity": 0.82
    }
    dummy_yield = {
        "insights": "Current data siphoning rate is 30%. Potential for 45% if mesh-sync is optimized. Throughput can increase by 50%.",
        "yield_delta": 15.0
    }
    
    # Run the ascension check
    result = asyncio.run(supra.run_ascension_check(dummy_telemetry, dummy_yield))
    
    print("\n" + "="*60)
    print("[SUPRA] ASCENSION CHECK COMPLETE")
    print("="*60)
    print(f"Status: {result['status'].upper()}")
    print(f"Synergy Score: {result['strategy']['synergy_score']:.2f}")
    print(f"Decision: {result['strategy']['decision']}")
    print(f"Mutations Staged: {len(result['mutations_staged'])}")
    print(f"Execution Time: {result['execution_time']:.3f}s")
    if result['mutations_staged']:
        print(f"Staged Files: {result['mutations_staged']}")
    print("="*60)