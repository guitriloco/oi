"""
SUPRA Intelligence Fusion V3
Enhanced multi-model fusion for strategic decision synthesis.
"""
import time
import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from collections import defaultdict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SUPRA.IntelligenceFusionV3")

@dataclass
class SovereignWeights:
    """Refined weights for Sovereign-level strategic decisions."""
    strategic: float = 0.85
    evolutionary: float = 0.95
    technical: float = 0.75
    efficiency: float = 0.80
    yield_priority: float = 0.90

class IntelligenceFusionV3:
    """
    Enhanced Intelligence Fusion for SUPRA Command.
    Fuses multi-model inputs for system-wide mutation decisions.
    Supports: Claude (strategic), Gemini (yield), Custom models.
    """
    def __init__(self):
        self.weights = SovereignWeights()
        self.fusion_history = []
        self.model_inputs = defaultdict(dict)
        
    def register_model_input(self, model_name: str, input_data: Dict[str, Any]):
        """Register input from a specific model."""
        self.model_inputs[model_name] = input_data
        
    def fuse_multi_model(self, inputs: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """
        Fuses inputs from multiple models into a unified strategic directive.
        """
        strategy_components = []
        total_weight = 0.0
        
        for model_name, input_data in inputs.items():
            weight = self._get_model_weight(model_name)
            total_weight += weight
            
            # Extract key insights based on model type
            if model_name == "claude":
                insight = self._extract_claude_insight(input_data)
            elif model_name == "gemini":
                insight = self._extract_gemini_insight(input_data)
            elif model_name == "local":
                insight = self._extract_local_insight(input_data)
            else:
                insight = self._extract_generic_insight(input_data)
                
            strategy_components.append({
                "model": model_name,
                "weight": weight,
                "insight": insight,
                "contribution": weight * insight["score"]
            })
        
        # Normalize and synthesize
        fused_response = self._synthesize_strategy(strategy_components, total_weight)
        synergy_score = self._calculate_synergy_score(inputs)
        mutation_required = synergy_score > 0.75
        
        result = {
            "fused_response": fused_response,
            "synergy_score": synergy_score,
            "mutation_required": mutation_required,
            "components": strategy_components,
            "timestamp": time.time(),
            "decision": self._make_decision(synergy_score, strategy_components)
        }
        
        self.fusion_history.append(result)
        return result
        
    def fuse_sovereign_strategy(self, claude_input: str, gemini_input: str) -> Dict[str, Any]:
        """
        Legacy interface for compatibility with older code.
        """
        inputs = {
            "claude": {"analysis": claude_input, "type": "strategic"},
            "gemini": {"insights": gemini_input, "type": "yield"}
        }
        return self.fuse_multi_model(inputs)
        
    def _get_model_weight(self, model_name: str) -> float:
        """Get weighting factor for a specific model."""
        weights_map = {
            "claude": self.weights.strategic,
            "gemini": self.weights.yield_priority,
            "local": self.weights.technical,
            "custom": self.weights.efficiency
        }
        return weights_map.get(model_name, 0.5)
        
    def _extract_claude_insight(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract insight from Claude-style strategic input."""
        analysis = data.get("analysis", "")
        words = analysis.lower().split()
        
        # Score based on key strategic terms
        strategic_terms = ["optimize", "improve", "bottleneck", "performance", "latency", "memory", "efficiency"]
        matches = sum(1 for term in strategic_terms if term in " ".join(words))
        score = min(1.0, matches / len(strategic_terms))
        
        return {
            "score": score,
            "primary_concern": self._find_primary_concern(words),
            "recommended_action": self._determine_action(words)
        }
        
    def _extract_gemini_insight(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract insight from Gemini-style yield input."""
        insights = data.get("insights", "")
        words = insights.lower().split()
        
        # Score based on yield/value terms
        yield_terms = ["rate", "percentage", "potential", "optimize", "increase", "maximize"]
        matches = sum(1 for term in yield_terms if term in " ".join(words))
        score = min(1.0, matches / len(yield_terms))
        
        return {
            "score": score,
            "yield_delta": self._calculate_yield_delta(words),
            "priority_targets": self._extract_targets(words)
        }
        
    def _extract_local_insight(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract insight from local telemetry input."""
        return {
            "score": data.get("telemetry_score", 0.5),
            "primary_concern": data.get("primary_bottleneck", "unknown"),
            "severity": data.get("severity", 0.5)
        }
        
    def _extract_generic_insight(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generic insight extraction."""
        return {
            "score": 0.5,
            "content": str(data)[:200]
        }
        
    def _synthesize_strategy(self, components: List[Dict], total_weight: float) -> str:
        """Synthesize strategy from weighted components."""
        if not components:
            return "[NO_STRATEGY] No inputs available."
            
        # Sort by contribution
        sorted_comp = sorted(components, key=lambda x: x["contribution"], reverse=True)
        
        primary = sorted_comp[0]
        secondary = sorted_comp[1] if len(sorted_comp) > 1 else None
        
        synthesis = f"[STRATEGIC_ALIGNMENT] Priority: {primary['model']} insights on {primary['insight'].get('primary_concern', 'system')}"
        
        if secondary:
            synthesis += f" | Secondary: {secondary['model']} perspective on yield optimization"
            
        synthesis += f" | Synergy Weight: {total_weight:.2f}"
        
        return synthesis
        
    def _calculate_synergy_score(self, inputs: Dict[str, Dict[str, Any]]) -> float:
        """Calculate synergy score based on input overlap and complementarity."""
        if len(inputs) < 2:
            return 0.5
            
        all_words = []
        for data in inputs.values():
            content = " ".join(str(v) for v in data.values()).lower().split()
            all_words.append(set(content))
            
        # Calculate pairwise overlap
        total_overlap = 0.0
        pairs = 0
        for i in range(len(all_words)):
            for j in range(i + 1, len(all_words)):
                intersection = all_words[i].intersection(all_words[j])
                union = all_words[i].union(all_words[j])
                if union:
                    total_overlap += len(intersection) / len(union)
                pairs += 1
                
        return total_overlap / pairs if pairs > 0 else 0.5
        
    def _make_decision(self, synergy_score: float, components: List[Dict]) -> str:
        """Make strategic decision based on fusion results."""
        if synergy_score > 0.85:
            return "AGGRESSIVE_MUTATION"
        elif synergy_score > 0.75:
            return "MODERATE_MUTATION"
        elif synergy_score > 0.6:
            return "CONSERVATIVE_MUTATION"
        else:
            return "MONITOR_ONLY"
            
    def _find_primary_concern(self, words: List[str]) -> str:
        """Find the primary concern from strategic terms."""
        concerns = {
            "memory": "High memory allocation",
            "latency": "Excessive latency",
            "throughput": "Low throughput",
            "sync": "Synchronization issues",
            "bottleneck": "System bottleneck detected"
        }
        for word in words:
            if word in concerns:
                return concerns[word]
        return "General optimization needed"
        
    def _determine_action(self, words: List[str]) -> str:
        """Determine recommended action from words."""
        actions = {
            "memory": "Enable object pooling and pre-allocation",
            "latency": "Implement async pipeline and batch processing",
            "throughput": "Enable SIMD vectorization and ring buffers",
            "sync": "Apply lock-free RCU patterns"
        }
        for word in words:
            if word in actions:
                return actions[word]
        return "Apply generic optimizations"
        
    def _calculate_yield_delta(self, words: List[str]) -> float:
        """Calculate yield delta percentage from insights."""
        for word in words:
            if "%" in word:
                try:
                    return float(word.replace("%", ""))
                except:
                    pass
        return 15.0  # Default 15% potential improvement
        
    def _extract_targets(self, words: List[str]) -> List[str]:
        """Extract target nodes from insights."""
        nodes = ["AUTO", "OI", "OLOCOO", "PROJETS", "NOV", "REX", "VVV", "YES", "SUPRA"]
        return [n for n in nodes if n.lower() in " ".join(words)]
        
    def get_fusion_report(self) -> Dict[str, Any]:
        """Returns fusion history and statistics."""
        return {
            "total_fusions": len(self.fusion_history),
            "history": self.fusion_history,
            "weights": {
                "strategic": self.weights.strategic,
                "evolutionary": self.weights.evolutionary,
                "technical": self.weights.technical,
                "efficiency": self.weights.efficiency,
                "yield_priority": self.weights.yield_priority
            }
        }