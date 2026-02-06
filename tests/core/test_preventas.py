import pytest
import datetime
from src.preventas import PreventaManager
from src.libros import LibroManager, Libro
from src.usuarios import UsuarioManager, Usuario
from pathlib import Path
from src.persistence.json_functions import JsonFunctions

@pytest.fixture
def libro_manager(tmp_path):
    class TestJsonFunctions:
        def __init__(self, filepath):
            self.handler = JsonFunctions(Path(tmp_path) / "libros.json")

        def get_all(self):
            return self.handler.get_all()

        def save_all(self, data):
            self.handler.save_all(data)

    manager = LibroManager()
    manager.json_handler = TestJsonFunctions("data/libros.json").handler
    return manager

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

@pytest.fixture
def preventa_manager(tmp_path, libro_manager, usuario_manager):
    class TestJsonFunctions:
        def __init__(self, filepath):
            self.handler = JsonFunctions(Path(tmp_path) / "preventas.json")

        def get_all(self):
            return self.handler.get_all()

        def save_all(self, data):
            self.handler.save_all(data)

    manager = PreventaManager(libro_manager, usuario_manager)
    manager.json_handler = TestJsonFunctions("data/preventas.json").handler
    return manager

def test_solo_socios(preventa_manager, libro_manager, usuario_manager):
    usuario = Usuario("Nombre", "Apellido", "SOC", "no_socio", "Dir", "Tel")
    usuario_manager.anadir_usuario(usuario)
    libro = Libro("Libro", "Autor", "COD", "Edit", 10.0, cantidad=5, fecha_salida=datetime.date.today() + datetime.timedelta(days=40))
    libro_manager.registrar_libro(libro)
    with pytest.raises(ValueError):
        preventa_manager.registrar_preventa("SOC", "COD", 1)

def test_fecha_futura(preventa_manager, libro_manager, usuario_manager):
    usuario = Usuario("Nombre", "Apellido", "SOC", "socio", "Dir", "Tel")
    usuario_manager.anadir_usuario(usuario)
    libro = Libro("Libro", "Autor", "COD", "Edit", 10.0, cantidad=5, fecha_salida=datetime.date.today() + datetime.timedelta(days=20))
    libro_manager.registrar_libro(libro)
    with pytest.raises(ValueError):
        preventa_manager.registrar_preventa("SOC", "COD", 1)

def test_no_mas_cuando_cero(preventa_manager, libro_manager, usuario_manager):
    usuario = Usuario("Nombre", "Apellido", "SOC", "socio", "Dir", "Tel")
    usuario_manager.anadir_usuario(usuario)
    libro = Libro("Libro", "Autor", "COD", "Edit", 10.0, cantidad=1, fecha_salida=datetime.date.today() + datetime.timedelta(days=40))
    libro_manager.registrar_libro(libro)
    preventa_manager.registrar_preventa("SOC", "COD", 1)
    with pytest.raises(ValueError):
        preventa_manager.registrar_preventa("SOC", "COD", 1)