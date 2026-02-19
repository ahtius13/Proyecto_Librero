from fastapi import FastAPI
from routers import preventa_router

app=FastAPI()

app.include_router(preventa_router.router)