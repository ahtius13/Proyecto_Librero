from models.usuario import Usuario
from persistence.json_functions import JsonFunctions
from exceptions import usuarioDuplicado, usuarioInexistente
class usuario_service:
    def __init__(self):
        self.data =JsonFunctions("data/usuarios.json")
        
    def crearUsuario(self, usuario:Usuario):
        UsuariosJson: list=self.data.get_all()
        
        if usuario.idUsuario in [diccionarioUsuario.get("IdUsuario") for diccionarioUsuario in UsuariosJson]:
            raise usuarioDuplicado("Ya existe un usuario")
        else:
            UsuariosJson.append({
                "IdUsuario":usuario.idUsuario,

                "Nombre":usuario.nombre,

                "Apellido":usuario.apellido,

                "TipodeUsuario":usuario.tipoUsuario,

                "Dirección":usuario.direccion,

                "Teléfono":usuario.telefono
            })
            self.data.save_all(UsuariosJson)
            

    def modificarUsuario(self, id, usuario:Usuario):
        #necesito sacar el indice que representa el diccionario dentro de la list de diccionarios que es el json, para modificarlo.
        UsuariosJson: list=self.data.get_all()
        usuarioJson= next((usuario for usuario in UsuariosJson if usuario.get("IdUsuario")==id),None)
        if not usuarioJson:
            raise usuarioInexistente(f"No hay ningun usuario con la id {id}")
        else:
            UsuariosJson[id-1]

    def eliminarUsuario(self, id):
        UsuariosJson: list=self.data.get_all()
        usuarioJson= next((usuario for usuario in UsuariosJson if usuario.get("IdUsuario")==id),None)
        if not usuarioJson:
            raise usuarioInexistente(f"No hay ningun usuario con la id {id}")
        else:
            UsuariosJson.remove(usuarioJson)
            

    def consultarUsuario(self, id):
        pass
    
    def consultarUsuarios(self):
        pass