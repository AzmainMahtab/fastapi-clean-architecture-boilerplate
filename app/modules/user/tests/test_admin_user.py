import pytest

from app.core.pagination import PaginationParams
from app.modules.user.cqrs.command import (
    DeleteUserCommand,
    PruneUserCommand,
    RegisterUserCommand,
    UpdateUserStatusCommand,
)
from app.modules.user.cqrs.query import GetUserByEmailQuery, GetUserByUsernameQuery, GetUserByUuidQuery, ListUsersQuery
from app.modules.user.domain.entities import UserStatus
from app.modules.user.domain.events import UserUpdatedEvent
from app.modules.user.domain.exception import CannotUpdateToInactiveError, UserNotFoundError
from app.modules.user.use_cases.delete_user import DeleteUserUseCase
from app.modules.user.use_cases.get_user import GetUserUseCase
from app.modules.user.use_cases.list_users import ListUsersUseCase
from app.modules.user.use_cases.prune_user import PruneUserUseCase
from app.modules.user.use_cases.register_user import RegisterUserUseCase
from app.modules.user.use_cases.update_user_status import UpdateUserStatusUseCase


@pytest.fixture
def registered_user(user_repo, event_bus):
    uc = RegisterUserUseCase(user_repo=user_repo, event_bus=event_bus)
    cmd = RegisterUserCommand(
        email="test@example.com",
        password="StrongPass1!",
        password2="StrongPass1!",
        username="testuser",
        phone_number="+1234567890",
    )
    return uc.execute(cmd)


@pytest.mark.asyncio
async def test_update_status_to_active(registered_user, user_repo, event_bus) -> None:
    result = await registered_user
    uc = UpdateUserStatusUseCase(user_repo=user_repo, event_bus=event_bus)
    cmd = UpdateUserStatusCommand(uuid=result.user.uuid, new_status="active")
    updated = await uc.execute(cmd)
    assert updated.user.status == UserStatus.ACTIVE


@pytest.mark.asyncio
async def test_update_status_to_suspended(registered_user, user_repo, event_bus) -> None:
    result = await registered_user
    uc = UpdateUserStatusUseCase(user_repo=user_repo, event_bus=event_bus)
    cmd = UpdateUserStatusCommand(uuid=result.user.uuid, new_status="suspended")
    updated = await uc.execute(cmd)
    assert updated.user.status == UserStatus.SUSPENDED


@pytest.mark.asyncio
async def test_cannot_update_to_inactive(registered_user, user_repo, event_bus) -> None:
    result = await registered_user
    uc = UpdateUserStatusUseCase(user_repo=user_repo, event_bus=event_bus)
    cmd = UpdateUserStatusCommand(uuid=result.user.uuid, new_status="inactive")
    with pytest.raises(CannotUpdateToInactiveError):
        await uc.execute(cmd)


@pytest.mark.asyncio
async def test_update_status_user_not_found(user_repo, event_bus) -> None:
    uc = UpdateUserStatusUseCase(user_repo=user_repo, event_bus=event_bus)
    cmd = UpdateUserStatusCommand(uuid="nonexistent", new_status="active")
    with pytest.raises(UserNotFoundError):
        await uc.execute(cmd)


@pytest.mark.asyncio
async def test_update_status_publishes_user_updated_event(registered_user, user_repo, event_bus) -> None:
    result = await registered_user
    received: list[UserUpdatedEvent] = []

    async def handler(event: UserUpdatedEvent) -> None:
        received.append(event)

    event_bus.subscribe(UserUpdatedEvent, handler)

    uc = UpdateUserStatusUseCase(user_repo=user_repo, event_bus=event_bus)
    await uc.execute(UpdateUserStatusCommand(uuid=result.user.uuid, new_status="active"))

    assert len(received) == 1
    assert received[0].user_uuid == result.user.uuid
    assert received[0].email == "test@example.com"


@pytest.mark.asyncio
async def test_soft_delete_sets_deleted_at(registered_user, user_repo, event_bus) -> None:
    result = await registered_user
    uc = DeleteUserUseCase(user_repo=user_repo, event_bus=event_bus)
    cmd = DeleteUserCommand(uuid=result.user.uuid)
    deleted = await uc.execute(cmd)
    assert deleted.user.deleted_at is not None
    assert deleted.user.status == UserStatus.INACTIVE


@pytest.mark.asyncio
async def test_soft_delete_user_not_found(user_repo, event_bus) -> None:
    uc = DeleteUserUseCase(user_repo=user_repo, event_bus=event_bus)
    cmd = DeleteUserCommand(uuid="nonexistent")
    with pytest.raises(UserNotFoundError):
        await uc.execute(cmd)


@pytest.mark.asyncio
async def test_soft_delete_publishes_user_updated_event(registered_user, user_repo, event_bus) -> None:
    result = await registered_user
    received: list[UserUpdatedEvent] = []

    async def handler(event: UserUpdatedEvent) -> None:
        received.append(event)

    event_bus.subscribe(UserUpdatedEvent, handler)

    uc = DeleteUserUseCase(user_repo=user_repo, event_bus=event_bus)
    await uc.execute(DeleteUserCommand(uuid=result.user.uuid))

    assert len(received) == 1
    assert received[0].user_uuid == result.user.uuid
    assert received[0].email == "test@example.com"


