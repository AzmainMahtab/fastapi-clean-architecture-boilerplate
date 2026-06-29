from datetime import UTC, datetime

import jwt as pyjwt

from app.core.cache import ICacheService
from app.core.event_bus import IEventBus
from app.core.jwt import JWTService
from app.modules.auth.cqrs.command import RefreshTokenCommand
from app.modules.auth.cqrs.result import RefreshTokenResult
from app.modules.auth.domain.events import UserRefreshedTokenEvent
from app.modules.auth.domain.exception import InvalidTokenError, TokenBlacklistedError, TokenExpiredError
from app.modules.user.domain.interfaces import IUserRepository


class RefreshTokenUseCase:
    """Issue a new token pair from a valid refresh token.

    Implements **token rotation**: the old refresh token is immediately
    blacklisted so it cannot be used again. This limits the window of
    opportunity for a stolen refresh token.

    Also verifies the user account is still active and not suspended,
    preventing stale tokens from granting access to disabled accounts.
    """

    def __init__(self, jwt: JWTService, cache: ICacheService, event_bus: IEventBus, user_repo: IUserRepository):
        self._jwt = jwt
        self._cache = cache
        self._event_bus = event_bus
        self._user_repo = user_repo

    async def execute(self, command: RefreshTokenCommand) -> RefreshTokenResult:
        """Validate a refresh token, blacklist it, and issue a new pair.

        Args:
            command: Contains the refresh token string.

        Returns:
            A ``RefreshTokenResult`` containing a fresh access + refresh token pair.

        Raises:
            TokenExpiredError: The refresh token has expired.
            TokenBlacklistedError: The refresh token was previously revoked.
            InvalidTokenError: The token is malformed or is not a refresh token.
        """
        try:
            payload = self._jwt.decode(command.refresh_token)
        except pyjwt.ExpiredSignatureError:
            raise TokenExpiredError("Refresh token has expired.") from None
        except pyjwt.InvalidTokenError:
            raise InvalidTokenError("Invalid refresh token.") from None

        if payload.get("type") != "refresh":
            raise InvalidTokenError("Token is not a refresh token.")

        jti = payload["jti"]
        if await self._cache.exists(f"token:blacklist:{jti}"):
            raise TokenBlacklistedError("Refresh token has been revoked.")

        user_uuid = payload["sub"]

        # Verify the user still exists and is not suspended/inactive
        from app.modules.user.domain.entities import UserStatus

        user = await self._user_repo.get_by_uuid(user_uuid)
        if user is None:
            raise InvalidTokenError("User not found.")
        if user.status == UserStatus.SUSPENDED:
            raise InvalidTokenError("Account is suspended.")
        if user.status == UserStatus.INACTIVE:
            raise InvalidTokenError("Account is deactivated.")

        remaining = int(payload["exp"] - datetime.now(UTC).timestamp())
        await self._cache.set(f"token:blacklist:{jti}", "1", max(remaining, 1))

        tokens = self._jwt.create_token_pair(user_uuid)
        new_jti = str(payload.get("jti"))

        await self._event_bus.publish(UserRefreshedTokenEvent(user_uuid=user_uuid, old_jti=jti, new_jti=new_jti))

        return RefreshTokenResult(access_token=tokens["access_token"], refresh_token=tokens["refresh_token"])
