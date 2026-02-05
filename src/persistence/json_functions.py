import json
from pathlib import Path
from datetime import date

class JsonFunctions:
    def __init__(self, filepath, date_keys=None):
        self.filepath = Path(filepath)
        self.date_keys = date_keys or []  # Claves configurables para fechas
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        if not self.filepath.exists():
            self._write([])

    def _serialize(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()
        raise TypeError(f"Type {type(obj)} not serializable")

    def _deserialize(self, data):
        for item in data:
            for key in self.date_keys:
                if key in item and isinstance(item[key], str):
                    try:
                        item[key] = date.fromisoformat(item[key])
                    except ValueError:
                        pass  # Ignorar si no es formato válido
        return data

    def _read(self):
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            return self._deserialize(data)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _write(self, data):
        try:
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False, default=self._serialize)
        except Exception as e:
            raise IOError(f"Error al escribir en {self.filepath}: {e}")

    def get_all(self):
        return self._read()

    def save_all(self, data):
        self._write(data)