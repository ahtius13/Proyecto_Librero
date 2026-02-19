from datetime import date

class Libro:

    def __init__(self, isbn:str, titulo:str, autor:str, editorial:str, precio:float, cantidad:int, fecha_salida:date, fecha_devolucion:date):

        self.isbn = isbn
        self.titulo = titulo
        self.autor =autor
        self.editorial = editorial
        self.precio = precio
        self.cantidad = cantidad
        self.fecha_salida = fecha_salida
        self.fecha_devolucion = fecha_devolucion

    @classmethod

    def crearLibro(cls, isbn:str, titulo:str, autor:str, editorial:str, precio:float, cantidad:int, fecha_salida:date, fecha_devolucion:date):
        isbn = isbn
        titulo = titulo 
        autor = autor
        editorial = editorial
        precio = precio
        cantidad = cantidad
        fecha_salida = fecha_salida
        fecha_devolucion = fecha_devolucion 

        return cls(isbn, titulo, autor, editorial, precio, cantidad, fecha_salida, fecha_devolucion)
        
    
    def toDiccionario(self)->dict:
        diccionarioLibro={
                "Isbn":self.isbn,

                "Titulo":self.titulo,

                "Autor":self.autor,

                "Editorial":self.editorial,

                "Precio":self.precio,

                "Cantidad":self.cantidad,

                "Fecha Salida":self.fecha_salida,

                "Fecha Devolución":self.fecha_devolucion
            }
        return diccionarioLibro
    
    @staticmethod

    def fromLibroDiccionario(diccionario:dict):

        libro=Libro(diccionario.get("Isbn"), diccionario.get("Titulo"),diccionario.get("Autor"),diccionario.get("Editorial"),diccionario.get("Precio"),diccionario.get("Cantidad"),diccionario.get("Fecha Salida",diccionario.get("Fecha Devolución")))
        
        return libro