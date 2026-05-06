from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel

class ClusterRegion(str, Enum):
    ALPHA = "US-EAST"
    BETA = "EU-CENTRAL"
    GAMMA = "ASIA-PACIFIC"
    DELTA = "GLOBAL-SOUTH"

class ClusterRole(str, Enum):
    EXECUTION_FORGE = "execution-forge"
    ETERNAL_VAULT = "eternal-vault"
    SENSORY_PULSE = "sensory-pulse"
    OPTICS = "optics"

class ClusterNodeInfo(BaseModel):
    name: str
    region: ClusterRegion
    role: ClusterRole
    base_url: str
    coordinate: List[float]

CLUSTER_REGISTRY: Dict[ClusterRegion, ClusterNodeInfo] = {
    ClusterRegion.ALPHA: ClusterNodeInfo(
        name="Vertex Alpha",
        region=ClusterRegion.ALPHA,
        role=ClusterRole.EXECUTION_FORGE,
        base_url="http://localhost:8101",
        coordinate=[0.0, 0.0, 1.0]
    ),
    ClusterRegion.BETA: ClusterNodeInfo(
        name="Vertex Beta",
        region=ClusterRegion.BETA,
        role=ClusterRole.ETERNAL_VAULT,
        base_url="http://localhost:8102",
        coordinate=[1.0, 0.0, 0.0]
    ),
    ClusterRegion.GAMMA: ClusterNodeInfo(
        name="Vertex Gamma",
        region=ClusterRegion.GAMMA,
        role=ClusterRole.SENSORY_PULSE,
        base_url="http://localhost:8103",
        coordinate=[-1.0, 0.0, 0.0]
    ),
    ClusterRegion.DELTA: ClusterNodeInfo(
        name="Vertex Delta",
        region=ClusterRegion.DELTA,
        role=ClusterRole.OPTICS,
        base_url="http://localhost:8104",
        coordinate=[0.0, 1.0, 0.0]
    )
}

def get_cluster_by_region(region: ClusterRegion) -> Optional[ClusterNodeInfo]:
    return CLUSTER_REGISTRY.get(region)
