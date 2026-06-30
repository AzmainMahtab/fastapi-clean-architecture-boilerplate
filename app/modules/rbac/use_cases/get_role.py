from app.modules.rbac.cqrs.query import GetRoleByUuidQuery
from app.modules.rbac.domain.entities import Role
from app.modules.rbac.domain.exception import RoleNotFoundError
from app.modules.rbac.domain.interfaces import IRbacRepository


class GetRoleUseCase:
    def __init__(self, rbac_repo: IRbacRepository):
        self.rbac_repo = rbac_repo

    async def by_uuid(self, query: GetRoleByUuidQuery) -> Role:
        role = await self.rbac_repo.get_role_by_uuid(query.uuid)
        if not role:
            raise RoleNotFoundError(f"Role with uuid {query.uuid} not found.")
        return role
