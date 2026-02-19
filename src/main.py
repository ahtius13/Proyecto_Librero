"""
Punto de entrada de la API.
Aquí se crean los managers (una sola vez) y se inyectan en cada router.
"""
from fastapi import FastAPI
from src.libros import LibroManager
from src.usuarios import UsuarioManager
from src.prestamos import PrestamoManager
from src.ventas import VentaManager
from src.preventas import PreventaManager

import src.routes.libros as r_libros
import src.routes.usuarios as r_usuarios
import src.routes.prestamos as r_prestamos
import src.routes.ventas as r_ventas
import src.routes.preventas as r_preventas

app = FastAPI(title="API Librería")

# ── Instancias únicas de los managers ──────────────────────────────────
libro_manager    = LibroManager("data/libros.json")
usuario_manager  = UsuarioManager("data/usuarios.json")
prestamo_manager = PrestamoManager(libro_manager)
venta_manager    = VentaManager(libro_manager, usuario_manager)
preventa_manager = PreventaManager(libro_manager, usuario_manager)

# ── Inyección en los módulos de rutas ──────────────────────────────────
r_libros.libro_manager    = libro_manager
r_libros.usuario_manager  = usuario_manager

r_usuarios.usuario_manager = usuario_manager

r_prestamos.prestamo_manager = prestamo_manager
r_prestamos.usuario_manager  = usuario_manager

r_ventas.venta_manager   = venta_manager
r_ventas.usuario_manager = usuario_manager

r_preventas.preventa_manager = preventa_manager
r_preventas.usuario_manager  = usuario_manager

# routers 
app.include_router(r_libros.router)
app.include_router(r_usuarios.router)
app.include_router(r_prestamos.router)
app.include_router(r_ventas.router)
app.include_router(r_preventas.router)