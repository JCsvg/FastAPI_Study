from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import DATABASE_URL

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
