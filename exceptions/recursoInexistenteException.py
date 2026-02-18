from fastapi import HTTPException
class RecursoInexistenteException(HTTPException):
    def __init__(self, recurso: str, identificador:str):
        
        super().__init__(404, f"no se ha encontrado ningun {recurso} con el identificador {identificador}")