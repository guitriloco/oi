"""
SUPRA Mutation Loop
Continuous Architectural Evolution Loop for the Sovereign Line.
"""
import sys
import os
import time
import asyncio
from typing import Dict, Any, List

# Ensure we can import from local engines
sys.path.insert(0, os.path.dirname(__file__))

from engines.mutator import Mutator

class MutationLoop:
    """
    Continuous Architectural Evolution Loop.
    Monitors the Sovereign Line and triggers mutations when bottlenecks are detected.
    """
    def __init__(self):
        self.mutator = Mutator(model="codellama")
        self.evolution_history = []
        self.target_nodes = ["AUTO", "OI", "OLOCOO"]
        
    def register_node(self, node_name: str):
        """Register a node as a mutation target."""
        if node_name not in self.target_nodes:
            self.target_nodes.append(node_name)
            print(f"[MutationLoop] Registered new mutation target: {node_name}")

    async def execute_evolution(self, target_node: str, performance_signals: Dict[str, Any]) -> str:
        """
        Triggers a mutation cycle for a specific node.
        """
        print(f"[MutationLoop] Analyzing {target_node} for evolution...")
        
        # 1. Analyze the bottleneck from performance signals
        signal = self.mutator.analyze_bottleneck(target_node, performance_signals)
        print(f"[MutationLoop] Bottleneck detected: {signal.bottleneck_type} (severity: {signal.severity:.2f})")
        
        # 2. Determine if mutation is required based on severity threshold
        if signal.severity < 0.5:
            print(f"[MutationLoop] Severity {signal.severity:.2f} below threshold. No mutation needed.")
            return None
            
        # 3. Generate and save the mutation
        dummy_path = f"/home/team/shared/expansion_code/SUPRA/mutations/{target_node}_core.cpp"
        new_code = self.mutator.mutate(dummy_path, performance_signals)
        log_path = self.mutator.save_mutation(new_code, dummy_path)
        
        # 4. Log the evolution
        evolution_record = {
            "timestamp": time.time(),
            "node": target_node,
            "signal": signal,
            "log_path": log_path
        }
        self.evolution_history.append(evolution_record)
        
        print(f"[MutationLoop] Evolution successful. New logic staged at: {log_path}")
        return log_path

    async def scan_and_evolve(self, all_node_telemetry: Dict[str, Dict[str, Any]]) -> List[str]:
        """
        Scans all nodes for bottlenecks and evolves as needed.
        Returns list of evolved node log paths.
        """
        evolved_nodes = []
        
        for node_name, telemetry in all_node_telemetry.items():
            if node_name in self.target_nodes:
                log_path = await self.execute_evolution(node_name, telemetry)
                if log_path:
                    evolved_nodes.append(log_path)
        
        return evolved_nodes

    def get_evolution_report(self) -> Dict[str, Any]:
        """
        Returns the full evolution report.
        """
        return {
            "mutator_stats": self.mutator.get_evolution_report(),
            "evolution_history": self.evolution_history,
            "registered_targets": self.target_nodes
        }