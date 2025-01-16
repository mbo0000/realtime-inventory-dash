# Makefile

# system agnostic 
ifeq ($(OS), Windows_NT)
	OPEN_CMD:=start ""
else
	OPEN_CMD:=open
endif

.PHONY: up down viz

up:
	docker compose down
	docker compose up -d

down:
	docker compose down
	rm -rf postgres/pgdata/*

viz:
	$(OPEN_CMD) "http://localhost:8501"