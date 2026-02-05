import datetime
from typing import List
from src.libros import LibroManager

class PrestamoManager:
    def __init__(self, libro_manager: LibroManager):
        self.libro_manager = libro_manager

    def registrar_prestamo(self, codigo_libro: str, cantidad: int, duracion_dias: int):
        libro = next((l for l in self.libro_manager.libros if l.codigo == codigo_libro), None)
        if not libro:
            raise ValueError("Libro no encontrado")
        fecha_prestamo = datetime.date.today()
        fecha_vencimiento = fecha_prestamo + datetime.timedelta(days=duracion_dias)
        libro.prestamos.append({
            "cantidad": cantidad,
            "fecha_prestamo": fecha_prestamo,
            "fecha_vencimiento": fecha_vencimiento
        })
        self.libro_manager.aumentar_cantidad(codigo_libro, cantidad)
        self.libro_manager._guardar_libros()

    def mostrar_activos(self, codigo_libro: str = None) -> List[dict]:
        prestamos = []
        for libro in self.libro_manager.libros:
            if codigo_libro is None or libro.codigo == codigo_libro:
                for p in libro.prestamos:
                    if p["fecha_vencimiento"] >= datetime.date.today():
                        prestamos.append(p)
        return prestamos

    def detectar_vencidos(self, codigo_libro: str = None) -> List[dict]:
        prestamos = []
        for libro in self.libro_manager.libros:
            if codigo_libro is None or libro.codigo == codigo_libro:
                for p in libro.prestamos:
                    if p["fecha_vencimiento"] < datetime.date.today():
                        prestamos.append(p)
        return prestamos

    def devolver_prestamo(self, codigo_libro: str, cantidad: int):
        libro = next((l for l in self.libro_manager.libros if l.codigo == codigo_libro), None)
        if not libro:
            raise ValueError("Libro no encontrado")
        remaining = cantidad
        new_prestamos = []
        for p in libro.prestamos:
            if remaining > 0 and p["cantidad"] > 0:
                devolver_aqui = min(remaining, p["cantidad"])
                p["cantidad"] -= devolver_aqui
                remaining -= devolver_aqui
                self.libro_manager.reducir_cantidad(codigo_libro, devolver_aqui)
            if p["cantidad"] > 0:
                new_prestamos.append(p)
        libro.prestamos = new_prestamos
        if remaining > 0:
            raise ValueError("Préstamo no encontrado o cantidad insuficiente")
        self.libro_manager._guardar_libros()