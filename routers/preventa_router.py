from fastapi import FastAPI, HTTPException, APIRouter, status
from schemas.preventa_model import Preventa_model
from src.usuarios import UsuarioManager, Usuario
from src.libros import Libro, LibroManager
from src.preventas import PreventaManager
from exceptions.recursoInexistenteException import RecursoInexistenteException
router=APIRouter(prefix="/preventa", tags=["USUARIO"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def registrarVenta(preventa_model:Preventa_model):
    numUsuario=preventa_model.numero_socio
    numLibro=preventa_model.ISBN
    cantidad=preventa_model.cantidad
    usuario_manager=UsuarioManager()
    libro_manager=LibroManager()
    #verificando que esxista
    try:
        usuario_manager.consultar_usuario(numUsuario)
    except ValueError:
        raise RecursoInexistenteException("usuario", numUsuario)

    if not any(iter(libro.codigo==numLibro for libro in libro_manager.mostrar_todos())):
        raise RecursoInexistenteException("libro", numLibro)
    
    preventa_manager=PreventaManager(libro_manager, usuario_manager)

    try:
        preventa_manager.registrar_preventa(numUsuario,numLibro, cantidad)
    except  ValueError as error:
        raise HTTPException(400, str(error))
