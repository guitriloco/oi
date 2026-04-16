from dataclasses import dataclass, field
from typing import Dict, List, Optional
import time

@dataclass
class ClusterNode:
    node_id: str
    hostname: str
    ip: str
    capabilities: Dict[str, str]
    status: str = "active"
    last_seen: float = field(default_factory=time.time)

class ClusterState:
    def __init__(self):
        self.nodes: Dict[str, ClusterNode] = {}

    def update_node(self, node: ClusterNode):
        self.nodes[node.node_id] = node

    def get_active_nodes(self) -> List[ClusterNode]:
        current_time = time.time()
        # Consider a node inactive if not seen for more than 60 seconds
        return [
            node for node in self.nodes.values()
            if node.status == "active" and (current_time - node.last_seen) < 60
        ]

    def get_node(self, node_id: str) -> Optional[ClusterNode]:
        return self.nodes.get(node_id)
