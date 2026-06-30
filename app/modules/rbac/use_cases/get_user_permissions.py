from app.modules.rbac.cqrs.query import GetUserPermissionsQuery
from app.modules.rbac.cqrs.result import UserPermissionsResult
from app.modules.rbac.domain.interfaces import IRbacRepository


class GetUserPermissionsUseCase:
    def __init__(self, rbac_repo: IRbacRepository):
        self.rbac_repo = rbac_repo

    async def execute(self, query: GetUserPermissionsQuery) -> UserPermissionsResult:
        permissions = await self.rbac_repo.get_user_permissions(query.user_id)
        return UserPermissionsResult(permissions=permissions)
