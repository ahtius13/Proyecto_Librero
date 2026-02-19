"""
Rutas: /usuarios
Permisos:
  - GET perfil propio  → cualquier usuario autenticado
  - GET todos / POST / PUT / DELETE → solo admin
"""
from fastapi import APIRouter, Header, HTTPException, Request
from src.usuarios import Usuario, UsuarioManager
from src.routes._auth import get_usuario, require_admin

router = APIRouter(prefix="/usuarios", tags=["usuarios"])

usuario_manager: UsuarioManager = None


# GET /usuarios/all  →  lista completa (admin)
@router.get("/all")
async def mostrar_todos(x_user_id: str = Header(...)):
    usuario = get_usuario(usuario_manager, x_user_id)
    require_admin(usuario)
    return [u.to_dict() for u in usuario_manager.mostrar_todos()]


# GET /usuarios/{numero_socio}  →  perfil propio o cualquiera (admin)
@router.get("/{numero_socio}")
async def consultar_usuario(numero_socio: str, x_user_id: str = Header(...)):
    usuario = get_usuario(usuario_manager, x_user_id)

    if usuario.tipo != "admin" and usuario.numero_socio != numero_socio:
        raise HTTPException(status_code=401, detail="Solo puedes consultar tu propio perfil")

    try:
        target = usuario_manager.consultar_usuario(numero_socio)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return target.to_dict()


# POST /usuarios/  →  añadir usuario (admin)
@router.post("/")
async def anadir_usuario(request: Request, x_user_id: str = Header(...)):
    usuario = get_usuario(usuario_manager, x_user_id)
    require_admin(usuario)

    body = await request.json()

    try:
        nuevo = Usuario(
            nombre=body["nombre"],
            apellido=body["apellido"],
            numero_socio=body["numero_socio"],
            tipo=body["tipo"],
            direccion=body["direccion"],
            telefono=body["telefono"],
        )
        usuario_manager.anadir_usuario(nuevo)
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Campo obligatorio faltante: {e}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"mensaje": "Usuario añadido correctamente", "numero_socio": nuevo.numero_socio}


# PUT /usuarios/{numero_socio}  →  modificar usuario (admin)
@router.put("/{numero_socio}")
async def modificar_usuario(numero_socio: str, request: Request, x_user_id: str = Header(...)):
    usuario = get_usuario(usuario_manager, x_user_id)
    require_admin(usuario)

    body = await request.json()

    try:
        usuario_manager.modificar_usuario(numero_socio, **body)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return {"mensaje": "Usuario modificado correctamente"}


# DELETE /usuarios/{numero_socio}  →  eliminar usuario (admin)
@router.delete("/{numero_socio}")
async def eliminar_usuario(numero_socio: str, x_user_id: str = Header(...)):
    usuario = get_usuario(usuario_manager, x_user_id)
    require_admin(usuario)

    try:
        usuario_manager.eliminar_usuario(numero_socio)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return {"mensaje": "Usuario eliminado correctamente"}