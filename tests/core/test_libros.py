import pytest
from datetime import date, timedelta
from src.libros import LibroService
from src.persistence.json_functions import JsonFunctions

# Fixture del inventario
@pytest.fixture
def inventario(tmp_path):
    repo = JsonFunctions(tmp_path / "libros.json")
    return LibroService(repo)

# Fixture de un libro ejemplo
@pytest.fixture
def libro():
    return {
        "SBN": "1234567890",
        "Titulo": "Python Básico",
        "Autor": "Autor Ejemplo",
        "Editorial": "Editorial Ejemplo",
        "Precio": 29.99,
        "stock": 5,
        "Fecha Salida": date.today(),
        "Fecha Prestamo": None
    }

def test_no_sbn_repetido(inventario, libro):
    inventario.registrar_libro(libro)
    with pytest.raises(ValueError):
        inventario.registrar_libro(libro)

def test_fecha_salida_posterior_actual(inventario, libro):
    libro["Fecha Salida"] = date.today() - timedelta(days=1)
    with pytest.raises(ValueError):
        inventario.registrar_libro(libro)

def test_reduccion_stock_venta(inventario, libro):
    inventario.registrar_libro(libro)
    inventario.vender_o_prestar(libro["SBN"], 2)
    libros = inventario.repo.get_all()
    assert libros[0]["stock"] == 3

def test_no_venta_sin_stock(inventario, libro):
    inventario.registrar_libro(libro)
    with pytest.raises(ValueError):
        inventario.vender_o_prestar(libro["SBN"], 10)
