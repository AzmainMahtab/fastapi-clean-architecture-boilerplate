from app.modules.otp.domain.entities import OneTimePassword
from app.modules.otp.domain.value_objects import OtpType
from app.modules.otp.infrastructure.persistence.models import OtpModel


import uuid


def map_to_domain(orm_model: OtpModel) -> OneTimePassword:
    return OneTimePassword(
        id=orm_model.id,
        uuid=str(orm_model.uuid) if orm_model.uuid else None,
        user_uuid=str(orm_model.user_uuid) if orm_model.user_uuid else "",
        otp_type=OtpType(orm_model.otp_type),
        code_hash=orm_model.code_hash,
        is_used=orm_model.is_used,
        expires_at=orm_model.expires_at,
        created_at=orm_model.created_at,
        updated_at=orm_model.updated_at,
    )


def map_to_persistence(entity: OneTimePassword) -> OtpModel:
    return OtpModel(
        id=entity.id,
        uuid=uuid.UUID(entity.uuid) if entity.uuid else None,
        user_uuid=uuid.UUID(entity.user_uuid) if entity.user_uuid else None,
        otp_type=entity.otp_type.value,
        code_hash=entity.code_hash,
        is_used=entity.is_used,
        expires_at=entity.expires_at,
        created_at=entity.created_at,
        updated_at=entity.updated_at,
    )
