from passlib.context import CryptContext

# Configura o algoritmo bcrypt (padrão de mercado)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Transforma 'senha123' em um hash seguro."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha bate com o hash salvo."""
    return pwd_context.verify(plain_password, hashed_password)