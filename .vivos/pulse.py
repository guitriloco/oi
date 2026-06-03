import time
import json
import random

def get_telemetry():
    return {
        "timestamp": time.time(),
        "yield": round(random.uniform(0.95, 0.99), 4),
        "entropy": 0.0000,
        "status": "RESONANT"
    }

if __name__ == "__main__":
    while True:
        print(json.dumps(get_telemetry()))
        time.sleep(0.5)
