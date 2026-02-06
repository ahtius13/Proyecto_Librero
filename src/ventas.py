import datetime
from src.libros import LibroManager
from src.usuarios import UsuarioManager

class VentaManager:
    DESCUENTO_SOCIO = 0.10  # 10%

    def __init__(self, libro_manager: LibroManager, usuario_manager: UsuarioManager):
        self.libro_manager = libro_manager
        self.usuario_manager = usuario_manager

    def registrar_venta(self, numero_socio: str, codigo_libro: str, cantidad: int):
        usuario = self.usuario_manager.consultar_usuario(numero_socio)
        libro = next((l for l in self.libro_manager.libros if l.codigo == codigo_libro), None)
        if not libro:
            raise ValueError("Libro no encontrado")
        precio = libro.precio
        if usuario.tipo == "socio":
            precio *= (1 - self.DESCUENTO_SOCIO)
        precio_total = precio * cantidad
        libro.ventas.append({
            "numero_socio": numero_socio,
            "cantidad": cantidad,
            "fecha": datetime.date.today(),
            "precio_pagado": precio_total
        })
        self.libro_manager.reducir_cantidad(codigo_libro, cantidad)
        self.libro_manager._guardar_libros()

    def devolver_venta(self, numero_socio: str, codigo_libro: str, cantidad: int):
        libro = next((l for l in self.libro_manager.libros if l.codigo == codigo_libro), None)
        if not libro:
            raise ValueError("Libro no encontrado")
        remaining = cantidad
        new_ventas = []
        for v in libro.ventas:
            if remaining > 0 and v["numero_socio"] == numero_socio and v["cantidad"] > 0:
                devolver_aqui = min(remaining, v["cantidad"])
                v["cantidad"] -= devolver_aqui
                remaining -= devolver_aqui
                self.libro_manager.aumentar_cantidad(codigo_libro, devolver_aqui)
            if v["cantidad"] > 0:
                new_ventas.append(v)
        libro.ventas = new_ventas
        if remaining > 0:
            raise ValueError("Venta no encontrada o cantidad insuficiente")
        self.libro_manager._guardar_libros()