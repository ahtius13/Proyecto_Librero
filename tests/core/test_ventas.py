import pytest
from src.ventas import VentaManager
from src.libros import LibroManager, Libro
from src.usuarios import UsuarioManager, Usuario
from pathlib import Path
from src.persistence.json_functions import JsonFunctions

@pytest.fixture
def libro_manager(tmp_path):
    handler = JsonFunctions(Path(tmp_path) / "libros.json")
    manager = LibroManager()
    manager.json_handler = handler
    return manager

@pytest.fixture
def usuario_manager(tmp_path):
    handler = JsonFunctions(Path(tmp_path) / "usuarios.json")
    manager = UsuarioManager()
    manager.json_handler = handler
    return manager

@pytest.fixture
def venta_manager(libro_manager, usuario_manager):
    return VentaManager(libro_manager, usuario_manager)

def test_descuento_socio(venta_manager, libro_manager, usuario_manager):
    usuario = Usuario("Nombre", "Apellido", "SOC", "socio", "Dir", "Tel")
    usuario_manager.anadir_usuario(usuario)
    libro = Libro("Libro", "Autor", "COD", "Edit", 10.0, cantidad=5)
    libro_manager.registrar_libro(libro)
    venta_manager.registrar_venta("SOC", "COD", 1)
    libro_actual = next(l for l in libro_manager.libros if l.codigo == "COD")
    assert len(libro_actual.ventas) == 1
    assert libro_actual.ventas[0]["precio_pagado"] == 9.0  # 10% descuento

def test_reducir_stock(venta_manager, libro_manager, usuario_manager):
    usuario = Usuario("Nombre", "Apellido", "SOC", "no_socio", "Dir", "Tel")
    usuario_manager.anadir_usuario(usuario)
    libro = Libro("Libro", "Autor", "COD", "Edit", 10.0, cantidad=5)
    libro_manager.registrar_libro(libro)
    venta_manager.registrar_venta("SOC", "COD", 2)
    assert next(l for l in libro_manager.libros if l.codigo == "COD").cantidad == 3

def test_no_vender_sin_stock(venta_manager, libro_manager, usuario_manager):
    usuario = Usuario("Nombre", "Apellido", "SOC", "no_socio", "Dir", "Tel")
    usuario_manager.anadir_usuario(usuario)
    libro = Libro("Libro", "Autor", "COD", "Edit", 10.0, cantidad=1)
    libro_manager.registrar_libro(libro)
    with pytest.raises(ValueError):
        venta_manager.registrar_venta("SOC", "COD", 2)