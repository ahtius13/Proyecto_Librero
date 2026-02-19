from pydantic import BaseModel


class Preventa_model(BaseModel):
        numero_socio: str
        ISBN:str
        cantidad:int