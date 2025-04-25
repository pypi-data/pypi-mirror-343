# pyright: reportGeneralTypeIssues=false

from typing import Annotated, Any, Literal, Mapping, Sequence

from pydantic import Field

from toloka.a9s.client.models.data_manager.fields import FilterField, SortField
from toloka.a9s.client.models.generated.ai.toloka.a9s.data_manager.web.ui.assignee import AccountView
from toloka.a9s.client.models.generated.ai.toloka.a9s.data_manager.web.ui.search import (
    SearchCountView,
    SearchForm,
    SearchFormSort,
    SearchView,
    SearchViewBatchProcessInfo,
    SearchViewRow,
    SearchViewRowElement,
    SearchViewRowElementTemporal,
    SearchViewRowElementTemporalTemporalLog,
    SearchViewRowQuorum,
)
from toloka.a9s.client.models.generated.ai.toloka.platform.common.web.form.search import (
    ListFilterCondition,
    SingleFilterCondition,
)
from toloka.a9s.client.models.types import (
    AnnotationGroupId,
    AnnotationId,
    AnnotationProcessId,
    BatchId,
    ProjectId,
    TemporalLogId,
    TemporalLogStatus,
    WorkflowItemStatus,
)
from toloka.a9s.client.models.utils import none_default_validator


class AccountViewStrict(AccountView):
    account_id: str
    display_name: str
    login: str
    username: str


class QuorumDataManagerView(SearchViewRowQuorum):
    id: str
    completed_count: int
    total_count: int


class SearchViewRowElementTemporalTemporalLogStrict(SearchViewRowElementTemporalTemporalLog):
    id: TemporalLogId
    snapshot: Mapping[str, Any]
    step_name: str
    step_type: str
    status: TemporalLogStatus
    meta: Mapping[str, Any]
    created_at: str
    modified_at: str
    component_name: str | None = None
    input_data: Mapping[str, Any] | None = None
    output_data: Mapping[str, Any] | None = None
    steps_history: Sequence[Mapping[str, Any]]
    vendor_type: str
    iteration: int
    run_id: str
    workflow_id: str
    workflow_name: str
    retry_key: str


class SearchViewRowElementTemporalStrict(SearchViewRowElementTemporal):
    temporal_id: AnnotationProcessId
    temporal_status: WorkflowItemStatus
    source_file_name: str
    version: int
    upload_id: str
    priority: int
    instance_id: str
    input_data: Mapping[str, Any]
    workflow_name: str
    solution_id: str
    submitted_items_link_id: str | None = None
    latest_log: SearchViewRowElementTemporalTemporalLogStrict | None = None


class SearchViewRowElementStrict(SearchViewRowElement):
    annotation_id: AnnotationId
    created_at: str
    modified_at: str
    assignee: AccountViewStrict | None = None
    temporal: SearchViewRowElementTemporalStrict | None = None
    values: Mapping[str, Any]
    metadata: Mapping[str, Any]


class AnnotationGroupDataManagerView(SearchViewRow):
    group_id: AnnotationGroupId
    created_at: str
    modified_at: str | None = None
    annotation_count: int
    quorum: QuorumDataManagerView | None = None
    elements: Sequence[SearchViewRowElementStrict]
    group_values: Mapping[str, Any] | None = None


class SearchViewStrict(SearchView):
    has_more: bool
    data: Annotated[Sequence[AnnotationGroupDataManagerView], none_default_validator(default_factory=list)]
    processes: Annotated[Sequence[SearchViewBatchProcessInfo], none_default_validator(default_factory=list)] | None = (
        None
    )


class SearchCountViewStrict(SearchCountView):
    count: int
    total: int


class SingleFilterConditionStrict(SingleFilterCondition):
    type: Literal['SINGLE_FILTER_CONDITION'] = 'SINGLE_FILTER_CONDITION'
    field: FilterField


class ListFilterConditionStrict(ListFilterCondition):
    type: Literal['LIST_FILTER_CONDITION'] = 'LIST_FILTER_CONDITION'
    conditions: Annotated[
        'Sequence[FilterConditionStrict]',
        Field(max_length=2147483647, min_length=1),
    ]


class SearchFormSortStrict(SearchFormSort):
    field: SortField


FilterConditionStrict = ListFilterConditionStrict | SingleFilterConditionStrict


class SearchFormStrictProject(SearchForm):
    project_id: ProjectId
    batch_id: None = None
    filter: FilterConditionStrict | None = None
    sort_list: Sequence[SearchFormSortStrict] | None = None


class SearchFormStrictBatch(SearchForm):
    batch_id: BatchId
    project_id: None = None
    filter: FilterConditionStrict | None = None
    sort_list: Sequence[SearchFormSortStrict] | None = None


SearchFormStrict = SearchFormStrictProject | SearchFormStrictBatch
