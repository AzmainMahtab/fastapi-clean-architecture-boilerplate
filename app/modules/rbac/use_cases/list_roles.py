from app.core.pagination import Page
from app.modules.rbac.cqrs.query import ListRolesQuery
from app.modules.rbac.cqrs.result import ListRolesResult
from app.modules.rbac.domain.interfaces import IRbacRepository


class ListRolesUseCase:
    def __init__(self, rbac_repo: IRbacRepository):
        self.rbac_repo = rbac_repo

    async def execute(self, query: ListRolesQuery) -> ListRolesResult:
        roles, total = await self.rbac_repo.list_roles(pagination=query.pagination)
        page = Page(items=roles, total=total, offset=query.pagination.offset, limit=query.pagination.limit)
        return ListRolesResult(page=page)
