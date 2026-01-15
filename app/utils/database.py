import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Pega a URL do ambiente (definida no docker-compose)
# Se não achar, usa um valor padrão (bom para testes locais fora do docker)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/fastapi_db")

# Cria a engine (o motor que fala com o banco)
engine = create_engine(DATABASE_URL)

# Cria a fábrica de sessões (cada requisição vai pedir uma sessão daqui)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe base para seus models herdarem depois
Base = declarative_base()

# Dependência para injetar a sessão nas rotas (Dependency Injection)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()