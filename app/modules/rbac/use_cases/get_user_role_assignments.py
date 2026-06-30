from app.modules.rbac.cqrs.query import GetUserRolesQuery
from app.modules.rbac.cqrs.result import UserRoleAssignmentsResult
from app.modules.rbac.domain.interfaces import IRbacRepository


class GetUserRoleAssignmentsUseCase:
    def __init__(self, rbac_repo: IRbacRepository):
        self.rbac_repo = rbac_repo

    async def execute(self, query: GetUserRolesQuery) -> UserRoleAssignmentsResult:
        assignments = await self.rbac_repo.get_user_role_assignments(query.user_id)
        return UserRoleAssignmentsResult(assignments=assignments)
