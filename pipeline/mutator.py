import requests
import json
import os

class Mutator:
    def __init__(self, model="codellama"):
        self.model = model
        self.ollama_url = "http://localhost:11434/api/generate"

    def mutate(self, file_path, performance_signals):
        with open(file_path, 'r') as f:
            original_code = f.read()

        prompt = f"""
        Improve the following C++ code based on these performance signals: {performance_signals}
        
        Original Code:
        ```cpp
        {original_code}
        ```
        
        Provide only the improved C++ code within a single code block.
        """

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }

        try:
            response = requests.post(self.ollama_url, json=payload, timeout=5)
            response.raise_for_status()
            result = response.json()
            mutated_code_raw = result['response']
            
            # Extract code from markdown block if present
            if "```cpp" in mutated_code_raw:
                mutated_code = mutated_code_raw.split("```cpp")[1].split("```")[0].strip()
            elif "```" in mutated_code_raw:
                mutated_code = mutated_code_raw.split("```")[1].split("```")[0].strip()
            else:
                mutated_code = mutated_code_raw.strip()

            return mutated_code
        except Exception as e:
            print(f"Error communicating with Ollama: {e}. Using fallback mock mutation.")
            return self._mock_mutate(original_code)

    def _mock_mutate(self, original_code):
        # Add a comment to the code to simulate mutation
        if "// Mutated for performance" in original_code:
            return original_code + "\n// Further mutation\n"
        return original_code + "\n// Mutated for performance\n"

    def save_mutation(self, mutated_code, original_file_path):
        mutation_dir = "mutation_logs"
        if not os.path.exists(mutation_dir):
            os.makedirs(mutation_dir)
        
        filename = os.path.basename(original_file_path)
        import time
        timestamp = int(time.time())
        mutation_path = os.path.join(mutation_dir, f"mutation_{timestamp}_{filename}")
        
        with open(mutation_path, 'w') as f:
            f.write(mutated_code)
        
        return mutation_path
