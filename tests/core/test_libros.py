import pytest
import datetime
from src.libros import Libro, LibroManager
import pytest
import datetime
from src.libros import Libro, LibroManager
from pathlib import Path
from src.persistence.json_functions import JsonFunctions

@pytest.fixture
def libro_manager(tmp_path):
    # Para tests, override el filepath a uno temporal
    class TestJsonFunctions:
        def __init__(self, filepath):
            self.handler = JsonFunctions(Path(tmp_path) / "libros.json")

        def get_all(self):
            return self.handler.get_all()

        def save_all(self, data):
            self.handler.save_all(data)

    manager = LibroManager()
    manager.json_handler = TestJsonFunctions("data/libros.json").handler  # Usa temporal
    return manager

def test_no_duplicados(libro_manager):
    libro1 = Libro("Libro1", "Autor1", "COD1", "Edit1", 10.0)
    libro_manager.registrar_libro(libro1)
    with pytest.raises(ValueError):
        libro_manager.registrar_libro(Libro("Libro2", "Autor2", "COD1", "Edit2", 15.0))

def test_fecha_salida_futura(libro_manager):
    with pytest.raises(ValueError):
        libro_manager.registrar_libro(Libro("Libro", "Autor", "COD", "Edit", 10.0, fecha_salida=datetime.date.today() - datetime.timedelta(days=1)))

def test_reducir_cantidad(libro_manager):
    libro = Libro("Libro", "Autor", "COD", "Edit", 10.0, cantidad=5)
    libro_manager.registrar_libro(libro)
    libro_manager.reducir_cantidad("COD", 2)
    assert next(l for l in libro_manager.libros if l.codigo == "COD").cantidad == 3

def test_no_reducir_sin_stock(libro_manager):
    libro = Libro("Libro", "Autor", "COD", "Edit", 10.0, cantidad=1)
    libro_manager.registrar_libro(libro)
    with pytest.raises(ValueError):
        libro_manager.reducir_cantidad("COD", 2)