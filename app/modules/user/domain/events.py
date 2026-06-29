from dataclasses import dataclass

from app.modules.user.domain.value_objects import Email, PhoneNumber


@dataclass(frozen=True)
class UserRegisteredEvent:
    """Domain Event:
    Fired when a user successfully registers.
    """

    email: Email
    username: str
    phone_number: PhoneNumber
    first_name: str | None
    last_name: str | None


@dataclass(frozen=True)
class UserUpdatedEvent:
    """Domain Event: Fired when a user's profile or status changes.

    Published after any user mutation (status update, soft delete, restore,
    permanent delete) so that cross-cutting concerns like cache invalidation,
    audit logging, or webhook delivery can react without coupling modules.
    """

    user_uuid: str
    email: str
