import pytest
from datetime import date, timedelta
from src.libros import LibroService
from src.persistence.json_functions import JsonFunctions

# Fixture para el repositorio temporal
@pytest.fixture
def inventario(tmp_path):
    repo = JsonFunctions(tmp_path / "libros.json")
    return LibroService(repo)

# Fixture para un libro de ejemplo
@pytest.fixture
def libro():
    return {
        "codigo": "L001",
        "titulo": "Python Básico",
        "autor": "Autor Ejemplo",
        "fecha_salida": date.today(),
        "cantidad": 5
    }

def test_no_codigos_repetidos(inventario, libro):
    inventario.registrar_libro(libro)

    with pytest.raises(ValueError):
        inventario.registrar_libro(libro)

def test_fecha_salida_posterior_actual(inventario, libro):
    libro["fecha_salida"] = date.today() - timedelta(days=1)

    with pytest.raises(ValueError):
        inventario.registrar_libro(libro)

def test_reduccion_stock_venta(inventario, libro):
    inventario.registrar_libro(libro)

    inventario.vender_o_prestar(libro["codigo"], 2)

    libros = inventario.repo.get_all()
    assert libros[0]["cantidad"] == 3

def test_no_venta_sin_stock(inventario, libro):
    inventario.registrar_libro(libro)

    with pytest.raises(ValueError):
        inventario.vender_o_prestar(libro["codigo"], 10)
