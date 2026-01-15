from fastapi import FastAPI

from .utils import database
from . import models # <--- Importa os novos arquivos

# Cria as tabelas no banco ao iniciar (se não existirem)
models.Base.metadata.create_all(bind=database.engine)


app = FastAPI()

from .routes import auth_router, order_router

app.include_router(auth_router)
app.include_router(order_router)

@app.get("/")
async def read_root():
    return {"Hello": "World"}