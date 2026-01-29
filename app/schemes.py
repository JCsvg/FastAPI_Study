from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UsuarioScheme(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    ativo: Optional[bool] = True
    admin: Optional[bool] = False

    class Config:
        from_attributes = True

class PedidoScheme(BaseModel):
    cliente_id: int
    class Config:
        from_attributes = True

class ItemPedidoScheme(BaseModel):
    pedido_id: int
    produto_id: int
    quantidade: int

    class Config:
        from_attributes = True


class ProdutoScheme(BaseModel):
    nome: str
    descricao: Optional[str] = None
    preco: float

    class Config:
        from_attributes = True

class ReciboScheme(BaseModel):
    pedido_id: int
    data_emissao: datetime
    valor: float

    class Config:
        from_attributes = True