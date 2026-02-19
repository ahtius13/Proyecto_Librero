"""
Rutas: /prestamos  y  /devolucion/prestamos
Permisos: solo admin
"""
from fastapi import APIRouter, Header, HTTPException, Request
from src.prestamos import PrestamoManager
from src.usuarios import UsuarioManager
from src.routes._auth import get_usuario, require_admin

router = APIRouter(tags=["prestamos"])

prestamo_manager: PrestamoManager = None
usuario_manager: UsuarioManager = None


# POST /prestamos/  →  registrar préstamo de editorial
@router.post("/prestamos/")
async def registrar_prestamo(request: Request, x_user_id: str = Header(...)):
    usuario = get_usuario(usuario_manager, x_user_id)
    require_admin(usuario)

    body = await request.json()

    try:
        prestamo_manager.registrar_prestamo(
            codigo_libro=body["codigo_libro"],
            cantidad=int(body["cantidad"]),
            duracion_dias=int(body["duracion_dias"]),
        )
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Campo obligatorio faltante: {e}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"mensaje": "Préstamo registrado correctamente"}


# GET /prestamos/  →  préstamos activos
@router.get("/prestamos/")
async def mostrar_activos(codigo_libro: str = None, x_user_id: str = Header(...)):
    usuario = get_usuario(usuario_manager, x_user_id)
    require_admin(usuario)

    prestamos = prestamo_manager.mostrar_activos(codigo_libro=codigo_libro)
    return [
        {
            "cantidad": p["cantidad"],
            "fecha_prestamo": p["fecha_prestamo"].isoformat(),
            "fecha_vencimiento": p["fecha_vencimiento"].isoformat(),
        }
        for p in prestamos
    ]


# GET /prestamos/vencidos  →  préstamos que superaron su plazo
@router.get("/prestamos/vencidos")
async def mostrar_vencidos(codigo_libro: str = None, x_user_id: str = Header(...)):
    usuario = get_usuario(usuario_manager, x_user_id)
    require_admin(usuario)

    prestamos = prestamo_manager.detectar_vencidos(codigo_libro=codigo_libro)
    return [
        {
            "cantidad": p["cantidad"],
            "fecha_prestamo": p["fecha_prestamo"].isoformat(),
            "fecha_vencimiento": p["fecha_vencimiento"].isoformat(),
        }
        for p in prestamos
    ]


# POST /devolucion/prestamos/{codigo_libro}  →  devolver libros a editorial
@router.post("/devolucion/prestamos/{codigo_libro}")
async def devolver_prestamo(codigo_libro: str, request: Request, x_user_id: str = Header(...)):
    usuario = get_usuario(usuario_manager, x_user_id)
    require_admin(usuario)

    body = await request.json()

    try:
        prestamo_manager.devolver_prestamo(
            codigo_libro=codigo_libro,
            cantidad=int(body["cantidad"]),
        )
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Campo obligatorio faltante: {e}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"mensaje": "Devolución a editorial registrada correctamente"}