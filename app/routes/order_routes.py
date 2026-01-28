from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..utils.database import get_db
from ..models import Pedido

from app.schemes import PedidoScheme, UsuarioScheme

order_router = APIRouter(prefix="/pedidos", tags=["pedidos"])


@order_router.get("/")
async def read_root():
    return {"Hello": "World"}

@order_router.post("/pedido")
async def criar_pedido(
    pedido_scheme: PedidoScheme,
    db: Session = Depends(get_db)
):
    
    # Verificação se o usuário existe
    if not pedido_scheme.cliente_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O campo 'cliente_id' é obrigatório."
        )

    novo_pedido = Pedido(cliente_id=pedido_scheme.cliente_id)
    
    db.add(novo_pedido)
    db.commit()
    db.refresh(novo_pedido)

    return {
        "id": novo_pedido.id,
        "cliente_id": novo_pedido.cliente_id,
        "status": novo_pedido.status,
        "mensagem": "Pedido criado com sucesso!"
    }
