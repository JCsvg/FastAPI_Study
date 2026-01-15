import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# -------------------------------------------------------------
# 1. Importe seus Models e o Base para o autogenerate funcionar
# -------------------------------------------------------------
# Ajuste o import conforme a pasta do seu projeto. 
# Como seu env.py está dentro de 'alembic/', talvez precise ajustar o sys.path ou rodar da raiz.
from app.utils.database import Base  
from app.models import * # Importe seus models para o Alembic "ver" eles

# config object, which provides access to the values within the .ini file in use.
config = context.config

# -------------------------------------------------------------
# 2. AQUI É O PULO DO GATO (Sobrescreve a URL)
# -------------------------------------------------------------
# Lê a variável de ambiente que o Docker ou seu .env definiu
database_url = os.getenv("DATABASE_URL")

if database_url:
    # Sobrescreve a configuração do .ini com a URL real do ambiente
    config.set_main_option("sqlalchemy.url", database_url)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Define o target_metadata para o autogenerate funcionar
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
