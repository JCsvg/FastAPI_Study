from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.utils.database import get_db
from ..models import Usuario
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from ..utils.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def criar_token(
    id_usuario: int,
    duração_token: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
):
    data_expiracao = datetime.now(timezone.utc) + duração_token
    dir_info = {"sub": str(id_usuario), "exp": data_expiracao}
    token_jwt = jwt.encode(dir_info, SECRET_KEY, algorithm=ALGORITHM)

    return token_jwt


def autenticar_usuario(senha_fornecida: str, db_session: Session, usuario_email: str):
    usuario = db_session.query(Usuario).filter(Usuario.email == usuario_email).first()

    if not usuario:
        return 1
    elif not bcrypt_context.verify(senha_fornecida, usuario.senha):
        return 2
    return usuario


def verificar_token(
    token: str = Depends(OAuth2PasswordBearer("auth/login")),
    session: Session = Depends(get_db),
) -> Usuario | None:

    try:
        token_decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usuario_id = token_decoded.get("sub")
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        ) from JWTError

    if usuario_id is None:
        return None

    usuario = session.query(Usuario).filter(Usuario.id == int(usuario_id)).first()
    return usuario


def obter_nome_mes(numero_mes: int) -> str:
    meses = {
        1: "JAN",
        2: "FEV",
        3: "MAR",
        4: "ABR",
        5: "MAI",
        6: "JUN",
        7: "JUL",
        8: "AGO",
        9: "SET",
        10: "OUT",
        11: "NOV",
        12: "DEZ",
    }
    # O .get retorna um valor padrão se o número for inválido
    return meses.get(numero_mes, "JAN")


def gerar_codigo_transacao(id_pedido: int, id_cliente: int, data: datetime) -> str:
    mes = obter_nome_mes.get(data.month)
    codigo = f"{mes}{id_cliente}{id_pedido}"
    return codigo
