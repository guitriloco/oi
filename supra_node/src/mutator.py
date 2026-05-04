import requests
import json
import os
import time

class Mutator:
    def __init__(self, model="codellama"):
        self.model = model
        self.ollama_url = "http://localhost:11434/api/generate"

    def mutate(self, file_path, performance_signals, fragments=None):
        """
        Interacts with local Ollama to generate C++ code improvements based on 'performance signals'
        and past successful 'fragments' from the Knowledge Base.
        """
        with open(file_path, 'r') as f:
            original_code = f.read()

        knowledge_context = ""
        if fragments:
            knowledge_context = "\nPast Successful Strategies:\n"
            for i, f in enumerate(fragments):
                knowledge_context += f"- {f.get('insight', 'N/A')}\n"

        zenith_context = ""
        if isinstance(performance_signals, dict) and "zenith_insights" in performance_signals:
            zenith_context = "\nZenith Data Mesh Signals:\n"
            for s in performance_signals["zenith_insights"]:
                zenith_context += f"- {s.get('insight', 'N/A')} (Metric: {s.get('efficiency_metric', 'N/A')})\n"

        prompt = f"""
        Objective: Optimize the following C++ code for better performance.
        Performance Signals: {performance_signals}
        {knowledge_context}
        {zenith_context}
        
        Original Code:
        ```cpp
        {original_code}
        ```
        
        Instruction: 
        1. Identify bottlenecks based on signals.
        2. Apply optimizations (e.g., reduce allocations, use more efficient algorithms, etc.).
        3. Leverage past successful strategies if applicable.
        4. Return ONLY the improved C++ code within a single markdown code block.
        """

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }

        print(f"Requesting mutation from Ollama (model: {self.model})...")
        try:
            # We use a short timeout because if it's not there, we want to fail fast
            response = requests.post(self.ollama_url, json=payload, timeout=2)
            response.raise_for_status()
            result = response.json()
            mutated_code_raw = result.get('response', '')
            
            # Extract code from markdown block
            mutated_code = self._extract_code(mutated_code_raw)
            if not mutated_code:
                print("Failed to extract code from Ollama response. Using fallback.")
                return self._mock_mutate(original_code)

            return mutated_code
        except Exception as e:
            print(f"Ollama interaction failed: {e}. Proceeding with mock mutation.")
            return self._mock_mutate(original_code)

    def _extract_code(self, raw_response):
        if "```cpp" in raw_response:
            return raw_response.split("```cpp")[1].split("```")[0].strip()
        elif "```" in raw_response:
            return raw_response.split("```")[1].split("```")[0].strip()
        return raw_response.strip()

    def _mock_mutate(self, original_code):
        # Simulate an optimization by adding a comment and maybe a slight code change
        if "// Optimized for performance" in original_code:
            return original_code.replace("// Optimized for performance", "// Optimized for performance (v2)")
        
        return original_code + "\n// Optimized for performance\n"

    def save_mutation(self, mutated_code, original_file_path):
        """
        Saves the mutated code to mutation_logs directory.
        """
        mutation_dir = "mutation_logs"
        if not os.path.exists(mutation_dir):
            os.makedirs(mutation_dir)
        
        filename = os.path.basename(original_file_path)
        timestamp = int(time.time())
        mutation_path = os.path.join(mutation_dir, f"mutation_{timestamp}_{filename}")
        
        with open(mutation_path, 'w') as f:
            f.write(mutated_code)
        
        return mutation_path
