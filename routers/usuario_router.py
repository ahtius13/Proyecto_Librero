from fastapi import APIRouter, status, HTTPException
from schemas. usuario_model import Usuario_model
from src.usuarios import Usuario, UsuarioManager
from exceptions.recursoYaExistenteException import RecursoYaExistenteException
from exceptions.recursoInexistenteException import RecursoInexistenteException

router=APIRouter(prefix="/usuario", tags=["USUARIO"])

#USUARIOS

@router.post("/", status_code=status.HTTP_201_CREATED)
def crear_usuario(usuario_model:Usuario_model) :
    #crea un nuevo usuario indicado en el json
    usuario_manager=UsuarioManager()
    usuario=Usuario(usuario_model.nombre, usuario_model.apellido,usuario_model.numero_socio, usuario_model.tipo, usuario_model.direccion, usuario_model.telefono)
    try:
        #Comprobando si no existe con try
        usuario_manager.anadir_usuario(usuario)

        return {"message":f"el usuario con identificador {usuario.numero_socio} ha sido creado"}
    except ValueError():
        raise RecursoYaExistenteException("usuario",usuario.numero_socio)
    

@router.get("/", status_code=status.HTTP_200_OK)
def ver_usuarios() :
    #devuelve todos los usuarios guardados.
    usuario_manager=UsuarioManager()
    listaUsuariosJSON=[usuario.to_dict() for usuario in usuario_manager.mostrar_todos()]
    return listaUsuariosJSON

@router.get("/{numSocio}", status_code=status.HTTP_200_OK)
def ver_usuario(numSocio) :
    #ver informacion sobre usuario con el numSocio indicado.
    usuario_manager=UsuarioManager()
    try:
        #Comprobando si existe con try
        usuario=usuario_manager.consultar_usuario(numSocio)

        return usuario.to_dict()
    except ValueError:
        raise RecursoInexistenteException("usuario", numSocio)

@router.put("/{numSocio}", status_code=status.HTTP_200_OK)
def modificar_usuario(numSocio, usuario_model:Usuario_model) :
    #modifica usuario con el numsocio indicado con el contenido indicado en el JSON
    usuario_manager=UsuarioManager()
    try:
        #Comprobando si existe con try
        usuario_manager.consultar_usuario(numSocio)

        if numSocio != usuario_model.numero_socio:
            raise HTTPException(400, "no se puede cambiar el numero de socio de un usuario")
        usuario_manager.modificar_usuario(numSocio, usuario_model.nombre, usuario_model.apellido,usuario_model.numero_socio, usuario_model.tipo, usuario_model.direccion, usuario_model.telefono)
    except ValueError:
        raise RecursoInexistenteException("usuario", numSocio)
    
@router.delete("/{numSocio}", status_code=status.HTTP_200_OK)
def eliminar_usuario(numSocio) :
    #elimina usuario con el numSocio indicado.
    usuario_manager=UsuarioManager()
    
    usuario_manager=UsuarioManager()
    try:
        #Comprobando si existe con try
        usuario_manager.consultar_usuario(numSocio)

        usuario_manager.eliminar_usuario()
    except ValueError:
        raise RecursoInexistenteException("usuario", numSocio)