# Atalho para subir tudo
up:
	docker compose -f docker/docker-compose.yml up --build

# Atalho para derrubar tudo
down:
	docker compose -f docker/docker-compose.yml down

# Atalho para ver os logs
logs:
	docker compose -f docker/docker-compose.yml logs -f