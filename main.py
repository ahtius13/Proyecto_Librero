from fastapi import FastAPI
import src.routes.libros as r_libros
import src.routes.usuarios as r_usuarios
import src.routes.prestamos as r_prestamos
import src.routes.ventas as r_ventas
import src.routes.preventas as r_preventas

app = FastAPI(title="API Librería")
app.include_router(r_libros.router)
app.include_router(r_usuarios.router)
app.include_router(r_prestamos.router)
app.include_router(r_ventas.router)
app.include_router(r_preventas.router)