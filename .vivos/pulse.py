import time
import json
import os

def send_pulse():
    # Simulate telemetry reporting to the OMNI-HUB
    manifest_path = ".vivos/manifest.json"
    if not os.path.exists(manifest_path):
        return
        
    try:
        with open(manifest_path, "r") as f:
            manifest = json.load(f)
    except:
        return
        
    payload = {
        "timestamp": time.time(),
        "repo": os.path.basename(os.getcwd()),
        "aggregate": manifest.get("aggregate"),
        "role": manifest.get("nexus_role"),
        "status": "VIVOS_ACTIVE",
        "yield_delta": 0.013
    }
    
    print(f"[PULSE] {json.dumps(payload)}")

if __name__ == "__main__":
    send_pulse()
