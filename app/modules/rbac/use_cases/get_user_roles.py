from app.modules.rbac.cqrs.query import GetUserRolesQuery
from app.modules.rbac.cqrs.result import UserRolesResult
from app.modules.rbac.domain.interfaces import IRbacRepository


class GetUserRolesUseCase:
    def __init__(self, rbac_repo: IRbacRepository):
        self.rbac_repo = rbac_repo

    async def execute(self, query: GetUserRolesQuery) -> UserRolesResult:
        roles = await self.rbac_repo.get_user_roles(query.user_id)
        return UserRolesResult(roles=roles)
