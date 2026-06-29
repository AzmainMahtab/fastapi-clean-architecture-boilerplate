from collections.abc import Generator

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from app.main import app as fastapi_app
from app.modules.user.api.dependencies import get_event_bus, get_register_use_case
from app.modules.user.tests.conftest import InMemoryUserRepository
from app.modules.user.use_cases.register_user import RegisterUserUseCase


@pytest.fixture
def app() -> FastAPI:
    return fastapi_app


@pytest.fixture
def override_deps(app: FastAPI, user_repo: InMemoryUserRepository, event_bus) -> Generator[None]:
    async def get_uc_override() -> RegisterUserUseCase:
        return RegisterUserUseCase(user_repo=user_repo, event_bus=event_bus)

    app.dependency_overrides[get_event_bus] = lambda: event_bus
    app.dependency_overrides[get_register_use_case] = get_uc_override
    yield
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_register_returns_201(app, override_deps) -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/users/register",
            json={
                "email": "newuser@example.com",
                "password": "StrongPass1!",
                "password2": "StrongPass1!",
                "username": "newuser",
                "phone_number": "+1234567890",
            },
        )

    assert response.status_code == 201
    body = response.json()
    assert body["success"] is True
    assert body["status"] == "success"
    assert body["statusCode"] == 201
    data = body["data"]
    assert data["email"] == "newuser@example.com"
    assert data["username"] == "newuser"
    assert data["phone_number"] == "+1234567890"
    assert data["status"] == "pending_verification"
    assert "uuid" in data


@pytest.mark.asyncio
async def test_register_returns_409_on_duplicate(app, override_deps) -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post(
            "/api/v1/users/register",
            json={
                "email": "dupe@example.com",
                "password": "StrongPass1!",
                "password2": "StrongPass1!",
                "username": "user1",
                "phone_number": "+1111111111",
            },
        )
        response = await client.post(
            "/api/v1/users/register",
            json={
                "email": "dupe@example.com",
                "password": "StrongPass1!",
                "password2": "StrongPass1!",
                "username": "user2",
                "phone_number": "+2222222222",
            },
        )

    assert response.status_code == 409
    body = response.json()
    assert body["success"] is False
    assert body["errors"][0]["code"] == "USER_ALREADY_EXISTS"


@pytest.mark.asyncio
async def test_register_validates_email(app, override_deps) -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/users/register",
            json={
                "email": "not-an-email",
                "password": "StrongPass1!",
                "password2": "StrongPass1!",
                "username": "testuser",
                "phone_number": "+1234567890",
            },
        )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_register_missing_required_field(app, override_deps) -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/api/v1/users/register", json={"email": "test@example.com"})

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_register_response_has_all_profile_fields(app, override_deps) -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/users/register",
            json={
                "email": "profile@example.com",
                "password": "StrongPass1!",
                "password2": "StrongPass1!",
                "username": "profileuser",
                "phone_number": "+9999999999",
                "first_name": "John",
                "last_name": "Doe",
            },
        )

    assert response.status_code == 201
    body = response.json()
    assert body["success"] is True
    data = body["data"]
    assert data["username"] == "profileuser"
    assert data["phone_number"] == "+9999999999"
