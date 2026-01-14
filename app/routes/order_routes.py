from fastapi import APIRouter

order_router = APIRouter(prefix="/pedidos", tags=["pedidos"])

@order_router.get("/")
async def read_root():
    return {"Hello": "World"}