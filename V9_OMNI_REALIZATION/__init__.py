"""
SUPRA - Multi-Model Fusion & Self-Mutation Command Overlord
CTO.NEW Phase 2 - Ascension Node

The SUPRA node implements architectural self-evolution through:
1. IntelligenceFusion: Multi-model strategic synthesis
2. MutationLoop: Continuous evolution of bottlenecked nodes
3. TelemetryMonitor: Real-time monitoring of the Sovereign Line
4. YieldMonitor: Yield and ROI tracking for optimization

Usage:
    from supra_command import SupraCommand
    
    supra = SupraCommand()
    result = await supra.run_ascension_check(telemetry, yield_report)
"""

__version__ = "3.0.0"
__author__ = "CTO.NEW"
__status__ = "PRODUCTION"

from .supra_command import SupraCommand
from .intelligence_fusion_v3 import IntelligenceFusionV3
from .mutation_loop import MutationLoop
from .engines.mutator import Mutator

__all__ = [
    "SupraCommand",
    "IntelligenceFusionV3", 
    "MutationLoop",
    "Mutator"
]