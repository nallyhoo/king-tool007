.PHONY: help build up down logs

help:
	@echo "Commands:"
	@echo "  build         : Build all services"
	@echo "  up            : Start all services in detached mode"
	@echo "  down          : Stop all services"
	@echo "  logs          : Tail logs from all services"

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

# Production commands
build-prod:
	docker-compose -f docker-compose.prod.yml build

up-prod:
	docker-compose -f docker-compose.prod.yml up -d

down-prod:
	docker-compose -f docker-compose.prod.yml down
