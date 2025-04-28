from typing import Any, Optional
from urllib.parse import urlparse
from ninja import Schema, Field
from ninja.pagination import PaginationBase


class PageNumberPagination(PaginationBase):
    "DRF compatible Page number pagination"

    items_attribute = "results"

    class Input(Schema):
        page: int = Field(1, ge=1)

    class Output(Schema):
        results: list[Any]
        count: int
        next: Optional[str] = None
        previous: Optional[str] = None

    def __init__(self, page_size: int = 20, **kwargs):
        self.page_size = page_size
        super().__init__(**kwargs)

    def paginate_queryset(
        self,
        queryset,
        pagination: Input,
        *,
        request,
        **params,
    ):
        offset = (pagination.page - 1) * self.page_size
        count = self._items_count(queryset)
        return {
            "results": queryset[offset : offset + self.page_size],
            "next": self.get_next_link(request, count, pagination.page),
            "previous": self.get_previous_link(request, count, pagination.page),
            "count": count,
        }

    def has_next(self, count: int, page: int):
        return count > (page * self.page_size)

    def has_previous(self, count: int, page: int):
        return page > 1

    def get_next_link(self, request, count: int, page: int):
        if not self.has_next(count, page):
            return None
        url = request.get_full_path()
        page_number = page + 1
        return urlparse(url)._replace(query=f"page={page_number}").geturl()

    def get_previous_link(self, request, count: int, page: int):
        if not self.has_previous(count, page):
            return None
        url = request.get_full_path()
        page_number = page - 1
        return urlparse(url)._replace(query=f"page={page_number}").geturl()


class LimitOffsetPagination(PaginationBase):
    "DRF compatible LIMIT/Offset pagination"

    items_attribute = "results"

    class Input(Schema):
        limit: int = Field(20, ge=1)
        offset: int = Field(0, ge=0)

    class Output(Schema):
        results: list[Any]
        count: int
        next: Optional[str] = None
        previous: Optional[str] = None

    def __init__(self, page_size: int = 20, **kwargs):
        self.page_size = page_size
        super().__init__(**kwargs)

    def paginate_queryset(
        self,
        queryset,
        pagination: Input,
        *,
        request,
        **params,
    ):
        offset = pagination.offset
        count = self._items_count(queryset)
        return {
            "results": queryset[offset : offset + pagination.limit],
            "next": self.get_next_link(request, count, pagination.offset),
            "previous": self.get_previous_link(request, count, pagination.offset),
            "count": count,
        }

    def has_next(self, count: int, offset: int):
        return count > offset

    def has_previous(self, count: int, offset: int):
        return offset > 0

    def get_next_link(self, request, count: int, offset: int):
        if not self.has_next(count, offset):
            return None
        url = request.get_full_path()
        new_offset = offset - self.page_size
        return urlparse(url)._replace(query=f"offset={new_offset}").geturl()

    def get_previous_link(self, request, count: int, offset: int):
        if not self.has_previous(count, offset):
            return None
        url = request.get_full_path()
        new_offset = offset - self.page_size
        return urlparse(url)._replace(query=f"offset={new_offset}").geturl()
