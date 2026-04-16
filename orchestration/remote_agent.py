import time
import requests
import uuid
import platform
import os
import sys

class RemoteAgent:
    def __init__(self, master_url, node_id=None):
        self.master_url = master_url.rstrip('/')
        self.node_id = node_id or f"node-{uuid.uuid4().hex[:8]}"
        self.capabilities = self._get_capabilities()
        self.hostname = platform.node()
        self.ip = "127.0.0.1" # In a real scenario, this would be the actual IP

    def _get_capabilities(self):
        return {
            "os": platform.system(),
            "processor": platform.processor(),
            "cpu_count": str(os.cpu_count()),
            "python_version": sys.version.split()[0]
        }

    def register(self):
        print(f"[*] Registering node {self.node_id} with master at {self.master_url}")
        try:
            resp = requests.post(f"{self.master_url}/register", json={
                "node_id": self.node_id,
                "hostname": self.hostname,
                "ip": self.ip,
                "capabilities": self.capabilities
            })
            resp.raise_for_status()
            print("[+] Registered successfully.")
        except Exception as e:
            print(f"[-] Registration failed: {e}")

    def run_task(self, task):
        print(f"[*] Running task {task['task_id']}")
        payload = task['payload']
        # Simple simulation of task execution
        # In a real scenario, this might involve wraith_core
        time.sleep(0.1)
        result = f"[RemoteNode-{self.node_id}] Processed: {payload}"
        return result

    def poll_and_execute(self):
        while True:
            try:
                resp = requests.get(f"{self.master_url}/tasks/{self.node_id}")
                resp.raise_for_status()
                tasks = resp.json()
                
                for task in tasks:
                    result = self.run_task(task)
                    requests.post(f"{self.master_url}/results", json={
                        "task_id": task['task_id'],
                        "node_id": self.node_id,
                        "result": result,
                        "status": "completed"
                    })
                
                # Check for new fragments (simplified)
                # In Phase 4, nodes should also stay in sync with the latest code/fragments
                
            except Exception as e:
                print(f"[-] Error during polling: {e}")
            
            time.sleep(2)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--master", default="http://localhost:8000", help="Master API URL")
    args = parser.parse_args()

    agent = RemoteAgent(args.master)
    agent.register()
    agent.poll_and_execute()
