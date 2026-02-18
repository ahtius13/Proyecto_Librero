import pytest
import datetime
from src.preventas import PreventaManager
from src.libros import LibroManager, Libro
from src.usuarios import UsuarioManager, Usuario


@pytest.fixture
def libro_manager(tmp_path):
    libros_file = tmp_path / "libros.json"
    libros_file.write_text("[]")  # JSON vacío
    return LibroManager(filepath=str(libros_file))


@pytest.fixture
def usuario_manager(tmp_path):
    usuarios_file = tmp_path / "usuarios.json"
    usuarios_file.write_text("[]")
    return UsuarioManager(filepath=str(usuarios_file))


@pytest.fixture
def preventa_manager(tmp_path, libro_manager, usuario_manager):
    preventas_file = tmp_path / "preventas.json"
    preventas_file.write_text("[]")
    return PreventaManager(libro_manager, usuario_manager)


def test_solo_socios(preventa_manager, libro_manager, usuario_manager):
    usuario = Usuario("Nombre", "Apellido", "SOC", "no_socio", "Dir", "Tel")
    usuario_manager.anadir_usuario(usuario)

    libro = Libro(
        "Libro", "Autor", "COD", "Edit", 10.0, cantidad=5,
        fecha_salida=datetime.date.today() + datetime.timedelta(days=40)
    )
    libro_manager.registrar_libro(libro)

    with pytest.raises(ValueError):
        preventa_manager.registrar_preventa("SOC", "COD", 1)


def test_fecha_futura(preventa_manager, libro_manager, usuario_manager):
    usuario = Usuario("Nombre", "Apellido", "SOC", "socio", "Dir", "Tel")
    usuario_manager.anadir_usuario(usuario)

    libro = Libro(
        "Libro", "Autor", "COD", "Edit", 10.0, cantidad=5,
        fecha_salida=datetime.date.today() + datetime.timedelta(days=20)
    )
    libro_manager.registrar_libro(libro)

    with pytest.raises(ValueError):
        preventa_manager.registrar_preventa("SOC", "COD", 1)


def test_no_mas_cuando_cero(preventa_manager, libro_manager, usuario_manager):
    usuario = Usuario("Nombre", "Apellido", "SOC", "socio", "Dir", "Tel")
    usuario_manager.anadir_usuario(usuario)

    libro = Libro(
        "Libro", "Autor", "COD", "Edit", 10.0, cantidad=1,
        fecha_salida=datetime.date.today() + datetime.timedelta(days=40)
    )
    libro_manager.registrar_libro(libro)

    preventa_manager.registrar_preventa("SOC", "COD", 1)

    with pytest.raises(ValueError):
        preventa_manager.registrar_preventa("SOC", "COD", 1)
