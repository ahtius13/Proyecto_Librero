import pytest
from freezegun import freeze_time
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

    with freeze_time("2023-03-01"):
        assert len(prestamo_manager.detectar_vencidos()) == 1
