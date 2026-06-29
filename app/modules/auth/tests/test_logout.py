import pytest

from app.modules.auth.cqrs.command import LogoutCommand
from app.modules.auth.domain.events import UserLoggedOutEvent
from app.modules.auth.use_cases.logout import LogoutUseCase


@pytest.mark.asyncio
async def test_logout_with_invalid_token_raises_error(cache, jwt_service, event_bus) -> None:
    uc = LogoutUseCase(jwt=jwt_service, cache=cache, event_bus=event_bus)
    command = LogoutCommand(refresh_token="invalid-token-string")
    from app.modules.auth.domain.exception import InvalidTokenError

    with pytest.raises(InvalidTokenError):
        await uc.execute(command)


@pytest.mark.asyncio
async def test_logout_invalid_type_token_raises_error(user_repo, cache, jwt_service, event_bus) -> None:
    access_token = jwt_service.create_access_token("some-uuid")

    uc = LogoutUseCase(jwt=jwt_service, cache=cache, event_bus=event_bus)
    command = LogoutCommand(refresh_token=access_token)
    from app.modules.auth.domain.exception import InvalidTokenError

    with pytest.raises(InvalidTokenError, match=r".*not a refresh token.*"):
        await uc.execute(command)


@pytest.mark.asyncio
async def test_logout_success_publishes_event(user_repo, cache, jwt_service, event_bus) -> None:
    tokens = jwt_service.create_token_pair("test-user-uuid")
    refresh_token = tokens["refresh_token"]

    received_events: list[UserLoggedOutEvent] = []

    async def handler(event: UserLoggedOutEvent) -> None:
        received_events.append(event)

    event_bus.subscribe(UserLoggedOutEvent, handler)

    uc = LogoutUseCase(jwt=jwt_service, cache=cache, event_bus=event_bus)
    command = LogoutCommand(refresh_token=refresh_token)
    result = await uc.execute(command)

    assert result.message == "Logged out successfully."
    assert len(received_events) == 1
    assert received_events[0].user_uuid == "test-user-uuid"
    assert received_events[0].jti is not None
    assert received_events[0].access_jti is None


@pytest.mark.asyncio
async def test_logout_with_access_token_blacklists_both(user_repo, cache, jwt_service, event_bus) -> None:
    tokens = jwt_service.create_token_pair("test-user-uuid")
    refresh_token = tokens["refresh_token"]
    access_token = tokens["access_token"]

    received_events: list[UserLoggedOutEvent] = []

    async def handler(event: UserLoggedOutEvent) -> None:
        received_events.append(event)

    event_bus.subscribe(UserLoggedOutEvent, handler)

    uc = LogoutUseCase(jwt=jwt_service, cache=cache, event_bus=event_bus)
    command = LogoutCommand(refresh_token=refresh_token, access_token=access_token)
    result = await uc.execute(command)

    assert result.message == "Logged out successfully."
    assert len(received_events) == 1
    assert received_events[0].user_uuid == "test-user-uuid"
    assert received_events[0].jti is not None
    assert received_events[0].access_jti is not None
    assert received_events[0].jti != received_events[0].access_jti


@pytest.mark.asyncio
async def test_logout_with_expired_access_token_silently_skips(user_repo, cache, jwt_service, event_bus) -> None:
    from datetime import UTC, datetime

    tokens = jwt_service.create_token_pair("test-user-uuid")
    refresh_token = tokens["refresh_token"]

    expired_payload = {
        "sub": "test-user-uuid",
        "type": "access",
        "jti": "expired-jti",
        "iat": datetime.now(UTC),
        "exp": datetime.now(UTC),
    }
    import jwt as pyjwt

    expired_access = pyjwt.encode(expired_payload, jwt_service._secret_key, algorithm=jwt_service._algorithm)

    received_events: list[UserLoggedOutEvent] = []

    async def handler(event: UserLoggedOutEvent) -> None:
        received_events.append(event)

    event_bus.subscribe(UserLoggedOutEvent, handler)

    uc = LogoutUseCase(jwt=jwt_service, cache=cache, event_bus=event_bus)
    command = LogoutCommand(refresh_token=refresh_token, access_token=expired_access)
    result = await uc.execute(command)

    assert result.message == "Logged out successfully."
    assert len(received_events) == 1
    assert received_events[0].access_jti is None
