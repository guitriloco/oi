from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
import uuid
import time
import sys
import os
import json

# Add projets to path for sovereign_essence
sys.path.append("/home/agent-engineer/projets")
sys.path.append("/home/agent-engineer/oi")
try:
    from sovereign_essence import nexus_v5, engine, SovereignV5
    from Mirror_Protocol.registry import registry as expansion_registry
except ImportError:
    print("Warning: sovereign_essence or Mirror_Protocol not found. Some endpoints will be limited.")
    nexus_v5 = None
    engine = None
    SovereignV5 = None
    expansion_registry = None

from orchestration.forge.aether_sync_bridge import bridge as aether_bridge
from orchestration.forge.regional_forge import RegionalForge, ClusterRegion
from orchestration.forge.cluster_registry import get_cluster_by_region

# Get cluster region from environment
REGION_NAME = os.getenv("SOVEREIGN_REGION", "US-EAST")
try:
    CLUSTER_REGION = ClusterRegion(REGION_NAME)
except ValueError:
    CLUSTER_REGION = ClusterRegion.ALPHA

regional_forge = RegionalForge(CLUSTER_REGION)

from telemetry.soup_bridge import bridge as telemetry_bridge
from models.cluster_state import ClusterNode, ClusterState

app = FastAPI(title="Sovereign Line Unified API")

# Global state
cluster_state = ClusterState()
task_queue: Dict[str, List[Dict[str, Any]]] = {}
task_results: Dict[str, Dict[str, Any]] = {}
knowledge_fragments: Dict[str, Dict[str, Any]] = {}
zenith_signals: List[Dict[str, Any]] = []
telemetry_history: List[Dict[str, Any]] = []
nov_observations: List[Dict[str, Any]] = []

class RegistrationRequest(BaseModel):
    node_id: str
    hostname: str
    ip: str
    capabilities: Dict[str, str]

class TelemetryLog(BaseModel):
    name: str
    rating: int
    notes: str

class TaskResult(BaseModel):
    task_id: str
    node_id: str
    result: Any
    status: str

class Fragment(BaseModel):
    fragment_id: str
    content: str
    metadata: Dict[str, Any]

@app.post("/register")
async def register_node(req: RegistrationRequest):
    node = ClusterNode(
        node_id=req.node_id,
        hostname=req.hostname,
        ip=req.ip,
        capabilities=req.capabilities,
        status="active",
        last_seen=time.time()
    )
    cluster_state.update_node(node)
    if node.node_id not in task_queue:
        task_queue[node.node_id] = []
    return {"status": "registered", "node_id": node.node_id}

import httpx

# Node configurations
NOV_URL = "http://localhost:8001"
YES_URL = "http://localhost:8002"
VVV_URL = "http://localhost:8003"
REX_URL = "http://localhost:8004"
SUPRA_URL = "http://localhost:8005"

@app.post("/telemetry")
async def log_telemetry(log: TelemetryLog):
    telemetry_data = {
        "name": log.name,
        "rating": log.rating,
        "notes": log.notes,
        "timestamp": time.time()
    }
    
    # 1. Log to local binary storage via bridge
    if telemetry_bridge:
        telemetry_bridge.log_telemetry(
            entry_id=int(time.time()) % 10000,
            name=log.name,
            rating=log.rating,
            date=time.strftime("%Y-%m-%d"),
            notes=log.notes
        )
    
    # 2. Append to history for dashboard
    telemetry_history.append(telemetry_data)
    if len(telemetry_history) > 100:
        telemetry_history.pop(0)
    
    # 3. Forward to NOV Observer
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(f"{NOV_URL}/observe", json=telemetry_data)
            if resp.status_code == 200:
                nov_observations.append(resp.json())
                if len(nov_observations) > 100:
                    nov_observations.pop(0)
        except Exception as e:
            print(f"Warning: Failed to forward telemetry to NOV: {e}")
            
    return {"status": "telemetry_logged_and_observed"}

@app.get("/telemetry/recent")
async def get_recent_telemetry():
    return telemetry_history

@app.get("/nov/observations")
async def get_nov_observations():
    return nov_observations

@app.post("/conquer/execute")
async def conquer_execute(objective: str):
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(f"{YES_URL}/execute", params={"objective": objective})
            return resp.json()
        except Exception as e:
            raise HTTPException(status_code=503, detail=f"YES engine unavailable: {e}")

