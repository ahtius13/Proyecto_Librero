from fastapi import Header, HTTPException
from src.usuarios import UsuarioManager


def get_usuario(usuario_manager: UsuarioManager, x_user_id: str = Header(...)):
    """
    Recupera el usuario a partir del header X-User-Id.
    Lanza 401 si el header no viene o el usuario no existe.
    """
    if not x_user_id:
        raise HTTPException(status_code=401, detail="Header X-User-Id requerido")
    try:
        return usuario_manager.consultar_usuario(x_user_id)
    except ValueError:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")


def require_admin(usuario):
    if usuario.tipo != "admin":
        raise HTTPException(status_code=401, detail="Acción reservada al administrador")


def require_socio_o_admin(usuario):
    if usuario.tipo not in ("socio", "admin"):
        raise HTTPException(status_code=401, detail="Acción reservada a socios o administrador")