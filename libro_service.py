from models.libro import Libro
from datetime import date, timedelta
from persistence.json_functions import JsonFunctions
from exceptions import libroDuplicado, libroInexistente, camposLibroError
class Libro_Service:

    def __init__(self):
        self.data =JsonFunctions("data/libros.json")
        self.librosJson: list=self.data.get_all()

    def __modificarLibroData(self, indice, libro:Libro):
        self.libroJson[indice]=self.__fromLibroToDict(libro)

        self.data.save_all(self.librosJson)

    def __eliminarLibroData(self, indice):
        self.librosJson.pop(indice)

        self.data.save_all(self.librosJson)

    def __crearLibroData(self, libro:Libro):
        if libro.isbn in [diccionarioLibro.get("Isbn") for diccionarioLibro in self.librosJson]:
            raise libroDuplicado(f"Ya existe un libro con el isbm {libro.isbn}")
        libro.isbm = int(self.librosJson[-1].isbm)+1
        self.librosJson.append(self.__fromLibroToDict(libro))
        self.data.save_all(self.librosJson)

    def __verificarLibroExistente(isbn, listaLibros:list):
        #Evalua si existe el libro con el isbm en la lista indicada y devuelve su indice en el json
        indice=""
        listaId=[libro.get("Isbn") for libro in listaLibros]
        if isbn in listaId:
            indice=listaId.index(isbn)
        else:
            raise libroInexistente(f"No hay ningun libro con el Isbm {isbn}")
        return indice
    
    def __fromLibroToDict(libro:Libro)->dict:
        diccionarioLibro={
                "Isbn":libro.isbn,

                "Titulo":libro.titulo,

                "Autor":libro.autor,

                "Editorial":libro.editorial,

                "Precio":libro.precio,

                "Cantidad":libro.cantidad,

                "Fecha Salida":libro.fecha_salida,

                "Fecha Devolución":libro.fecha_devolucion
            }
        return diccionarioLibro
    
    def __fromDictToLibro(diccionario:dict)->Libro:
        libro = Libro(
                diccionario.get("Isbn"),

                diccionario.get("Titulo"),

                diccionario.get("Autor"),

                diccionario.get("Editorial"),

                diccionario.get("Precio"),

                diccionario.get("Cantidad"),

                diccionario.get("Fecha Salida"),

                diccionario.get("Fecha Devolución")
            )
        return libro
        
    def crearLibro(self, libroDicc:dict):
        libro:Libro=self.__fromDictToLibro(libroDicc)
        
        
        if libro.titulo == None or libro.autor == None or libro.editorial == None or libro.cantidad < 0 or libro.precio <= 0:
            raise camposLibroError("Campos introducidos incorrectos")
        else:
            self.__crearLibroData(libro)
            
              

    def modificarLibro(self, isbn, datosDicc:dict):
        indice=self.__verificarLibroExistente(isbn, self.librosJson)
        libro:Libro=self.__fromDictToLibro(datosDicc)
        #validaciones de reglas de negocio
        if libro.isbm in [isbn] and libro.titulo!=None:
            self.__modificarLibroData(indice, libro)
        else:
            raise camposLibroError("Campos introducidos incorrectos")
            

    def eliminarLibro(self, isbn):
        i=self.__verificarLibroExistente(isbn, self.librosJson)
        #validaciones de reglas de negocio
        self.__eliminarLibroData(i)
        
            

    def consultarLibro(self, isbn):
        i=self.__verificarLibroExistente(isbn, self.librosJson)
        return self.data.get_all[i]
    


    def vender_devolver_libro(self, isbn, datosDicc:dict):
        indice=self.__verificarLibroExistente(isbn, self.librosJson)
        libro:Libro=self.__fromDictToLibro(datosDicc)
        #validaciones de reglas de negocio
        if libro.isbm in [isbn] and libro.cantidad > 0:
            self.__modificarLibroData(indice, libro)
        else:
            raise camposLibroError("El libro no se encuentra en Stock")