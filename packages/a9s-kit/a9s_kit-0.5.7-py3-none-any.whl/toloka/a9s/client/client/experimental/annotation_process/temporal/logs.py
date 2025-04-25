from typing import Sequence

from toloka.a9s.client.base.client import AsyncBaseAnnotationStudioClient
from toloka.a9s.client.base.exception import AnnotationStudioError
from toloka.a9s.client.models.annotation_process.temporal import (
    TemporalLogsViewStrict,
    TemporalLogViewStrict,
    UpdateTemporalLogFormStrict,
)
from toloka.a9s.client.models.types import AnnotationProcessId, TemporalLogId
from toloka.a9s.client.models.utils import model_dump_a9s


class AsyncAnnotationStudioTemporalLogsClient(AsyncBaseAnnotationStudioClient):
    async def get_logs(self, temporal_process_id: AnnotationProcessId) -> Sequence[TemporalLogViewStrict]:
        response = await self.client.make_retriable_request(
            method='GET',
            url=f'{self.V1_PREFIX}/annotation-processes/temporal/logs',
            params={'temporal_process_id': temporal_process_id},
        )
        view = TemporalLogsViewStrict.model_validate(response.json())
        return view.logs

    async def update(self, temporal_log_id: TemporalLogId, form: UpdateTemporalLogFormStrict) -> TemporalLogViewStrict:
        response = await self.client.make_retriable_request(
            method='PUT',
            url=f'{self.V1_PREFIX}/annotation-processes/temporal/logs/update',
            body=model_dump_a9s(form),
            params={
                'temporal_log_id': temporal_log_id,
            },
        )
        return TemporalLogViewStrict.model_validate(response.json())

    async def create(
        self, temporal_process_id: AnnotationProcessId, form: UpdateTemporalLogFormStrict
    ) -> TemporalLogViewStrict:
        response = await self.client.make_request(
            method='PUT',
            url=f'{self.V1_PREFIX}/annotation-processes/temporal/logs/create',
            body=model_dump_a9s(form),
            params={
                'temporal_process_id': temporal_process_id,
            },
        )
        return TemporalLogViewStrict.model_validate(response.json())

    async def get_log(self, log_id: TemporalLogId) -> TemporalLogViewStrict | None:
        try:
            response = await self.client.make_retriable_request(
                method='GET',
                url=f'{self.V1_PREFIX}/annotation-processes/temporal/logs/get/{log_id}',
            )
            return TemporalLogViewStrict.model_validate(response.json())
        except AnnotationStudioError as e:
            if e.status == 404:
                return None
            raise e

    async def get_logs_by_retry_key(self, retry_key: str) -> Sequence[TemporalLogViewStrict]:
        try:
            response = await self.client.make_retriable_request(
                method='GET',
                url=f'{self.V1_PREFIX}/annotation-processes/temporal/logs/get-by-retry-key/{retry_key}',
            )
            return TemporalLogsViewStrict.model_validate(response.json()).logs
        except AnnotationStudioError as e:
            if e.status == 404:
                return []
            raise e
