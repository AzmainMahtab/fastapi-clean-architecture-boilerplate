from app.core.pagination import Page
from app.modules.user.cqrs.query import ListUsersQuery
from app.modules.user.cqrs.result import ListUsersResult
from app.modules.user.domain.entities import UserStatus
from app.modules.user.domain.interfaces import IUserRepository


class ListUsersUseCase:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    async def execute(self, command: ListUsersQuery) -> ListUsersResult:
        status_enum = UserStatus(command.status) if command.status else None
        users, total = await self.user_repo.list_all(
            status=status_enum, include_deleted=command.include_deleted, pagination=command.pagination
        )
        return ListUsersResult(
            page=Page(items=users, total=total, offset=command.pagination.offset, limit=command.pagination.limit)
        )
