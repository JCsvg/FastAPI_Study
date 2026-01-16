from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..models import Usuario
from ..utils.database import get_db  # <--- 1. Importe sua função geradora
from ..utils.cripto import bcrypt_context

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def home():
    return {
        "Mensagem": "Você acessou a pagina de autenticação!",
        "Autencicação": False
    }

@auth_router.post("/cadastrar", status_code=status.HTTP_201_CREATED)
async def cadastrar_usuario(
    nome: str,    
    email: str, 
    senha: str, 
    ativo: bool = True,
    admin: bool = False,
    db: Session = Depends(get_db) 
):
    # Verificação -- O email já existe?
    usuario_existente = db.query(Usuario).filter(Usuario.email == email).first()
    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Email já cadastrado"
        )

    senha_criptografada = bcrypt_context.hash(senha)

    novo_usuario = Usuario(
        nome=nome,
        email=email,
        senha=senha_criptografada,
        ativo=ativo,
        admin=admin 
    )

    # Transação no Banco
    db.add(novo_usuario)      # Adiciona na "fila" de gravação
    db.commit()               # Salva de verdade no banco (gera o ID)
    db.refresh(novo_usuario)  # Atualiza o objeto com o ID gerado pelo banco
    
    return {
        "id": novo_usuario.id,
        "email": novo_usuario.email,
        "status": "Usuário cadastrado com sucesso!"
    }