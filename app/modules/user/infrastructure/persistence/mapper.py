from app.modules.user.domain.entities import User, UserStatus
from app.modules.user.domain.value_objects import Email, HashedPassword, PhoneNumber
from app.modules.user.infrastructure.persistence.models import UserModel


def map_to_domain(orm_model: UserModel) -> User:
    return User(
        id=orm_model.id,
        uuid=str(orm_model.uuid) if orm_model.uuid else None,
        email=Email(orm_model.email),
        hashed_password=HashedPassword(orm_model.hashed_password),
        phone_number=PhoneNumber(orm_model.phone_number),
        username=orm_model.username,
        first_name=orm_model.first_name,
        last_name=orm_model.last_name,
        status=UserStatus(orm_model.status),
        created_at=orm_model.created_at,
        updated_at=orm_model.updated_at,
        deleted_at=orm_model.deleted_at,
    )


def map_to_persistence(entity: User) -> UserModel:
    return UserModel(
        id=entity.id,
        uuid=entity.uuid,
        email=entity.email.value,
        hashed_password=entity.hashed_password.value,
        phone_number=entity.phone_number.value,
        username=entity.username,
        first_name=entity.first_name,
        last_name=entity.last_name,
        status=entity.status.value if entity.status else "pending_verification",
        created_at=entity.created_at,
        updated_at=entity.updated_at,
        deleted_at=entity.deleted_at,
    )
