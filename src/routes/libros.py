"""
Rutas: /libros
Permisos:
  - GET  → socio, no_socio, admin
  - POST / PUT / DELETE → solo admin
"""
from fastapi import APIRouter, Header, HTTPException, Query, Request
from src.libros import Libro, LibroManager
from src.usuarios import UsuarioManager
from src.routes._auth import get_usuario, require_admin
import datetime

router = APIRouter(prefix="/libros", tags=["libros"])

libro_manager: LibroManager = None
usuario_manager: UsuarioManager = None


# GET /libros/all  →  todos los libros con stock
@router.get("/all")
async def mostrar_todos(x_user_id: str = Header(...)):
    get_usuario(usuario_manager, x_user_id)
    libros = libro_manager.mostrar_todos()
    return [l.to_dict() for l in libros]


# GET /libros/buscar  →  búsqueda por título, autor o editorial
@router.get("/buscar")
async def buscar_libros(
    titulo: str = Query(None),
    autor: str = Query(None),
    editorial: str = Query(None),
    x_user_id: str = Header(...),
):
    get_usuario(usuario_manager, x_user_id)
    libros = libro_manager.consultar_libros(titulo=titulo, autor=autor, editorial=editorial)
    return [l.to_dict() for l in libros]


# GET /libros/{codigo}  →  un libro concreto
@router.get("/{codigo}")
async def consultar_libro(codigo: str, x_user_id: str = Header(...)):
    get_usuario(usuario_manager, x_user_id)
    libros = libro_manager.consultar_libros()
    libro = next((l for l in libros if l.codigo == codigo), None)
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return libro.to_dict()


# POST /libros/  →  registrar libro (admin)
@router.post("/")
async def registrar_libro(request: Request, x_user_id: str = Header(...)):
    usuario = get_usuario(usuario_manager, x_user_id)
    require_admin(usuario)

    body = await request.json()

    fecha_salida = None
    if body.get("fecha_salida"):
        try:
            fecha_salida = datetime.date.fromisoformat(body["fecha_salida"])
        except ValueError:
            raise HTTPException(status_code=400, detail="Formato de fecha_salida inválido (YYYY-MM-DD)")

    fecha_prestamo = None
    if body.get("fecha_prestamo"):
        try:
            fecha_prestamo = datetime.date.fromisoformat(body["fecha_prestamo"])
        except ValueError:
            raise HTTPException(status_code=400, detail="Formato de fecha_prestamo inválido (YYYY-MM-DD)")

    try:
        libro = Libro(
            titulo=body["titulo"],
            autor=body["autor"],
            codigo=body["codigo"],
            editorial=body["editorial"],
            precio=float(body["precio"]),
            cantidad=int(body.get("cantidad", 0)),
            fecha_salida=fecha_salida,
            fecha_prestamo=fecha_prestamo,
        )
        libro_manager.registrar_libro(libro)
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Campo obligatorio faltante: {e}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"mensaje": "Libro registrado correctamente", "codigo": libro.codigo}


# PUT /libros/{codigo}  →  modificar libro (admin)
@router.put("/{codigo}")
async def modificar_libro(codigo: str, request: Request, x_user_id: str = Header(...)):
    usuario = get_usuario(usuario_manager, x_user_id)
    require_admin(usuario)

    body = await request.json()

    for campo_fecha in ("fecha_salida", "fecha_prestamo"):
        if campo_fecha in body and body[campo_fecha] is not None:
            try:
                body[campo_fecha] = datetime.date.fromisoformat(body[campo_fecha])
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Formato de {campo_fecha} inválido (YYYY-MM-DD)")

    try:
        libro_manager.modificar_libro(codigo, **body)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return {"mensaje": "Libro modificado correctamente"}


# DELETE /libros/{codigo}  →  eliminar libro (admin)
@router.delete("/{codigo}")
async def eliminar_libro(codigo: str, x_user_id: str = Header(...)):
    usuario = get_usuario(usuario_manager, x_user_id)
    require_admin(usuario)

    try:
        libro_manager.eliminar_libro(codigo)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return {"mensaje": "Libro eliminado correctamente"}