from pydantic import BaseModel, EmailStr, DateTime, Enum as PydanticEnum
from typing import Optional
from models import StatusPedido

class UsuarioScheme(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    ativo: Optional[bool] = True
    admin: Optional[bool] = False

    class Config:
        from_attributes = True

class PedidoScheme(BaseModel):
    usuario_id: int
    item: str
    quantidade: int
    preco: float

    class Config:
        from_attributes = True