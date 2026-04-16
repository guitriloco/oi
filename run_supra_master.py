import concurrent.futures
import time
import random
import sys
import os

from pipeline.mutator import Mutator
from integrity.validator import Validator
from orchestration.rebuilder import Rebuilder

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

def audit(execution_time, task_count):
    """
    AUDIT phase: analyze performance signals.
    """
    avg_time = execution_time / task_count if task_count > 0 else 0
    print(f"\n[AUDIT] Total time: {execution_time:.4f}s for {task_count} tasks.")
    print(f"[AUDIT] Average task execution time: {avg_time:.4f}s")
    return {"avg_execution_time": avg_time, "task_count": task_count, "timestamp": time.time()}

def run_mutation_cycle(performance_signals):
    """
    Full Mutation Phase: MUTATE -> VALIDATE -> REBUILD
    """
    print("\n[MUTATE] Starting mutation phase...")
    mutator = Mutator()
    target_file = "src/wraith_engine.cpp"
    
    # MUTATE
    mutated_code = mutator.mutate(target_file, performance_signals)
    if not mutated_code:
        print("[MUTATE] Mutation failed to generate.")
        return False

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
                return True
            else:
                print("[REBUILD] Failed to reload module.")
                return False
        else:
            print("[REBUILD] Rebuild failed.")
            return False
    else:
        print("[VALIDATE] Mutation failed validation.")
        return False

def main():
    nodes = [Node(i) for i in range(1, 4)]
    tasks = [f"Payload-{i}" for i in range(20)]
    
    print("=== Supra-Codex Master Orchestrator ===")
    print(f"Nodes initialized: {len(nodes)}")
    print(f"Tasks scheduled: {len(tasks)}")
    print("---------------------------------------")
    
    # 1. Initial execution (Performance Baseline)
    start_time = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = []
        for i, task in enumerate(tasks):
            node = nodes[i % len(nodes)]
            futures.append(executor.submit(node.run_task, task))
        
        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                # print(f"Result: {result}")
            except Exception as exc:
                print(f"Task generated an exception: {exc}")

    end_time = time.time()
    execution_time = end_time - start_time
    print("---------------------------------------")
    print(f"All tasks completed in {execution_time:.2f} seconds.")
    
    # 2. AUDIT
    performance_signals = audit(execution_time, len(tasks))
    
    # 3. MUTATE -> VALIDATE -> REBUILD
    if run_mutation_cycle(performance_signals):
        print("\n=== Mutation Cycle Complete: System Evolved ===")
        
        # 4. Optional: Run again to show performance change
        print("\n[POST-MUTATION] Running tasks again with evolved core...")
        start_time = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(nodes[i % len(nodes)].run_task, task) for i, task in enumerate(tasks)]
            concurrent.futures.wait(futures)
        execution_time = time.time() - start_time
        print(f"[POST-MUTATION] Tasks completed in {execution_time:.2f} seconds.")
        audit(execution_time, len(tasks))
    else:
        print("\n=== Mutation Cycle Failed or Skipped ===")

if __name__ == "__main__":
    main()
