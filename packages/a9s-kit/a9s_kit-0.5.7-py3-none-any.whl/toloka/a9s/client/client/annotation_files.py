from httpx._types import ResponseContent

from toloka.a9s.client.base.client import AsyncBaseAnnotationStudioClient
from toloka.a9s.client.models.types import AnnotationId
from toloka.common.http.client import AsyncHttpClient


class AsyncAnnotationStudioAnnotationFilesClient(AsyncBaseAnnotationStudioClient):
    def __init__(self, transport: AsyncHttpClient) -> None:
        super().__init__(transport)

    async def get(self, file_id: str) -> ResponseContent:
        response = await self.client.make_retriable_request(
            method='GET',
            url=f'{self.V1_PREFIX}/annotation-files/download/{file_id}',
            follow_redirects=True,
        )
        if response.content is None:
            raise ValueError('File not found')
        return response.content

    async def share(self, file_id: str, annotation_id: AnnotationId) -> None:
        await self.client.make_retriable_request(
            method='POST',
            url=f'{self.V1_PREFIX}/annotation-files/share/{file_id}',
            body={'annotation_id': annotation_id},
        )
