import pytest
from src.prestamos import PrestamoManager
from src.libros import LibroManager, Libro


@pytest.fixture
def libro_manager(tmp_path):
    libros_file = tmp_path / "libros.json"
    libros_file.write_text("[]")
    return LibroManager(filepath=str(libros_file))


@pytest.fixture
def prestamo_manager(tmp_path, libro_manager):
    prestamos_file = tmp_path / "prestamos.json"
    prestamos_file.write_text("[]")
    return PrestamoManager(libro_manager, filepath=str(prestamos_file))


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
    assert len(libro_actual.prestamos) == 0
