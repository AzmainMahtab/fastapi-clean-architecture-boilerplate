import pytest

from app.modules.auth.infrastructure.event_handlers import create_invalidate_user_caches_handler
from app.modules.user.domain.events import UserUpdatedEvent


@pytest.mark.asyncio
async def test_user_updated_event_invalidates_auth_caches(cache, event_bus) -> None:
    """Verify that the cache invalidation handler deletes auth-owned cache keys."""
    await cache.set("profile:uuid-123", {"name": "Test User"}, 60)
    await cache.set("auth:credentials:test@example.com", {"uuid": "uuid-123"}, 60)

    handler = create_invalidate_user_caches_handler(cache)
    event_bus.subscribe(UserUpdatedEvent, handler)
    await event_bus.publish(UserUpdatedEvent(user_uuid="uuid-123", email="test@example.com"))

    assert await cache.exists("profile:uuid-123") is False
    assert await cache.exists("auth:credentials:test@example.com") is False


@pytest.mark.asyncio
async def test_user_updated_event_nonexistent_keys(cache, event_bus) -> None:
    """Verify the handler does not error when cache keys do not exist."""
    handler = create_invalidate_user_caches_handler(cache)
    event_bus.subscribe(UserUpdatedEvent, handler)
    await event_bus.publish(UserUpdatedEvent(user_uuid="nonexistent", email="ghost@example.com"))
