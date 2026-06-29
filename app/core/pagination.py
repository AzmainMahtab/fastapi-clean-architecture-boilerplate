from dataclasses import dataclass

from pydantic import BaseModel, Field

from app.core.settings import settings

DEFAULT_PAGE_SIZE = settings.DEFAULT_PAGE_SIZE
MAX_PAGE_SIZE = settings.MAX_PAGE_SIZE


@dataclass(frozen=True)
class PaginationParams:
    offset: int = 0
    limit: int = DEFAULT_PAGE_SIZE


@dataclass(frozen=True)
class Page[T]:
    items: list[T]
    total: int
    offset: int
    limit: int


class PaginatedResponse[T](BaseModel):
    items: list[T] = Field(description="List of items in the current page.")
    total: int = Field(description="Total number of items matching the query across all pages.")
    offset: int = Field(description="Number of skipped records for pagination.")
    limit: int = Field(description="Maximum number of records returned in this page.")
