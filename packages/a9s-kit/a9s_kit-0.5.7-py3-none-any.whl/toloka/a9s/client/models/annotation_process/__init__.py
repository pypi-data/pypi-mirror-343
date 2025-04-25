# pyright: reportGeneralTypeIssues=false

from typing import Annotated, Sequence, TypeGuard, overload

from pydantic import Field

from toloka.a9s.client.models.annotation_process.quorum import (
    QuorumAnnotationProcessParametersStrict,
)
from toloka.a9s.client.models.annotation_process.status_workflow import (
    StatusWorkflowAnnotationProcessParametersStrict,
)
from toloka.a9s.client.models.annotation_process.temporal import (
    TemporalAnnotationProcessParametersStrict,
    TemporalAnnotationProcessViewDataStrict,
)
from toloka.a9s.client.models.annotation_process.view import (
    AnnotationProcessData,
    AnnotationProcessDataType,
    AnnotationProcessViewStrict,
    TemporalAnnotationProcessViewStrict,
    UnrecognizedAnnotationProcessViewDataStrict,
)
from toloka.a9s.client.models.generated.ai.toloka.a9s.annotation_process.web.ui.view import (
    AnnotationProcessListView,
)
from toloka.a9s.client.models.generated.ai.toloka.a9s.annotation_process.web.v1.upload import (
    UploadFormV1,
    UploadFormV1Data,
    UploadViewV1,
    UploadViewV1Data,
)
from toloka.a9s.client.models.types import AnnotationGroupId, AnnotationId
from toloka.a9s.client.models.utils import none_default_validator

AnnotationProcessViewStrictVariant = AnnotationProcessViewStrict[
    Annotated[
        AnnotationProcessData,
        Field(discriminator='type'),
    ]
    | UnrecognizedAnnotationProcessViewDataStrict
]


class AnnotationProcessListViewStrict(AnnotationProcessListView):
    processes: Annotated[
        Sequence[AnnotationProcessViewStrictVariant],
        none_default_validator(default_factory=list),
    ]


class UploadViewV1DataStrict(UploadViewV1Data):
    annotation_id: AnnotationId | None = None
    annotation_group_id: AnnotationGroupId


class UploadViewV1Strict(UploadViewV1):
    data: Sequence[UploadViewV1DataStrict]


@overload
def is_annotation_process_instance(
    process: AnnotationProcessViewStrictVariant,
    data_type: type[TemporalAnnotationProcessViewDataStrict],
) -> TypeGuard[TemporalAnnotationProcessViewStrict]: ...


@overload
def is_annotation_process_instance(
    process: AnnotationProcessViewStrictVariant,
    data_type: type[AnnotationProcessDataType],
) -> TypeGuard[AnnotationProcessViewStrict[AnnotationProcessDataType]]: ...


def is_annotation_process_instance(
    process: AnnotationProcessViewStrictVariant,
    data_type: type[AnnotationProcessDataType],
) -> TypeGuard[AnnotationProcessViewStrict[AnnotationProcessDataType]]:
    return isinstance(process.data, data_type)


class UploadFormV1DataStrict(UploadFormV1Data):
    params: (
        Sequence[
            QuorumAnnotationProcessParametersStrict
            | StatusWorkflowAnnotationProcessParametersStrict
            | TemporalAnnotationProcessParametersStrict
        ]
        | None
    ) = None


class UploadFormV1Strict(UploadFormV1):
    data: Sequence[UploadFormV1DataStrict]
