from datetime import UTC, datetime, timedelta

import pytest

from app.modules.otp.cqrs.command import GenerateOtpCommand, ValidateOtpCommand
from app.modules.otp.domain.entities import OneTimePassword
from app.modules.otp.domain.events import OtpValidatedEvent
from app.modules.otp.domain.exceptions import InvalidOtpError, OtpAlreadyUsedError, OtpExpiredError
from app.modules.otp.domain.value_objects import OtpType
from app.modules.otp.use_cases.generate_otp import GenerateOtpUseCase
from app.modules.otp.use_cases.validate_otp import ValidateOtpUseCase


@pytest.mark.asyncio
async def test_validate_otp_success(otp_repo, cache, event_bus):
    """A valid OTP code is accepted and marked as used."""
    generate = GenerateOtpUseCase(otp_repo=otp_repo, cache=cache, event_bus=event_bus)
    validate = ValidateOtpUseCase(otp_repo=otp_repo, cache=cache, event_bus=event_bus)

    # Generate an OTP (with NullCache we need to seed the DB)
    gen_command = GenerateOtpCommand(user_uuid="user-001", otp_type=OtpType.LOGIN)
    gen_result = await generate.execute(gen_command)

    # Bypass cache: retrieve the OTP entity and verify via DB fallback
    # Since NullCache returns None, validate will fall through to DB hash check
    # We need the actual generated code, but GenerateOtpUseCase doesn't return it.
    # Let's inspect the OTP entity directly.
    otp = await otp_repo.find_by_uuid(gen_result.otp_uuid)
    assert otp is not None

    # For NullCache, the validate will use DB fallback. We can't know the code.
    # Instead, let's test with a code we know by seeding the cache directly.
    # Actually, let's test the cache path by setting the cache ourselves.
    from app.core.hasher import get_password_hash

    # Test 1: Cache path - set cache directly with known code
    known_code = "123456"
    await cache.set("otp:user-002:login-otp", {"code": known_code, "uuid": gen_result.otp_uuid}, 300)

    # Create a matching OTP in the repo
    otp2 = OneTimePassword(
        user_uuid="user-002",
        otp_type=OtpType.LOGIN,
        code_hash=get_password_hash(known_code),
        expires_at=datetime.now(UTC) + timedelta(seconds=300),
    )
    otp2 = await otp_repo.create(otp2)

    val_command = ValidateOtpCommand(user_uuid="user-002", otp_type=OtpType.LOGIN, code=known_code)
    result = await validate.execute(val_command)

    assert result.success is True
    assert result.otp_uuid == otp2.uuid

    # OTP should now be marked as used
    used_otp = await otp_repo.find_by_uuid(otp2.uuid)
    assert used_otp is not None
    assert used_otp.is_used is True


@pytest.mark.asyncio
async def test_validate_otp_db_fallback(otp_repo, cache, event_bus):
    """OTP validation falls back to DB hash check when cache is empty."""
    from app.core.hasher import get_password_hash

    known_code = "654321"
    otp = OneTimePassword(
        user_uuid="user-003",
        otp_type=OtpType.LOGIN,
        code_hash=get_password_hash(known_code),
        expires_at=datetime.now(UTC) + timedelta(seconds=300),
    )
    otp = await otp_repo.create(otp)

    validate = ValidateOtpUseCase(otp_repo=otp_repo, cache=cache, event_bus=event_bus)
    command = ValidateOtpCommand(user_uuid="user-003", otp_type=OtpType.LOGIN, code=known_code)
    result = await validate.execute(command)

    assert result.success is True


@pytest.mark.asyncio
async def test_validate_otp_invalid_code(otp_repo, cache, event_bus):
    """An invalid OTP code raises InvalidOtpError."""
    from app.core.hasher import get_password_hash

    otp = OneTimePassword(
        user_uuid="user-004",
        otp_type=OtpType.LOGIN,
        code_hash=get_password_hash("111111"),
        expires_at=datetime.now(UTC) + timedelta(seconds=300),
    )
    await otp_repo.create(otp)

    validate = ValidateOtpUseCase(otp_repo=otp_repo, cache=cache, event_bus=event_bus)
    command = ValidateOtpCommand(user_uuid="user-004", otp_type=OtpType.LOGIN, code="222222")

    with pytest.raises(InvalidOtpError):
        await validate.execute(command)


@pytest.mark.asyncio
async def test_validate_otp_expired(otp_repo, cache, event_bus):
    """An expired OTP raises OtpExpiredError."""
    from app.core.hasher import get_password_hash

    otp = OneTimePassword(
        user_uuid="user-005",
        otp_type=OtpType.LOGIN,
        code_hash=get_password_hash("111111"),
        expires_at=datetime.now(UTC) - timedelta(seconds=10),  # already expired
    )
    await otp_repo.create(otp)

    validate = ValidateOtpUseCase(otp_repo=otp_repo, cache=cache, event_bus=event_bus)
    command = ValidateOtpCommand(user_uuid="user-005", otp_type=OtpType.LOGIN, code="111111")

    with pytest.raises(OtpExpiredError):
        await validate.execute(command)


@pytest.mark.asyncio
async def test_validate_otp_already_used(otp_repo, cache, event_bus):
    """An already-used OTP raises OtpAlreadyUsedError."""
    from app.core.hasher import get_password_hash

    otp = OneTimePassword(
        user_uuid="user-006",
        otp_type=OtpType.LOGIN,
        code_hash=get_password_hash("111111"),
        is_used=True,
        expires_at=datetime.now(UTC) + timedelta(seconds=300),
    )
    await otp_repo.create(otp)

    validate = ValidateOtpUseCase(otp_repo=otp_repo, cache=cache, event_bus=event_bus)
    command = ValidateOtpCommand(user_uuid="user-006", otp_type=OtpType.LOGIN, code="111111")

    with pytest.raises(OtpAlreadyUsedError):
        await validate.execute(command)


@pytest.mark.asyncio
async def test_validate_otp_publishes_event(otp_repo, cache, event_bus):
    """OtpValidatedEvent is published on successful validation."""
    from app.core.hasher import get_password_hash

    published_events = []

    async def capture_event(event):
        published_events.append(event)

    event_bus.subscribe(OtpValidatedEvent, capture_event)

    known_code = "123123"
    otp = OneTimePassword(
        user_uuid="user-007",
        otp_type=OtpType.LOGIN,
        code_hash=get_password_hash(known_code),
        expires_at=datetime.now(UTC) + timedelta(seconds=300),
    )
    otp = await otp_repo.create(otp)

    validate = ValidateOtpUseCase(otp_repo=otp_repo, cache=cache, event_bus=event_bus)
    command = ValidateOtpCommand(user_uuid="user-007", otp_type=OtpType.LOGIN, code=known_code)
    result = await validate.execute(command)

    assert len(published_events) == 1
    assert published_events[0].user_uuid == "user-007"
    assert published_events[0].otp_type == OtpType.LOGIN
    assert published_events[0].otp_uuid == result.otp_uuid
