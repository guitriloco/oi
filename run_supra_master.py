import concurrent.futures
import time
import random
import sys
import os

from pipeline.mutator import Mutator
from integrity.validator import Validator
from orchestration.rebuilder import Rebuilder

try:
    import wraith_core
except ImportError:
    print("Warning: wraith_core not found. Ensure the project is built.")
    wraith_core = None

class Node:
    def __init__(self, node_id):
        self.node_id = node_id
        if wraith_core:
            self.engine = wraith_core.WraithEngine(f"Node-{node_id}")
        else:
            self.engine = None
    
    def run_task(self, task_data):
        # print(f"Node {self.node_id} starting task: {task_data}")
        # Simulate some work
        time.sleep(random.uniform(0.01, 0.05))
        if self.engine:
            result = self.engine.process_data(task_data)
        else:
            result = f"[Node-{self.node_id} (Mock)] Processed: {task_data}"
        # print(f"Node {self.node_id} finished task: {task_data}")
        return result

def audit(execution_time, task_count):
    avg_time = execution_time / task_count if task_count > 0 else 0
    print(f"[AUDIT] Total time: {execution_time:.4f}s for {task_count} tasks.")
    print(f"[AUDIT] Average task execution time: {avg_time:.4f}s")
    return {"avg_execution_time": avg_time, "timestamp": time.time()}

def run_mutation_cycle(performance_signals):
    print("[MUTATE] Starting mutation phase...")
    mutator = Mutator()
    target_file = "src/wraith_engine.cpp"
    mutated_code = mutator.mutate(target_file, performance_signals)
    
    if not mutated_code:
        print("[MUTATE] Mutation failed to generate.")
        return False

    mutation_path = mutator.save_mutation(mutated_code, target_file)
    print(f"[MUTATE] Mutation saved to {mutation_path}")

    print("[VALIDATE] Starting validation phase...")
    validator = Validator()
    if validator.validate(mutation_path, target_file):
        print("[VALIDATE] Mutation passed validation.")
        
        print("[REBUILD] Starting rebuild phase (Hot-swap)...")
        # Apply mutation
        with open(target_file, 'w') as f:
            f.write(mutated_code)
        
        rebuilder = Rebuilder()
        if rebuilder.rebuild():
            print("[REBUILD] System rebuilt. Reloading module...")
            global wraith_core
            wraith_core = rebuilder.reload_module('wraith_core')
            print("[REBUILD] System hot-swapped successfully.")
            return True
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
    
    # AUDIT
    performance_signals = audit(execution_time, len(tasks))
    
    # MUTATE -> VALIDATE -> REBUILD
    if run_mutation_cycle(performance_signals):
        print("=== Mutation Cycle Complete ===")
    else:
        print("=== Mutation Cycle Failed or Skipped ===")

if __name__ == "__main__":
    main()
