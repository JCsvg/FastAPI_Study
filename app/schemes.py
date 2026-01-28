from pydantic import BaseModel, EmailStr
from typing import Optional

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

class LoginScheme(BaseModel):
    email: EmailStr
    senha: str

    class Config:
        from_attributes = True