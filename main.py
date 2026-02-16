from fastapi import FastAPI
from routers import usuario_router

app=FastAPI()

app.include_router(usuario_router)