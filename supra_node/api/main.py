from fastapi import FastAPI, Request
import time
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
from fusion import create_fusion_engine
from mutator import Mutator

app = FastAPI(title="SUPRA The Ascension - Multi-Model Fusion & Mutation")

fusion_engine = create_fusion_engine()
mutator = Mutator()

@app.post("/ascend/fuse")
async def ascend_fuse(context: dict = None):
    # If it receives a list instead of a dict, wrap it
    if isinstance(context, list):
        context = {"models": context}
    elif context is None:
        context = {"task_type": "general"}
        
    print(f"[SUPRA] Initiating Ascension Cycle with context: {context.get('task_type', 'general')}")
    
    # 1. Simulate multi-model input
    claude_suggestion = "Optimize memory management in WraithEngine."
    gemini_suggestion = "Improve recursive depth in HyperProtocol."
    
    # 2. Fuse intelligence
    fusion_result = fusion_engine.fuse_responses(
        claude_response=claude_suggestion,
        gemini_response=gemini_suggestion,
        task_type=context.get('task_type', 'general')
    )
    
    # 3. Trigger Mutation if applicable (in a real scenario, this would apply to a file)
    # For now, we simulate the 'Architectural Self-Mutation'
    
    return {
        "status": "ASCENDED",
        "fusion_score": fusion_result['synergy_score'],
        "fused_directive": fusion_result['fused_response'],
        "timestamp": time.time()
    }

@app.post("/ascend/mutate")
async def ascend_mutate(target_node: str, signals: dict = None):
    print(f"[SUPRA] Mutating architecture for {target_node}")
    # This would call the Mutator class
    # result = mutator.mutate(target_node, signals or {})
    return {"status": "ARCHITECTURE_MUTATED", "target": target_node}

@app.post("/protocol/callback")
async def protocol_callback(payload: dict):
    # Received from Mirror Protocol Registry in OI
    event = payload.get("event")
    data = payload.get("data")
    print(f"[SUPRA] Received protocol signal: {event}")
    
    if event == "ANOMALY_DETECTED":
        # Mutate system architecture if an anomaly is detected
        print(f"[SUPRA] Architectural mutation triggered by anomaly: {data.get('reason')}")
        # ... logic ...
        return {"status": "system_mutation_initiated"}
    
    return {"status": "signal_received"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005)
