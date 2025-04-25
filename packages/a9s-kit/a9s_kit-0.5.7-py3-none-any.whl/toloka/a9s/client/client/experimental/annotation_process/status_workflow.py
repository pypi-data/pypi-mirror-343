__all__ = [
    'AsyncAnnotationStudioStatusWorkflowClient',
    'StatusWorkflowAnnotationProcessViewStrict',
    'StatusWorkflowConfigViewStrict',
    'StatusWorkflowConfigForm',
    'UpdateStatusWorkflowForm',
    'StatusWorkflowProcessesForm',
]


from pydantic import TypeAdapter

from toloka.a9s.client.base.client import AsyncBaseAnnotationStudioClient
from toloka.a9s.client.base.exception import AnnotationStudioError
from toloka.a9s.client.models.annotation_process.status_workflow import (
    StatusWorkflowAnnotationProcessViewDataStrict,
    StatusWorkflowConfigBatchForm,
    StatusWorkflowConfigProjectForm,
    StatusWorkflowConfigViewStrict,
)
from toloka.a9s.client.models.annotation_process.view import (
    AnnotationProcessViewStrict,
    StatusWorkflowAnnotationProcessViewStrict,
)
from toloka.a9s.client.models.generated.ai.toloka.a9s.annotation_process.processes.status_workflow.web.ui.form import (
    StatusWorkflowConfigForm,
    StatusWorkflowProcessesForm,
    UpdateStatusWorkflowForm,
)
from toloka.a9s.client.models.utils import model_dump_a9s


class AsyncAnnotationStudioStatusWorkflowClient(AsyncBaseAnnotationStudioClient):
    async def update_status(self, form: UpdateStatusWorkflowForm) -> StatusWorkflowAnnotationProcessViewStrict:
        response = await self.client.make_retriable_request(
            method='PUT',
            url=f'{self.V1_PREFIX}/annotation-processes/status-workflow/update-status',
            body=model_dump_a9s(form),
        )
        return StatusWorkflowAnnotationProcessViewStrict.model_validate(response.json())

    async def set_batch_defaults(self, form: StatusWorkflowConfigBatchForm) -> StatusWorkflowConfigViewStrict:
        response = await self.client.make_request(
            method='POST',
            url=f'{self.UI_API_PREFIX}/annotation-processes/status-workflow/set-batch-defaults',
            body=model_dump_a9s(form),
        )
        return StatusWorkflowConfigViewStrict.model_validate(response.json())

    async def set_project_defaults(self, form: StatusWorkflowConfigProjectForm) -> StatusWorkflowConfigViewStrict:
        response = await self.client.make_request(
            method='POST',
            url=f'{self.UI_API_PREFIX}/annotation-processes/status-workflow/set-project-defaults',
            body=model_dump_a9s(form),
        )
        return StatusWorkflowConfigViewStrict.model_validate(response.json())

    async def get_project_defaults(self, project_id: str) -> StatusWorkflowConfigViewStrict | None:
        try:
            response = await self.client.make_request(
                method='GET',
                params={'project_id': project_id},
                url=f'{self.UI_API_PREFIX}/annotation-processes/status-workflow/get-project-defaults',
            )
        except AnnotationStudioError as e:
            if e.status == 404:
                return None
            raise e
        return StatusWorkflowConfigViewStrict.model_validate(response.json())

    async def get_batch_defaults(self, batch_id: str) -> StatusWorkflowConfigViewStrict | None:
        try:
            response = await self.client.make_request(
                method='GET',
                params={'batch_id': batch_id},
                url=f'{self.UI_API_PREFIX}/annotation-processes/status-workflow/get-batch-defaults',
            )
        except AnnotationStudioError as e:
            if e.status == 404:
                return None
            raise e
        return StatusWorkflowConfigViewStrict.model_validate(response.json())

    async def get_possible_statuses(self, batch_id: str) -> list[str]:
        response = await self.client.make_retriable_request(
            method='GET',
            url=f'{self.UI_API_PREFIX}/annotation-processes/status-workflow/get-possible-statuses',
            params={'batch_id': batch_id},
        )
        return TypeAdapter(list[str]).validate_python(response.json())

    async def set_default_config(
        self, form: StatusWorkflowProcessesForm
    ) -> AnnotationProcessViewStrict[StatusWorkflowAnnotationProcessViewDataStrict]:
        response = await self.client.make_request(
            method='POST',
            url=f'{self.UI_API_PREFIX}/annotation-processes/status-workflow/set-default-config',
            body=model_dump_a9s(form),
        )
        return AnnotationProcessViewStrict.model_validate(response.json())
