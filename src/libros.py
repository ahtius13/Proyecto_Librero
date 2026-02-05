from datetime import date
from src.persistence.json_functions import JsonFunctions

class LibroService:
    def __init__(self, repo):
        self.repo = repo

    def registrar_libro(self, libro):
        libros = self.repo.get_all()

        if any(l["SBN"] == libro["SBN"] for l in libros):
            raise ValueError("SBN duplicado")

        if libro.get("Fecha Salida") and libro["Fecha Salida"] < date.today():
            raise ValueError("Fecha de salida inválida")

        libros.append(libro)
        self.repo.save_all(libros)

    def modificar_libro(self, SBN, nuevos_datos):
        libros = self.repo.get_all()
        for libro in libros:
            if libro["SBN"] == SBN:
                libro.update(nuevos_datos)
                self.repo.save_all(libros)
                return
        raise ValueError("Libro no encontrado")

    def eliminar_libro(self, SBN):
        libros = self.repo.get_all()
        libros = [l for l in libros if l["SBN"] != SBN]
        self.repo.save_all(libros)

    def buscar_libros(self, campo, valor):
        return [
            l for l in self.repo.get_all()
            if valor.lower() in str(l[campo]).lower()
        ]

    def vender_o_prestar(self, SBN, cantidad):
        libros = self.repo.get_all()
        for libro in libros:
            if libro["SBN"] == SBN:
                if libro["stock"] < cantidad:
                    raise ValueError("Stock insuficiente")
                libro["stock"] -= cantidad
                self.repo.save_all(libros)
                return
        raise ValueError("Libro no encontrado")
