# Makefile

# system agnostic 
ifeq ($(OS), Windows_NT)
	OPEN_CMD:=cmd /c start
	REMOVE_CMD:=powershell.exe -Command Remove-Item -Recurse -Force
	WAIT_CMD:=timeout /T
else
	OPEN_CMD:=open
	REMOVE_CMD:=rm -rf
	WAIT_CMD:=sleep
endif

.PHONY: down run viz flink_job up wait

run: up wait flink_job

up:
	docker compose down
	docker compose up -d

down:
	docker compose down
	$(REMOVE_CMD) ./postgres/pgdata/*

wait:
	$(WAIT_CMD) 10

flink_job:
	docker exec flink_jobmanager python code/job.py

viz:
	$(OPEN_CMD) "http://localhost:8501"