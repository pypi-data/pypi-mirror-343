# pyright: reportGeneralTypeIssues=false

from typing import Any, Generic, Mapping, TypeVar

from toloka.a9s.client.models.annotation_process.agreement import AgreementAnnotationProcessViewDataStrict
from toloka.a9s.client.models.annotation_process.annotation_edit_time import (
    AnnotationEditTimeAnnotationProcessViewDataStrict,
)
from toloka.a9s.client.models.annotation_process.metric_provider import MetricProviderAnnotationProcessViewDataStrict
from toloka.a9s.client.models.annotation_process.post_acceptance import PostAcceptanceAnnotationProcessViewDataStrict
from toloka.a9s.client.models.annotation_process.quorum import QuorumAnnotationProcessViewDataStrict
from toloka.a9s.client.models.annotation_process.status_workflow import StatusWorkflowAnnotationProcessViewDataStrict
from toloka.a9s.client.models.annotation_process.temporal import TemporalAnnotationProcessViewDataStrict
from toloka.a9s.client.models.generated.ai.toloka.a9s.annotation_process.model.ParticularAnnotationProcessViewJava.lang.ObjectJava.lang import (  # noqa: E501
    Object,
)
from toloka.a9s.client.models.generated.ai.toloka.a9s.annotation_process.web.ui.view import AnnotationProcessView
from toloka.a9s.client.models.types import AnnotationId, AnnotationProcessId, BatchId, ProjectId


class UnrecognizedAnnotationProcessViewDataStrict(Object):
    type: str


AnnotationProcessData = (
    MetricProviderAnnotationProcessViewDataStrict
    | PostAcceptanceAnnotationProcessViewDataStrict
    | QuorumAnnotationProcessViewDataStrict
    | StatusWorkflowAnnotationProcessViewDataStrict
    | AgreementAnnotationProcessViewDataStrict
    | AnnotationEditTimeAnnotationProcessViewDataStrict
    | TemporalAnnotationProcessViewDataStrict
)


AnnotationProcessDataType = TypeVar(
    'AnnotationProcessDataType',
    bound=AnnotationProcessData | Mapping[str, Any] | UnrecognizedAnnotationProcessViewDataStrict,
)


class AnnotationProcessViewStrict(AnnotationProcessView, Generic[AnnotationProcessDataType]):
    id: AnnotationProcessId
    data: AnnotationProcessDataType  # type: ignore[assignment]
    created_at: str
    modified_at: str
    completed: bool
    project_id: ProjectId
    batch_id: BatchId


class AnnotationScopedAnnotationProcessViewStrict(
    AnnotationProcessViewStrict[AnnotationProcessDataType], Generic[AnnotationProcessDataType]
):
    annotation_id: AnnotationId


PostAcceptanceAnnotationProcessViewStrict = AnnotationProcessViewStrict[PostAcceptanceAnnotationProcessViewDataStrict]
AgreementAnnotationProcessViewStrict = AnnotationProcessViewStrict[AgreementAnnotationProcessViewDataStrict]
AnnotationEditTimeAnnotationProcessViewStrict = AnnotationProcessViewStrict[
    AnnotationEditTimeAnnotationProcessViewDataStrict
]
MetricProviderAnnotationProcessViewStrict = AnnotationProcessViewStrict[MetricProviderAnnotationProcessViewDataStrict]
QuorumAnnotationProcessViewStrict = AnnotationProcessViewStrict[QuorumAnnotationProcessViewDataStrict]
StatusWorkflowAnnotationProcessViewStrict = AnnotationProcessViewStrict[StatusWorkflowAnnotationProcessViewDataStrict]
TemporalAnnotationProcessViewStrict = AnnotationScopedAnnotationProcessViewStrict[
    TemporalAnnotationProcessViewDataStrict
]
