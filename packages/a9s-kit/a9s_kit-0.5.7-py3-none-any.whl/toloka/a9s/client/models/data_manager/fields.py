import inspect
from copy import deepcopy
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Generic, Literal, NewType, Sequence, TypeVar

from pydantic import GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema
from typing_extensions import Self

NestableSortField = Literal['values']

NestableFilterField = Literal[
    'values',
    'annotation_values',
    'active_edit_values',
    'any_values',
    'metadata',
    'temporal_dimensions',
    'temporal_input_data',
    'temporal_dependent_item_ids',
    'temporal_log_input_data',
    'temporal_log_output_data',
    'temporal_meta',
    'temporal_snapshot',
    'temporal_steps_history',
]


NestableFieldType = TypeVar('NestableFieldType', bound=str, covariant=True)


# pydantic ignores __get_pydantic_core_schema__ for specified generic dataclasses for some reason
if TYPE_CHECKING:

    @dataclass
    class NestedField(str, Generic[NestableFieldType]):
        field: NestableFieldType
        path: Sequence[str]

        @classmethod
        def from_string(cls, value: str) -> 'NestedField[Any]':
            raise NotImplementedError('from_string is not implemented for TYPE_CHECKING')
else:

    @dataclass
    class NestedField(str):
        field: str
        path: Sequence[str]

        def __new__(cls, *args: Any, **kwargs: Any) -> Self:
            bound = inspect.signature(cls.__init__).bind(object(), *args, **kwargs)
            bound.apply_defaults()
            bound_dict = dict(bound.arguments)
            bound_dict.pop('self')

            value = NestedField._params_to_string(
                bound_dict['field'],
                bound_dict['path'],
            )

            return super().__new__(cls, value)

        def __class_getitem__(cls, *args, **kwargs):
            return cls

        def __deepcopy__(self, memo: Any) -> 'NestedField':
            return NestedField(self.field, deepcopy(self.path))

        @classmethod
        def from_string(cls, value: str) -> 'NestedField':
            if '.' not in value:
                return cls(value, [])
            field, path_str = value.split('.', 1)
            path = path_str.split('.')
            return cls(field, path)

        @staticmethod
        def _params_to_string(field: str, path: Sequence[str]) -> str:
            return f'{field}{"." + ".".join(path) if path else ""}'

        def __str__(self) -> str:
            return self._params_to_string(self.field, self.path)

        @classmethod
        def __get_pydantic_core_schema__(cls, source_type: Any, handler: GetCoreSchemaHandler) -> CoreSchema:
            string_schema = core_schema.no_info_after_validator_function(
                cls.from_string,
                schema=core_schema.str_schema(),
            )
            python_schema = core_schema.is_instance_schema(cls)

            return core_schema.union_schema(
                [python_schema, string_schema],
                serialization=core_schema.to_string_ser_schema(),
                mode='left_to_right',
            )


UnknownField = NewType('UnknownField', str)


SortField = (
    Literal[
        'annotation_count',
        'created_at',
        'group_id',
        'group_status',
        'modified_at',
        'quorum_priority_order',
        'status_workflow_priority_order_max_in_group',
        'status_workflow_priority_order_min_in_group',
        'status_workflow_status_priority_order_max_in_group',
        'status_workflow_status_priority_order_min_in_group',
    ]
    | NestedField[NestableSortField | UnknownField]
    | UnknownField
)


FilterField = (
    Literal[
        'account_id',
        'quorum_unavailable_for',
        'status_workflow_completed',
        'status_workflow_id',
        'status_workflow_responsible',
        'status_workflow_status',
        'status_workflow_status_is_initial',
        'status_workflow_unavailable_for',
        'temporal_component_name',
        'temporal_dependent_item_ids',
        'temporal_instance_id',
        'temporal_iteration',
        'temporal_log_created_at',
        'temporal_log_id',
        'temporal_log_input_data',
        'temporal_log_modified_at',
        'temporal_log_output_data',
        'temporal_log_workflow_name',
        'temporal_meta',
        'temporal_priority',
        'temporal_process_id',
        'temporal_retry_key',
        'temporal_run_id',
        'temporal_snapshot',
        'temporal_solution_id',
        'temporal_source_file_name',
        'temporal_status',
        'temporal_step_name',
        'temporal_step_status',
        'temporal_step_type',
        'temporal_steps_history',
        'temporal_submitted_items_link_id',
        'temporal_upload_id',
        'temporal_vendor_type',
        'temporal_version',
        'temporal_workflow_id',
        'temporal_workflow_name',
    ]
    | NestedField[NestableFilterField | UnknownField]
    | SortField
    | UnknownField
)
