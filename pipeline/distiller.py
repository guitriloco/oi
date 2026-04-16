import requests
import json
import time

class Distiller:
    def __init__(self, model="codellama"):
        self.model = model
        self.ollama_url = "http://localhost:11434/api/generate"

    def distill(self, original_code, mutated_code, prev_signals, current_signals):
        """
        Analyzes the difference between original and mutated code alongside performance changes.
        If improvement is significant, generates a knowledge fragment.
        """
        prev_avg = prev_signals.get("avg_execution_time", 0)
        curr_avg = current_signals.get("avg_execution_time", 0)

        if prev_avg == 0:
            return None

        improvement = (prev_avg - curr_avg) / prev_avg
        print(f"[DISTILL] Performance change: {improvement*100:.2f}%")

        # Only distill if improvement is > 1%
        if improvement > 0.01:
            print("[DISTILL] Significant improvement detected. Distilling insight...")
            insight = self._get_insight(original_code, mutated_code, improvement)
            fragment = {
                "timestamp": time.time(),
                "improvement": improvement,
                "insight": insight,
                "prev_avg": prev_avg,
                "curr_avg": curr_avg
            }
            return fragment
        
        return None

    def _get_insight(self, original_code, mutated_code, improvement):
        prompt = f"""
        Analyze the following C++ code change that resulted in a {improvement*100:.2f}% performance improvement.
        
        Original Code:
        ```cpp
        {original_code}
        ```
        
        Mutated Code:
        ```cpp
        {mutated_code}
        ```
        
        Instruction:
        Provide a concise (1-2 sentences) summary of why this optimization was successful. 
        Focus on the specific technique used.
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
            insight = result.get('response', '').strip()
            return insight
        except Exception as e:
            print(f"[DISTILL] Ollama distillation failed: {e}. Using fallback insight.")
            return self._mock_insight(mutated_code)

    def _mock_insight(self, mutated_code):
        if "vector" in mutated_code.lower():
            return "Optimization focused on efficient container usage and memory locality."
        return "Generic performance optimization through code refinement."
