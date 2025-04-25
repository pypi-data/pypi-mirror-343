from toloka.a9s.client.base.client import AsyncBaseTolokaClient
from toloka.a9s.client.models.collaboration_item import CollaborationItemPatch, CollaborationItemResponse
from toloka.a9s.client.models.tenant import TenantsView


class AsyncTolokaClient(AsyncBaseTolokaClient):
    async def get_user_tenants(self) -> TenantsView:
        response = await self.client.make_retriable_request(
            method='GET',
            url=f'{self.UI_API_PREFIX}/user/tenant',
        )
        return TenantsView.model_validate(response.json())

    async def get_collaboration_item(self, item_id: str) -> CollaborationItemResponse:
        response = await self.client.make_retriable_request(
            method='GET',
            url=f'{self.UI_API_PREFIX}/tb/collaboration-tool/items/{item_id}?withJson=true',
        )
        return CollaborationItemResponse.model_validate(response.json())

    async def patch_collaboration_items(
        self, item_id: str, updates: list[CollaborationItemPatch]
    ) -> CollaborationItemResponse:
        await self.client.make_retriable_request(
            method='POST',
            url=f'{self.UI_API_PREFIX}/collaboration-tool/items/{item_id}/update-fields',
            body={'updates': [update.model_dump() for update in updates]},
        )
        return await self.get_collaboration_item(item_id=item_id)
