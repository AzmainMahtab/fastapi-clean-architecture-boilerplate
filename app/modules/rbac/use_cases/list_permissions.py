from app.core.pagination import Page
from app.modules.rbac.cqrs.query import ListPermissionsQuery
from app.modules.rbac.cqrs.result import ListPermissionsResult
from app.modules.rbac.domain.interfaces import IRbacRepository


class ListPermissionsUseCase:
    def __init__(self, rbac_repo: IRbacRepository):
        self.rbac_repo = rbac_repo

    async def execute(self, query: ListPermissionsQuery) -> ListPermissionsResult:
        permissions, total = await self.rbac_repo.list_permissions(pagination=query.pagination)
        page = Page(items=permissions, total=total, offset=query.pagination.offset, limit=query.pagination.limit)
        return ListPermissionsResult(page=page)