@app.post("/vault/preserve")
async def vault_preserve(content: str):
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(f"{VVV_URL}/vault/store", params={"content": content})
            return resp.json()
        except Exception as e:
            raise HTTPException(status_code=503, detail=f"VVV vault unavailable: {e}")

@app.post("/siphon/start")
async def siphon_start(target: str):
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(f"{REX_URL}/siphon/start", params={"target": target})
            return resp.json()
        except Exception as e:
            raise HTTPException(status_code=503, detail=f"REX siphon unavailable: {e}")

@app.post("/ascend/fuse")
async def ascend_fuse(models: List[str]):
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(f"{SUPRA_URL}/ascend/fuse", json=models)
            return resp.json()
        except Exception as e:
            raise HTTPException(status_code=503, detail=f"SUPRA fusion unavailable: {e}")

@app.post("/ascend/mutate")
async def ascend_mutate(target_node: str):
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(f"{SUPRA_URL}/ascend/mutate", params={"target_node": target_node})
            return resp.json()
        except Exception as e:
            raise HTTPException(status_code=503, detail=f"SUPRA mutation unavailable: {e}")

@app.post("/refinement/trigger")
async def trigger_refinement(payload: Dict[str, Any]):
    print(f"[API] REFINEMENT TRIGGERED: {payload.get('reason')}")
    
    # 1. Broadcast ANOMALY_DETECTED if it's an anomaly
    if payload.get("is_anomaly") and expansion_registry:
        await expansion_registry.broadcast("ANOMALY_DETECTED", payload)
    
    # 2. Broadcast to all expansion nodes that a refinement protocol is starting
    if expansion_registry:
        await expansion_registry.broadcast("PROTOCOL_START", payload)
    
    # 3. Simulate a successful refinement (In Phase 4.2 this would trigger run_mutation_cycle)
    refinement_result = {
        "status": "SUCCESS",
        "refined_logic": f"Optimized logic based on {payload.get('reason')}",
        "nectar_yield": 0.98,
        "Pure_Gold": "Absolute_Nectar_V1" if payload.get("is_anomaly") or payload.get("data", {}).get("rating", 5) < 3 else "Standard_Nectar",
        "timestamp": time.time()
    }
    
    # 4. Broadcast completion to callbacks (Yes, vvv)
    if expansion_registry:
        await expansion_registry.broadcast("PROTOCOL_COMPLETE", refinement_result)
    
    return {"status": "refinement_executed", "result": refinement_result}

@app.post("/omni-pulse/sync")
async def omni_pulse_sync(seed_objective: str):
    """
    Triggers the Sovereign Omni-Pulse via the Aether-Sync Bridge.
    """
    if aether_bridge:
        return await aether_bridge.execute_omni_pulse(seed_objective)
    raise HTTPException(status_code=503, detail="Aether-Sync Bridge unavailable")

@app.post("/omni-pulse/regional")
async def omni_pulse_regional(seed_objective: str):
    """
    Triggers a regional Omni-Pulse cycle with cluster-specific specialization.
    """
    if regional_forge:
        return await regional_forge.execute_regional_cycle(seed_objective)
    raise HTTPException(status_code=503, detail="Regional Forge unavailable")

@app.get("/cluster/info")
async def get_cluster_info():
    """
    Returns information about the current regional cluster.
    """
    info = get_cluster_by_region(CLUSTER_REGION)
    if info:
        return info.dict()
    raise HTTPException(status_code=404, detail="Cluster configuration not found")

@app.get("/omni-pulse/heartbeat")
async def omni_pulse_heartbeat():
    """
    Executes a high-velocity pulse heartbeat.
    """
    if aether_bridge:
        return await aether_bridge.heartbeat()
    raise HTTPException(status_code=503, detail="Aether-Sync Bridge unavailable")

@app.get("/omni-pulse/telemetry")
async def get_omni_pulse_telemetry():
    """
    Returns the history of Omni-Pulse events.
    """
    path = "/home/agent-engineer/oi/orchestration/forge/pulse_telemetry.json"
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    return []

