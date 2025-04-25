# pyright: reportGeneralTypeIssues=false


from typing import Any, Literal, Mapping, Sequence

from pydantic import BaseModel, SerializeAsAny

from toloka.a9s.client.models.generated.ai.toloka.a9s.annotation.parameters import TemporalAnnotationProcessParameters
from toloka.a9s.client.models.generated.ai.toloka.a9s.annotation_process.model.temporal import (
    TemporalAnnotationProcessView,
)
from toloka.a9s.client.models.generated.ai.toloka.a9s.annotation_process.processes.temporal.web.form import (
    TemporalConfigForm,
    UpdateTemporalForm,
    UpdateTemporalLogForm,
)
from toloka.a9s.client.models.generated.ai.toloka.a9s.annotation_process.processes.temporal.web.view import (
    TemporalConfigView,
    TemporalLogsView,
    TemporalLogView,
)
from toloka.a9s.client.models.types import (
    AnnotationProcessId,
    BatchId,
    ProjectId,
    TemporalConfigId,
    TemporalLogId,
    TemporalLogStatus,
    WorkflowItemStatus,
)


class TemporalConfigViewStrict(TemporalConfigView):
    id: TemporalConfigId
    workflow_name: str
    solution_id: str


class TemporalAnnotationProcessViewDataStrict(TemporalAnnotationProcessView):
    type: Literal['temporal'] = 'temporal'

    workflow_name: str
    solution_id: str
    instance_id: str
    status: WorkflowItemStatus
    priority: int
    version: int
    upload_id: str
    source_file_name: str
    submitted_items_link_id: str | None = None
    input_data: Mapping[str, Any]


class TemporalAnnotationProcessParametersStrict(TemporalAnnotationProcessParameters):
    type: Literal['temporal'] = 'temporal'

    temporal_status: WorkflowItemStatus
    source_file_name: str
    version: int
    upload_id: str
    submitted_items_link_id: str | None
    priority: int
    instance_id: str
    input_data: Mapping[str, Any]
    completed: bool


class TemporalLogViewStrict(TemporalLogView):
    id: TemporalLogId
    snapshot: Mapping[str, Any]
    temporal_process_id: str
    created_at: str
    modified_at: str
    step_name: str
    component_name: str | None = None
    input_data: Mapping[str, Any] | None = None
    output_data: Mapping[str, Any] | None = None
    meta: Mapping[str, Any]
    step_type: str
    status: TemporalLogStatus
    vendor_type: str
    steps_history: Sequence[Mapping[str, Any]]
    run_id: str
    workflow_name: str
    retry_key: str
    workflow_id: str
    iteration: int
    dimensions: Mapping[str, Any] | None = None
    is_deleted: bool


class UpdateTemporalLogFormStrict(UpdateTemporalLogForm):
    snapshot: Mapping[str, Any]
    step_name: str
    component_name: str | None
    step_type: str
    status: TemporalLogStatus
    input_data: Mapping[str, Any] | SerializeAsAny[BaseModel] | None
    output_data: Mapping[str, Any] | SerializeAsAny[BaseModel] | None
    meta: Mapping[str, Any] | SerializeAsAny[BaseModel]
    steps_history: Sequence[Mapping[str, Any] | SerializeAsAny[BaseModel]]
    run_id: str
    workflow_name: str
    vendor_type: str
    retry_key: str
    workflow_id: str
    iteration: int
    dependent_item_ids: Sequence[str] | None
    dimensions: Mapping[str, Any] | SerializeAsAny[BaseModel] | None
    deleted: bool


class TemporalLogsViewStrict(TemporalLogsView):
    logs: Sequence[TemporalLogViewStrict]


class UpdateTemporalFormStrict(UpdateTemporalForm):
    annotation_process_id: AnnotationProcessId
    temporal_status: WorkflowItemStatus
    source_file_name: str
    version: int
    upload_id: str
    submitted_items_link_id: str | None
    priority: int
    instance_id: str
    input_data: Mapping[str, Any]
    completed: bool


class ProjectTemporalConfigFormStrict(TemporalConfigForm):
    project_id: ProjectId
    batch_id: None = None
    workflow_name: str
    solution_id: str


class BatchTemporalConfigFormStrict(TemporalConfigForm):
    project_id: None = None
    batch_id: BatchId
    workflow_name: str
    solution_id: str
