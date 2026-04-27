import concurrent.futures
import time
import random
import sys
import os
import threading
import requests

from pipeline.mutator import Mutator
from pipeline.distiller import Distiller
from integrity.validator import Validator
from orchestration.rebuilder import Rebuilder
from orchestration.sovereignty_api import start_api
from models.knowledge_base import KnowledgeBase

# Initial attempt to load the core module
try:
    import wraith_core
except ImportError:
    print("Warning: wraith_core not found. It will be built during the first cycle or needs manual build.")
    wraith_core = None

class Node:
    def __init__(self, node_id):
        self.node_id = node_id
        # We'll use the global wraith_core which might be reloaded
    
    def run_task(self, task_data):
        # Access the current wraith_core from global scope
        global wraith_core
        # Simulate some work
        time.sleep(random.uniform(0.01, 0.05))
        if wraith_core:
            try:
                engine = wraith_core.WraithEngine(f"Node-{self.node_id}")
                result = engine.process_data(task_data)
            except Exception as e:
                result = f"[Node-{self.node_id}] Error: {e}"
        else:
            result = f"[Node-{self.node_id} (Mock)] Processed: {task_data}"
        return result

class RemoteNode(Node):
    def __init__(self, node_id, master_url="http://localhost:8000"):
        super().__init__(node_id)
        self.master_url = master_url

    def run_task(self, task_data):
        try:
            # Dispatch task via API
            resp = requests.post(f"{self.master_url}/tasks", params={"node_id": self.node_id}, json=task_data)
            resp.raise_for_status()
            task_id = resp.json()["task_id"]

            # Poll for result
            timeout = 10
            start_poll = time.time()
            while time.time() - start_poll < timeout:
                try:
                    res_resp = requests.get(f"{self.master_url}/results/{task_id}")
                    if res_resp.status_code == 200:
                        return res_resp.json()["result"]
                except:
                    pass
                time.sleep(0.5)
            return f"[RemoteNode-{self.node_id}] Error: Task timed out"
        except Exception as e:
            return f"[RemoteNode-{self.node_id}] Error: {e}"

def audit(execution_time, task_count):
    """
    AUDIT phase: analyze performance signals.
    """
    avg_time = execution_time / task_count if task_count > 0 else 0
    print(f"\n[AUDIT] Total time: {execution_time:.4f}s for {task_count} tasks.")
    print(f"[AUDIT] Average task execution time: {avg_time:.4f}s")
    return {"avg_execution_time": avg_time, "task_count": task_count, "timestamp": time.time()}

def run_mutation_cycle(performance_signals, kb):
    """
    Full Mutation Phase: MUTATE -> VALIDATE -> REBUILD
    """
    print("\n[MUTATE] Starting mutation phase...")
    mutator = Mutator()
    target_file = "src/wraith_engine.cpp"
    
    with open(target_file, 'r') as f:
        original_code = f.read()

    # Get recent knowledge fragments to inform mutation
    fragments = kb.get_all_fragments(limit=3)
    
    # Check for Zenith signals via API
    try:
        resp = requests.get("http://localhost:8000/zenith/signals")
        if resp.status_code == 200:
            zenith_data = resp.json()
            if zenith_data:
                print(f"[MUTATE] Incorporating {len(zenith_data)} signals from ZENITH data stream.")
                performance_signals["zenith_insights"] = zenith_data
    except Exception as e:
        print(f"[MUTATE] Warning: Could not pull Zenith signals: {e}")

    # MUTATE
    mutated_code = mutator.mutate(target_file, performance_signals, fragments=fragments)
    if not mutated_code:
        print("[MUTATE] Mutation failed to generate.")
        return None, None

    mutation_path = mutator.save_mutation(mutated_code, target_file)
    print(f"[MUTATE] Mutation saved to {mutation_path}")

    # VALIDATE
    print("\n[VALIDATE] Starting validation phase...")
    validator = Validator()
    if validator.validate(mutation_path, target_file):
        print("[VALIDATE] Mutation passed validation and smoke tests.")
        
        # REBUILD
        print("\n[REBUILD] Starting rebuild phase (Hot-swap)...")
        # Apply mutation to the main source tree
        with open(target_file, 'w') as f:
            f.write(mutated_code)
        
        rebuilder = Rebuilder()
        if rebuilder.rebuild():
            print("[REBUILD] System rebuilt successfully.")
            
            # Reload the module
            global wraith_core
            wraith_core = rebuilder.reload_module('wraith_core')
            if wraith_core:
                print("[REBUILD] System hot-swapped successfully.")
                return original_code, mutated_code
            else:
                print("[REBUILD] Failed to reload module.")
                return None, None
        else:
            print("[REBUILD] Rebuild failed.")
            return None, None
    else:
        print("[VALIDATE] Mutation failed validation.")
        return None, None

