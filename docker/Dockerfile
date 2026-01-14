# Usa uma imagem leve do Python 3.11 (compatível com suas libs)
FROM python:3.11-slim

# Define a pasta de trabalho dentro do container
WORKDIR /app

# Variáveis para otimizar o Python no Docker
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instala dependências do sistema operacional
# (Necessário para compilar o psycopg2 e libs de criptografia como bcrypt/passlib)
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copia o requirements.txt da raiz para dentro do container
# O Docker só acha esse arquivo se rodarmos o build a partir da raiz (explico abaixo)
COPY requirements.txt .

# Instala as dependências do Python
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copia a pasta 'app' inteira para dentro do container
COPY app ./app

# Expõe a porta 8000
EXPOSE 8000

# Comando para rodar a aplicação
# Aponta para app.main (pasta app, arquivo main.py)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]