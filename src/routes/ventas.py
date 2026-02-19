"""
Rutas: /ventas  y  /devolucion/compra
Permisos:
  - POST /ventas/{codigo}          → todos (descuento automático si es socio)
  - POST /devolucion/compra/{cod}  → todos (solo su propia compra)
"""
from fastapi import APIRouter, Header, HTTPException, Request
from src.ventas import VentaManager
from src.usuarios import UsuarioManager
from src.routes._auth import get_usuario

router = APIRouter(tags=["ventas"])

venta_manager: VentaManager = None
usuario_manager: UsuarioManager = None


# POST /ventas/{codigo_libro}  →  comprar libro
@router.post("/ventas/{codigo_libro}")
async def comprar_libro(codigo_libro: str, request: Request, x_user_id: str = Header(...)):
    usuario = get_usuario(usuario_manager, x_user_id)

    body = await request.json()

    try:
        cantidad = int(body.get("cantidad", 1))
        venta_manager.registrar_venta(
            numero_socio=usuario.numero_socio,
            codigo_libro=codigo_libro,
            cantidad=cantidad,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "mensaje": "Compra registrada correctamente",
        "descuento_aplicado": usuario.tipo == "socio",
    }


# POST /devolucion/compra/{codigo_libro}  →  devolver libro comprado
@router.post("/devolucion/compra/{codigo_libro}")
async def devolver_compra(codigo_libro: str, request: Request, x_user_id: str = Header(...)):
    usuario = get_usuario(usuario_manager, x_user_id)

    body = await request.json()

    try:
        cantidad = int(body.get("cantidad", 1))
        venta_manager.devolver_venta(
            numero_socio=usuario.numero_socio,
            codigo_libro=codigo_libro,
            cantidad=cantidad,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"mensaje": "Devolución registrada correctamente"}