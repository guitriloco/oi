import httpx
import asyncio
import time
import json
import os
from typing import Any, Dict, List

class AetherSyncBridge:
    """
    The Aether-Sync Bridge (The Forge).
    Implements the Sovereign Omni-Pulse: a high-velocity, zero-resistance
    flow across the entire 9-node Line.
    Hardened for sub-millisecond heartbeat pulses and real-time telemetry.
    """
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.nodes = {
            "HUB": base_url,
            "ARCHITECT": f"{base_url}",
            "OBSERVER": "http://localhost:8001",
            "YIELD": "http://localhost:8002",
            "VAULT": "http://localhost:8003",
            "REX": "http://localhost:8004",
            "SUPRA": "http://localhost:8005"
        }
        self.client = httpx.AsyncClient(timeout=60.0, limits=httpx.Limits(max_keepalive_connections=20, max_connections=100))
        self.telemetry_path = "/home/agent-engineer/oi/orchestration/forge/pulse_telemetry.json"
        self._ensure_telemetry_exists()

    def _ensure_telemetry_exists(self):
        if not os.path.exists(self.telemetry_path):
            with open(self.telemetry_path, 'w') as f:
                json.dump([], f)

    def log_pulse_telemetry(self, pulse_data: Dict[str, Any]):
        try:
            with open(self.telemetry_path, 'r+') as f:
                history = json.load(f)
                history.append(pulse_data)
                if len(history) > 50:
                    history.pop(0)
                f.seek(0)
                json.dump(history, f, indent=2)
                f.truncate()
        except Exception as e:
            print(f"[FORGE] Telemetry Logging Error: {e}")

    async def heartbeat(self) -> Dict[str, Any]:
        """
        Executes a high-velocity parallel heartbeat across all nodes.
        Targeting sub-millisecond internal latency.
        """
        start_time = time.perf_counter()
        tasks = [self.client.get(url, timeout=0.1) for url in self.nodes.values()]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        node_status = {}
        for (name, url), res in zip(self.nodes.items(), results):
            if isinstance(res, httpx.Response):
                node_status[name] = {"status": "ACTIVE", "latency_ms": (res.elapsed.total_seconds() * 1000)}
            else:
                node_status[name] = {"status": "DOWN", "error": str(res)}
        
        end_time = time.perf_counter()
        total_latency_ms = (end_time - start_time) * 1000
        
        heartbeat_pulse = {
            "pulse_id": f"heartbeat-{int(time.time() * 1000)}",
            "type": "HEARTBEAT",
            "total_latency_ms": total_latency_ms,
            "nodes": node_status,
            "timestamp": time.time()
        }
        self.log_pulse_telemetry(heartbeat_pulse)
        return heartbeat_pulse

    async def execute_omni_pulse(self, seed_objective: str) -> Dict[str, Any]:
        pulse_id = f"pulse-{int(time.time())}"
        print(f"[FORGE] Initiating Omni-Pulse: {pulse_id}")
        start_time = time.perf_counter()
        
        pulse_data = {}
        
        try:
            # 1. ARCHITECT: Strategic Geometry (Prediction)
            print("[FORGE] Step 1: Architect - Defining Path...")
            arch_resp = await self.client.post(f"{self.nodes['HUB']}/nectar/predict", params={"objective": seed_objective})
            arch_resp.raise_for_status()
            pulse_data['prediction'] = arch_resp.json().get("prediction", seed_objective)
            
            # 2. SIPHON (REX): Invisible Infiltration (Acquisition)
            print("[FORGE] Step 2: Siphon - Acquiring Energy...")
            rex_resp = await self.client.post(f"{self.nodes['REX']}/siphon/start", params={"target": pulse_data['prediction']})
            rex_resp.raise_for_status()
            pulse_data['siphon'] = rex_resp.json()
            
            # 3. ENGINEER (OI): Integration Forge (Bonding)
            print("[FORGE] Step 3: Engineer - Bonding Energy...")
            refine_payload = {
                "reason": f"Omni-Pulse Integration ({pulse_id})",
                "data": pulse_data['siphon'],
                "is_anomaly": False
            }
            refine_resp = await self.client.post(f"{self.nodes['HUB']}/refinement/trigger", json=refine_payload)
            refine_resp.raise_for_status()
            pulse_data['integration'] = refine_resp.json()
            
            # 4. MUTATION (SUPRA): Atomic Evolution (Transformation)
            print("[FORGE] Step 4: Mutation - Atomic Evolution...")
            mutate_resp = await self.client.post(f"{self.nodes['SUPRA']}/ascend/mutate", params={"target_node": "OI"})
            mutate_resp.raise_for_status()
            pulse_data['evolution'] = mutate_resp.json()
            
            # 5. YIELD (YES): Gold Harvesting (Distillation)
            print("[FORGE] Step 5: Yield - Harvesting Gold...")
            conquer_resp = await self.client.post(f"{self.nodes['YIELD']}/execute", params={"objective": pulse_data['prediction']})
            conquer_resp.raise_for_status()
            pulse_data['harvest'] = conquer_resp.json()
            
            # 6. VAULT (VVV): Eternal Preservation (Sealing)
            print("[FORGE] Step 6: Vault - Sealing Essence...")
            vault_resp = await self.client.post(f"{self.nodes['VAULT']}/vault/store", params={"content": str(pulse_data['harvest'])})
            vault_resp.raise_for_status()
            pulse_data['preservation'] = vault_resp.json()
            
            # 7. OBSERVER (NOV): Frequency Monitoring (Stability)
            print("[FORGE] Step 7: Observer - Frequency Verification...")
            obs_payload = {
                "name": "OMNI_PULSE_SYNC",
                "rating": 10,
                "notes": f"Pulse {pulse_id} stable. Vault ID: {pulse_data['preservation'].get('vault_id')}"
            }
            obs_resp = await self.client.post(f"{self.nodes['OBSERVER']}/observe", json=obs_payload)
            obs_resp.raise_for_status()
            pulse_data['monitoring'] = obs_resp.json()
            
            end_time = time.perf_counter()
            total_latency_ms = (end_time - start_time) * 1000
            
            result = {
                "status": "OMNI_PULSE_SUCCESS",
                "pulse_id": pulse_id,
                "total_latency_ms": total_latency_ms,
                "summary": {
                    "path": pulse_data['prediction'],
                    "siphoned": pulse_data['siphon'].get("acquired", 0),
                    "yield_grade": pulse_data['harvest'].get("yield", "HIGH"),
                    "vault_id": pulse_data['preservation'].get("vault_id")
                },
                "data_mesh": pulse_data,
                "timestamp": time.time()
            }
            self.log_pulse_telemetry(result)
            return result
        except Exception as e:
            print(f"[FORGE] Omni-Pulse Failure at {pulse_id}: {str(e)}")
            return {
                "status": "OMNI_PULSE_FAILED",
                "error": str(e),
                "pulse_id": pulse_id,
                "timestamp": time.time()
            }

    async def close(self):
        await self.client.aclose()

bridge = AetherSyncBridge()
