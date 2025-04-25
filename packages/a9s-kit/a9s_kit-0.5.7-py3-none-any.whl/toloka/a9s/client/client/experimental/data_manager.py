__all__ = [
    'AsyncDataManagerClient',
    'SearchFormStrict',
    'SearchFormStrictBatch',
    'SearchFormStrictProject',
]

from typing import AsyncGenerator

from toloka.a9s.client.base.client import AsyncBaseAnnotationStudioClient
from toloka.a9s.client.models.data_manager import (
    AnnotationGroupDataManagerView,
    SearchCountViewStrict,
    SearchFormStrict,
    SearchFormStrictBatch,
    SearchFormStrictProject,
    SearchViewRowElementStrict,
    SearchViewStrict,
)
from toloka.a9s.client.models.generated.ai.toloka.a9s.data_manager.web.ui.search import (
    SearchFormPagination,
)
from toloka.a9s.client.models.utils import model_dump_a9s
from toloka.a9s.client.pagination import async_paginate


class AsyncDataManagerClient(AsyncBaseAnnotationStudioClient):
    API_PREFIX: str = f'{AsyncBaseAnnotationStudioClient.UI_API_PREFIX}/data-manager'
    DEFAULT_LIMIT: int = 100

    async def search_page(self, form: SearchFormStrict) -> SearchViewStrict:
        response = await self.client.make_retriable_request(
            method='PUT',
            url=f'{self.API_PREFIX}/search',
            body=model_dump_a9s(form),
        )
        return SearchViewStrict.model_validate(response.json())

    async def count(self, form: SearchFormStrict) -> SearchCountViewStrict:
        response = await self.client.make_retriable_request(
            method='PUT',
            url=f'{self.API_PREFIX}/count',
            body=model_dump_a9s(form),
        )
        return SearchCountViewStrict.model_validate(response.json())

    async def get_all_groups(self, form: SearchFormStrict) -> AsyncGenerator[AnnotationGroupDataManagerView, None]:
        current_form = form.model_copy(deep=True)
        if current_form.pagination is None:
            current_form.pagination = SearchFormPagination(offset=0, limit=self.DEFAULT_LIMIT)
        pagination = current_form.pagination

        async def get_next_page(page: SearchViewStrict | None) -> SearchViewStrict:
            if page:
                pagination.offset += pagination.limit
            return await self.search_page(current_form)

        row: AnnotationGroupDataManagerView
        async for row in async_paginate(get_next_page=get_next_page):
            yield row

    async def get_all_elements(self, form: SearchFormStrict) -> AsyncGenerator[SearchViewRowElementStrict, None]:
        group: AnnotationGroupDataManagerView
        async for group in self.get_all_groups(form):
            element: SearchViewRowElementStrict
            for element in group.elements:
                yield element
