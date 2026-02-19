"""
Tests de flujo de la API con TestClient.
Se parchean los managers para no depender de archivos JSON en disco.
"""
import datetime
import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

from src.libros import Libro, LibroManager
from src.usuarios import Usuario, UsuarioManager
from src.prestamos import PrestamoManager
from src.ventas import VentaManager
from src.preventas import PreventaManager

import src.routes.libros as r_libros
import src.routes.usuarios as r_usuarios
import src.routes.prestamos as r_prestamos
import src.routes.ventas as r_ventas
import src.routes.preventas as r_preventas

from src.main import app

client = TestClient(app)

# ══════════════════════════════════════════════════════════════════════
# FIXTURES — datos de prueba y managers sin I/O
# ══════════════════════════════════════════════════════════════════════

@pytest.fixture(autouse=True)
def setup_managers():
    """
    Antes de cada test:
      - Crea managers reales pero sin ficheros JSON (mock de _guardar_*)
      - Precarga usuarios y libros de prueba
      - Los inyecta en los módulos de rutas
    """
    # ── Usuarios ──────────────────────────────────────────────────────
    um = UsuarioManager.__new__(UsuarioManager)
    um.json_handler = MagicMock()
    um.usuarios = [
        Usuario("Admin",  "Test", "admin-01",  "admin",    "Calle A", "600000001"),
        Usuario("Socio",  "Test", "socio-01",  "socio",    "Calle B", "600000002"),
        Usuario("Visita", "Test", "visita-01", "no_socio", "Calle C", "600000003"),
    ]
    um._guardar_usuarios = MagicMock()

    # ── Libros ────────────────────────────────────────────────────────
    lm = LibroManager.__new__(LibroManager)
    lm.json_handler = MagicMock()
    lm.libros = [
        Libro("El Quijote",    "Cervantes",  "ISBN-001", "Planeta",   15.0, 5),
        Libro("Dune",          "Herbert",    "ISBN-002", "Minotauro", 20.0, 3),
        Libro("Sin stock",     "Autor X",    "ISBN-003", "Planeta",    9.0, 0),
        Libro(
            "Preventa futura", "Autor Y", "ISBN-004", "Anagrama", 25.0, 10,
            fecha_salida=datetime.date.today() + datetime.timedelta(days=40)
        ),
    ]
    lm._guardar_libros = MagicMock()

    # ── Services ──────────────────────────────────────────────────────
    pm = PrestamoManager.__new__(PrestamoManager)
    pm.libro_manager = lm

    vm = VentaManager.__new__(VentaManager)
    vm.libro_manager  = lm
    vm.usuario_manager = um
    vm.DESCUENTO_SOCIO = 0.10

    prvm = PreventaManager.__new__(PreventaManager)
    prvm.libro_manager   = lm
    prvm.usuario_manager = um

    # ── Inyección en routers ──────────────────────────────────────────
    r_libros.libro_manager     = lm
    r_libros.usuario_manager   = um
    r_usuarios.usuario_manager = um
    r_prestamos.prestamo_manager = pm
    r_prestamos.usuario_manager  = um
    r_ventas.venta_manager     = vm
    r_ventas.usuario_manager   = um
    r_preventas.preventa_manager = prvm
    r_preventas.usuario_manager  = um

    yield {
        "um": um, "lm": lm, "pm": pm, "vm": vm, "prvm": prvm
    }


# ══════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════

def headers(user_id: str) -> dict:
    return {"X-User-Id": user_id}

ADMIN   = "admin-01"
SOCIO   = "socio-01"
VISITA  = "visita-01"
UNKNOWN = "no-existe"


# ══════════════════════════════════════════════════════════════════════
# 1. LIBROS — GET
# ══════════════════════════════════════════════════════════════════════

