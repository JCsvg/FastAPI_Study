# Atalho para subir tudo
up:
	docker compose --env-file .env -f docker/docker-compose.yml up --build
# Atalho para derrubar tudo
down:
	docker compose -f docker/docker-compose.yml down

# Atalho para ver os logs
logs:
	docker compose -f docker/docker-compose.yml logs -f

# Atalho para criar migrações
migrar:
	docker compose --env-file .env -f docker/docker-compose.yml run --rm api alembic revision --autogenerate -m "$(msg)"

# Atalho para aplicar as migrações no banco
atualizar:
	docker compose --env-file .env -f docker/docker-compose.yml run --rm api alembic upgrade head