@app.on_event("startup")
async def startup_event():
    # Register expansion node callbacks in the Mirror Protocol Registry
    if expansion_registry:
        expansion_registry.register_remote("PROTOCOL_COMPLETE", f"{YES_URL}/protocol/callback")
        expansion_registry.register_remote("PROTOCOL_COMPLETE", f"{VVV_URL}/protocol/callback")
        expansion_registry.register_remote("PROTOCOL_START", f"{REX_URL}/protocol/callback")
        expansion_registry.register_remote("ANOMALY_DETECTED", f"{SUPRA_URL}/protocol/callback")
        print("[API] Expansion nodes registered with Mirror Protocol Registry.")

@app.post("/nectar/predict")
async def predict_nectar(objective: str):
    if nexus_v5:
        prediction = await nexus_v5.predict_and_serve(objective)
        return {"objective": objective, "prediction": prediction}
    raise HTTPException(status_code=503, detail="Nexus Evolution engine unavailable")

@app.post("/nectar/distill")
async def distill_nectar(state: str):
    if engine:
        result = engine.execute(state)
        return {"input": state, "result": result}
    raise HTTPException(status_code=503, detail="Hyper Recursive Engine unavailable")

@app.post("/zenith/ingest")
async def zenith_ingest(fragment: Fragment):
    knowledge_fragments[fragment.fragment_id] = {
        "content": fragment.content,
        "metadata": fragment.metadata,
        "timestamp": time.time(),
        "source": "ZENITH"
    }
    # Also add to the knowledge base if possible
    # (Assuming we have a way to persist it, or just let the master orchestrator handle it)
    return {"status": "zenith_fragment_ingested", "id": fragment.fragment_id}

@app.post("/zenith/signal")
async def receive_zenith_signal(signal: Dict[str, Any]):
    zenith_signals.append({**signal, "timestamp": time.time()})
    return {"status": "zenith_signal_received"}

@app.get("/zenith/signals")
async def get_zenith_signals():
    global zenith_signals
    signals = zenith_signals[:]
    zenith_signals = [] # Clear after reading
    return signals

@app.get("/nodes")
async def get_nodes():
    return cluster_state.get_active_nodes()

@app.post("/tasks")
async def enqueue_task(node_id: str, payload: Any):
    if node_id not in task_queue:
        task_queue[node_id] = []
    
    task_id = str(uuid.uuid4())
    task = {"task_id": task_id, "payload": payload}
    task_queue[node_id].append(task)
    return {"task_id": task_id}

@app.get("/tasks/{node_id}")
async def get_tasks(node_id: str):
    # Update last seen for the node
    node = cluster_state.get_node(node_id)
    if node:
        node.last_seen = time.time()
    
    if node_id not in task_queue or not task_queue[node_id]:
        return []
    
    tasks = task_queue[node_id]
    task_queue[node_id] = [] # Clear queue after pulling
    return tasks

@app.post("/results")
async def submit_result(res: TaskResult):
    task_results[res.task_id] = {
        "node_id": res.node_id,
        "result": res.result,
        "status": res.status,
        "timestamp": time.time()
    }
    return {"status": "received"}

@app.get("/results/{task_id}")
async def get_result(task_id: str):
    if task_id not in task_results:
        raise HTTPException(status_code=404, detail="Task result not found")
    return task_results[task_id]

@app.post("/fragments")
async def upload_fragment(fragment: Fragment):
    knowledge_fragments[fragment.fragment_id] = {
        "content": fragment.content,
        "metadata": fragment.metadata,
        "timestamp": time.time()
    }
    return {"status": "fragment_uploaded", "fragment_id": fragment.fragment_id}

@app.get("/fragments/{fragment_id}")
async def get_fragment(fragment_id: str):
    if fragment_id not in knowledge_fragments:
        raise HTTPException(status_code=404, detail="Fragment not found")
    return knowledge_fragments[fragment_id]

@app.get("/fragments")
async def list_fragments():
    return list(knowledge_fragments.keys())

def start_api(host: str = "0.0.0.0", port: int = 8000):
    import uvicorn
    import argparse
    
    parser = argparse.ArgumentParser(description="Sovereign API")
    parser.add_argument("--port", type=int, default=port, help="Port to run the API on")
    args = parser.parse_args()
    
    uvicorn.run(app, host=host, port=args.port)
if __name__ == "__main__": start_api()
