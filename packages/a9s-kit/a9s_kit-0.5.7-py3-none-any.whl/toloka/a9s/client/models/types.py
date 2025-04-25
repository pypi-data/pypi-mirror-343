from typing import Literal, NewType
from uuid import UUID

AnnotationEditId = NewType('AnnotationEditId', str)
AnnotationGroupId = NewType('AnnotationGroupId', str)
AnnotationId = NewType('AnnotationId', str)
AnnotationMetricId = NewType('AnnotationMetricId', str)
AnnotationProcessId = NewType('AnnotationProcessId', str)
AsyncQualityConfigId = NewType('AsyncQualityConfigId', str)
BatchId = NewType('BatchId', str)
GroundTruthBucketId = NewType('GroundTruthBucketId', str)
GroundTruthConfigId = NewType('GroundTruthConfigId', str)
GroundTruthId = NewType('GroundTruthId', str)
GroundTruthOutputValueId = NewType('GroundTruthOutputValueId', str)
MoneyConfigId = NewType('MoneyConfigId', UUID)
MoneyConfigVersionId = NewType('MoneyConfigVersionId', UUID)
PipelineConfigId = NewType('PipelineConfigId', UUID)
PipelineId = NewType('PipelineId', str)
PipelineInstanceId = NewType('PipelineInstanceId', UUID)
ProgressLogId = NewType('ProgressLogId', UUID)
ProjectId = NewType('ProjectId', str)
QualificationFilterId = NewType('QualificationFilterId', UUID)
QualificationId = NewType('QualificationId', UUID)
QualityConfigId = NewType('QualityConfigId', str)
ResetId = NewType('ResetId', str)
RestrictionId = NewType('RestrictionId', str)
StatusWorkflowConfigId = NewType('StatusWorkflowConfigId', str)
TemporalConfigId = NewType('TemporalConfigId', str)
TemporalLogId = NewType('TemporalLogId', str)
TenantId = NewType('TenantId', str)
UserQualificationId = NewType('UserQualificationId', UUID)

WorkflowItemStatus = Literal['pending', 'processing', 'completed', 'archived']
TemporalLogStatus = Literal['PENDING', 'COMPLETED']
