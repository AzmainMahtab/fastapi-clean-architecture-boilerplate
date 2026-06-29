.PHONY: help up down db-up db-down migrate-generate migrate-up migrate-down test logs

# Variables
API_CONTAINER = api-local
MSG ?= "empty migration message"

# ==========================================
# MAIN COMMANDS
# ==========================================

help: ## Show this help menu
	@echo "Backend Commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

up: ## Start databases and backend (rebuilds backend if needed)
	docker network create backend-network 2>/dev/null || true
	docker compose -f db.yml up -d
	docker compose  up --build -d

down: ## Stop databases and backend
	docker compose  down
	docker compose -f db.yml down

# ==========================================
# DATABASE ONLY
# ==========================================

db-up: ## Start ONLY the databases (creates network if missing)
	docker network create backend-network 2>/dev/null || true
	docker compose -f db.yml up -d

db-down: ## Stop ONLY the databases
	docker compose -f db.yml down

# ==========================================
# ALEMBIC MIGRATIONS (via docker exec)
# ==========================================

migrate-generate: ## Generate a new migration (usage: make migrate-generate MSG="create users table")
	docker exec $(API_CONTAINER) alembic revision --autogenerate -m "$(MSG)"

migrate-up: ## Apply all pending migrations to the database
	docker exec $(API_CONTAINER) alembic upgrade head

migrate-down: ## Rollback the last applied migration
	docker exec $(API_CONTAINER) alembic downgrade -1

# ==========================================
# TESTS
# ==========================================

.PHONY: test

TEST_IMAGE = backend-test

test: ## Run tests (usage: make test, or make test ARGS="-v -k test_register")
	docker build --target test -t $(TEST_IMAGE) .
	docker run --rm \
		-v ./app:/app/app \
		--env-file .env \
		$(TEST_IMAGE) \
		pytest $(ARGS)

# ==========================================
# UTILITIES
# ==========================================

logs: ## Tail the backend logs (Ctrl+C to exit)
	docker compose  logs -f api
