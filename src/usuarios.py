from typing import List
from src.persistence.json_functions import JsonFunctions

class Usuario:
    def __init__(self, nombre: str, apellido: str, numero_socio: str, tipo: str, direccion: str, telefono: str):
        if tipo not in ["socio", "no_socio", "admin"]:
            raise ValueError("Tipo de usuario inválido")
        self.nombre = nombre
        self.apellido = apellido
        self.numero_socio = numero_socio
        self.tipo = tipo
        self.direccion = direccion
        self.telefono = telefono

    def to_dict(self) -> dict:
        return {
            "nombre": self.nombre,
            "apellido": self.apellido,
            "numero_socio": self.numero_socio,
            "tipo": self.tipo,
            "direccion": self.direccion,
            "telefono": self.telefono
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Usuario':
        return cls(
            data["nombre"], data["apellido"], data["numero_socio"], data["tipo"], data["direccion"], data["telefono"]
        )

class UsuarioManager:
    def __init__(self):
        self.json_handler = JsonFunctions("data/usuarios.json")
        self.usuarios = self._cargar_usuarios()

    def _cargar_usuarios(self) -> List[Usuario]:
        data = self.json_handler.get_all()
        return [Usuario.from_dict(d) for d in data]

    def _guardar_usuarios(self):
        data = [usuario.to_dict() for usuario in self.usuarios]
        self.json_handler.save_all(data)

    def anadir_usuario(self, usuario: Usuario):
        if any(u.numero_socio == usuario.numero_socio for u in self.usuarios):
            raise ValueError("Número de socio duplicado")
        self.usuarios.append(usuario)
        self._guardar_usuarios()

    def modificar_usuario(self, numsocio: str, **kwargs):
        for usuario in self.usuarios:
            if usuario.numero_socio == numsocio:
                for key, value in kwargs.items():
                    if hasattr(usuario, key):
                        setattr(usuario, key, value)
                self._guardar_usuarios()
                return
        raise ValueError("Usuario no encontrado")

    def eliminar_usuario(self, numero_socio: str):
        self.usuarios = [u for u in self.usuarios if u.numero_socio != numero_socio]
        self._guardar_usuarios()

    def consultar_usuario(self, numero_socio: str) -> Usuario:
        for usuario in self.usuarios:
            if usuario.numero_socio == numero_socio:
                return usuario
        raise ValueError("Usuario no encontrado")

    def mostrar_todos(self) -> List[Usuario]:
        return self.usuarios