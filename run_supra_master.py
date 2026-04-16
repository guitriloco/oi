import concurrent.futures
import time
import random
import sys

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
        print(f"Node {self.node_id} starting task: {task_data}")
        time.sleep(random.uniform(0.1, 0.5))
        if self.engine:
            result = self.engine.process_data(task_data)
        else:
            result = f"[Node-{self.node_id} (Mock)] Processed: {task_data}"
        print(f"Node {self.node_id} finished task: {task_data}")
        return result

def main():
    nodes = [Node(i) for i in range(1, 4)]
    tasks = [f"Payload-{i}" for i in range(10)]
    
    print("=== Supra-Codex Master Orchestrator ===")
    print(f"Nodes initialized: {len(nodes)}")
    print(f"Tasks scheduled: {len(tasks)}")
    print("---------------------------------------")
    
    start_time = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        # Round-robin assignment to nodes
        futures = []
        for i, task in enumerate(tasks):
            node = nodes[i % len(nodes)]
            futures.append(executor.submit(node.run_task, task))
        
        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                print(f"Result: {result}")
            except Exception as exc:
                print(f"Task generated an exception: {exc}")

    end_time = time.time()
    print("---------------------------------------")
    print(f"All tasks completed in {end_time - start_time:.2f} seconds.")

if __name__ == "__main__":
    main()
