import os
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env que está na raiz
load_dotenv()

# Pega as variáveis de ambiente
SECRET_KEY = os.getenv("SECRET_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))