class TestLibrosGet:

    def test_all_devuelve_solo_libros_con_stock(self):
        r = client.get("/libros/all", headers=headers(SOCIO))
        assert r.status_code == 200
        codigos = [l["codigo"] for l in r.json()]
        assert "ISBN-001" in codigos
        assert "ISBN-003" not in codigos   # sin stock

    def test_all_sin_header_devuelve_401(self):
        r = client.get("/libros/all")
        assert r.status_code in (401, 422)

    def test_all_usuario_desconocido_devuelve_401(self):
        r = client.get("/libros/all", headers=headers(UNKNOWN))
        assert r.status_code == 401

    def test_buscar_por_titulo(self):
        r = client.get("/libros/buscar", params={"titulo": "dune"}, headers=headers(VISITA))
        assert r.status_code == 200
        assert any(l["codigo"] == "ISBN-002" for l in r.json())

    def test_buscar_por_editorial(self):
        r = client.get("/libros/buscar", params={"editorial": "planeta"}, headers=headers(SOCIO))
        assert r.status_code == 200
        codigos = [l["codigo"] for l in r.json()]
        assert "ISBN-001" in codigos

    def test_buscar_sin_resultados(self):
        r = client.get("/libros/buscar", params={"titulo": "zzz_inexistente"}, headers=headers(SOCIO))
        assert r.status_code == 200
        assert r.json() == []

    def test_consultar_libro_por_codigo(self):
        r = client.get("/libros/ISBN-001", headers=headers(SOCIO))
        assert r.status_code == 200
        assert r.json()["titulo"] == "El Quijote"

    def test_consultar_libro_inexistente_devuelve_404(self):
        r = client.get("/libros/ISBN-999", headers=headers(SOCIO))
        assert r.status_code == 404


# ══════════════════════════════════════════════════════════════════════
# 2. LIBROS — POST / PUT / DELETE (solo admin)
# ══════════════════════════════════════════════════════════════════════

class TestLibrosAdmin:

    def test_registrar_libro_admin(self):
        payload = {
            "titulo": "Nuevo libro",
            "autor": "Autor Z",
            "codigo": "ISBN-100",
            "editorial": "Espasa",
            "precio": 12.5,
            "cantidad": 4,
        }
        r = client.post("/libros/", json=payload, headers=headers(ADMIN))
        assert r.status_code == 200
        assert r.json()["codigo"] == "ISBN-100"

    def test_registrar_libro_codigo_duplicado(self):
        payload = {
            "titulo": "Copia",
            "autor": "Autor",
            "codigo": "ISBN-001",   # ya existe
            "editorial": "X",
            "precio": 10.0,
        }
        r = client.post("/libros/", json=payload, headers=headers(ADMIN))
        assert r.status_code == 400

    def test_registrar_libro_fecha_pasada(self):
        payload = {
            "titulo": "Viejo",
            "autor": "Autor",
            "codigo": "ISBN-200",
            "editorial": "X",
            "precio": 10.0,
            "fecha_salida": "2000-01-01",
        }
        r = client.post("/libros/", json=payload, headers=headers(ADMIN))
        assert r.status_code == 400

    def test_registrar_libro_no_admin_devuelve_401(self):
        payload = {
            "titulo": "Test",
            "autor": "Autor",
            "codigo": "ISBN-300",
            "editorial": "X",
            "precio": 10.0,
        }
        r = client.post("/libros/", json=payload, headers=headers(SOCIO))
        assert r.status_code == 401

    def test_modificar_libro_admin(self):
        r = client.put("/libros/ISBN-001", json={"precio": 99.0}, headers=headers(ADMIN))
        assert r.status_code == 200

    def test_modificar_libro_inexistente(self):
        r = client.put("/libros/ISBN-999", json={"precio": 1.0}, headers=headers(ADMIN))
        assert r.status_code == 404

    def test_eliminar_libro_admin(self):
        r = client.delete("/libros/ISBN-002", headers=headers(ADMIN))
        assert r.status_code == 200

    def test_eliminar_libro_no_admin_devuelve_401(self):
        r = client.delete("/libros/ISBN-001", headers=headers(SOCIO))
        assert r.status_code == 401


# ══════════════════════════════════════════════════════════════════════
# 3. USUARIOS
# ══════════════════════════════════════════════════════════════════════

