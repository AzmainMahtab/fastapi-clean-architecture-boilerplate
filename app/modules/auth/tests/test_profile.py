import pytest

from app.modules.auth.cqrs.query import GetProfileQuery
from app.modules.auth.use_cases.profile import GetProfileUseCase
from app.modules.user.domain.exception import UserNotFoundError


@pytest.mark.asyncio
async def test_get_profile_success(active_user, user_repo, cache) -> None:
    uc = GetProfileUseCase(user_repo=user_repo, cache=cache)
    query = GetProfileQuery(user_uuid=active_user.uuid)
    result = await uc.execute(query)

    assert result.user.uuid == active_user.uuid
    assert result.user.email.value == "active@example.com"
    assert result.user.username == "testuser"
    assert result.user.status.value == "active"


@pytest.mark.asyncio
async def test_get_profile_not_found_raises_error(user_repo, cache) -> None:
    uc = GetProfileUseCase(user_repo=user_repo, cache=cache)
    query = GetProfileQuery(user_uuid="nonexistent-uuid")

    with pytest.raises(UserNotFoundError):
        await uc.execute(query)
