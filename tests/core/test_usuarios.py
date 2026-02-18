import pytest
from src.usuarios import Usuario, UsuarioManager
from pathlib import Path
from src.persistence.json_functions import JsonFunctions

@pytest.fixture
def usuario_manager(tmp_path):
    test_file = tmp_path / "usuarios.json"
    test_file.write_text("[]")  # Inicializa el JSON vacío
    return UsuarioManager(filepath=str(test_file))


def test_no_duplicados(usuario_manager):
    usuario1 = Usuario("Nombre1", "Apellido1", "SOC1", "socio", "Dir1", "Tel1")
    usuario_manager.anadir_usuario(usuario1)

    with pytest.raises(ValueError):
        usuario_manager.anadir_usuario(
            Usuario("Nombre2", "Apellido2", "SOC1", "socio", "Dir2", "Tel2")
        )


def test_anadir_correcto(usuario_manager):
    usuario = Usuario("Nombre", "Apellido", "SOC", "socio", "Dir", "Tel")
    usuario_manager.anadir_usuario(usuario)
    assert len(usuario_manager.usuarios) == 1


def test_modificar(usuario_manager):
    usuario = Usuario("Nombre", "Apellido", "SOC", "socio", "Dir", "Tel")
    usuario_manager.anadir_usuario(usuario)
    usuario_manager.modificar_usuario("SOC", telefono="NuevoTel")
    assert usuario_manager.consultar_usuario("SOC").telefono == "NuevoTel"


def test_eliminar(usuario_manager):
    usuario = Usuario("Nombre", "Apellido", "SOC", "socio", "Dir", "Tel")
    usuario_manager.anadir_usuario(usuario)

    usuario_manager.eliminar_usuario("SOC")

    assert len(usuario_manager.usuarios) == 0