class TestUsuarios:

    def test_mostrar_todos_admin(self):
        r = client.get("/usuarios/all", headers=headers(ADMIN))
        assert r.status_code == 200
        assert len(r.json()) == 3

    def test_mostrar_todos_no_admin_devuelve_401(self):
        r = client.get("/usuarios/all", headers=headers(SOCIO))
        assert r.status_code == 401

    def test_consultar_perfil_propio(self):
        r = client.get(f"/usuarios/{SOCIO}", headers=headers(SOCIO))
        assert r.status_code == 200
        assert r.json()["numero_socio"] == SOCIO

    def test_consultar_perfil_ajeno_no_admin_devuelve_401(self):
        r = client.get(f"/usuarios/{VISITA}", headers=headers(SOCIO))
        assert r.status_code == 401

    def test_consultar_cualquier_perfil_admin(self):
        r = client.get(f"/usuarios/{SOCIO}", headers=headers(ADMIN))
        assert r.status_code == 200

    def test_anadir_usuario_admin(self):
        payload = {
            "nombre": "Nuevo",
            "apellido": "Usuario",
            "numero_socio": "socio-99",
            "tipo": "socio",
            "direccion": "Calle X",
            "telefono": "600111222",
        }
        r = client.post("/usuarios/", json=payload, headers=headers(ADMIN))
        assert r.status_code == 200
        assert r.json()["numero_socio"] == "socio-99"

    def test_anadir_usuario_duplicado(self):
        payload = {
            "nombre": "Dup",
            "apellido": "Dup",
            "numero_socio": SOCIO,   # ya existe
            "tipo": "socio",
            "direccion": "X",
            "telefono": "000",
        }
        r = client.post("/usuarios/", json=payload, headers=headers(ADMIN))
        assert r.status_code == 400

    def test_modificar_usuario_admin(self):
        r = client.put(f"/usuarios/{SOCIO}", json={"telefono": "999999999"}, headers=headers(ADMIN))
        assert r.status_code == 200

    def test_eliminar_usuario_admin(self):
        r = client.delete(f"/usuarios/{VISITA}", headers=headers(ADMIN))
        assert r.status_code == 200

    def test_eliminar_usuario_no_admin_devuelve_401(self):
        r = client.delete(f"/usuarios/{VISITA}", headers=headers(SOCIO))
        assert r.status_code == 401


# ══════════════════════════════════════════════════════════════════════
# 4. PRÉSTAMOS
# ══════════════════════════════════════════════════════════════════════

class TestPrestamos:

    def test_registrar_prestamo_admin(self):
        payload = {"codigo_libro": "ISBN-001", "cantidad": 2, "duracion_dias": 30}
        r = client.post("/prestamos/", json=payload, headers=headers(ADMIN))
        assert r.status_code == 200

    def test_registrar_prestamo_no_admin_devuelve_401(self):
        payload = {"codigo_libro": "ISBN-001", "cantidad": 1, "duracion_dias": 30}
        r = client.post("/prestamos/", json=payload, headers=headers(SOCIO))
        assert r.status_code == 401

    def test_registrar_prestamo_libro_inexistente(self):
        payload = {"codigo_libro": "ISBN-999", "cantidad": 1, "duracion_dias": 30}
        r = client.post("/prestamos/", json=payload, headers=headers(ADMIN))
        assert r.status_code == 400

    def test_mostrar_activos(self, setup_managers):
        # Añadir un préstamo activo directamente al libro
        libro = next(l for l in setup_managers["lm"].libros if l.codigo == "ISBN-001")
        libro.prestamos.append({
            "cantidad": 2,
            "fecha_prestamo": datetime.date.today(),
            "fecha_vencimiento": datetime.date.today() + datetime.timedelta(days=30),
        })
        r = client.get("/prestamos/", headers=headers(ADMIN))
        assert r.status_code == 200
        assert len(r.json()) >= 1

    def test_mostrar_vencidos(self, setup_managers):
        # Añadir un préstamo vencido
        libro = next(l for l in setup_managers["lm"].libros if l.codigo == "ISBN-001")
        libro.prestamos.append({
            "cantidad": 1,
            "fecha_prestamo": datetime.date.today() - datetime.timedelta(days=60),
            "fecha_vencimiento": datetime.date.today() - datetime.timedelta(days=1),
        })
        r = client.get("/prestamos/vencidos", headers=headers(ADMIN))
        assert r.status_code == 200
        assert len(r.json()) >= 1

    def test_devolver_prestamo(self, setup_managers):
        libro = next(l for l in setup_managers["lm"].libros if l.codigo == "ISBN-001")
        libro.prestamos.append({
            "cantidad": 3,
            "fecha_prestamo": datetime.date.today() - datetime.timedelta(days=60),
            "fecha_vencimiento": datetime.date.today() - datetime.timedelta(days=1),
        })
        stock_antes = libro.cantidad
        r = client.post("/devolucion/prestamos/ISBN-001", json={"cantidad": 2}, headers=headers(ADMIN))
        assert r.status_code == 200
        assert libro.cantidad == stock_antes - 2

    def test_devolver_mas_de_lo_prestado(self, setup_managers):
        libro = next(l for l in setup_managers["lm"].libros if l.codigo == "ISBN-001")
        libro.prestamos.append({
            "cantidad": 1,
            "fecha_prestamo": datetime.date.today() - datetime.timedelta(days=5),
            "fecha_vencimiento": datetime.date.today() - datetime.timedelta(days=1),
        })
        r = client.post("/devolucion/prestamos/ISBN-001", json={"cantidad": 999}, headers=headers(ADMIN))
        assert r.status_code == 400


