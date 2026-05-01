import json
import os

class SeenStorage:
    def __init__(self, path="seen.json"):
        self.path = path
        self.data = self._load()

    def _load(self):
        if not os.path.exists(self.path):
            return set()
        return set(json.load(open(self.path)))

    def add(self, item_id):
        self.data.add(item_id)
        self._save()

    def exists(self, item_id):
        return item_id in self.data

    def _save(self):
        json.dump(list(self.data), open(self.path, "w"))