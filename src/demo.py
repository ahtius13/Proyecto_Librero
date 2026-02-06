"""
Demo del sistema de gestión de librería.
"""

from src.libros import LibroManager, Libro
from src.usuarios import UsuarioManager, Usuario
from src.prestamos import PrestamoManager
from src.ventas import VentaManager
from src.preventas import PreventaManager
import datetime


def mostrar_libros(manager, titulo="Libros disponibles"):
    print(f"\n=== {titulo} ===")
    disponibles = manager.mostrar_todos()
    if not disponibles:
        print("No hay libros disponibles.")
        return
    for libro in disponibles:
        print(f"- {libro.codigo} | {libro.titulo} ({libro.autor}) | "
              f"Stock: {libro.cantidad} | Precio: {libro.precio:.2f} €")


def mostrar_usuarios(manager):
    print("\n=== Usuarios registrados ===")
    usuarios = manager.mostrar_todos()
    if not usuarios:
        print("No hay usuarios registrados.")
        return
    for u in usuarios:
        print(f"- {u.numero_socio} | {u.nombre} {u.apellido} | Tipo: {u.tipo}")


def main():
    print("=== INICIANDO DEMOSTRACIÓN DEL SISTEMA DE LIBRERÍA ===\n")

    # Inicializamos los managers
    libro_manager = LibroManager()
    usuario_manager = UsuarioManager()
    prestamo_manager = PrestamoManager(libro_manager)
    venta_manager = VentaManager(libro_manager, usuario_manager)
    preventa_manager = PreventaManager(libro_manager, usuario_manager)

    # 1. Registrar algunos libros
    print("1. Registrando libros de ejemplo...")
    libros_ejemplo = [
        Libro("Cien años de soledad", "Gabriel García Márquez", "ISBN001", "Penguin", 18.50, cantidad=10,
              fecha_salida=datetime.date(2025, 6, 1)),
        Libro("1984", "George Orwell", "ISBN002", "Planeta", 12.99, cantidad=5),
        Libro("El principito", "Antoine de Saint-Exupéry", "ISBN003", "Salamandra", 9.75, cantidad=3,
              fecha_salida=datetime.date(2026, 3, 15)),
    ]

    for libro in libros_ejemplo:
        try:
            libro_manager.registrar_libro(libro)
            print(f"Registrado: {libro.titulo} ({libro.codigo})")
        except ValueError as e:
            print(f"Error al registrar {libro.titulo}: {e}")

    mostrar_libros(libro_manager, "Inventario inicial")

    # 2. Registrar usuarios
    print("\n2. Registrando usuarios...")
    usuarios_ejemplo = [
        Usuario("Ana", "Martínez", "SOC001", "socio", "Calle Falsa 123", "555-1234"),
        Usuario("Carlos", "Gómez", "SOC002", "socio", "Av. Siempre Viva 456", "555-5678"),
        Usuario("Admin", "Principal", "ADMIN01", "admin", "Oficina Central", "555-0000"),
        Usuario("Pepe", "López", "NSOC001", "no_socio", "Calle Real 789", "555-9999"),
    ]

    for usuario in usuarios_ejemplo:
        try:
            usuario_manager.anadir_usuario(usuario)
            print(f"Registrado: {usuario.numero_socio} - {usuario.nombre} ({usuario.tipo})")
        except ValueError as e:
            print(f"Error: {e}")

    mostrar_usuarios(usuario_manager)

    # 3. Registrar un préstamo
    print("\n3. Registrando un préstamo de editorial...")
    try:
        prestamo_manager.registrar_prestamo("ISBN001", 8, duracion_dias=60)
        print("Préstamo registrado: 8 unidades de 'Cien años de soledad'")
    except ValueError as e:
        print(f"Error en préstamo: {e}")

    mostrar_libros(libro_manager, "Stock después del préstamo")

    # 4. Venta a un socio (con descuento)
    print("\n4. Realizando una venta a socio (debería aplicar 10% descuento)...")
    try:
        venta_manager.registrar_venta("SOC001", "ISBN002", 2)
        print("Venta registrada: 2 unidades de '1984' a SOC001 (socio)")
    except ValueError as e:
        print(f"Error en venta: {e}")

    mostrar_libros(libro_manager, "Stock después de la venta")

    # 5. Preventa (solo socios, libro con fecha futura)
    print("\n5. Intentando preventa (solo socios y libros con salida > 30 días)...")
    try:
        preventa_manager.registrar_preventa("SOC002", "ISBN003", 2)
        print("Preventa registrada: 2 unidades de 'El principito' para SOC002")
    except ValueError as e:
        print(f"Error en preventa: {e}")

    # Intentamos preventa con no-socio → debería fallar
    try:
        preventa_manager.registrar_preventa("NSOC001", "ISBN003", 1)
        print("Esto NO debería haber funcionado")
    except ValueError as e:
        print(f"Correcto: Preventa rechazada para no socio → {e}")

    mostrar_libros(libro_manager, "Stock después de preventa")

    # 6. Devolución de préstamo
    print("\n6. Devolviendo parte del préstamo...")
    try:
        prestamo_manager.devolver_prestamo("ISBN001", 3)
        print("Devolución exitosa: 3 unidades devueltas")
    except ValueError as e:
        print(f"Error en devolución: {e}")

    mostrar_libros(libro_manager, "Stock después de devolución")

    print("\n=== DEMOSTRACIÓN FINALIZADA ===\n")
    print("Puedes inspeccionar los archivos data/libros.json y data/usuarios.json")
    print("para ver cómo se han guardado todos los datos.\n")


if __name__ == "__main__":
    main()