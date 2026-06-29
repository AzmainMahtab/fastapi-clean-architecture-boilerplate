# FastAPI Backend Boilerplate

A generic backend boilerplate built with **FastAPI**, **SQLAlchemy** (async), **PostgreSQL**, **Redis**, and **Argon2id** password hashing. Follows a **modular monolith** architecture with **Clean Architecture / DDD** and **CQRS** patterns.

Includes user management, authentication (JWT), and OTP modules out of the box.

---

## Quick Start

### 1. Prerequisites

- [Docker](https://docs.docker.com/get-docker/) + [Docker Compose](https://docs.docker.com/compose/install/)
- Make (optional — all commands work via raw `docker compose`)

### 2. Environment

```bash
cp example.env .env
```

Edit `.env` if needed — defaults work for local development.

### 3. Run

```bash
make up
```

This starts PostgreSQL, Redis, and the API server with hot-reload on `http://localhost:8000`.

### 4. Apply migrations

```bash
make migrate-up
```

---

## Commands (Makefile)

| Command | Description |
|---------|-------------|
| `make up` | Start databases + backend |
| `make down` | Stop everything |
| `make db-up` | Start only PostgreSQL + Redis |
| `make db-down` | Stop only databases |
| `make migrate-generate MSG="desc"` | Generate a new Alembic migration |
| `make migrate-up` | Apply pending migrations |
| `make migrate-down` | Rollback last migration |
| `make logs` | Tail API logs |

### Without Make

```bash
# Start databases
docker compose -f db.yml up -d

# Start API
docker compose up --build -d

# Migrations
docker exec api-local alembic upgrade head
docker exec api-local alembic revision --autogenerate -m "description"
```

---

## Migrations

Alembic auto-generates migrations by detecting changes in SQLAlchemy models. The entrypoint runs `alembic upgrade head` automatically on container start.

### Workflow

1. Change a model in `app/modules/*/infrastructure/persistence/models.py`
2. Generate: `make migrate-generate MSG="add field to users"`
3. Review the generated file in `alembic/versions/`
4. Apply: `make migrate-up`

### Running locally without Docker

```bash
uv sync
uv run alembic upgrade head
uv run uvicorn app.main:app --reload
```

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     FastAPI App                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Module A    │  │   Module B   │  │   Module C   │  │
│  │  (e.g. User)  │  │     ...      │  │     ...      │  │
│  └──────┬───────┘  └──────────────┘  └──────────────┘  │
│         │                                                │
│  ┌──────┴───────┐                                        │
│  │   API Layer   │  FastAPI routers, Pydantic schemas    │
│  │  (api/)       │  Dependency injection, OpenAPI docs   │
│  └──────┬───────┘                                        │
│         │                                                │
│  ┌──────┴───────┐                                        │
│  │  Use Cases   │  Application business logic            │
│  │ (use_cases/) │  Orchestrates domain + infrastructure  │
│  └──────┬───────┘                                        │
│         │                                                │
│  ┌──────┴───────┐           ┌──────────────────┐         │
│  │   Domain     │◄──────────│   CQRS DTOs       │         │
│  │ (domain/)    │  Events   │ (cqrs/command.py  │         │
│  │  Entities    │           │  query.py         │         │
│  │  ValueObjects│           │  result.py)       │         │
│  │  Interfaces  │           └──────────────────┘         │
│  └──────┬───────┘                                        │
│         │                                                │
│  ┌──────┴───────┐                                        │
│  │ Infrastruct. │  SQLAlchemy, Redis, external APIs      │
│  │(infrastruct/ │  Repository impl, mappers, models      │
│  └──────┬───────┘                                        │
│         │                                                │
│  ┌──────┴───────┐  ┌────────────┐  ┌──────────────┐     │
│  │  PostgreSQL  │  │   Redis    │  │   Event Bus   │     │
│  └──────────────┘  └────────────┘  │ (in-memory)   │     │
│                                    └──────────────┘     │
└─────────────────────────────────────────────────────────┘
```

Each module is **self-contained** with its own:

- **API** — FastAPI router + Pydantic schemas + dependency injection
- **Domain** — entities, value objects, repository ports, events, exceptions
- **Use Cases** — application business logic
- **CQRS** — command, query, and result DTOs
- **Infrastructure** — persistence (SQLAlchemy models, mapper, repository implementation)
- **Tests** — colocated inside the module

Cross-cutting concerns live in `app/core/`:
- `event_bus.py` — in-memory event bus (IEventBus port + InMemoryEventBus)
- `pagination.py` — reusable PaginationParams, Page[T], PaginatedResponse[T]
- `health.py` — database and Redis health checks
- `settings.py` — Pydantic Settings from environment
- `database.py` — async SQLAlchemy engine, session factory, base model

---

## Project Structure

```
app/
├── main.py                          # FastAPI app entrypoint
├── core/
│   ├── event_bus.py                 # IEventBus + InMemoryEventBus
│   ├── pagination.py                # PaginationParams, Page[T], PaginatedResponse[T]
│   ├── health.py                    # DB + Redis health checks
│   ├── database.py                  # Async engine, session, Base
│   ├── settings.py                  # Pydantic Settings
│   ├── hasher.py                    # Argon2id password hashing
│   └── tests/
│       └── test_event_bus.py
├── modules/
│   └── user/
│       ├── api/
│       │   ├── router.py            # Endpoints
│       │   ├── schemas.py           # Pydantic request/response models
│       │   └── dependencies.py      # FastAPI DI providers
│       ├── cqrs/
│       │   ├── command.py           # Command DTOs (writes)
│       │   ├── query.py             # Query DTOs (reads)
│       │   └── result.py            # Result DTOs
│       ├── domain/
│       │   ├── entities.py          # User entity + UserStatus enum
│       │   ├── value_objects.py     # Email, HashedPassword
│       │   ├── interfaces.py        # IUserRepository port
│       │   ├── events.py            # Domain events
│       │   └── exception.py         # Domain exceptions
│       ├── use_cases/
│       │   ├── register_user.py
│       │   ├── update_user_status.py
│       │   ├── delete_user.py
│       │   ├── prune_user.py
│       │   ├── restore_user.py
│       │   ├── get_user.py
│       │   └── list_users.py
│       ├── infrastructure/
│       │   └── persistence/
│       │       ├── models.py        # SQLAlchemy ORM model
│       │       ├── mapper.py        # Domain <-> ORM mapping
│       │       └── repository.py    # SQLAlchemyUserRepository
│       └── tests/
│           ├── conftest.py          # InMemoryUserRepository + fixtures
│           ├── test_register_user.py
│           ├── test_admin_user.py
│           └── test_api.py
├── alembic/                         # Database migrations
├── alembic.ini
├── Dockerfile
├── docker-compose.yml               # API service
├── db.yml                           # PostgreSQL + Redis services
├── Makefile
├── pyproject.toml
└── example.env
```

---

## Why This Architecture

### Modular Monolith

All code lives in one deployable unit, but modules are **isolated by domain boundaries**. This gives you:

- **Cohesion** — related concepts (user registration, user queries, user deletion) live together
- **Autonomy** — each module could be extracted into a microservice later without rewriting
- **Simplicity** — one deployment, one CI pipeline, no network calls between modules

### Clean Architecture / DDD (Domain-Driven Design)

Layers are strictly separated with **inward dependency**:

- **Domain** — pure Python, no framework dependencies. Contains the business rules.
- **Use Cases** — orchestrate domain objects and infrastructure ports.
- **Infrastructure** — implements ports defined by the domain (e.g., `IUserRepository` → `SQLAlchemyUserRepository`).
- **API** — thin layer that translates HTTP ↔ use case commands/queries.

This makes the business logic **testable without databases or HTTP** (use case tests use an in-memory repository).

### CQRS (Command Query Responsibility Segregation)

Reads and writes have separate DTOs and separate use cases:

- **Commands** — mutate state, may publish domain events
- **Queries** — never mutate state, never publish events

This avoids the common pitfall of a single "UserService" that mixes reads and writes, and makes the API surface self-documenting.

### Event Bus

The in-memory `IEventBus` lets use cases publish domain events (`UserRegisteredEvent`) without knowing who handles them. This enables **side-effect decoupling** — future features like sending welcome emails or updating search indexes can subscribe to events without modifying existing use cases.
