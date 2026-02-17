from fastapi import Response
import pytest
from src.usuarios import Usuario, UsuarioManager
import pytest
from src.usuarios import Usuario, UsuarioManager
from pathlib import Path
from src.persistence.json_functions import JsonFunctions
from fastapi.testclient import TestClient
from main import app


client=TestClient(app)

@pytest.fixture
def usuario_manager(tmp_path):
    class TestJsonFunctions:
        def __init__(self, filepath):
            self.handler = JsonFunctions(Path(tmp_path) / "usuarios.json")

        def get_all(self):
            return self.handler.get_all()

        def save_all(self, data):
            self.handler.save_all(data)

    manager = UsuarioManager()
    manager.json_handler = TestJsonFunctions("data/usuarios.json").handler
    return manager

def test_no_duplicados(usuario_manager):
    usuario1 = Usuario("Nombre1", "Apellido1", "SOC1", "socio", "Dir1", "Tel1")
    usuario_manager.anadir_usuario(usuario1)
    with pytest.raises(ValueError):
        usuario_manager.anadir_usuario(Usuario("Nombre2", "Apellido2", "SOC1", "socio", "Dir2", "Tel2"))

def test_anadir_correcto(usuario_manager):
    usuario = Usuario("Nombre", "Apellido", "SOC", "socio", "Dir", "Tel")
    usuario_manager.anadir_usuario(usuario)
    assert len(usuario_manager.usuarios) == 1

def test_modificar(usuario_manager):
    usuario = Usuario("Nombre", "Apellido", "SOC", "socio", "Dir", "Tel")
    usuario_manager.anadir_usuario(usuario)
    usuario_manager.modificar_usuario("SOC", telefono="NuevoTel")
    assert usuario_manager.consultar_usuario("SOC").telefono == "NuevoTel"

def test_eliminar(usuario_manager):
    usuario = Usuario("Nombre", "Apellido", "SOC", "socio", "Dir", "Tel")
    usuario_manager.anadir_usuario(usuario)
    usuario_manager.eliminar_usuario("SOC")
    assert len(usuario_manager.usuarios) == 0

#Valicaciones endpoints
def test_endpoint_crearUsuario():
    numSocio="SOC002"
    respuesta:Response=client.post("/usuario", json={
  "nombre": "ruben",
  "apellido": "a",
  "numero_socio": numSocio,
  "tipo": "socio",
  "direccion": "string",
  "telefono": "string"
})
    assert respuesta.status_code==201
    assert next(iter([usuario for usuario in UsuarioManager().mostrar_todos() if usuario.numero_socio==numSocio]), False)
