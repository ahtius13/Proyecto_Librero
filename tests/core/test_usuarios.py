from fastapi import Response
import pytest
from src.usuarios import Usuario, UsuarioManager
from pathlib import Path
from src.persistence.json_functions import JsonFunctions
from fastapi.testclient import TestClient
from fastapi import HTTPException
from main import app


client=TestClient(app)

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

#Valicaciones endpoints
#CREATE
def test_endpoint_crearUsuario():
    manager=UsuarioManager()
    numSocio="SociPruebaCrear"
    manager.eliminar_usuario(numSocio)
    respuesta:Response=client.post("/usuario", json={
  "nombre": "ruben",
  "apellido": "a",
  "numero_socio": numSocio,
  "tipo": "socio",
  "direccion": "string",
  "telefono": "string"
})
    assert respuesta.status_code==201
    assert next(iter([usuario for usuario in UsuarioManager().mostrar_todos() if usuario.numero_socio==numSocio]), False)

def test_endpoint_crearUsuario_YaExistente():
    manager=UsuarioManager()
    numSocio="SociPruebaCrear"
    manager.eliminar_usuario(numSocio)
    manager.anadir_usuario(Usuario("ruben","a",numSocio,"socio","string", "string"))
    respuesta:Response=client.post("/usuario", json={
  "nombre": "ruben",
  "apellido": "a",
  "numero_socio": numSocio,
  "tipo": "socio",
  "direccion": "string",
  "telefono": "string"
})
    assert respuesta.status_code==409

def test_endpoint_crearUsuario_JsonMal():
    Response=client.post("/usuario", json={
  "nombre": "ruben",
  "apellido": "a",
  "tipo": "socio",
  "direccion": "string",
  "telefono": "string"
}) 
    #422 codigo que se lanza cuando no coincide con el basemodel
    assert Response.status_code==422
    
#READ
def test_endpoint_verUsuario():
    manager=UsuarioManager()
    numSocio="SociPruebaVer"
    manager.eliminar_usuario(numSocio)
    manager.anadir_usuario(Usuario("ruben","a",numSocio,"socio","string", "string"))
    respuesta:Response=client.get(f"usuario/{numSocio}")
    json:dict=respuesta.json()
    assert respuesta.status_code==200
    assert json.get("nombre")=="ruben"

def test_endpoint_verUsuario_Inexistente():
    numSocio="SocioInexistente"
    respuesta:Response=client.get(f"usuario/{numSocio}")
    assert respuesta.status_code==404

def test_endpoint_verUsuarios():
    manager=UsuarioManager()
    numSocio="SociPruebaVertodos"
    manager.eliminar_usuario(numSocio)

    manager.anadir_usuario(Usuario("ruben","a",numSocio,"socio","string", "string"))
    respuesta:Response=client.get(f"usuario")
    json:dict=respuesta.json()
    assert respuesta.status_code==200
    personasConNombre=[diccionario for diccionario in json if diccionario.get("numero_socio")==numSocio]
    assert len(personasConNombre)

#UPDATE
def test_endpoint_modificarUsuario():
    manager=UsuarioManager()
    numSocio="SociPruebaModificar"
    manager.eliminar_usuario(numSocio)

    manager.anadir_usuario(Usuario("ruben","a",numSocio,"socio","string", "string"))
    Response=client.put(f"/usuario/{numSocio}", json={
  "nombre": "manolo",
  "apellido": "a",
  "numero_socio": numSocio,
  "tipo": "socio",
  "direccion": "string",
  "telefono": "string"
}) 
    #422 codigo que se lanza cuando no coincide con el basemodel
    assert Response.status_code==200
    assert next(iter([usuario.nombre=="manolo" for usuario in UsuarioManager().mostrar_todos() if usuario.numero_socio==numSocio]))

def test_endpoint_modificarUsuario_JsonMal():
    Response=client.put("/usuario/1", json={
  "nombre": "ruben",
  "apellido": "a",
  "tipo": "socio",
  "direccion": "string",
  "telefono": "string"
}) 
    #422 codigo que se lanza cuando no coincide con el basemodel
    assert Response.status_code==422

def test_endpoint_modificarUsuario_CambiarIdentificador():
    numSocio="SociPruebaModificar"
    
    Response=client.put(f"/usuario/{numSocio}", json={
    "nombre": "manolo",
    "apellido": "a",
    "numero_socio": "socioModificado",
    "tipo": "socio",
    "direccion": "string",
    "telefono": "string"
    }) 
    #422 codigo que se lanza cuando no coincide con el basemodel
    assert Response.status_code==400

def test_endpoint_modificarUsuario_Inexistente():
    
    numSocio="SocioInexistente"

    Response=client.put(f"/usuario/{numSocio}", json={
    "nombre": "manolo",
    "apellido": "a",
    "numero_socio": numSocio,
    "tipo": "socio",
    "direccion": "string",
    "telefono": "string"
    }) 
    assert Response.status_code==404

#DELETE
def test_endpoint_eliminarUsuario():
    manager=UsuarioManager()
    numSocio="SociPruebaEliminar"
    manager.eliminar_usuario(numSocio)

    manager.anadir_usuario(Usuario("eliminado","a",numSocio,"socio","string", "string"))
    Response=client.delete(f"/usuario/{numSocio}") 
    #422 codigo que se lanza cuando no coincide con el basemodel
    assert Response.status_code==200
    assert not len([usuario for usuario in UsuarioManager().mostrar_todos() if usuario.numero_socio==numSocio])


def test_endpoint_eliminarUsuario_Inexistente():
    
    numSocio="SocioInexistente"

    Response=client.delete(f"/usuario/{numSocio}") 
    assert Response.status_code==404