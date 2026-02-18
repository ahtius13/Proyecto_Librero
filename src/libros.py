import datetime
from typing import List, Optional
from src.persistence.json_functions import JsonFunctions

class Libro:
    def __init__(self, titulo: str, autor: str, codigo: str, editorial: str, precio: float, cantidad: int = 0,
                 fecha_salida: Optional[datetime.date] = None, fecha_prestamo: Optional[datetime.date] = None,
                 prestamos: List[dict] = None, ventas: List[dict] = None, preventas: List[dict] = None):
        self.titulo = titulo
        self.autor = autor
        self.codigo = codigo
        self.editorial = editorial
        self.precio = precio
        self.cantidad = cantidad
        self.fecha_salida = fecha_salida
        self.fecha_prestamo = fecha_prestamo
        self.prestamos = prestamos or []  # Lista de {'cantidad': int, 'fecha_prestamo': date, 'fecha_vencimiento': date}
        self.ventas = ventas or []  # Lista de {'numero_socio': str, 'cantidad': int, 'fecha': date, 'precio_pagado': float}
        self.preventas = preventas or []  # Lista de {'numero_socio': str, 'cantidad': int}

    def to_dict(self) -> dict:
        return {
            "titulo": self.titulo,
            "autor": self.autor,
            "codigo": self.codigo,
            "editorial": self.editorial,
            "precio": self.precio,
            "cantidad": self.cantidad,
            "fecha_salida": self.fecha_salida.isoformat() if self.fecha_salida else None,
            "fecha_prestamo": self.fecha_prestamo.isoformat() if self.fecha_prestamo else None,
            "prestamos": [{
                "cantidad": p['cantidad'],
                "fecha_prestamo": p['fecha_prestamo'].isoformat(),
                "fecha_vencimiento": p['fecha_vencimiento'].isoformat()
            } for p in self.prestamos],
            "ventas": [{
                "numero_socio": v['numero_socio'],
                "cantidad": v['cantidad'],
                "fecha": v['fecha'].isoformat(),
                "precio_pagado": v['precio_pagado']
            } for v in self.ventas],
            "preventas": self.preventas
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Libro':
        fecha_salida = datetime.date.fromisoformat(data["fecha_salida"]) if data.get("fecha_salida") else None
        fecha_prestamo = datetime.date.fromisoformat(data["fecha_prestamo"]) if data.get("fecha_prestamo") else None
        prestamos = [{
            "cantidad": p["cantidad"],
            "fecha_prestamo": datetime.date.fromisoformat(p["fecha_prestamo"]),
            "fecha_vencimiento": datetime.date.fromisoformat(p["fecha_vencimiento"])
        } for p in data.get("prestamos", [])]
        ventas = [{
            "numero_socio": v["numero_socio"],
            "cantidad": v["cantidad"],
            "fecha": datetime.date.fromisoformat(v["fecha"]),
            "precio_pagado": v["precio_pagado"]
        } for v in data.get("ventas", [])]
        preventas = data.get("preventas", [])
        return cls(
            data["titulo"], data["autor"], data["codigo"], data["editorial"], data["precio"], data["cantidad"],
            fecha_salida, fecha_prestamo, prestamos, ventas, preventas
        )

class LibroManager:
    def __init__(self, filepath: str = "data/libros.json"):
        self.json_handler = JsonFunctions(filepath)
        self.libros = self._cargar_libros()

    def _cargar_libros(self) -> List[Libro]:
        data = self.json_handler.get_all()
        return [Libro.from_dict(d) for d in data]

    def _guardar_libros(self):
        data = [libro.to_dict() for libro in self.libros]
        self.json_handler.save_all(data)

    # Métodos CRUD para libros (iguales)
    def registrar_libro(self, libro: Libro):
        if any(l.codigo == libro.codigo for l in self.libros):
            raise ValueError("Código de libro duplicado")
        if libro.fecha_salida and libro.fecha_salida < datetime.date.today():
            raise ValueError("Fecha de salida no puede ser anterior a la actual")
        self.libros.append(libro)
        self._guardar_libros()

    def modificar_libro(self, codigo: str, **kwargs):
        for libro in self.libros:
            if libro.codigo == codigo:
                for key, value in kwargs.items():
                    if hasattr(libro, key):
                        setattr(libro, key, value)
                self._guardar_libros()
                return
        raise ValueError("Libro no encontrado")

    def eliminar_libro(self, codigo: str):
        self.libros = [l for l in self.libros if l.codigo != codigo]
        self._guardar_libros()

    def consultar_libros(self, titulo: Optional[str] = None, autor: Optional[str] = None, editorial: Optional[str] = None) -> List[Libro]:
        return [l for l in self.libros if
                (titulo is None or titulo.lower() in l.titulo.lower()) and
                (autor is None or autor.lower() in l.autor.lower()) and
                (editorial is None or editorial.lower() in l.editorial.lower())]

    def mostrar_todos(self) -> List[Libro]:
        return [l for l in self.libros if l.cantidad > 0]

    def reducir_cantidad(self, codigo: str, cantidad: int):
        for libro in self.libros:
            if libro.codigo == codigo:
                if libro.cantidad < cantidad:
                    raise ValueError("Stock insuficiente")
                libro.cantidad -= cantidad
                self._guardar_libros()
                return
        raise ValueError("Libro no encontrado")

    def aumentar_cantidad(self, codigo: str, cantidad: int):
        for libro in self.libros:
            if libro.codigo == codigo:
                libro.cantidad += cantidad
                self._guardar_libros()
                return
        raise ValueError("Libro no encontrado")