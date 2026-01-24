# src/persistence/json_repository.py
import json
from pathlib import Path

class JsonFunctions:
    def __init__(self, filepath):
        self.filepath = Path(filepath)
        if not self.filepath.exists():
            self._write([])

    def _read(self):
        with open(self.filepath, "r", encoding="utf-8") as f:
            return json.load(f)

    def _write(self, data):
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def get_all(self):
        return self._read()

    def save_all(self, data):
        self._write(data)