def get_remote_nodes(master_url="http://localhost:8000"):
    try:
        resp = requests.get(f"{master_url}/nodes")
        if resp.status_code == 200:
            return [RemoteNode(node["node_id"], master_url) for node in resp.json()]
    except:
        pass
    return []

def main():
    # Start Sovereignty API in a background thread
    api_thread = threading.Thread(target=start_api, kwargs={"port": 8000}, daemon=True)
    api_thread.start()
    print("[*] Sovereignty API started on port 8000.")
    time.sleep(1) # Give it a second to start

    local_nodes = [Node(i) for i in range(1, 4)]
    tasks = [f"Payload-{i}" for i in range(20)]
    
    kb = KnowledgeBase()
    distiller = Distiller()

    print("=== Supra-Codex Master Orchestrator (Cluster Sovereign) ===")
    
    # Check for remote nodes
    remote_nodes = get_remote_nodes()
    nodes = local_nodes + remote_nodes
    
    print(f"Nodes initialized: {len(nodes)} ({len(local_nodes)} local, {len(remote_nodes)} remote)")
    print(f"Tasks scheduled: {len(tasks)}")
    print("---------------------------------------")
    
    # 1. Initial execution (Performance Baseline)
    start_time = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(nodes)) as executor:
        futures = []
        for i, task in enumerate(tasks):
            node = nodes[i % len(nodes)]
            futures.append(executor.submit(node.run_task, task))
        
        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
            except Exception as exc:
                print(f"Task generated an exception: {exc}")

    end_time = time.time()
    execution_time = end_time - start_time
    print("---------------------------------------")
    print(f"Initial tasks completed in {execution_time:.2f} seconds.")
    
    # Initial AUDIT
    performance_signals = audit(execution_time, len(tasks))
    
    # Main Evolution Loop (run for a few cycles to demonstrate)
    for cycle in range(1, 3):
        print(f"\n=== EVOLUTION CYCLE {cycle} ===")
        
        # Refresh remote nodes at the start of each cycle
        remote_nodes = get_remote_nodes()
        nodes = local_nodes + remote_nodes
        print(f"Active Cluster: {len(nodes)} nodes ({len(local_nodes)} local, {len(remote_nodes)} remote)")

        # 3. MUTATE -> VALIDATE -> REBUILD
        original_code, mutated_code = run_mutation_cycle(performance_signals, kb)
        
        if original_code and mutated_code:
            print(f"\n[CYCLE {cycle}] Mutation Cycle Complete: System Evolved")
            
            # 4. Run again to show performance change and DISTILL
            print(f"\n[POST-MUTATION] Running tasks again with evolved core (Cycle {cycle})...")
            start_time = time.time()
            with concurrent.futures.ThreadPoolExecutor(max_workers=len(nodes)) as executor:
                futures = [executor.submit(nodes[i % len(nodes)].run_task, task) for i, task in enumerate(tasks)]
                concurrent.futures.wait(futures)
            execution_time = time.time() - start_time
            print(f"[POST-MUTATION] Tasks completed in {execution_time:.2f} seconds.")
            
            new_performance_signals = audit(execution_time, len(tasks))

            # 5. DISTILL
            fragment = distiller.distill(original_code, mutated_code, performance_signals, new_performance_signals)
            if fragment:
                kb.add_fragment(fragment)
                print(f"[DISTILL] Knowledge fragment added: {fragment['insight']}")
                
                # Propagate Knowledge Fragment to the Cluster via API
                try:
                    requests.post("http://localhost:8000/fragments", json={
                        "fragment_id": f"frag-{int(time.time())}",
                        "content": mutated_code,
                        "metadata": fragment
                    })
                    print("[DISTILL] Fragment propagated to cluster sovereignty API.")
                except Exception as e:
                    print(f"[DISTILL] Failed to propagate fragment: {e}")
            else:
                print("[DISTILL] No significant knowledge gained from this cycle.")
            
            # Update performance signals for the next cycle
            performance_signals = new_performance_signals
        else:
            print(f"\n=== Mutation Cycle {cycle} Failed or Skipped ===")
            break

if __name__ == "__main__":
    main()
