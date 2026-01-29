from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..utils.database import get_db
from ..models import Pedido, Usuario, Produto, ItemPedido, StatusPedido, Recibo
from ..utils.support import verificar_token, gerar_codigo_transacao

from app.schemes import PedidoScheme, ProdutoScheme, ItemPedidoScheme, ReciboScheme
from datetime import datetime

order_router = APIRouter(
    prefix="/pedidos", tags=["pedidos"], dependencies=[Depends(verificar_token)]
)


@order_router.get("/")
async def pedido():
    return {"Hello": "World"}


@order_router.post("/pedido")
async def criar_pedido(pedido_scheme: PedidoScheme, db: Session = Depends(get_db)):

    # Verificação se o usuário existe
    if not pedido_scheme.cliente_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O campo 'cliente_id' é obrigatório.",
        )

    novo_pedido = Pedido(cliente_id=pedido_scheme.cliente_id)

    db.add(novo_pedido)
    db.commit()
    db.refresh(novo_pedido)

    return {
        "id": novo_pedido.id,
        "cliente_id": novo_pedido.cliente_id,
        "status": novo_pedido.status,
        "mensagem": "Pedido criado com sucesso!",
    }


@order_router.get("/pedido/cancelar/{id_pedido}")
async def cancelar_pedido(
    id_pedido: int,
    usuario: Usuario = Depends(verificar_token),
    db: Session = Depends(get_db),
):
    pedido = db.query(Pedido).filter(Pedido.id == id_pedido).first()

    if not pedido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Pedido não encontrado."
        )

    if pedido.cliente_id != usuario.id and not usuario.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para cancelar este pedido.",
        )

    if pedido.status == StatusPedido.CANCELADO:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O pedido já está cancelado.",
        )

    pedido.status = "cancelado"
    db.commit()
    db.refresh(pedido)

    return {
        "id": pedido.id,
        "cliente_id": pedido.cliente_id,
        "status": pedido.status,
        "mensagem": "Pedido cancelado com sucesso!",
        "pedido": pedido,
    }


@order_router.get("/listar")
async def listar_pedidos(
    usuario: Usuario = Depends(verificar_token), db: Session = Depends(get_db)
):
    if not usuario.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas administradores podem listar todos os pedidos.",
        )

    pedidos = db.query(Pedido).all()

    return {"pedidos": pedidos}


@order_router.post("/pedido/adicionar-item/{id_pedido}")
async def adicionar_item_ao_pedido(
    id_pedido: int,
    item_scheme: ItemPedidoScheme,
    usuario: Usuario = Depends(verificar_token),
    db: Session = Depends(get_db),
):
    pedido = db.query(Pedido).filter(Pedido.id == id_pedido).first()

    produto = db.query(Produto).filter(Produto.id == item_scheme.produto_id).first()

    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Produto não existe."
        )

    if not pedido or not pedido.status == StatusPedido.PENDENTE:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido não existe ou foi Finalizado/Cancelado",
        )

    if not usuario.admin and usuario.id != pedido.cliente_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Você não tem autorzação para alterar nesse pedido!!",
        )

    novo_item_pedido = ItemPedido(
        pedido_id=item_scheme.pedido_id,
        produto_id=item_scheme.produto_id,
        quantidade=item_scheme.quantidade,
        valor=float(produto.preco * item_scheme.quantidade),
    )

    db.add(novo_item_pedido)
    db.commit()
    db.refresh(novo_item_pedido)

    return {
        "mensagem": f"novo item ({novo_item_pedido.quantidade} x {produto.nome}) adicionado com sucesso"
    }


@order_router.post("/criar-produto")
async def criar_produto(
    produto_scheme: ProdutoScheme,
    usuario: Usuario = Depends(verificar_token),
    db: Session = Depends(get_db),
):
    if not usuario.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas administradores podem listar todos os pedidos.",
        )

    novo_produto = Produto(
        nome=produto_scheme.nome,
        descricao=produto_scheme.descricao,
        preco=produto_scheme.preco,
    )

    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)

    return {"mensagem": f"Novo Produto {produto_scheme.nome} criado com sucesso"}


order_router.post("/recibo/{id_pedido}")


async def criar_recibo(
    id_pedido: int,
    recibo_scheme: ReciboScheme,
    usuario: Usuario = Depends(verificar_token),
    db: Session = Depends(get_db),
):
    pedido = db.query(Pedido).filter(Pedido.id == id_pedido).first()

    if not usuario.admin and usuario.id != pedido.cliente_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Você não tem autorzação para alterar nesse pedido!!",
        )
    
    if not pedido or pedido.status != StatusPedido.PENDENTE:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido não existe ou foi Finalizado/Cancelado",
        )
    
    data_agora = datetime.now()

    novo_recibo = Recibo(
        pedido_id = id_pedido,
        codigo_transacao = gerar_codigo_transacao(
            id_pedido=id_pedido,
            id_cliente=usuario.id,
            data= data_agora
        ),
        data_emissao=data_agora,
        valor= 0.00
    )

    #db.add(novo_recibo)
    #db.commit()
    #db.refresh(novo_recibo)

    return {
        "mensagem": "Recibo criado com sucesso!"
    }
