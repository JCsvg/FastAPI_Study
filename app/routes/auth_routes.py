from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..models import Usuario
from ..utils.database import get_db  
from ..utils.support import bcrypt_context, criar_token, autenticar_usuario, verificar_token
from ..schemes import UsuarioScheme

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def home():
    return {
        "Mensagem": "Você acessou a pagina de autenticação!",
        "Autencicação": False
    }

@auth_router.post("/cadastrar", status_code=status.HTTP_201_CREATED)
async def cadastrar_usuario(
    UsuarioScheme: UsuarioScheme,
    db: Session = Depends(get_db) 
):
    # Verificação -- O email já existe?
    usuario_existente = db.query(Usuario).filter(Usuario.email == UsuarioScheme.email).first()
    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Email já cadastrado"
        )

    senha_criptografada = bcrypt_context.hash(UsuarioScheme.senha)

    novo_usuario = Usuario(
        nome=UsuarioScheme.nome,
        email=UsuarioScheme.email,
        senha=senha_criptografada,
        ativo=UsuarioScheme.ativo,
        admin=UsuarioScheme.admin
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

@auth_router.post("/login")
async def login(
    from_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    usuario = autenticar_usuario(
        senha_fornecida=from_data.password,
        db_session=db,
        usuario_email=from_data.username
    )

    if usuario == 1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    elif usuario == 2:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Senha incorreta"
        )
    
    access_token = criar_token(usuario.id)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@auth_router.get("/refresh")
async def refresh_token(
    usuario: Usuario = Depends(verificar_token),
    db: Session = Depends(get_db)
):
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado"
        )
    
    new_access_token = criar_token(usuario.id)
    new_refresh_token = criar_token(usuario.id, timedelta(days=7))

    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }