from fastapi import HTTPException
class RecursoYaExistenteException(HTTPException):
    def __init__(self, recurso: str, identificador:str):
        super().__init__(409, f"ya existe un objeto del recurso {recurso} con el identificador {identificador}")