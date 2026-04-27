from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
import uuid
import time
import sys
import os

# Add projets to path for sovereign_essence
sys.path.append("/home/agent-engineer/projets")
try:
    from sovereign_essence import nexus_v5, engine, SovereignV5
except ImportError:
    print("Warning: sovereign_essence not found. Some endpoints will be limited.")
    nexus_v5 = None
    engine = None
    SovereignV5 = None

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
    uvicorn.run(app, host=host, port=port)
