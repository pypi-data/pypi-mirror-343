__all__ = ['AsyncAnnotationStudioTemporalClient']

from toloka.a9s.client.base.client import AsyncBaseAnnotationStudioClient
from toloka.a9s.client.client.experimental.annotation_process.temporal.logs import (
    AsyncAnnotationStudioTemporalLogsClient,
)
from toloka.a9s.client.models.annotation_process.temporal import (
    BatchTemporalConfigFormStrict,
    ProjectTemporalConfigFormStrict,
    TemporalConfigViewStrict,
)
from toloka.a9s.client.models.annotation_process.view import TemporalAnnotationProcessViewStrict
from toloka.a9s.client.models.generated.ai.toloka.a9s.annotation_process.processes.temporal.web.form import (
    UpdateTemporalForm,
)
from toloka.a9s.client.models.utils import model_dump_a9s
from toloka.common.http.client import AsyncHttpClient


class AsyncAnnotationStudioTemporalClient(AsyncBaseAnnotationStudioClient):
    logs: AsyncAnnotationStudioTemporalLogsClient

    def __init__(self, transport: AsyncHttpClient) -> None:
        super().__init__(transport)
        self.logs = AsyncAnnotationStudioTemporalLogsClient(transport)

    async def update(self, form: UpdateTemporalForm) -> TemporalAnnotationProcessViewStrict:
        """Update an existing temporal annotation process.

        Args:
            form: The update form containing the new configuration for the process

        Returns:
            TemporalAnnotationProcessViewStrict: The updated temporal annotation process view
        """
        response = await self.client.make_retriable_request(
            method='PUT',
            url=f'{self.V1_PREFIX}/annotation-processes/temporal/update',
            body=model_dump_a9s(form),
        )
        return TemporalAnnotationProcessViewStrict.model_validate(response.json())

    async def set_project_defaults(self, form: ProjectTemporalConfigFormStrict) -> TemporalConfigViewStrict:
        """Set default configuration for temporal annotation processes at the project level.

        Args:
            form: The configuration form containing the default settings

        Returns:
            TemporalConfigViewStrict: The updated temporal configuration view
        """
        response = await self.client.make_retriable_request(
            method='POST',
            url=f'{self.V1_PREFIX}/annotation-processes/temporal/set-project-defaults',
            body=model_dump_a9s(form),
        )
        return TemporalConfigViewStrict.model_validate(response.json())

    async def set_batch_defaults(self, form: BatchTemporalConfigFormStrict) -> TemporalConfigViewStrict:
        """Set default configuration for temporal annotation processes at the batch level.

        Args:
            form: The configuration form containing the default settings

        Returns:
            TemporalConfigViewStrict: The updated temporal configuration view
        """
        response = await self.client.make_retriable_request(
            method='POST',
            url=f'{self.V1_PREFIX}/annotation-processes/temporal/set-batch-defaults',
            body=model_dump_a9s(form),
        )
        return TemporalConfigViewStrict.model_validate(response.json())
