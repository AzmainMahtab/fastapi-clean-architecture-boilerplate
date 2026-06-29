import pytest

from app.modules.auth.cqrs.command import RefreshTokenCommand
from app.modules.auth.use_cases.refresh import RefreshTokenUseCase


@pytest.mark.asyncio
async def test_refresh_with_invalid_token_raises_error(user_repo, cache, jwt_service, event_bus) -> None:
    uc = RefreshTokenUseCase(jwt=jwt_service, cache=cache, event_bus=event_bus, user_repo=user_repo)
    command = RefreshTokenCommand(refresh_token="invalid-token-string")
    from app.modules.auth.domain.exception import InvalidTokenError

    with pytest.raises(InvalidTokenError):
        await uc.execute(command)


@pytest.mark.asyncio
async def test_refresh_with_expired_token_raises_error(user_repo, cache, jwt_service, event_bus, monkeypatch) -> None:
    """Test that an expired refresh token raises TokenExpiredError.

    Create a token directly with an expired timestamp.
    """
    from datetime import UTC, datetime, timedelta

    import jwt as pyjwt

    # Manually encode an expired token
    expired_payload = {
        "sub": "test-uuid",
        "type": "refresh",
        "jti": "test-jti",
        "iat": datetime.now(UTC) - timedelta(days=8),
        "exp": datetime.now(UTC) - timedelta(days=1),
    }
    expired_token = pyjwt.encode(expired_payload, "test-secret-key-for-testing-only", algorithm="HS256")

    uc = RefreshTokenUseCase(jwt=jwt_service, cache=cache, event_bus=event_bus, user_repo=user_repo)
    command = RefreshTokenCommand(refresh_token=expired_token)
    from app.modules.auth.domain.exception import TokenExpiredError

    with pytest.raises(TokenExpiredError):
        await uc.execute(command)


@pytest.mark.asyncio
async def test_refresh_for_suspended_user_raises_error(
    suspended_user, user_repo, cache, jwt_service, event_bus
) -> None:
    """Test that refresh tokens for suspended users are rejected."""
    tokens = jwt_service.create_token_pair(suspended_user.uuid)
    refresh_token = tokens["refresh_token"]

    uc = RefreshTokenUseCase(jwt=jwt_service, cache=cache, event_bus=event_bus, user_repo=user_repo)
    command = RefreshTokenCommand(refresh_token=refresh_token)
    from app.modules.auth.domain.exception import InvalidTokenError

    with pytest.raises(InvalidTokenError, match=r".*suspended.*"):
        await uc.execute(command)


@pytest.mark.asyncio
async def test_refresh_for_inactive_user_raises_error(inactive_user, user_repo, cache, jwt_service, event_bus) -> None:
    """Test that refresh tokens for inactive users are rejected."""
    tokens = jwt_service.create_token_pair(inactive_user.uuid)
    refresh_token = tokens["refresh_token"]

    uc = RefreshTokenUseCase(jwt=jwt_service, cache=cache, event_bus=event_bus, user_repo=user_repo)
    command = RefreshTokenCommand(refresh_token=refresh_token)
    from app.modules.auth.domain.exception import InvalidTokenError

    with pytest.raises(InvalidTokenError, match=r".*deactivated.*"):
        await uc.execute(command)
