from dataclasses import dataclass


@dataclass(frozen=True)
class GetProfileQuery:
    user_uuid: str