# ══════════════════════════════════════════════════════════════════════
# 5. VENTAS
# ══════════════════════════════════════════════════════════════════════

class TestVentas:

    def test_comprar_libro_socio_aplica_descuento(self, setup_managers):
        libro = next(l for l in setup_managers["lm"].libros if l.codigo == "ISBN-001")
        stock_antes = libro.cantidad
        r = client.post("/ventas/ISBN-001", json={"cantidad": 1}, headers=headers(SOCIO))
        assert r.status_code == 200
        assert r.json()["descuento_aplicado"] is True
        assert libro.cantidad == stock_antes - 1
        # Verificar precio con descuento registrado
        venta = libro.ventas[-1]
        assert venta["precio_pagado"] == pytest.approx(15.0 * 0.9)

    def test_comprar_libro_no_socio_sin_descuento(self, setup_managers):
        libro = next(l for l in setup_managers["lm"].libros if l.codigo == "ISBN-001")
        r = client.post("/ventas/ISBN-001", json={"cantidad": 1}, headers=headers(VISITA))
        assert r.status_code == 200
        assert r.json()["descuento_aplicado"] is False
        venta = libro.ventas[-1]
        assert venta["precio_pagado"] == pytest.approx(15.0)

    def test_comprar_libro_sin_stock(self):
        r = client.post("/ventas/ISBN-003", json={"cantidad": 1}, headers=headers(SOCIO))
        assert r.status_code == 400

    def test_comprar_libro_inexistente(self):
        r = client.post("/ventas/ISBN-999", json={"cantidad": 1}, headers=headers(SOCIO))
        assert r.status_code == 400

    def test_devolucion_compra(self, setup_managers):
        libro = next(l for l in setup_managers["lm"].libros if l.codigo == "ISBN-001")
        # Simular una venta previa
        libro.ventas.append({
            "numero_socio": SOCIO,
            "cantidad": 2,
            "fecha": datetime.date.today(),
            "precio_pagado": 27.0,
        })
        stock_antes = libro.cantidad
        r = client.post("/devolucion/compra/ISBN-001", json={"cantidad": 1}, headers=headers(SOCIO))
        assert r.status_code == 200
        assert libro.cantidad == stock_antes + 1

    def test_devolucion_compra_inexistente(self):
        r = client.post("/devolucion/compra/ISBN-001", json={"cantidad": 1}, headers=headers(SOCIO))
        assert r.status_code == 400

    def test_usuario_desconocido_no_puede_comprar(self):
        r = client.post("/ventas/ISBN-001", json={"cantidad": 1}, headers=headers(UNKNOWN))
        assert r.status_code == 401


# ══════════════════════════════════════════════════════════════════════
# 6. PREVENTAS
# ══════════════════════════════════════════════════════════════════════

class TestPreventas:

    def test_preventa_socio_ok(self, setup_managers):
        libro = next(l for l in setup_managers["lm"].libros if l.codigo == "ISBN-004")
        stock_antes = libro.cantidad
        r = client.post("/preventas/ISBN-004", json={"cantidad": 1}, headers=headers(SOCIO))
        assert r.status_code == 200
        assert libro.cantidad == stock_antes - 1

    def test_preventa_no_socio_devuelve_401(self):
        r = client.post("/preventas/ISBN-004", json={"cantidad": 1}, headers=headers(VISITA))
        assert r.status_code == 401

    def test_preventa_libro_sin_fecha_futura(self):
        # ISBN-001 no tiene fecha de salida → debe fallar
        r = client.post("/preventas/ISBN-001", json={"cantidad": 1}, headers=headers(SOCIO))
        assert r.status_code == 400

    def test_preventa_sin_stock_suficiente(self, setup_managers):
        libro = next(l for l in setup_managers["lm"].libros if l.codigo == "ISBN-004")
        libro.cantidad = 0
        r = client.post("/preventas/ISBN-004", json={"cantidad": 1}, headers=headers(SOCIO))
        assert r.status_code == 400

    def test_preventa_admin_tambien_puede(self):
        r = client.post("/preventas/ISBN-004", json={"cantidad": 1}, headers=headers(ADMIN))
        assert r.status_code == 200