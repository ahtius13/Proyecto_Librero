from pydantic import BaseModel


class Usuario_model(BaseModel):
        nombre: str
        apellido: str
        numero_socio: str
        tipo: str
        direccion: str
        telefono: str
        