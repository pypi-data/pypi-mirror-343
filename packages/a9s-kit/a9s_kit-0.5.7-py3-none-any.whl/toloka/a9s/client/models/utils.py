import datetime
import inspect
import re
from dataclasses import asdict, dataclass
from string import Template
from typing import Any, Callable

from pydantic import BaseModel, BeforeValidator, GetCoreSchemaHandler, TypeAdapter
from pydantic_core import CoreSchema, core_schema
from typing_extensions import Self

from toloka.a9s.client.base.types import AnnotationStudioEnvironment, is_a9s_environment
from toloka.a9s.client.models.types import (
    AnnotationGroupId,
    AnnotationId,
    AnnotationProcessId,
    BatchId,
    ProjectId,
    TemporalLogId,
)

DATETIME_ADAPTER = TypeAdapter(datetime.datetime)
OPTIONAL_DATETIME_ADAPTER: TypeAdapter[datetime.datetime | None] = TypeAdapter(datetime.datetime | None)


def none_default_validator(
    default: Any | None = None,
    default_factory: Callable[[], Any] | None = None,
) -> BeforeValidator:
    def validator(v: Any) -> Any:
        if v is None:
            if default_factory:
                return default_factory()
            return default
        return v

    return BeforeValidator(validator)


def model_dump_a9s(model: BaseModel) -> dict[str, Any]:
    return model.model_dump(mode='json', by_alias=True)


@dataclass
class TemplateField(str):
    def __new__(cls, *args: Any, **kwargs: Any) -> Self:
        bound = inspect.signature(cls.__init__).bind(object(), *args, **kwargs)
        bound.apply_defaults()
        bound_dict = dict(bound.arguments)
        bound_dict.pop('self')

        return super().__new__(cls, cls.get_template().substitute(bound_dict))

    def __str__(self) -> str:
        return self.serialize(self)

    def __deepcopy__(self, memo: Any) -> Self:
        return type(self)(**self.__dict__)

    @classmethod
    def get_template(cls) -> Template:
        raise NotImplementedError

    @classmethod
    def get_pattern(cls) -> str:
        raise NotImplementedError

    @classmethod
    def from_template(cls, template: str) -> Self:
        pattern = re.compile(cls.get_pattern())
        match = pattern.match(template)
        if not match:
            raise ValueError(f'Invalid template: {template}')
        return cls(**match.groupdict())

    @classmethod
    def serialize(cls, obj: 'TemplateField | str') -> str:
        if not isinstance(obj, TemplateField):
            return obj
        return obj.get_template().substitute(asdict(obj))

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: Any, handler: GetCoreSchemaHandler) -> CoreSchema:
        string_schema = core_schema.no_info_after_validator_function(
            cls.from_template,
            schema=core_schema.str_schema(pattern=cls.get_pattern()),
        )
        python_schema = core_schema.is_instance_schema(cls)

        return core_schema.union_schema(
            [python_schema, string_schema],
            serialization=core_schema.plain_serializer_function_ser_schema(cls.serialize),
            mode='left_to_right',
        )


def parse_a9s_environment_from_id(
    id: ProjectId | BatchId | AnnotationId | AnnotationGroupId | TemporalLogId | AnnotationProcessId,
) -> AnnotationStudioEnvironment:
    """Parse environment from A9S identifier.

    Args:
        id: parsable A9S identifier

    Returns:
        Environment name extracted from the identifier

    Raises:
        ValueError: If identifier format is invalid or environment cannot be determined
    """

    id_parts = id.split('.')
    if len(id_parts) < 2:
        raise ValueError(f'Unexpected identifier format: {id}')

    if not is_a9s_environment(id_parts[0]):
        raise ValueError(f"Can't extract known A9S environment from identifier {id}")
    return id_parts[0]
