"""
SUPRA Sovereign Line Monitor
Real-time telemetry monitoring for all 9 nodes.
"""
import time
from typing import Dict, Any, List, Optional
from enum import Enum

class NodeHealth(Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    CRITICAL = "critical"
    UNKNOWN = "unknown"

class NodeStatus:
    """Status snapshot for a single node."""
    def __init__(self, name: str):
        self.name = name
        self.health = NodeHealth.UNKNOWN
        self.metrics: Dict[str, float] = {}
        self.last_updated = time.time()
        self.alerts: List[str] = []

class SovereignLineMonitor:
    """
    Monitors the entire 9-node Sovereign Line in real-time.
    Provides telemetry feeds to SUPRA for mutation decisions.
    """
    def __init__(self):
        self.nodes: Dict[str, NodeStatus] = {}
        self.alert_thresholds = {
            "memory": 0.80,
            "latency": 0.70,
            "throughput": 0.30,
            "sync": 0.75
        }
        self._setup_default_nodes()
        
    def _setup_default_nodes(self):
        """Initialize all 9 Sovereign Line nodes."""
        node_names = ["AUTO", "NOV", "PROJETS", "OI", "REX", "OLOCOO", "SUPRA", "YES", "VVV"]
        for name in node_names:
            self.nodes[name] = NodeStatus(name=name)
            
    def update_node_metrics(self, node_name: str, metrics: Dict[str, float]):
        """Update metrics for a specific node."""
        if node_name not in self.nodes:
            self.nodes[node_name] = NodeStatus(name=node_name)
            
        self.nodes[node_name].metrics = metrics
        self.nodes[node_name].last_updated = time.time()
        self.nodes[node_name].health = self._calculate_health(node_name, metrics)
        
    def _calculate_health(self, node_name: str, metrics: Dict[str, float]) -> NodeHealth:
        """Calculate health status based on metrics."""
        if not metrics:
            return NodeHealth.UNKNOWN
            
        critical_count = 0
        degraded_count = 0
        
        for metric_name, value in metrics.items():
            threshold = self.alert_thresholds.get(metric_name, 0.75)
            
            if metric_name == "throughput":
                if value < threshold:
                    critical_count += 1
                elif value < threshold * 1.3:
                    degraded_count += 1
            else:
                if value > threshold:
                    critical_count += 1
                elif value > threshold * 0.8:
                    degraded_count += 1
                    
        if critical_count > 0:
            return NodeHealth.CRITICAL
        elif degraded_count > 0:
            return NodeHealth.DEGRADED
        else:
            return NodeHealth.HEALTHY
            
    def get_all_telemetry(self) -> Dict[str, Dict[str, Any]]:
        """Get telemetry data for all nodes, formatted for SUPRA."""
        result = {
            "nodes": {},
            "overall_health": self._calculate_overall_health(),
            "timestamp": time.time()
        }
        
        critical_nodes = []
        degraded_nodes = []
        
        for name, status in self.nodes.items():
            result["nodes"][name] = {
                "health": status.health.value,
                "metrics": status.metrics,
                "last_updated": status.last_updated
            }
            
            if status.health == NodeHealth.CRITICAL:
                critical_nodes.append(name)
            elif status.health == NodeHealth.DEGRADED:
                degraded_nodes.append(name)
                
        result["critical_nodes"] = critical_nodes
        result["degraded_nodes"] = degraded_nodes
        
        return result
        
    def _calculate_overall_health(self) -> str:
        """Calculate overall system health."""
        critical = sum(1 for n in self.nodes.values() if n.health == NodeHealth.CRITICAL)
        degraded = sum(1 for n in self.nodes.values() if n.health == NodeHealth.DEGRADED)
        
        if critical > 0:
            return "critical"
        elif degraded > 0:
            return "degraded"
        else:
            return "healthy"
            
    def get_bottleneck_summary(self) -> Dict[str, Any]:
        """Get summary of bottlenecks across all nodes."""
        bottlenecks = []
        
        for name, status in self.nodes.items():
            for metric, value in status.metrics.items():
                threshold = self.alert_thresholds.get(metric, 0.75)
                
                if metric == "throughput" and value < threshold:
                    severity = 1.0 - (value / threshold)
                    bottlenecks.append({
                        "node": name,
                        "type": metric,
                        "value": value,
                        "severity": min(1.0, severity)
                    })
                elif value > threshold:
                    severity = (value - threshold) / threshold
                    bottlenecks.append({
                        "node": name,
                        "type": metric,
                        "value": value,
                        "severity": min(1.0, severity)
                    })
                    
        bottlenecks.sort(key=lambda x: x["severity"], reverse=True)
        
        return {
            "bottlenecks": bottlenecks,
            "count": len(bottlenecks),
            "most_critical": bottlenecks[0] if bottlenecks else None
        }
        
    def get_critical_path(self) -> List[str]:
        """Get the critical path nodes that need immediate attention."""
        critical = [name for name, status in self.nodes.items() 
                     if status.health == NodeHealth.CRITICAL]
        degraded = [name for name, status in self.nodes.items() 
                    if status.health == NodeHealth.DEGRADED]
        return critical + degraded

def generate_simulated_telemetry() -> Dict[str, Dict[str, float]]:
    """Generate simulated telemetry for testing."""
    import random
    random.seed(int(time.time()) % 10000)
    
    return {
        "AUTO": {"memory": random.uniform(0.6, 0.9), "latency": random.uniform(0.4, 0.8)},
        "OI": {"memory": random.uniform(0.7, 0.95), "latency": random.uniform(0.6, 0.85)},
        "OLOCOO": {"memory": random.uniform(0.5, 0.8), "sync": random.uniform(0.6, 0.9)},
        "PROJETS": {"memory": random.uniform(0.4, 0.7), "latency": random.uniform(0.3, 0.6)},
        "NOV": {"memory": random.uniform(0.3, 0.6), "latency": random.uniform(0.2, 0.5)},
        "REX": {"memory": random.uniform(0.6, 0.85), "latency": random.uniform(0.5, 0.8)},
        "SUPRA": {"memory": random.uniform(0.4, 0.7), "latency": random.uniform(0.3, 0.6)},
        "YES": {"memory": random.uniform(0.5, 0.75), "latency": random.uniform(0.4, 0.7)},
        "VVV": {"memory": random.uniform(0.3, 0.6), "latency": random.uniform(0.2, 0.5)}
    }

if __name__ == "__main__":
    monitor = SovereignLineMonitor()
    
    simulated = generate_simulated_telemetry()
    for node_name, metrics in simulated.items():
        monitor.update_node_metrics(node_name, metrics)
    
    telemetry = monitor.get_all_telemetry()
    print("[Monitor] Sovereign Line Telemetry:")
    print(f"  Overall Health: {telemetry['overall_health']}")
    print(f"  Critical Nodes: {telemetry.get('critical_nodes', [])}")
    print(f"  Degraded Nodes: {telemetry.get('degraded_nodes', [])}")
    
    bottlenecks = monitor.get_bottleneck_summary()
    print(f"\n[Monitor] Bottlenecks ({bottlenecks['count']} detected):")
    for b in bottlenecks['bottlenecks'][:3]:
        print(f"  - {b['node']}: {b['type']} = {b['value']:.2f} (severity: {b['severity']:.2f})")