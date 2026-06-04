import time
import json
import os

EXPECTED_MEMBERS = ['oi', 'olocoo', 'Auto', 'Mutante-Apex-Functions']

def send_wraith_pulse():
    manifest_path = ".vivos/manifest.json"
    if not os.path.exists(manifest_path):
        return
        
    try:
        with open(manifest_path, "r") as f:
            manifest = json.load(f)
    except:
        return
        
    workspace_root = os.path.expanduser("~")
    active_count = 0
    for member in EXPECTED_MEMBERS:
        if os.path.exists(os.path.join(workspace_root, member, ".vivos/manifest.json")):
            active_count += 1
            
    payload = {
        "timestamp": time.time(),
        "repo": os.path.basename(os.getcwd()),
        "aggregate": "WRAITH-MESH",
        "role": manifest.get("nexus_role"),
        "resonance_ratio": f"{active_count}/{len(EXPECTED_MEMBERS)}",
        "status": "FUSION_ACTIVE" if active_count == len(EXPECTED_MEMBERS) else "FUSION_DEGRADED",
        "yield_delta": 0.042
    }
    
    print(f"[WRAITH-PULSE] {json.dumps(payload)}")

if __name__ == "__main__":
    send_wraith_pulse()
