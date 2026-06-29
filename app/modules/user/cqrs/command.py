from dataclasses import dataclass


@dataclass(frozen=True)
class RegisterUserCommand:
    email: str
    password: str
    password2: str
    username: str
    phone_number: str
    first_name: str | None = None
    last_name: str | None = None


@dataclass(frozen=True)
class UpdateUserStatusCommand:
    uuid: str
    new_status: str


@dataclass(frozen=True)
class DeleteUserCommand:
    uuid: str


@dataclass(frozen=True)
class PruneUserCommand:
    uuid: str


@dataclass(frozen=True)
class RestoreUserByUuidCommand:
    uuid: str
