import enum
from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, Enum as SQLEnum
from .utils.database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    senha = Column(String, nullable=False)
    ativo = Column(Boolean, default=True)
    admin = Column(Boolean, default=False)


class StatusPedido(str, enum.Enum):
    PENDENTE = "pendente"
    FINALIZADO = "finalizado"
    CANCELADO = "cancelado"

class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(SQLEnum(StatusPedido), index=True, nullable=False, default=StatusPedido.PENDENTE)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    valor = Column(Float, nullable=False)


class ItemPedido(Base):
    __tablename__ = "itens_pedido"

    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    quantidade = Column(Integer, nullable=False)
    valor_total = Column(Float, nullable=False)

class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True, nullable=False)
    descricao = Column(String, nullable=True)
    preco = Column(Float, nullable=False)

class Recibo(Base):
    __tablename__ = "recibos"

    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    data_emissao = Column(String, nullable=False)
    valor_total = Column(Float, nullable=False)