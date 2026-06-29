from app.modules.user.cqrs.query import GetUserByEmailQuery, GetUserByUsernameQuery, GetUserByUuidQuery
from app.modules.user.domain.entities import User
from app.modules.user.domain.exception import UserNotFoundError
from app.modules.user.domain.interfaces import IUserRepository
from app.modules.user.domain.value_objects import Email


class GetUserUseCase:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    async def by_uuid(self, command: GetUserByUuidQuery) -> User:
        user = await self.user_repo.get_by_uuid(command.uuid)
        if not user:
            raise UserNotFoundError(f"User with uuid {command.uuid} not found.")
        return user

    async def by_username(self, command: GetUserByUsernameQuery) -> User:
        user = await self.user_repo.get_by_username(command.username)
        if not user:
            raise UserNotFoundError(f"User with username {command.username} not found.")
        return user

    async def by_email(self, command: GetUserByEmailQuery) -> User:
        email_vo = Email(command.email)
        user = await self.user_repo.get_by_email(email_vo)
        if not user:
            raise UserNotFoundError(f"User with email {command.email} not found.")
        return user
