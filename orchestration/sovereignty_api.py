from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
import uuid
import time

from models.cluster_state import ClusterNode, ClusterState

app = FastAPI(title="Supra-Codex Sovereignty API")

# Global state
cluster_state = ClusterState()
task_queue: Dict[str, List[Dict[str, Any]]] = {}  # node_id -> list of tasks
task_results: Dict[str, Dict[str, Any]] = {}      # task_id -> result
knowledge_fragments: Dict[str, Dict[str, Any]] = {} # fragment_id -> fragment

class RegistrationRequest(BaseModel):
    node_id: str
    hostname: str
    ip: str
    capabilities: Dict[str, str]

class TaskAssignment(BaseModel):
    task_id: str
    payload: Any

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
