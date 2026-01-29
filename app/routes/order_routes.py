from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..utils.database import get_db
from ..models import Pedido, Usuario
from ..utils.support import verificar_token

from app.schemes import PedidoScheme

order_router = APIRouter(prefix="/pedidos", tags=["pedidos"], dependencies=[Depends(verificar_token)])


@order_router.get("/")
async def pedido():
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

@order_router.get("/pedido/cancelar/{id_pedido}")
async def cancelar_pedido(id_pedido: int, usuario: Usuario = Depends(verificar_token), db: Session = Depends(get_db)):
    pedido = db.query(Pedido).filter(Pedido.id == id_pedido).first()

    if not pedido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido não encontrado."
        )
    
    if pedido.cliente_id != usuario.id and not usuario.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para cancelar este pedido."
        )

    if pedido.status == "cancelado":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O pedido já está cancelado."
        )

    pedido.status = "cancelado"
    db.commit()
    db.refresh(pedido)

    return {
        "id": pedido.id,
        "cliente_id": pedido.cliente_id,
        "status": pedido.status,
        "mensagem": "Pedido cancelado com sucesso!",
        "pedido": pedido
    }