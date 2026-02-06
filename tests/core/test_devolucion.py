import pytest
import datetime
from src.prestamos import PrestamoManager
from src.libros import LibroManager, Libro
from pathlib import Path
from src.persistence.json_functions import JsonFunctions

@pytest.fixture
def libro_manager(tmp_path):
    handler = JsonFunctions(Path(tmp_path) / "libros.json")
    manager = LibroManager()
    manager.json_handler = handler
    return manager

@pytest.fixture
def prestamo_manager(libro_manager):
    return PrestamoManager(libro_manager)

def test_stock_disminuye_al_devolver(prestamo_manager, libro_manager):
    libro = Libro("Libro", "Autor", "COD", "Edit", 10.0)
    libro_manager.registrar_libro(libro)
    prestamo_manager.registrar_prestamo("COD", 5, 30)
    prestamo_manager.devolver_prestamo("COD", 5)
    libro_actual = next(l for l in libro_manager.libros if l.codigo == "COD")
    assert libro_actual.cantidad == 0

def test_prestamo_se_marca_como_finalizado(prestamo_manager, libro_manager):
    libro = Libro("Libro", "Autor", "COD", "Edit", 10.0)
    libro_manager.registrar_libro(libro)
    prestamo_manager.registrar_prestamo("COD", 5, 30)
    prestamo_manager.devolver_prestamo("COD", 5)
    libro_actual = next(l for l in libro_manager.libros if l.codigo == "COD")
    assert len(libro_actual.prestamos) == 0  # Marcado como finalizado al eliminar el préstamo