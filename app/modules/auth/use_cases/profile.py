from app.core.cache import ICacheService
from app.modules.auth.cqrs.query import GetProfileQuery
from app.modules.auth.cqrs.result import UserProfileResult
from app.modules.user.domain.entities import User, UserStatus
from app.modules.user.domain.exception import UserNotFoundError
from app.modules.user.domain.interfaces import IUserRepository
from app.modules.user.domain.value_objects import Email, PhoneNumber


class GetProfileUseCase:
    """Retrieve the authenticated user's profile.

    Results are cached in Redis for 5 minutes to accelerate repeated
    profile fetches. The cache is invalidated whenever the user's
    profile data changes.
    """

    CACHE_TTL = 300

    def __init__(self, user_repo: IUserRepository, cache: ICacheService):
        self._user_repo = user_repo
        self._cache = cache

    async def execute(self, query: GetProfileQuery) -> UserProfileResult:
        """Fetch the user profile by UUID.

        Checks the Redis cache first (key ``profile:{user_uuid}``).
        On a cache hit the serialized data is rehydrated into a ``User``
        entity. On a miss the database is queried and the result is cached
        for subsequent requests.

        Args:
            query: Contains the user's UUID.

        Returns:
            A ``UserProfileResult`` wrapping the ``User`` domain entity.

        Raises:
            UserNotFoundError: No user matches the given UUID.
        """
        cached = await self._cache.get(f"profile:{query.user_uuid}")
        if cached:
            user = User(
                uuid=cached["uuid"],
                email=Email(cached["email"]),
                username=cached.get("username", ""),
                phone_number=PhoneNumber(cached.get("phone_number", "")),
                first_name=cached.get("first_name"),
                last_name=cached.get("last_name"),
                status=UserStatus(cached["status"]),
                created_at=cached.get("created_at"),
                updated_at=cached.get("updated_at"),
            )
            return UserProfileResult(user=user)

        db_user = await self._user_repo.get_by_uuid(query.user_uuid)
        if db_user is None:
            raise UserNotFoundError(f"User with uuid {query.user_uuid} not found.")
        user = db_user

        await self._cache.set(
            f"profile:{query.user_uuid}",
            {
                "uuid": user.uuid,
                "email": user.email.value,
                "username": user.username,
                "phone_number": user.phone_number.value,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "status": user.status.value,
                "created_at": user.created_at.isoformat() if user.created_at else None,
                "updated_at": user.updated_at.isoformat() if user.updated_at else None,
            },
            self.CACHE_TTL,
        )

        return UserProfileResult(user=user)
