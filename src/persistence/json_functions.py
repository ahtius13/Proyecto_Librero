import json
from pathlib import Path
from datetime import date

class JsonFunctions:
    def __init__(self, filepath):
        self.filepath = Path(filepath)
        if not self.filepath.exists():
            self._write([])

    def _serialize(self, obj):
        """Convierte objetos date a string ISO."""
        if isinstance(obj, date):
            return obj.isoformat()
        raise TypeError(f"Type {type(obj)} not serializable")

    def _deserialize(self, data):
        """Convierte strings ISO a objetos date si existen fechas."""
        for item in data:
            for key in ["Fecha Salida", "Fecha Prestamo"]:
                if key in item and isinstance(item[key], str):
                    item[key] = date.fromisoformat(item[key])
        return data

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

