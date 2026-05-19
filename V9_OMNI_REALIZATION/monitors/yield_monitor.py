"""
SUPRA Yield Monitor
Yield and ROI tracking for the Sovereign Line.
"""
import time
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from enum import Enum

class YieldStatus(Enum):
    OPTIMAL = "optimal"
    SUBOPTIMAL = "suboptimal"
    CRITICAL = "critical"

@dataclass
class YieldSnapshot:
    """Yield data for a specific node or system."""
    source: str
    rate: float  # 0.0 - 100.0 percentage
    potential: float  # Maximum potential percentage
    efficiency: float  # rate / potential ratio
    status: YieldStatus = YieldStatus.SUBOPTIMAL
    recommendations: List[str] = field(default_factory=list)
    timestamp: float = field(default_factory=time.time)

class YieldMonitor:
    """
    Monitors yield and ROI across the Sovereign Line.
    Provides yield reports to SUPRA for strategic optimization decisions.
    """
    def __init__(self):
        self.yield_history: List[YieldSnapshot] = []
        self.current_yield: Dict[str, YieldSnapshot] = {}
        self.baseline_yield = 30.0  # Baseline 30%
        
    def update_yield(self, source: str, rate: float, potential: float, recommendations: List[str] = None):
        """Update yield data for a source."""
        efficiency = rate / potential if potential > 0 else 0.0
        
        if rate >= potential * 0.9:
            status = YieldStatus.OPTIMAL
        elif rate >= potential * 0.5:
            status = YieldStatus.SUBOPTIMAL
        else:
            status = YieldStatus.CRITICAL
            
        snapshot = YieldSnapshot(
            source=source,
            rate=rate,
            potential=potential,
            efficiency=efficiency,
            status=status,
            recommendations=recommendations or []
        )
        
        self.current_yield[source] = snapshot
        self.yield_history.append(snapshot)
        
    def get_yield_report(self) -> Dict[str, Any]:
        """Get comprehensive yield report for SUPRA."""
        if not self.current_yield:
            return self._get_default_report()
            
        total_rate = sum(s.rate for s in self.current_yield.values())
        total_potential = sum(s.potential for s in self.current_yield.values())
        avg_efficiency = total_rate / total_potential if total_potential > 0 else 0.0
        
        critical_sources = [s.source for s in self.current_yield.values() 
                           if s.status == YieldStatus.CRITICAL]
        optimal_sources = [s.source for s in self.current_yield.values() 
                          if s.status == YieldStatus.OPTIMAL]
        
        # Calculate yield insights
        yield_delta = total_potential - total_rate
        improvement_potential = (yield_delta / total_potential * 100) if total_potential > 0 else 0
        
        return {
            "total_rate": total_rate,
            "total_potential": total_potential,
            "average_efficiency": avg_efficiency,
            "yield_delta": yield_delta,
            "improvement_potential": improvement_potential,
            "critical_sources": critical_sources,
            "optimal_sources": optimal_sources,
            "sources_count": len(self.current_yield),
            "insights": self._generate_insights(),
            "recommendations": self._generate_recommendations(),
            "timestamp": time.time()
        }
        
    def _get_default_report(self) -> Dict[str, Any]:
        """Return default report when no data available."""
        return {
            "total_rate": self.baseline_yield,
            "total_potential": 45.0,
            "average_efficiency": self.baseline_yield / 45.0,
            "yield_delta": 15.0,
            "improvement_potential": 33.0,
            "critical_sources": [],
            "optimal_sources": [],
            "sources_count": 0,
            "insights": [f"Current yield rate is {self.baseline_yield}%. 15% improvement potential available."],
            "recommendations": ["Optimize mesh-sync", "Reduce memory allocation in signal.proto"],
            "timestamp": time.time()
        }
        
    def _generate_insights(self) -> List[str]:
        """Generate strategic insights from yield data."""
        insights = []
        
        if not self.current_yield:
            return ["No yield data available. Operating at baseline."]
            
        avg_eff = sum(s.efficiency for s in self.current_yield.values()) / len(self.current_yield)
        
        if avg_eff < 0.5:
            insights.append("Critical: System yield below 50% efficiency. Immediate optimization required.")
        elif avg_eff < 0.7:
            insights.append("Warning: Yield efficiency below optimal. Mutation recommended.")
        else:
            insights.append("System operating at acceptable efficiency levels.")
            
        # Find the weakest link
        if self.current_yield:
            weakest = min(self.current_yield.values(), key=lambda s: s.efficiency)
            insights.append(f"Weakest link: {weakest.source} at {weakest.efficiency:.1%} efficiency.")
            
        return insights
        
    def _generate_recommendations(self) -> List[str]:
        """Generate actionable recommendations."""
        recommendations = []
        
        critical = [s for s in self.current_yield.values() if s.status == YieldStatus.CRITICAL]
        if critical:
            recommendations.append(f"Optimize {len(critical)} critical source(s) for immediate yield improvement.")
            
        suboptimal = [s for s in self.current_yield.values() if s.status == YieldStatus.SUBOPTIMAL]
        if suboptimal:
            recommendations.append(f"Schedule mutation for {len(suboptimal)} suboptimal source(s).")
            
        if not recommendations:
            recommendations.append("Maintain current architecture. No mutations required.")
            
        return recommendations

def generate_simulated_yield() -> Dict[str, List[float]]:
    """Generate simulated yield data for testing."""
    import random
    
    return {
        "REX": [random.uniform(25, 35), 45.0],  # rate, potential
        "OLOCOO": [random.uniform(28, 38), 50.0],
        "OI": [random.uniform(30, 40), 55.0],
        "AUTO": [random.uniform(35, 45), 50.0],
        "YES": [random.uniform(32, 42), 48.0]
    }

if __name__ == "__main__":
    monitor = YieldMonitor()
    
    # Simulate yield updates
    simulated = generate_simulated_yield()
    for source, (rate, potential) in simulated.items():
        monitor.update_yield(source, rate, potential)
    
    # Get yield report
    report = monitor.get_yield_report()
    print("[YieldMonitor] Sovereign Line Yield Report:")
    print(f"  Total Rate: {report['total_rate']:.1f}%")
    print(f"  Total Potential: {report['total_potential']:.1f}%")
    print(f"  Average Efficiency: {report['average_efficiency']:.1%}")
    print(f"  Improvement Potential: {report['improvement_potential']:.1f}%")
    print(f"  Critical Sources: {report['critical_sources']}")
    print(f"  Insights: {report['insights']}")