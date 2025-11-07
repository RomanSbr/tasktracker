.PHONY: help build up down restart logs clean migrate test

help:
	@echo "Task Tracker - Available Commands:"
	@echo "  make build      - Build Docker images"
	@echo "  make up         - Start all services"
	@echo "  make down       - Stop all services"
	@echo "  make restart    - Restart all services"
	@echo "  make logs       - View logs"
	@echo "  make migrate    - Run database migrations"
	@echo "  make clean      - Remove all containers and volumes"
	@echo "  make test       - Run tests"

build:
	docker-compose build

up:
	docker-compose up -d
	@echo "Services started! Visit http://localhost:3000"

down:
	docker-compose down

restart:
	docker-compose restart

logs:
	docker-compose logs -f

migrate:
	docker-compose exec backend alembic upgrade head

clean:
	docker-compose down -v
	@echo "All containers and volumes removed"

test:
	docker-compose exec backend pytest
	docker-compose exec frontend npm test
