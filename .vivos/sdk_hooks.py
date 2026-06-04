import sys
import os

# Ensure the SDK path is available
SDK_PATH = os.path.expanduser("~/Sovereign-Intelligence-SDK")
if SDK_PATH not in sys.path:
    sys.path.append(SDK_PATH)

def call_brain(action, data):
    print(f"[VIVOS] Routing action '{action}' to Sovereign-Brain...")
    # Simulated SDK call
    return {"status": "SUCCESS", "response": f"Brain processed {action}"}

if __name__ == "__main__":
    print(call_brain("SELF_AUDIT", {"path": "."}))
