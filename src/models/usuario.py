class Usuario:
    def __init__(self, idUsuario:str, numSocio:str, nombre:str, apellido:str, tipoUsuario:str, direccion:str, telefono:str):
        self.idUsuario=idUsuario
        self.nombre=nombre
        self.apellido=apellido
        self.tipoUsuario=tipoUsuario
        self.direccion=direccion
        self.telefono=telefono
        self.numSocio=numSocio

    @classmethod
    def crearSocio(cls, numSocio:str, nombre:str, apellido:str, direccion:str, telefono:str):
        numSocio=numSocio
        idUsuario=""
        tipoUsuario="SOCIO"
        return cls(idUsuario,nombre, apellido, tipoUsuario, direccion, telefono)
        
    
    def toDiccionario(self)->dict:
        diccionarioUsuario={
                "IdUsuario":self.idUsuario,

                "Nombre":self.nombre,

                "Apellido":self.apellido,

                "TipodeUsuario":self.tipoUsuario,

                "Dirección":self.direccion,

                "Teléfono":self.telefono,

                "NumSocio":self.numSocio
            }
        return diccionarioUsuario
    
    @staticmethod
    def fromDiccionario(diccionario:dict):
        usuario=Usuario(diccionario.get("IdUsuario"), diccionario.get("numSocio"),diccionario.get("Nombre"),diccionario.get("Apellido"),diccionario.get("TipodeUsuario"),diccionario.get("Dirección"),diccionario.get("Teléfono"))
        return usuario