@pytest.mark.asyncio
async def test_prune_removes_user(registered_user, user_repo, event_bus) -> None:
    result = await registered_user
    uc = PruneUserUseCase(user_repo=user_repo, event_bus=event_bus)
    cmd = PruneUserCommand(uuid=result.user.uuid)
    pruned = await uc.execute(cmd)
    assert pruned.user.uuid == result.user.uuid
    assert await user_repo.get_by_uuid(result.user.uuid) is None


@pytest.mark.asyncio
async def test_prune_user_not_found(user_repo, event_bus) -> None:
    uc = PruneUserUseCase(user_repo=user_repo, event_bus=event_bus)
    cmd = PruneUserCommand(uuid="nonexistent")
    with pytest.raises(UserNotFoundError):
        await uc.execute(cmd)


@pytest.mark.asyncio
async def test_prune_publishes_user_updated_event(registered_user, user_repo, event_bus) -> None:
    result = await registered_user
    received: list[UserUpdatedEvent] = []

    async def handler(event: UserUpdatedEvent) -> None:
        received.append(event)

    event_bus.subscribe(UserUpdatedEvent, handler)

    uc = PruneUserUseCase(user_repo=user_repo, event_bus=event_bus)
    await uc.execute(PruneUserCommand(uuid=result.user.uuid))

    assert len(received) == 1
    assert received[0].user_uuid == result.user.uuid
    assert received[0].email == "test@example.com"


@pytest.mark.asyncio
async def test_get_user_by_uuid(registered_user, user_repo, event_bus) -> None:
    result = await registered_user
    uc = GetUserUseCase(user_repo=user_repo)
    cmd = GetUserByUuidQuery(uuid=result.user.uuid)
    user = await uc.by_uuid(cmd)
    assert user.id == result.user.id


@pytest.mark.asyncio
async def test_get_user_by_uuid_not_found(user_repo, event_bus) -> None:
    uc = GetUserUseCase(user_repo=user_repo)
    cmd = GetUserByUuidQuery(uuid="nonexistent")
    with pytest.raises(UserNotFoundError):
        await uc.by_uuid(cmd)


@pytest.mark.asyncio
async def test_get_user_by_username(registered_user, user_repo, event_bus) -> None:
    result = await registered_user
    uc = GetUserUseCase(user_repo=user_repo)
    cmd = GetUserByUsernameQuery(username="testuser")
    user = await uc.by_username(cmd)
    assert user.id == result.user.id


@pytest.mark.asyncio
async def test_get_user_by_email(registered_user, user_repo, event_bus) -> None:
    result = await registered_user
    uc = GetUserUseCase(user_repo=user_repo)
    cmd = GetUserByEmailQuery(email="test@example.com")
    user = await uc.by_email(cmd)
    assert user.id == result.user.id


@pytest.mark.asyncio
async def test_list_users_pagination(user_repo, event_bus) -> None:
    uc_r = RegisterUserUseCase(user_repo=user_repo, event_bus=event_bus)
    for i in range(5):
        await uc_r.execute(
            RegisterUserCommand(
                email=f"user{i}@test.com",
                password="StrongPass1!",
                password2="StrongPass1!",
                username=f"user{i}",
                phone_number=f"+1{i:09d}",
            )
        )

    uc = ListUsersUseCase(user_repo=user_repo)
    cmd = ListUsersQuery(pagination=PaginationParams(offset=0, limit=2))
    result = await uc.execute(cmd)
    assert len(result.page.items) == 2
    assert result.page.total == 5


@pytest.mark.asyncio
async def test_list_users_filters_by_status(user_repo, event_bus) -> None:
    uc_r = RegisterUserUseCase(user_repo=user_repo, event_bus=event_bus)
    for i in range(3):
        await uc_r.execute(
            RegisterUserCommand(
                email=f"user{i}@test.com",
                password="StrongPass1!",
                password2="StrongPass1!",
                username=f"user{i}",
                phone_number=f"+1{i:09d}",
            )
        )

    uc = ListUsersUseCase(user_repo=user_repo)
    cmd = ListUsersQuery(status="pending_verification")
    result = await uc.execute(cmd)
    assert len(result.page.items) == 3

    cmd2 = ListUsersQuery(status="active")
    result2 = await uc.execute(cmd2)
    assert len(result2.page.items) == 0


@pytest.mark.asyncio
async def test_list_users_excludes_deleted_by_default(user_repo, event_bus) -> None:
    uc_r = RegisterUserUseCase(user_repo=user_repo, event_bus=event_bus)
    r = await uc_r.execute(
        RegisterUserCommand(
            email="del@test.com",
            password="StrongPass1!",
            password2="StrongPass1!",
            username="del",
            phone_number="+1234567890",
        )
    )
    assert r.user.uuid is not None
    uc_d = DeleteUserUseCase(user_repo=user_repo, event_bus=event_bus)
    await uc_d.execute(DeleteUserCommand(uuid=r.user.uuid))

    uc = ListUsersUseCase(user_repo=user_repo)
    result = await uc.execute(ListUsersQuery(include_deleted=True))
    assert result.page.total == 1
