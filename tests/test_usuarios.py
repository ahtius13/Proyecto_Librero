import pytest


@pytest.fixture
def gestor_usuarios():
    return GestorUsuarios()


@pytest.fixture
def usuario():
    return Usuario(
        codigo="U001",
        nombre="Ana",
        apellido="López",
        tipo="socio",
        direccion="Calle Mayor",
        telefono="123456789"
    )


def test_codigo_socio_unico(gestor_usuarios, usuario):
    pass


def test_usuario_se_agrega(gestor_usuarios, usuario):
    pass


def test_modificar_usuario(gestor_usuarios, usuario):
    pass


def test_eliminar_usuario(gestor_usuarios, usuario):
    pass
