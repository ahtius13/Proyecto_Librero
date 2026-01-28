import json
from pathlib import Path
from datetime import date

class JsonFunctions:
    def __init__(self, filepath):
        self.filepath = Path(filepath)
        if not self.filepath.exists():
            self._write([])

    def _serialize(self, obj):
        """Convierte objetos no serializables a JSON."""
        if isinstance(obj, date):
            return obj.isoformat()  # "YYYY-MM-DD"
        raise TypeError(f"Type {type(obj)} not serializable")

    def _deserialize(self, d):
        """Convierte strings ISO a objetos date si es necesario."""
        for item in d:
            if "fecha_salida" in item and isinstance(item["fecha_salida"], str):
                item["fecha_salida"] = date.fromisoformat(item["fecha_salida"])
        return d

    def _read(self):
        with open(self.filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return self._deserialize(data)

    def _write(self, data):
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False, default=self._serialize)

    def get_all(self):
        return self._read()

    def save_all(self, data):
        self._write(data)
