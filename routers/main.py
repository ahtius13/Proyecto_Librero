from fastapi import FastAPI
app=FastAPI()

#USUARIOS
@app.get("/usuario")
def ver_usuarios() :
    #devuelve todos los usuarios guardados.
    pass

@app.post("/usuario")
def crear_usuario(data) :
    #crea un nuevo usuario indicado en el json
    pass

@app.get("/usuario/{numSocio}")
def ver_usuario(numSocio) :
    #ver informacion sobre usuario con el numSocio indicado.
    pass

@app.put("/usuario/{numSocio}")
def modificar_usuario(numSocio, data) :
    #modifica usuario con el numsocio indicado con el contenido indicado en el JSON
    pass

@app.delete("/usuario/{numSocio}")
def eliminar_usuario(numSocio) :
    #elimina usuario con el numSocio indicado.
    pass

#LIBROS
@app.get("/libro")
def ver_libros() :
    #devuelve todos los libros guardados
    pass

@app.post("/libro")
def crear_libro(data) :
    #crea un nuevo libro con la informacion JSON "data"
    pass

@app.get("/libro/{ISBN}")
def ver_libro(ISBN) :
    #devuelve informacion acerca del libro con el ISBN indicado 
    pass


@app.put("/libro/{ISBN}")
def modificar_libro(ISBN, data) :
    #modifica el libro con el ISBN indicado con el contenido de data
    pass

@app.delete("/libro/{ISBN}")
def eliminar_libro(ISBN) :
    #elimina el libro con el ISBN indicado.
    pass

#PRESTAMOS
@app.get("/prestamos")
def ver_prestamos() :
    #devuelve todos los prestamos activos.
    pass

@app.post("/prestamos")
def crear_prestamo(data) :
    #crea un nuevo prestamo con el contenido JSON "data"
    pass

@app.get("/prestamos/finalizados")
def ver_prestamos_finalizados() :
    #devuelve todos los prestamos que han finalizado.
    pass



@app.post("/prestamos/devolucion")
def devolver_prestamo(data) :
    #devuelve un prestamo
    pass


#VENTAS
@app.post("/venta")
def hacer_venta(data) :
    #registra una venta con el socio e ISBN y demas datos indicados en data
    pass

#PREVENTA
@app.post("/preventa")
def hacer_preventa(data) :
    #registra una preventa con la informacion indicada en data.
    pass
