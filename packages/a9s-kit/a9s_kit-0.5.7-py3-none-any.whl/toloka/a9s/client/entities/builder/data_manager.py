import datetime
from typing import Sequence

from pydantic import TypeAdapter

from toloka.a9s.client.models.data_manager import (
    FilterConditionStrict,
    ListFilterConditionStrict,
    SearchFormSortStrict,
    SearchFormStrictBatch,
    SearchFormStrictProject,
    SingleFilterConditionStrict,
)
from toloka.a9s.client.models.data_manager.fields import FilterField
from toloka.a9s.client.models.generated.ai.toloka.a9s.data_manager.web.ui.search import SearchFormPagination
from toloka.a9s.client.models.types import BatchId, ProjectId

TIMEDELTA_ADAPTER = TypeAdapter(datetime.timedelta)


class Filter:
    """A builder for creating complex filter conditions for Data Manager searches.

    This class provides methods to construct various types of filter conditions,
    combine them using logical operators (AND, OR), and build search forms
    for projects or batches.

    Attributes:
        condition: The underlying Pydantic model representing the filter condition.

    Examples:
        >>> import asyncio
        >>> import datetime
        >>> from toloka.a9s.client import AsyncKit
        >>> from toloka.a9s.client.entities.builder.data_manager import Filter
        >>> from toloka.a9s.client.models.data_manager.fields import NestedField
        >>>
        >>> async def main():
        ...     # Replace with actual credentials and project_id
        ...     kit = AsyncKit.from_credentials(environment='production', api_key='YOUR_API_KEY')
        ...     project_id = 'YOUR_PROJECT_ID'
        ...
        ...     # Find active groups created more than 3 days ago OR groups containing 'urgent' in metadata.comment
        ...     three_days_ago = datetime.timedelta(days=3)
        ...
        ...     # Construct the filter in a single expression:
        ...     # (status is ACTIVE AND created > 3 days ago) OR (metadata.comment contains 'urgent')
        ...     complex_filter = Filter.or_(
        ...         Filter.and_(
        ...             Filter.equals(field='group_status', value='ACTIVE'),
        ...             Filter.older_than(field='created_at', value=three_days_ago),
        ...         ),
        ...         Filter.contains(field=NestedField('metadata', ['comment']), value='urgent'),
        ...     )
        ...
        ...     # Build the search form for the project
        ...     search_form = complex_filter.build_project_form(project_id=project_id)
        ...
        ...     # Use the form with the kit
        ...     data_manager = kit.annotation_studio.data_manager
        ...     count_result = await data_manager.count(search_form)
        ...     print(f'Found {count_result.count} matching groups.')
        ...
        ...     async for element in data_manager.get_all_elements(search_form):
        ...         print(f'Processing element: {element.annotation_id}')
        >>>
        >>> # To run the example:
        >>> asyncio.run(main())

    """

    def __init__(self, condition: FilterConditionStrict) -> None:
        """Initializes the Filter object.

        Args:
            condition: The Pydantic model representing the filter condition.
        """
        self.condition = condition

    @classmethod
    def or_(cls, *filters: 'Filter') -> 'Filter':
        """Combines multiple filters using the logical OR operator.

        Args:
            *filters: A variable number of Filter objects to combine.

        Returns:
            A new Filter object representing the combined OR condition.
        """
        return Filter(
            ListFilterConditionStrict(condition_join_type='OR', conditions=[filter.condition for filter in filters])
        )

    @classmethod
    def and_(cls, *filters: 'Filter') -> 'Filter':
        """Combines multiple filters using the logical AND operator.

        Args:
            *filters: A variable number of Filter objects to combine.

        Returns:
            A new Filter object representing the combined AND condition.
        """
        return Filter(
            ListFilterConditionStrict(condition_join_type='AND', conditions=[filter.condition for filter in filters])
        )

    @classmethod
    def include_any_of(cls, field: FilterField, value: Sequence[str]) -> 'Filter':
        """Creates a filter condition where the field must contain at least one of the specified values.

        Args:
            field: The field to filter on.
            value: A sequence of strings representing the values to check for.

        Returns:
            A new Filter object representing the emulated 'INCLUDE_ANY_OF' condition using OR.
        """
        conditions = [SingleFilterConditionStrict(field=field, operator='EQUALS', value=v) for v in value]
        return Filter(ListFilterConditionStrict(condition_join_type='OR', conditions=conditions))

    @classmethod
    def include_all_of(cls, field: FilterField, value: Sequence[str]) -> 'Filter':
        """Creates a filter condition where the field must contain all of the specified values.

        Args:
            field: The field to filter on.
            value: A sequence of strings representing the values to check for.

        Returns:
            A new Filter object representing the emulated 'INCLUDE_ALL_OF' condition using AND.
        """
        conditions = [SingleFilterConditionStrict(field=field, operator='EQUALS', value=v) for v in value]
        return Filter(ListFilterConditionStrict(condition_join_type='AND', conditions=conditions))

    @classmethod
    def exclude_any_of(cls, field: FilterField, value: Sequence[str]) -> 'Filter':
        """Creates a filter condition where the field must not contain any of the specified values.

        Args:
            field: The field to filter on.
            value: A sequence of strings representing the values to exclude.

        Returns:
            A new Filter object representing the emulated 'EXCLUDE_ANY_OF' condition using AND with NOT_EQUALS.
            Equivalent to NOT (value1 OR value2) => (NOT value1) AND (NOT value2).
        """
        conditions = [SingleFilterConditionStrict(field=field, operator='NOT_EQUALS', value=v) for v in value]
        return Filter(ListFilterConditionStrict(condition_join_type='AND', conditions=conditions))

    @classmethod
    def exclude_all_of(cls, field: FilterField, value: Sequence[str]) -> 'Filter':
        """Creates a filter condition where the field must not contain all of the specified values.

        Args:
            field: The field to filter on.
            value: A sequence of strings representing the values to exclude.

        Returns:
            A new Filter object representing the emulated 'EXCLUDE_ALL_OF' condition using OR with NOT_EQUALS.
            Equivalent to NOT (value1 AND value2) => (NOT value1) OR (NOT value2).
        """
        conditions = [SingleFilterConditionStrict(field=field, operator='NOT_EQUALS', value=v) for v in value]
        return Filter(ListFilterConditionStrict(condition_join_type='OR', conditions=conditions))

    @classmethod
    def between(cls, field: FilterField, lower_bound: str, upper_bound: str) -> 'Filter':
        """Creates a filter condition where the field value must be between the two specified values (inclusive).

        Typically used for date ranges or numerical ranges.

        Args:
            field: The field to filter on.
            lower_bound: The string representing the lower bound (inclusive).
            upper_bound: The string representing the upper bound (inclusive).

        Returns:
            A new Filter object representing the 'BETWEEN' condition using AND with range operators.
        """
        conditions = [
            SingleFilterConditionStrict(field=field, operator='GREATER_THAN_OR_EQUALS', value=lower_bound),
            SingleFilterConditionStrict(field=field, operator='LESS_THAN_OR_EQUALS', value=upper_bound),
        ]
        return Filter(ListFilterConditionStrict(condition_join_type='AND', conditions=conditions))

    @classmethod
    def equals(cls, field: FilterField, value: str) -> 'Filter':
        """Creates a filter condition where the field value must exactly match the specified value.

        Args:
            field: The field to filter on.
            value: The string value to match.

        Returns:
            A new Filter object representing the 'EQUALS' condition.
        """
        return Filter(SingleFilterConditionStrict(field=field, operator='EQUALS', value=value))

    @classmethod
    def not_equals(cls, field: FilterField, value: str) -> 'Filter':
        """Creates a filter condition where the field value must not match the specified value.

        Args:
            field: The field to filter on.
            value: The string value to exclude.

        Returns:
            A new Filter object representing the 'NOT_EQUALS' condition.
        """
        return Filter(SingleFilterConditionStrict(field=field, operator='NOT_EQUALS', value=value))

    @classmethod
    def contains(cls, field: FilterField, value: str) -> 'Filter':
        """Creates a filter condition where the field value must contain the specified substring.

        Args:
            field: The field to filter on.
            value: The substring to search for.

        Returns:
            A new Filter object representing the 'CONTAINS' condition.
        """
        return Filter(SingleFilterConditionStrict(field=field, operator='CONTAINS', value=value))

    @classmethod
    def not_contains(cls, field: FilterField, value: str) -> 'Filter':
        """Creates a filter condition where the field value must not contain the specified substring.

        Args:
            field: The field to filter on.
            value: The substring to exclude.

        Returns:
            A new Filter object representing the 'NOT_CONTAINS' condition.
        """
        return Filter(SingleFilterConditionStrict(field=field, operator='NOT_CONTAINS', value=value))

    @classmethod
    def is_empty(cls, field: FilterField) -> 'Filter':
        """Creates a filter condition where the field must be empty or null.

        Args:
            field: The field to check for emptiness.

        Returns:
            A new Filter object representing the 'IS_EMPTY' condition.
        """
        return Filter(SingleFilterConditionStrict(field=field, operator='IS_EMPTY'))

    @classmethod
    def is_not_empty(cls, field: FilterField) -> 'Filter':
        """Creates a filter condition where the field must not be empty or null.

        Args:
            field: The field to check for non-emptiness.

        Returns:
            A new Filter object representing the 'IS_NOT_EMPTY' condition.
        """
        return Filter(SingleFilterConditionStrict(field=field, operator='IS_NOT_EMPTY'))

    @classmethod
    def greater_than(cls, field: FilterField, value: str) -> 'Filter':
        """Creates a filter condition where the field value must be greater than the specified value.

        Args:
            field: The field to filter on.
            value: The string representation of the value to compare against.

        Returns:
            A new Filter object representing the 'GREATER_THAN' condition.
        """
        return Filter(SingleFilterConditionStrict(field=field, operator='GREATER_THAN', value=value))

    @classmethod
    def greater_than_or_equals(cls, field: FilterField, value: str) -> 'Filter':
        """Creates a filter condition where the field value must be greater than or equal to the specified value.

        Args:
            field: The field to filter on.
            value: The string representation of the value to compare against.

        Returns:
            A new Filter object representing the 'GREATER_THAN_OR_EQUALS' condition.
        """
        return Filter(SingleFilterConditionStrict(field=field, operator='GREATER_THAN_OR_EQUALS', value=value))

    @classmethod
    def less_than(cls, field: FilterField, value: str) -> 'Filter':
        """Creates a filter condition where the field value must be less than the specified value.

        Args:
            field: The field to filter on.
            value: The string representation of the value to compare against.

        Returns:
            A new Filter object representing the 'LESS_THAN' condition.
        """
        return Filter(SingleFilterConditionStrict(field=field, operator='LESS_THAN', value=value))

    @classmethod
    def less_than_or_equals(cls, field: FilterField, value: str) -> 'Filter':
        """Creates a filter condition where the field value must be less than or equal to the specified value.

        Args:
            field: The field to filter on.
            value: The string representation of the value to compare against.

        Returns:
            A new Filter object representing the 'LESS_THAN_OR_EQUALS' condition.
        """
        return Filter(SingleFilterConditionStrict(field=field, operator='LESS_THAN_OR_EQUALS', value=value))

    @classmethod
    def older_than(cls, field: FilterField, value: datetime.timedelta) -> 'Filter':
        """Creates a filter condition where the date/time field value is older than the specified duration relative to
        now.

        Args:
            field: The date/time field to filter on.
            value: A timedelta object representing the duration.

        Returns:
            A new Filter object representing the 'OLDER_THAN' condition.
        """
        duration_str = TIMEDELTA_ADAPTER.dump_python(value, mode='json')
        return Filter(SingleFilterConditionStrict(field=field, operator='OLDER_THAN', value=duration_str))

    @classmethod
    def younger_than(cls, field: FilterField, value: datetime.timedelta) -> 'Filter':
        """Creates a filter condition where the date/time field value is younger than the specified duration relative to
        now.

        Args:
            field: The date/time field to filter on.
            value: A timedelta object representing the duration.

        Returns:
            A new Filter object representing the 'YOUNGER_THAN' condition.
        """
        duration_str = TIMEDELTA_ADAPTER.dump_python(value, mode='json')
        return Filter(SingleFilterConditionStrict(field=field, operator='YOUNGER_THAN', value=duration_str))

    def build_project_form(
        self,
        project_id: ProjectId,
        sort_list: Sequence[SearchFormSortStrict] | None = None,
        pagination: SearchFormPagination | None = None,
    ) -> SearchFormStrictProject:
        """Builds a search form specifically for querying within a project.

        Args:
            project_id: The ID of the project to search within.
            sort_list: An optional sequence of sorting criteria.
            pagination: An optional pagination configuration.

        Returns:
            A SearchFormStrictProject object ready to be used with the Data Manager client.
        """
        return SearchFormStrictProject(
            project_id=project_id,
            filter=self.condition,
            sort_list=sort_list,
            pagination=pagination,
        )

    def build_batch_form(
        self,
        batch_id: BatchId,
        sort_list: Sequence[SearchFormSortStrict] | None = None,
        pagination: SearchFormPagination | None = None,
    ) -> SearchFormStrictBatch:
        """Builds a search form specifically for querying within a batch.

        Args:
            batch_id: The ID of the batch to search within.
            sort_list: An optional sequence of sorting criteria.
            pagination: An optional pagination configuration.

        Returns:
            A SearchFormStrictBatch object ready to be used with the Data Manager client.
        """
        return SearchFormStrictBatch(
            batch_id=batch_id,
            filter=self.condition,
            sort_list=sort_list,
            pagination=pagination,
        )
