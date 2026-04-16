import json
import os

class KnowledgeBase:
    def __init__(self, storage_path="knowledge/fragments.json"):
        self.storage_path = storage_path
        self._ensure_storage_exists()
        self.fragments = self._load_fragments()

    def _ensure_storage_exists(self):
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        if not os.path.exists(self.storage_path):
            with open(self.storage_path, 'w') as f:
                json.dump([], f)

    def _load_fragments(self):
        try:
            with open(self.storage_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def add_fragment(self, fragment):
        """
        Adds a knowledge fragment to the base and persists it.
        A fragment should be a dictionary containing 'insight', 'improvement', etc.
        """
        self.fragments.append(fragment)
        self._save_fragments()

    def get_all_fragments(self, limit=5):
        """
        Returns the last 'limit' fragments.
        """
        return self.fragments[-limit:]

    def _save_fragments(self):
        with open(self.storage_path, 'w') as f:
            json.dump(self.fragments, f, indent=4)
