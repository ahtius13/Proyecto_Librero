from src.models.usuario import Usuario
from src.persistence.json_functions import JsonFunctions
from src.exceptions.usuarioDuplicado import UsuarioDuplicado
from src.exceptions.usuarioInexistente import Usuarioinexistente
from src.exceptions.camposUsuarioError import CamposUsuarioError
class Usuario_service:
    def __init__(self):
        self.data =JsonFunctions("data/usuarios.json")
        self.usuariosJson: list=self.data.get_all()

    def __modificarUsuarioData(self, indice, usuario:Usuario):
        self.usuariosJson[indice]=self.__fromUsuarioToDict(usuario)

        self.data.save_all(self.usuariosJson)

    def __eliminarUsuarioData(self, indice):
        self.usuariosJson.pop(indice)

        self.data.save_all(self.usuariosJson)

    def __crearUsuarioData(self, usuario:Usuario):
        if usuario.numSocio in [diccionarioUsuario.get("NumSocio") for diccionarioUsuario in self.usuariosJson]:
            raise UsuarioDuplicado(f"Ya existe un usuario con el numSocio {usuario.numSocio}")
        #idUsuario
        
        if len(self.usuariosJson):
            usuario.idUsuario=int(max([diccionarioUsuario.get("IdUsuario") for diccionarioUsuario in self.usuariosJson]))+1
        else:
            usuario.idUsuario=1

        self.usuariosJson.append(self.__fromUsuarioToDict(usuario))

        self.data.save_all(self.usuariosJson)

    def __verificarUsuarioExistente(self, id, listaUsuario:list):
        #Evalua si existe el usuario con el id en la lista indicada y devuelve su indice en el json
        indice=""
        listaId=[usuario.get("IdUsuario") for usuario in listaUsuario]
        if id in listaId:
            indice=listaId.index(id)
        else:
            raise Usuarioinexistente(f"No hay ningun usuario con la id {id}")
        return indice
    
    
    def __fromUsuarioToDict(self, usuario:Usuario)->dict:
        diccionarioUsuario={
                "IdUsuario":usuario.idUsuario,

                "Nombre":usuario.nombre,

                "Apellido":usuario.apellido,

                "TipodeUsuario":usuario.tipoUsuario,

                "Dirección":usuario.direccion,

                "Teléfono":usuario.telefono,

                "NumSocio":usuario.numSocio
            }
        return diccionarioUsuario
    
    def __fromDictToUsuario(self, diccionario:dict)->Usuario:
        usuario=Usuario(
                diccionario.get("IdUsuario"),

                diccionario.get("NumSocio"),

                diccionario.get("Nombre"),

                diccionario.get("Apellido"),

                diccionario.get("TipodeUsuario"),

                diccionario.get("Dirección"),

                diccionario.get("Teléfono")
            )
        return usuario
        
        #crear usuario imponiendo su id
    def crearUsuario(self, usuarioDicc:dict):
        usuario:Usuario=self.__fromDictToUsuario(usuarioDicc)
        #validaciones de reglas de negocio(duplicadoUsuarios, nombre no vacio)
        
        if usuario.tipoUsuario not in ["administrador", "socio", "no_socio"] or usuario.nombre==None:
            raise CamposUsuarioError("Campos introducidos incorrectos")
        else:
            self.__crearUsuarioData(usuario)
            
        
        
            

    def modificarUsuario(self, id, datosDicc:dict):
        indice=self.__verificarUsuarioExistente(id, self.usuariosJson)
        usuario:Usuario=self.__fromDictToUsuario(datosDicc)
        #validaciones de reglas de negocio
        if usuario.tipoUsuario in ["administrador", "socio", "no_socio"] and usuario.nombre!=None:
            usuario.idUsuario=id
            self.__modificarUsuarioData(indice, usuario)
        else:
            raise CamposUsuarioError("Campos introducidos incorrectos")
            

    def eliminarUsuario(self, id):
        indice=self.__verificarUsuarioExistente(id, self.usuariosJson)
        #validaciones de reglas de negocio
        self.__eliminarUsuarioData(indice)
        
            

    def consultarUsuario(self, id):
        indice=self.__verificarUsuarioExistente(id, self.usuariosJson)
        return self.data.get_all()[indice]
    
    def consultarUsuarios(self):
        return self.data.get_all()