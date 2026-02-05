from models.usuario import Usuario
from persistence.json_functions import JsonFunctions
from exceptions import usuarioDuplicado, usuarioInexistente, camposUsuarioError
class usuario_service:
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
        if usuario.numSocio in [diccionarioUsuario.get("numSocio") for diccionarioUsuario in self.usuariosJson]:
            raise usuarioDuplicado(f"Ya existe un usuario con el numSocio {usuario.numSocio}")
        usuario.idUsuario=int(self.usuariosJson[-1].idUsuario)+1
        self.usuariosJson.append(self.__fromUsuarioToDict(usuario))

        self.data.save_all(self.usuariosJson)

    def __verificarUsuarioExistente(id, listaUsuario:list):
        #Evalua si existe el usuario con el id en la lista indicada y devuelve su indice en el json
        indice=""
        listaId=[usuario.get("IdUsuario") for usuario in listaUsuario]
        if id in listaId:
            indice=listaId.index(id)
        else:
            raise usuarioInexistente(f"No hay ningun usuario con la id {id}")
        return indice
    
    def __fromUsuarioToDict(usuario:Usuario)->dict:
        diccionarioUsuario={
                "IdUsuario":usuario.idUsuario,

                "Nombre":usuario.nombre,

                "Apellido":usuario.apellido,

                "TipodeUsuario":usuario.tipoUsuario,

                "Dirección":usuario.direccion,

                "Teléfono":usuario.telefono,

                "NumSocio":usuario.nu
            }
        return diccionarioUsuario
    def __fromDictToUsuario(diccionario:dict)->Usuario:
        usuario=Usuario(
                diccionario.get("IdUsuario"),

                diccionario.get("Nombre"),

                diccionario.get("Apellido"),

                diccionario.get("TipodeUsuario"),

                diccionario.get("Dirección"),

                diccionario.get("Teléfono"),

                diccionario.get("NumSocio")
            )
        return usuario
        
    def crearUsuario(self, usuarioDicc:dict):
        usuario:Usuario=self.__fromDictToUsuario(usuarioDicc)
        #validaciones de reglas de negocio(duplicadoUsuarios, nombre no vacio)
        
        if usuario.tipoUsuario not in ["administrador", "socio", "no_socio"] or usuario.nombre==None:
            raise camposUsuarioError("Campos introducidos incorrectos")
        else:
            self.__crearUsuarioData(usuario)
            
        
        
            

    def modificarUsuario(self, id, datosDicc:dict):
        indice=self.__verificarUsuarioExistente(id, self.usuariosJson)
        usuario:Usuario=self.__fromDictToUsuario(datosDicc)
        #validaciones de reglas de negocio
        if usuario.tipoUsuario in ["administrador", "socio", "no_socio"] and usuario.nombre!=None:
            self.__modificarUsuarioData(indice, usuario)
        else:
            raise camposUsuarioError("Campos introducidos incorrectos")
            

    def eliminarUsuario(self, id):
        indice=self.__verificarUsuarioExistente(id, self.usuariosJson)
        #validaciones de reglas de negocio
        self.__eliminarUsuarioData(indice)
        
            

    def consultarUsuario(self, id):
        indice=self.__verificarUsuarioExistente(id, self.usuariosJson)
        return self.data.get_all[indice]
    
    def consultarUsuarios(self):
        return self.data.get_all()