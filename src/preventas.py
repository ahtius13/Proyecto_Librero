import datetime
from src.libros import LibroManager
from src.usuarios import UsuarioManager

class PreventaManager:
    def __init__(self, libro_manager: LibroManager, usuario_manager: UsuarioManager):
        self.libro_manager = libro_manager
        self.usuario_manager = usuario_manager

    def registrar_preventa(self, numero_socio: str, codigo_libro: str, cantidad: int):
        usuario = self.usuario_manager.consultar_usuario(numero_socio)
        if usuario.tipo != "socio":
            raise ValueError("Solo socios pueden hacer preventas")
        libro = next((l for l in self.libro_manager.libros if l.codigo == codigo_libro), None)
        if not libro:
            raise ValueError("Libro no encontrado")
        if not libro.fecha_salida or libro.fecha_salida < datetime.date.today() + datetime.timedelta(days=30):
            raise ValueError("Solo libros con fecha de salida al menos 1 mes en el futuro")
        if libro.cantidad < cantidad:
            raise ValueError("Cantidad disponible insuficiente para preventa")
        libro.preventas.append({
            "numero_socio": numero_socio,
            "cantidad": cantidad
        })
        self.libro_manager.reducir_cantidad(codigo_libro, cantidad)  # Reservar stock
        self.libro_manager._guardar_libros()