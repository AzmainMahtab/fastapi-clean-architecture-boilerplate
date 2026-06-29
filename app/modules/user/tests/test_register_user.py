import pytest

from app.modules.user.cqrs.command import RegisterUserCommand
from app.modules.user.domain.events import UserRegisteredEvent
from app.modules.user.domain.exception import UserAlreadyExistsError
from app.modules.user.use_cases.register_user import RegisterUserUseCase


@pytest.mark.asyncio
async def test_register_user_success(user_repo, event_bus) -> None:
    use_case = RegisterUserUseCase(user_repo=user_repo, event_bus=event_bus)
    command = RegisterUserCommand(
        email="test@example.com",
        password="securePass123!",
        password2="securePass123!",
        username="testuser",
        phone_number="+1234567890",
    )
    result = await use_case.execute(command)

    assert result.user.id is not None
    assert result.user.email.value == "test@example.com"
    assert result.user.username == "testuser"
    assert result.user.phone_number.value == "+1234567890"
    assert result.user.status.value == "pending_verification"


@pytest.mark.asyncio
async def test_register_duplicate_email_raises_error(user_repo, event_bus) -> None:
    use_case = RegisterUserUseCase(user_repo=user_repo, event_bus=event_bus)
    command = RegisterUserCommand(
        email="dupe@example.com",
        password="securePass123!",
        password2="securePass123!",
        username="user1",
        phone_number="+1111111111",
    )
    await use_case.execute(command)

    with pytest.raises(UserAlreadyExistsError):
        command2 = RegisterUserCommand(
            email="dupe@example.com",
            password="securePass123!",
            password2="securePass123!",
            username="user2",
            phone_number="+2222222222",
        )
        await use_case.execute(command2)


@pytest.mark.asyncio
async def test_register_publishes_event(user_repo, event_bus) -> None:
    received_events: list[UserRegisteredEvent] = []

    async def handler(event: UserRegisteredEvent) -> None:
        received_events.append(event)

    event_bus.subscribe(UserRegisteredEvent, handler)

    use_case = RegisterUserUseCase(user_repo=user_repo, event_bus=event_bus)
    command = RegisterUserCommand(
        email="event@test.com",
        password="securePass123!",
        password2="securePass123!",
        username="eventuser",
        phone_number="+3333333333",
        first_name="Event",
        last_name="Test",
    )
    await use_case.execute(command)

    assert len(received_events) == 1
    event = received_events[0]
    assert event.email.value == "event@test.com"
    assert event.username == "eventuser"
    assert event.phone_number.value == "+3333333333"
    assert event.first_name == "Event"
    assert event.last_name == "Test"


@pytest.mark.asyncio
async def test_register_no_event_on_duplicate(user_repo, event_bus) -> None:
    received_events: list[UserRegisteredEvent] = []

    async def handler(event: UserRegisteredEvent) -> None:
        received_events.append(event)

    event_bus.subscribe(UserRegisteredEvent, handler)

    use_case = RegisterUserUseCase(user_repo=user_repo, event_bus=event_bus)
    cmd = RegisterUserCommand(
        email="noevent@test.com",
        password="StrongPass1!",
        password2="StrongPass1!",
        username="noeventuser",
        phone_number="+4444444444",
    )

    await use_case.execute(cmd)
    assert len(received_events) == 1

    with pytest.raises(UserAlreadyExistsError):
        cmd2 = RegisterUserCommand(
            email="noevent@test.com",
            password="StrongPass1!",
            password2="StrongPass1!",
            username="otheruser",
            phone_number="+5555555555",
        )
        await use_case.execute(cmd2)
    assert len(received_events) == 1
