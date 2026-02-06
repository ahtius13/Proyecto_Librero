import pytest
import datetime
from src.prestamos import PrestamoManager
from src.libros import LibroManager, Libro
from pathlib import Path
from src.persistence.json_functions import JsonFunctions
from freezegun import freeze_time

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
def prestamo_manager(tmp_path, libro_manager):
    class TestJsonFunctions:
        def __init__(self, filepath):
            self.handler = JsonFunctions(Path(tmp_path) / "prestamos.json")

        def get_all(self):
            return self.handler.get_all()

        def save_all(self, data):
            self.handler.save_all(data)

    manager = PrestamoManager(libro_manager)
    manager.json_handler = TestJsonFunctions("data/prestamos.json").handler
    return manager

def test_incrementar_inventario(prestamo_manager, libro_manager):
    libro = Libro("Libro", "Autor", "COD", "Edit", 10.0)
    libro_manager.registrar_libro(libro)
    prestamo_manager.registrar_prestamo("COD", 5, 30)
    assert next(l for l in libro_manager.libros if l.codigo == "COD").cantidad == 5

@freeze_time("2023-01-01")
def test_detectar_vencidos(prestamo_manager, libro_manager):
    libro = Libro("Libro", "Autor", "COD", "Edit", 10.0)
    libro_manager.registrar_libro(libro)
    prestamo_manager.registrar_prestamo("COD", 5, 30)

    # Avanzamos el tiempo dentro del mismo test
    with freeze_time("2023-03-01"):
        assert len(prestamo_manager.detectar_vencidos()) == 1