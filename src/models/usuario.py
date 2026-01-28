class Usuario:
    def __init__(self, idUsuario:str, nombre:str, apellido:str, numSocio:str, tipoUsuario:str, direccion:str, telefono:str):
        self.idUsuario=idUsuario
        self.nombre=nombre
        self.apellido=apellido
        self.numSocio=numSocio
        self.tipoUsuario=tipoUsuario
        self.direccion=direccion
        self.telefono=telefono

    @classmethod
    def crearSocio(cls, nombre:str, apellido:str, direccion:str, telefono:str):
        """genera los datos de id autoincrementales """
        idUsuario=""
        numSocio=""
        tipoUsuario="SOCIO"
        return cls(idUsuario,nombre, apellido, numSocio, tipoUsuario, direccion, telefono)
        
