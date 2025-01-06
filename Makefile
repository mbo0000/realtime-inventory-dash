# Makefile

.PHONY: up down viz

up:
	docker compose down
	docker compose up -d

down:
	docker compose down
	rm -rf postgres/pgdata/*

viz:
	open http://localhost:8501