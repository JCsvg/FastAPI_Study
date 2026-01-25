from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..utils.database import get_db
from ..models import Pedido, Usuario

from app.schemes import PedidoScheme

order_router = APIRouter(prefix="/pedidos", tags=["pedidos"])

@order_router.get("/")
async def read_root():
    return {"Hello": "World"}

@order_router.post("/pedido")
async def criar_pedido(
    pedido_scheme: PedidoScheme, 
    db: Session = Depends(get_db)
):
    novo_pedido = Pedido