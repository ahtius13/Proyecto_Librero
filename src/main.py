# API REST del sistema Librero. endpoints para gestionar. _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

from fastapi import FastAPI, HTTPException

from src.usuarios import UsuarioManager, Usuario
from src.libros import LibroManager, Libro
from src.ventas import VentaManager
from src.prestamos import PrestamoManager
from src.preventas import PreventaManager

import datetime

app = FastAPI(title="API Librero")

# Crea los managers que conectan con la lógica del sistema. _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

libro_manager = LibroManager()
usuario_manager = UsuarioManager()
venta_manager = VentaManager(libro_manager, usuario_manager)
prestamo_manager = PrestamoManager(libro_manager)
preventa_manager = PreventaManager(libro_manager, usuario_manager)

"""

# USUARIOS _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _  _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

@app.post("/usuarios/")
def crear_usuario(data: dict):

    try:
        usuario = Usuario(
        data["nombre"],
        data["apellido"],
        data["numero_socio"],
        data["tipo"],
        data["direccion"],
        data["telefono"]
)
        usuario_manager.anadir_usuario(usuario)
        return {"mensaje": "Usuario creado"}
    except ValueError as e:
     raise HTTPException(status_code=400, detail=str(e))

@app.get("/usuarios/")
def listar_usuarios():
    return [u.to_dict() for u in usuario_manager.mostrar_todos()]

@app.get("/usuarios/{numero_socio}")
def obtener_usuario(numero_socio: str):

    try:
        usuario = usuario_manager.consultar_usuario(numero_socio)
        return usuario.to_dict()
    except ValueError:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

@app.put("/usuarios/{numero_socio}")
def modificar_usuario(numero_socio: str, datos: dict):
    try:
        usuario_manager.modificar_usuario(numero_socio, **datos)
        return {"mensaje": "Usuario modificado"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.delete("/usuarios/{numero_socio}")
def eliminar_usuario(numero_socio: str):

    try:

        usuario_manager.eliminar_usuario(numero_socio)

        return {"mensaje": "Usuario eliminado"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
"""
# LIBROS _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _  _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

@app.post("/libros/")
def crear_libro(data: dict):

    try:
    
        fecha = None
        if data.get("fecha_salida"):
            fecha = datetime.date.fromisoformat(data["fecha_salida"])

        libro = Libro(
        data["titulo"],
        data["autor"],
        data["codigo"],
        data["editorial"],
        data["precio"],
        data.get("cantidad", 0),
        fecha
    )

        libro_manager.registrar_libro(libro)
        return {"mensaje": "Libro creado"}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/libros/")
def listar_libros():
    libros = libro_manager.mostrar_todos()
    return [l.to_dict() for l in libros]

@app.get("/libros/buscar")
def buscar_libros(titulo: str = None, autor: str = None, editorial: str = None):
    libros = libro_manager.consultar_libros(titulo, autor, editorial)
    return [l.to_dict() for l in libros]


@app.delete("/libros/{codigo}")
def eliminar_libro(codigo: str):

    try:

        libro_manager.eliminar_libro(codigo)
        return {"mensaje": "Libro eliminado"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# VENTAS _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _  _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

@app.post("/ventas/")
def registrar_venta(numero_socio: str, codigo_libro: str, cantidad: int):

    try:

        venta_manager.registrar_venta(numero_socio, codigo_libro, cantidad)
        return {"mensaje": "Venta registrada"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/ventas/devolver")
def devolver_venta(numero_socio: str, codigo_libro: str, cantidad: int):

    try:

        venta_manager.devolver_venta(numero_socio, codigo_libro, cantidad)
        return {"mensaje": "Venta devuelta"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# PRESTAMOS _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _  _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

@app.post("/prestamos/")
def registrar_prestamo(codigo_libro: str, cantidad: int, duracion_dias: int):

    try:
        prestamo_manager.registrar_prestamo(codigo_libro, cantidad, duracion_dias)
        return {"mensaje": "Prestamo registrado"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/prestamos/")
def prestamos_activos():
    return prestamo_manager.mostrar_activos()

@app.get("/prestamos/vencidos")
def prestamos_vencidos():
    return prestamo_manager.detectar_vencidos()

@app.post("/prestamos/devolver")
def devolver_prestamo(codigo_libro: str, cantidad: int):
    try:
        prestamo_manager.devolver_prestamo(codigo_libro, cantidad)
        return {"mensaje": "Prestamo devuelto"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _  _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 