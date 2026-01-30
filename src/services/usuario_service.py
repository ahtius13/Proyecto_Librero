from models.usuario import Usuario
from persistence.json_functions import JsonFunctions
from exceptions import usuarioDuplicado, usuarioInexistente
class usuario_service:
    def __init__(self):
        self.data =JsonFunctions("data/usuarios.json")
        self.usuariosJson: list=self.data.get_all()

    def __verificarUsuarioExistente(id, listaUsuario:list):
        #Evalua si existe el usuario en la lista indicada
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

                "Teléfono":usuario.telefono
            }
        return diccionarioUsuario
        
    def crearUsuario(self, usuario:Usuario):
        
        if usuario.idUsuario in [diccionarioUsuario.get("IdUsuario") for diccionarioUsuario in self.usuariosJson]:
            raise usuarioDuplicado("Ya existe un usuario")
        else:
            self.usuariosJson.append(self.__fromUsuarioToDict(usuario))

            self.data.save_all(self.usuariosJson)
            

    def modificarUsuario(self, usuario:Usuario):
        indice=self.__verificarUsuarioExistente(usuario.idUsuario, self.usuariosJson)

        self.usuariosJson[indice]=self.__fromUsuarioToDict(usuario)

        self.data.save_all(self.usuariosJson)
        

    def eliminarUsuario(self, id):
        indice=self.__verificarUsuarioExistente(id, self.usuariosJson)

        self.usuariosJson.pop(indice)

        self.data.save_all(self.usuariosJson)
            

    def consultarUsuario(self, id):
        pass
    
    def consultarUsuarios(self):
        pass