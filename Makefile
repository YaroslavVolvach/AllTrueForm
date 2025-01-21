# Define Docker Compose command
DOCKER_COMPOSE = docker-compose

# Define Alembic command
ALEMBIC = docker-compose exec backend alembic

# Specify services you want to manage
SERVICES = frontend backend db

# The default target, if no target is specified
.PHONY: help
help:
	@echo "Makefile commands for Docker Compose:"
	@echo "  make build           - Build or rebuild the services, removing old images"
	@echo "  make up              - Start the services in detached mode"
	@echo "  make down            - Stop the services"
	@echo "  make restart         - Restart the services"
	@echo "  make logs            - View the logs of the services"
	@echo "  make status          - View the status of the containers"
	@echo "  make migration       - Create a new migration"
	@echo "  make migrate         - Apply database migrations"
	@echo "  make create_admin    - Create an admin user in the database"
	@echo "  make rebuild         - Remove old image, build a new one without cache, and start containers"

# Build the services defined in Docker Compose
.PHONY: build
build:
	@$(DOCKER_COMPOSE) build --no-cache

# Start the services in detached mode (run in the background)
.PHONY: up
up:
	@$(DOCKER_COMPOSE) up -d

# Stop and remove the services
.PHONY: down
down:
	@$(DOCKER_COMPOSE) down

# Restart the services (stop and start)
.PHONY: restart
restart:
	@$(DOCKER_COMPOSE) down
	@$(DOCKER_COMPOSE) up -d

# View logs of the services (follow the logs)
.PHONY: logs
logs:
	@$(DOCKER_COMPOSE) logs -f

# Check the status of containers
.PHONY: status
status:
	@$(DOCKER_COMPOSE) ps

.PHONY: init_migrations
init_migrations:
	if [ ! -d "./migrations" ] || [ ! "$(ls -A migrations)" ]; then \
		docker-compose exec backend alembic init migrations; \
	else \
		echo "Migrations directory already exists and is not empty, skipping initialization."; \
	fi

.PHONY: migration
migration: ## Create DB revision
	@read -p "Do you want to run with autogenerate? [y/N] " ans && ans=$${ans:-N}; \
	if [ $${ans} = y ] || [ $${ans} = Y ]; then \
		autogenerate="--autogenerate"; \
	else \
		autogenerate=""; \
	fi; \
	read -p "Enter description for a new revision: " revision_message; \
    docker-compose exec backend alembic revision -m "$$revision_message" $$autogenerate
	
.PHONY: migrate
migrate: ## Apply database migrations
	@read -p "Do you want to apply migrations? [y/N] " ans && ans=$${ans:-N}; \
	if [ $${ans} = y ] || [ $${ans} = Y ]; then \
		echo "Applying migrations..."; \
		docker-compose exec backend alembic upgrade head; \
	else \
		echo "Migration not applied."; \
	fi
# Create an admin user in the database (you can call a custom script for this)
.PHONY: create_admin
create_admin:
	@$(DOCKER_COMPOSE) exec backend python -c "from app.utils.create_admin import create_admin; create_admin()"

# Remove old images, build a new one without cache and start containers
.PHONY: rebuild
rebuild:
	@$(DOCKER_COMPOSE) down --rmi all
	@$(DOCKER_COMPOSE) up --build --no-cache -d

