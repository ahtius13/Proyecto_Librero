"""
Rutas: /preventas
Permisos: solo socios (y admin)
"""
from fastapi import APIRouter, Header, HTTPException, Request
from src.preventas import PreventaManager
from src.usuarios import UsuarioManager
from src.routes._auth import get_usuario, require_socio_o_admin

router = APIRouter(prefix="/preventas", tags=["preventas"])

preventa_manager: PreventaManager = None
usuario_manager: UsuarioManager = None


# POST /preventas/{codigo_libro}  →  reservar preventa
@router.post("/{codigo_libro}")
async def reservar_preventa(codigo_libro: str, request: Request, x_user_id: str = Header(...)):
    usuario = get_usuario(usuario_manager, x_user_id)
    require_socio_o_admin(usuario)

    body = await request.json()

    try:
        cantidad = int(body.get("cantidad", 1))
        preventa_manager.registrar_preventa(
            numero_socio=usuario.numero_socio,
            codigo_libro=codigo_libro,
            cantidad=cantidad,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "mensaje": "Preventa registrada correctamente",
        "codigo_libro": codigo_libro,
        "cantidad": cantidad,
    }