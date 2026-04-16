class OrchestrationManager:
    def __init__(self, node_count=3):
        self.node_count = node_count

    def deploy(self):
        print(f"Deploying {self.node_count} nodes...")
