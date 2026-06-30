from app.modules.rbac.cqrs.query import CheckUserPermissionQuery
from app.modules.rbac.cqrs.result import CheckPermissionResult
from app.modules.rbac.domain.interfaces import IRbacRepository


class CheckPermissionUseCase:
    def __init__(self, rbac_repo: IRbacRepository):
        self.rbac_repo = rbac_repo

    async def execute(self, query: CheckUserPermissionQuery) -> CheckPermissionResult:
        has_permission = await self.rbac_repo.user_has_permission(query.user_id, query.permission_name)
        return CheckPermissionResult(has_permission=has_permission)
