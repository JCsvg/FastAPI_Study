from fastapi import FastAPI

app = FastAPI()

from app.routes import auth_routes, order_routes

@app.get("/")
async def read_root():
    return {"Hello": "World"}