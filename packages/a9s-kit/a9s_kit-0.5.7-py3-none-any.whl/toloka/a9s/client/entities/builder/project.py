from __future__ import annotations

import uuid
from typing import Any, Generic, Literal, Mapping, Sequence, cast

from typing_extensions import TypeVar, Unpack

from toloka.a9s.client.client import AsyncKit
from toloka.a9s.client.entities.builder.common import StatusWorkflowForm
from toloka.a9s.client.entities.money_config import (
    AnnotationMoneyConfigFormParams,
    AnnotationMoneyConfigFormParamsWithDefaults,
    StatusWorkflowMoneyConfigFormParams,
    StatusWorkflowMoneyConfigFormParamsWithDefaults,
    apply_annotation_money_config_form_defaults,
    apply_status_workflow_money_config_form_defaults,
    build_annotation_money_config_form,
    build_status_workflow_money_config_form,
)
from toloka.a9s.client.entities.project import Project
from toloka.a9s.client.models.annotation_process.quorum import QuorumConfigProjectForm
from toloka.a9s.client.models.annotation_process.status_workflow import (
    StatusWorkflowConfigProjectForm,
    StatusWorkflowConfigViewStrict,
)
from toloka.a9s.client.models.extension_id import ExtensionId
from toloka.a9s.client.models.extensions import (
    with_ground_truth_extension_project,
    with_money_config_extension_project,
    with_quality_config_extension_project,
    with_webhook_extension_project,
)
from toloka.a9s.client.models.generated.ai.toloka.a9s.annotation_process.processes.quorum.web.ui.form import (
    QuorumConfigForm,
)
from toloka.a9s.client.models.generated.ai.toloka.a9s.annotation_process.processes.quorum.web.ui.view import (
    QuorumConfigView,
)
from toloka.a9s.client.models.generated.ai.toloka.a9s.project.web.v1.viewform import (
    BatchCompletionViewFormV1,
    PublicInstructionViewFormV1,
    TimeLimitViewFormV1,
)
from toloka.a9s.client.models.generated.ai.toloka.gts.config.web.v0.form import GroundTruthConfigForm
from toloka.a9s.client.models.ground_truth import GroundTruthConfigViewV0Strict
from toloka.a9s.client.models.money_config import MoneyConfigFormStrict, MoneyConfigViewStrict
from toloka.a9s.client.models.project import (
    ProjectExtensionInstanceConfigViewFormV1Strict,
    ProjectExtensionsViewFormV1Strict,
    ProjectFormV1Strict,
    ProjectViewV1Strict,
    SpecificationViewFormV1Strict,
)
from toloka.a9s.client.models.quality_management.config import (
    QualityConfigFormV0Strict,
    QualityConfigViewV0Strict,
)
from toloka.a9s.client.models.types import GroundTruthConfigId, MoneyConfigId, QualityConfigId
from toloka.a9s.client.models.webhooks import WebhookFormStrict, WebhookViewStrict

MCFOpt = TypeVar(
    'MCFOpt',
    bound=StatusWorkflowMoneyConfigFormParamsWithDefaults
    | AnnotationMoneyConfigFormParamsWithDefaults
    | MoneyConfigFormStrict
    | MoneyConfigId
    | None,
    covariant=True,
)
GTFOpt = TypeVar('GTFOpt', bound=GroundTruthConfigForm | GroundTruthConfigId | None, covariant=True)
QMFOpt = TypeVar('QMFOpt', bound=QualityConfigFormV0Strict | QualityConfigId | None, covariant=True)
QRMOpt = TypeVar('QRMOpt', bound=QuorumConfigForm | None, covariant=True)
SWOpt = TypeVar('SWOpt', bound=StatusWorkflowForm | None, covariant=True)
WHOpt = TypeVar('WHOpt', bound=WebhookFormStrict | str | None, covariant=True)

ResMC = TypeVar('ResMC', bound=MoneyConfigViewStrict | None, covariant=True, default=None)
ResGT = TypeVar('ResGT', bound=GroundTruthConfigViewV0Strict | None, covariant=True, default=None)
ResQM = TypeVar('ResQM', bound=QualityConfigViewV0Strict | None, covariant=True, default=None)
ResQRM = TypeVar('ResQRM', bound=QuorumConfigView | None, covariant=True, default=None)
ResSW = TypeVar('ResSW', bound=StatusWorkflowConfigViewStrict | None, covariant=True, default=None)
ResWH = TypeVar('ResWH', bound=WebhookViewStrict | None, covariant=True, default=None)


class ProjectBuilder(
    Generic[
        MCFOpt,
        GTFOpt,
        QMFOpt,
        QRMOpt,
        SWOpt,
        WHOpt,
        ResMC,
        ResGT,
        ResQM,
        ResQRM,
        ResSW,
        ResWH,
    ]
):
    """Builder for creating new Annotation Studio projects with various configurations.

    The `ProjectBuilder` provides an interface for configuring and creating new projects with different extensions
    (`money config`, `ground truth`, `quality management`, `webhooks`). Each extension configuration is strongly typed
    and can be added through `with_*` methods.

    Generic type parameters:

    * `MCFOpt`: Type of `money config` form or existing config ID
    * `GTFOpt`: Type of `ground truth` form or existing config ID
    * `QMFOpt`: Type of `quality management` form or existing config ID
    * `QRMOpt`: Type of `quorum` form
    * `SWOpt`: Type of `status workflow` form
    * `WHOpt`: Type of `webhook` form or existing webhook ID
    * `ResMC`: `Money config` view type after build
    * `ResGT`: `Ground truth` config view type after build
    * `ResQM`: `Quality management` config view type after build
    * `ResQRM`: `Quorum annotation process` config view type after build
    * `ResSW`: `Status annotation process workflow` config view type after build
    * `ResWH`: `Webhook` view type after build

    Attributes:
        kit: `AsyncKit` instance for making API calls
        form: `Project` creation form with basic parameters
        money_config: `Money config` form or ID
        ground_truth: `Ground truth` config form or ID
        quality_management: `Quality management` config form or ID
        quorum: `Quorum annotation process` config form
        status_workflow: `Status annotation process workflow` config form
        webhooks: `Webhook` form or ID

    Examples:

        Create a basic project:
        ```python
        builder = ProjectBuilder.from_parameters(
            kit=kit,
            name='Test project',
            specification=specification,
            public_instruction='Project instructions',
        )
        project = await builder.build()
        ```

        Create project with money config:
        ```python
        project = await builder.with_annotation_money_config(price=0.5, currency='USD').build()
        ```

        Create project with multiple configurations:
        ```python
        project = await builder
            .with_money_config(MoneyConfigId('existing-config-id'))
            .with_quality_management(QualityConfigId('existing-config-id'))
            .build()
        ```
    """

    def __init__(
        self,
        kit: AsyncKit,
        form: ProjectFormV1Strict,
        money_config: MCFOpt,
        ground_truth: GTFOpt,
        quality_management: QMFOpt,
        quorum: QRMOpt,
        status_workflow: SWOpt,
        webhooks: WHOpt,
    ) -> None:
        self.kit = kit
        self.form = form
        self.money_config = money_config
        self.ground_truth = ground_truth
        self.quality_management = quality_management
        self.quorum = quorum
        self.status_workflow = status_workflow
        self.webhooks = webhooks

    @classmethod
    def from_parameters(
        cls,
        kit: AsyncKit,
        name: str,
        specification: SpecificationViewFormV1Strict,
        public_instruction: str | None,
        private_comment: str | None = None,
        batch_completion: Literal['AUTO', 'MANUAL'] = 'AUTO',
        edit_ttl_in_seconds: int | None = None,
        metadata: Mapping[str, Any] | None = None,
        tags: Sequence[str] | None = None,
        existing_extensions: Mapping[ExtensionId, str] | None = None,
    ) -> InitialProjectBuilder:
        """Creates a new `ProjectBuilder` with basic project parameters.

        Creates an initial `ProjectBuilder` instance that can be used to configure and create a new project. The builder
        starts with basic project parameters and can be further configured with extensions using `with_*` methods.

        Args:
            kit: `AsyncKit` instance for making API calls
            name: Name of the project
            specification: Technical specification of the project that defines task fields and interfaces
            public_instruction: Instructions for annotators working on the project
            private_comment: Internal comment about the project, not shown to annotators
            batch_completion: Project completion type, either `'AUTO'` or `'MANUAL'`. If `'AUTO'` is set project will be
                automatically moved to `'COMPLETED'` status when all tasks are done.
            edit_ttl_in_seconds: Time limit for editing task in seconds
            metadata: An arbitrary dictionary with additional information about the project.
            tags: Tags on the project used in quality management async config.
            existing_extensions: A dictionary with extension IDs as keys and extension instance IDs as values.

        Returns:
            New `ProjectBuilder` instance with basic parameters set

        Examples:

            Create builder with minimal params:
            ```python
            builder = ProjectBuilder.from_parameters(
                kit=kit,
                name='Test project',
                specification=specification,
                public_instruction='Project instructions',
            )
            ```
        """

        return ProjectBuilder(
            kit=kit,
            form=ProjectFormV1Strict(
                name=name,
                private_comment=private_comment,
                public_instruction=PublicInstructionViewFormV1(
                    type='HTML',
                    value=public_instruction,
                ),
                specification=specification,
                batch_completion=BatchCompletionViewFormV1(type=batch_completion),
                time_limit=TimeLimitViewFormV1(edit_ttl_in_seconds=edit_ttl_in_seconds)
                if edit_ttl_in_seconds is not None
                else None,
                metadata=metadata,
                tags=tags or [],
                extensions=ProjectExtensionsViewFormV1Strict(
                    instances=[
                        ProjectExtensionInstanceConfigViewFormV1Strict(
                            extension_id=extension_id, instance_id=instance_id
                        )
                        for extension_id, instance_id in (existing_extensions or {}).items()
                    ]
                ),
            ),
            money_config=None,
            ground_truth=None,
            quality_management=None,
            quorum=None,
            status_workflow=None,
            webhooks=None,
        )

    async def build(self) -> Project[ProjectViewV1Strict, ResMC, ResGT, ResQM, ResQRM, ResSW, ResWH]:
        """Creates a new project with all configured extensions.

        Makes API calls to create the project and any configured extensions (money config, ground truth, quality
        management). Any configurations provided as IDs will be fetched from the API. All configured extensions
        will be linked to the created project.

        Returns:
            New `Project` instance with all configured extensions. The project type will reflect which configurations
            were enabled:

            * `ProjectWithMoneyConfig`: if money config was configured
            * `ProjectWithGroundTruth`: if ground truth was configured
            * `ProjectWithQualityManagement`: if quality management was configured

        Raises:
            ValueError: If any API call fails or if extension configurations are inconsistent with the project.

        Examples:

            Create basic project:
            ```python
            builder = ProjectBuilder.from_parameters(
                kit=kit,
                name='Test project',
                specification=specification,
                public_instruction='Project instructions',
            )
            project = await builder.build()
            ```

            Create project with multiple configurations:
            ```python
            project = await builder
                .with_annotation_money_config(price=0.5, currency='USD')
                .with_quality_management(QualityConfigId('existing-config-id'))
                .build()
            ```
        """

        money_config_params: (
            StatusWorkflowMoneyConfigFormParamsWithDefaults
            | AnnotationMoneyConfigFormParamsWithDefaults
            | MoneyConfigFormStrict
            | MoneyConfigId
            | None
        ) = self.money_config
        if money_config_params is None:
            money_config = None
        else:
            if isinstance(money_config_params, (MoneyConfigFormStrict, dict)):
                money_config_form: MoneyConfigFormStrict
                if isinstance(money_config_params, dict):
                    if 'mutable_transitions' in money_config_params:
                        money_config_form = await build_status_workflow_money_config_form(
                            kit=self.kit,
                            **money_config_params,
                        )
                    else:
                        money_config_form = await build_annotation_money_config_form(
                            kit=self.kit,
                            **money_config_params,
                        )
                else:
                    money_config_form = money_config_params

                money_config_id = (await self.kit.experts_portal.money_config.create(money_config_form)).config_id
            else:
                assert isinstance(money_config_params, uuid.UUID)
                money_config_id = money_config_params

            money_config = await self.kit.experts_portal.money_config.get_last_version(money_config_id)

        ground_truth_form: GroundTruthConfigForm | GroundTruthConfigId | None = self.ground_truth
        if ground_truth_form is None:
            ground_truth = None
        elif isinstance(ground_truth_form, GroundTruthConfigForm):
            ground_truth = await self.kit.annotation_studio.ground_truth_config.create(ground_truth_form)
        else:
            ground_truth = await self.kit.annotation_studio.ground_truth_config.get(ground_truth_form)

        quality_management_form: QualityConfigFormV0Strict | QualityConfigId | None = self.quality_management
        if quality_management_form is None:
            quality_management = None
        elif isinstance(quality_management_form, QualityConfigFormV0Strict):
            quality_management = await self.kit.quality_management.quality_config.create(quality_management_form)
        else:
            quality_management = await self.kit.quality_management.quality_config.get(quality_management_form)

        form = self.form
        if money_config is not None:
            form = with_money_config_extension_project(project_form=form, money_config_id=money_config.config_id)
            form.add_tenant_id_to_metadata(money_config.requester_id)
        if ground_truth is not None:
            form = with_ground_truth_extension_project(project_form=form, ground_truth_config_id=ground_truth.id)
        if quality_management is not None:
            form = with_quality_config_extension_project(project_form=form, quality_config_id=quality_management.id)

        webhook_form: WebhookFormStrict | str | None = self.webhooks
        if webhook_form is None:
            webhook = None
        elif isinstance(webhook_form, WebhookFormStrict):
            webhook = await self.kit.webhooks.create(webhook_form)
            form = with_webhook_extension_project(project_form=form, webhook_id=webhook.id)
        else:
            webhook = await self.kit.webhooks.get(webhook_id=webhook_form)
            form = with_webhook_extension_project(project_form=form, webhook_id=webhook.id)

        project = await self.kit.annotation_studio.project.create(form)

        quorum = None

        quorum_form: QuorumConfigForm | None = self.quorum
        if quorum_form is not None:
            quorum = await self.kit.annotation_studio.quorum.set_project_defaults(
                form=QuorumConfigProjectForm(
                    project_id=project.id,
                    **quorum_form.model_dump(),
                ),
            )
        status_workflow = None
        status_workflow_form: StatusWorkflowForm | None = self.status_workflow
        if status_workflow_form is not None:
            status_workflow = await self.kit.annotation_studio.status_workflow.set_project_defaults(
                form=StatusWorkflowConfigProjectForm(
                    project_id=project.id,
                    **status_workflow_form.model_dump(),
                )
            )

        return Project(
            project_id=project.id,
            view=project,
            money_config=cast(ResMC, money_config),
            ground_truth=cast(ResGT, ground_truth),
            quality_management=cast(ResQM, quality_management),
            quorum=cast(ResQRM, quorum),
            status_workflow=cast(ResSW, status_workflow),
            webhooks=cast(ResWH, webhook),
            kit=self.kit,
        )

    def with_money_config(
        self: ProjectBuilderWithoutMoneyConfig[
            GTFOpt, QMFOpt, QRMOpt, SWOpt, WHOpt, ResGT, ResQM, ResQRM, ResSW, ResWH
        ],
        money_config: StatusWorkflowMoneyConfigFormParams
        | AnnotationMoneyConfigFormParams
        | MoneyConfigFormStrict
        | MoneyConfigId,
    ) -> ProjectBuilderWithMoneyConfig[GTFOpt, QMFOpt, QRMOpt, SWOpt, WHOpt, ResGT, ResQM, ResQRM, ResSW, ResWH]:
        """Configures money config extension for the project being built.

        Adds money config configuration to the builder, either as parameters for a new config or an existing config ID.
        This is a generic method that accepts both predefined configs and new config forms. Consider using
        `with_annotation_money_config` for a simpler interface.

        Args:
            money_config: Either form for creating new money config or ID of existing config to use

        Returns:
            Updated builder with money config configuration added. The return type reflects that money config
            will be available after build.

        Examples:

            Use existing money config:
            ```python
            builder = builder.with_money_config(MoneyConfigId('existing-config'))
            ```

            Create new config:
            ```python
            form = MoneyConfigFormStrict(...)
            builder = builder.with_money_config(form)
            ```
        """
        money_config_with_defaults: (
            StatusWorkflowMoneyConfigFormParamsWithDefaults
            | AnnotationMoneyConfigFormParamsWithDefaults
            | MoneyConfigFormStrict
            | MoneyConfigId
        )
        if isinstance(money_config, dict):
            if 'mutable_transitions' in money_config:
                money_config_with_defaults = apply_status_workflow_money_config_form_defaults(**money_config)
            else:
                money_config_with_defaults = apply_annotation_money_config_form_defaults(**money_config)
        else:
            money_config_with_defaults = money_config

        return ProjectBuilderWithMoneyConfig[GTFOpt, QMFOpt, QRMOpt, SWOpt, WHOpt, ResGT, ResQM, ResQRM, ResSW, ResWH](
            kit=self.kit,
            form=self.form,
            money_config=money_config_with_defaults,
            ground_truth=self.ground_truth,
            quality_management=self.quality_management,
            quorum=self.quorum,
            status_workflow=self.status_workflow,
            webhooks=self.webhooks,
        )

    def with_annotation_money_config(
        self: ProjectBuilderWithoutMoneyConfig[
            GTFOpt, QMFOpt, QRMOpt, SWOpt, WHOpt, ResGT, ResQM, ResQRM, ResSW, ResWH
        ],
        **kwargs: Unpack[AnnotationMoneyConfigFormParams],
    ) -> ProjectBuilderWithMoneyConfig[GTFOpt, QMFOpt, QRMOpt, SWOpt, WHOpt, ResGT, ResQM, ResQRM, ResSW, ResWH]:
        """Configures annotation-based money config extension for the project being built.

        Adds money config configuration to the builder, with parameters for simple per-annotation payments.
        This is a convenience method that provides a simpler interface compared to `with_money_config`.

        Args:
            price (float): Price per annotation in specified currency
            currency (Literal['BU', 'USD']): Currency code, either 'BU' (Base Units) or 'USD'
            tenant_id (NotRequired[str | None]): Tenant identifier. If omitted API call will be made to get first
                available tenant
            skip_pending_balance (NotRequired[bool]): If True, payment will be processed without pending balance stage
            name (NotRequired[str]): Optional name for the money config (if unset, a random UUID will be used)

        Returns:
            Updated builder with annotation-based money config configuration added. The return type reflects that
            money config will be available after build.

        Examples:

            ```python
            builder = builder.with_annotation_money_config(price=0.5, currency='USD', skip_pending_balance=True)
            ```
        """

        return self.with_money_config(kwargs)

    def with_status_workflow_money_config(
        self: ProjectBuilderWithoutMoneyConfig[
            GTFOpt, QMFOpt, QRMOpt, StatusWorkflowForm, WHOpt, ResGT, ResQM, ResQRM, ResSW, ResWH
        ],
        **kwargs: Unpack[StatusWorkflowMoneyConfigFormParams],
    ) -> ProjectBuilderWithMoneyConfig[
        GTFOpt, QMFOpt, QRMOpt, StatusWorkflowForm, WHOpt, ResGT, ResQM, ResQRM, ResSW, ResWH
    ]:
        """Configures status workflow-based money config extension for the project being built.

        Adds money config configuration to the builder, with parameters specific to status workflow-based payments.
        This method can only be used when status workflow is also configured for the project.

        Args:
            snippet_price (float): Price shown in tasks list
            currency (Literal['BU', 'USD']): Currency code, either 'BU' (Base Units) or 'USD'
            mutable_transitions (StatusTransitionMutablePayments): Mapping from status to expected payment settings
            paid_transitions (StatusTransitionPayments): Mapping from status to actual payment settings
            tenant_id (NotRequired[str | None]): Tenant identifier. If omitted API call will be made to get first
                available tenant
            skip_pending_balance (NotRequired[bool]): If True, payment will be processed without pending balance stage
            name (NotRequired[str]): Optional name for the money config (if unset, a random UUID will be used)

        Returns:
            Updated builder with status workflow money config configuration added. The return type reflects that
            money config will be available after build.

        Examples:
            ```python
            builder = builder.with_status_workflow(status_workflow_form)
            mutable = {'in_progress': StatusTransitionMutablePayment(price=0.4)}
            paid = {'accepted': StatusTransitionPayment(price=0.4)}
            builder = builder.with_status_workflow_money_config(
                snippet_price=0.4, currency='USD', mutable_transitions=mutable, paid_transitions=paid
            )
            ```
        """

        return self.with_money_config(kwargs)

    def with_ground_truth(
        self: ProjectBuilderWithoutGroundTruth[
            MCFOpt, QMFOpt, QRMOpt, SWOpt, WHOpt, ResMC, ResQM, ResQRM, ResSW, ResWH
        ],
        ground_truth: GroundTruthConfigForm | GroundTruthConfigId,
    ) -> ProjectBuilderWithGroundTruth[MCFOpt, QMFOpt, QRMOpt, SWOpt, WHOpt, ResMC, ResQM, ResQRM, ResSW, ResWH]:
        """Configures ground truth extension for the project being built.

        Adds ground truth configuration to the builder, either as parameters for a new config or an existing config ID.
        Ground truth extension allows connecting project to a ground truth storage for quality control.

        Args:
            ground_truth: Either form for creating new ground truth config or ID of existing config to use

        Returns:
            Updated builder with ground truth configuration added. The return type reflects that ground truth
            will be available after build.

        Examples:

            Use existing ground truth config:
            ```python
            builder = builder.with_ground_truth(GroundTruthConfigId('existing-config'))
            ```

            Create new config:
            ```python
            form = GroundTruthConfigForm(...)
            builder = builder.with_ground_truth(form)
            ```
        """
        return ProjectBuilderWithGroundTruth[MCFOpt, QMFOpt, QRMOpt, SWOpt, WHOpt, ResMC, ResQM, ResQRM, ResSW, ResWH](
            kit=self.kit,
            form=self.form,
            money_config=self.money_config,
            ground_truth=ground_truth,
            quality_management=self.quality_management,
            quorum=self.quorum,
            status_workflow=self.status_workflow,
            webhooks=self.webhooks,
        )

    def with_quality_management(
        self: ProjectBuilderWithoutQualityManagement[
            MCFOpt, GTFOpt, QRMOpt, SWOpt, WHOpt, ResMC, ResGT, ResQRM, ResSW, ResWH
        ],
        quality_management: QualityConfigFormV0Strict | QualityConfigId,
    ) -> ProjectBuilderWithQualityManagement[MCFOpt, GTFOpt, QRMOpt, SWOpt, WHOpt, ResMC, ResGT, ResQRM, ResSW, ResWH]:
        """Configures quality management extension for the project being built.

        Adds quality management configuration to the builder, either as parameters for a new config or an existing
        config ID. Quality management extension allows setting restrictions on annotators' access to the project
        and its batches.

        Args:
            quality_management: Either form for creating new quality management config or ID of existing config to use

        Returns:
            Updated builder with quality management configuration added. The return type reflects that quality
            management will be available after build.

        Examples:

            Use existing quality management config:
            ```python
            builder = builder.with_quality_management(QualityConfigId('existing-config'))
            ```

            Create new config:
            ```python
            form = QualityConfigFormV0Strict(...)
            builder = builder.with_quality_management(form)
            ```
        """
        return ProjectBuilderWithQualityManagement[
            MCFOpt, GTFOpt, QRMOpt, SWOpt, WHOpt, ResMC, ResGT, ResQRM, ResSW, ResWH
        ](
            kit=self.kit,
            form=self.form,
            money_config=self.money_config,
            ground_truth=self.ground_truth,
            quality_management=quality_management,
            quorum=self.quorum,
            status_workflow=self.status_workflow,
            webhooks=self.webhooks,
        )

    def with_quorum(
        self: ProjectBuilderWithoutQuorum[MCFOpt, GTFOpt, QMFOpt, SWOpt, WHOpt, ResMC, ResGT, ResQM, ResSW, ResWH],
        quorum: QuorumConfigForm,
    ) -> ProjectBuilderWithQuorum[MCFOpt, GTFOpt, QMFOpt, SWOpt, WHOpt, ResMC, ResGT, ResQM, ResSW, ResWH]:
        """Configures quorum annotation process for the project being built.

        Adds quorum configuration to the builder. Quorum annotation process allows setting requirements
        for the minimum number of annotations per task.

        Args:
            quorum: Form for creating new quorum config

        Returns:
            Updated builder with quorum configuration added. The return type reflects that quorum
            settings will be available after build.

        Examples:

            ```python
            form = QuorumConfigForm(...)
            builder = builder.with_quorum(form)
            ```
        """
        return ProjectBuilderWithQuorum[MCFOpt, GTFOpt, QMFOpt, SWOpt, WHOpt, ResMC, ResGT, ResQM, ResSW, ResWH](
            kit=self.kit,
            form=self.form,
            money_config=self.money_config,
            ground_truth=self.ground_truth,
            quality_management=self.quality_management,
            quorum=quorum,
            status_workflow=self.status_workflow,
            webhooks=self.webhooks,
        )

    def with_status_workflow(
        self: 'ProjectBuilderWithoutStatusWorkflow[MCFOpt, GTFOpt, QMFOpt, QRMOpt, WHOpt, ResMC, ResGT, ResQM, ResQRM, ResWH]',  # noqa: E501
        status_workflow: StatusWorkflowForm,
    ) -> 'ProjectBuilderWithStatusWorkflow[MCFOpt, GTFOpt, QMFOpt, QRMOpt, WHOpt, ResMC, ResGT, ResQM, ResQRM, ResWH]':
        """Configures status workflow for the project being built.

        Adds status workflow configuration to the builder. Status workflow defines the sequence of statuses
        that tasks go through during annotation process.

        Args:
            status_workflow: Form for creating new status workflow config

        Returns:
            Updated builder with status workflow configuration added. The return type reflects that status workflow
            settings will be available after build.

        Examples:

            ```python
            form = StatusWorkflowForm(...)
            builder = builder.with_status_workflow(form)
            ```
        """
        return ProjectBuilderWithStatusWorkflow[
            MCFOpt, GTFOpt, QMFOpt, QRMOpt, WHOpt, ResMC, ResGT, ResQM, ResQRM, ResWH
        ](
            kit=self.kit,
            form=self.form,
            money_config=self.money_config,
            ground_truth=self.ground_truth,
            quality_management=self.quality_management,
            quorum=self.quorum,
            status_workflow=status_workflow,
            webhooks=self.webhooks,
        )

    def with_webhook(
        self: 'ProjectBuilderWithoutWebhook[MCFOpt, GTFOpt, QMFOpt, QRMOpt, SWOpt, ResMC, ResGT, ResQM, ResQRM, ResSW]',
        webhook: WebhookFormStrict | str,
    ) -> 'ProjectBuilderWithWebhook[MCFOpt, GTFOpt, QMFOpt, QRMOpt, SWOpt, ResMC, ResGT, ResQM, ResQRM, ResSW]':
        """Configures webhook extension for the project being built.

        Adds webhook configuration to the builder, either as parameters for a new webhook or an existing webhook ID.
        Webhooks allow sending notifications about project and annotation events to external systems.

        Args:
            webhook: Either parameters for creating new webhook or ID of existing webhook to use

        Returns:
            Updated builder with webhook configuration added. The return type reflects that webhook
            will be available after build.

        Examples:
            Use existing webhook:
            ```python
            builder = builder.with_webhook('existing-webhook-id')
            ```

            Create new webhook:
            ```python
            form = WebhookFormStrict(
                url='https://example.com/webhook',
                method='POST',
                enabled=True,
                mode='LIVE',
                actions=['STATUS_WORKFLOW_STATUS_CHANGED'],
                action_params=StatusWorkflowStatusChangedParams(
                    status_workflow_status_changed_statuses=['accepted', 'rejected']
                ),
            )
            builder = builder.with_webhook(form)
            ```
        """
        return ProjectBuilderWithWebhook[MCFOpt, GTFOpt, QMFOpt, QRMOpt, SWOpt, ResMC, ResGT, ResQM, ResQRM, ResSW](
            kit=self.kit,
            form=self.form,
            money_config=self.money_config,
            ground_truth=self.ground_truth,
            quality_management=self.quality_management,
            quorum=self.quorum,
            status_workflow=self.status_workflow,
            webhooks=webhook,
        )


InitialProjectBuilder = ProjectBuilder[None, None, None, None, None, None, None, None, None, None, None, None]
ProjectBuilderWithoutMoneyConfig = ProjectBuilder[
    None, GTFOpt, QMFOpt, QRMOpt, SWOpt, WHOpt, None, ResGT, ResQM, ResQRM, ResSW, ResWH
]
ProjectBuilderWithMoneyConfig = ProjectBuilder[
    StatusWorkflowMoneyConfigFormParamsWithDefaults
    | AnnotationMoneyConfigFormParamsWithDefaults
    | MoneyConfigFormStrict
    | MoneyConfigId,
    GTFOpt,
    QMFOpt,
    QRMOpt,
    SWOpt,
    WHOpt,
    MoneyConfigViewStrict,
    ResGT,
    ResQM,
    ResQRM,
    ResSW,
    ResWH,
]
ProjectBuilderWithoutGroundTruth = ProjectBuilder[
    MCFOpt, None, QMFOpt, QRMOpt, SWOpt, WHOpt, ResMC, None, ResQM, ResQRM, ResSW, ResWH
]
ProjectBuilderWithGroundTruth = ProjectBuilder[
    MCFOpt,
    GroundTruthConfigForm | GroundTruthConfigId,
    QMFOpt,
    QRMOpt,
    SWOpt,
    WHOpt,
    ResMC,
    GroundTruthConfigViewV0Strict,
    ResQM,
    ResQRM,
    ResSW,
    ResWH,
]
ProjectBuilderWithoutQualityManagement = ProjectBuilder[
    MCFOpt, GTFOpt, None, QRMOpt, SWOpt, WHOpt, ResMC, ResGT, None, ResQRM, ResSW, ResWH
]
ProjectBuilderWithQualityManagement = ProjectBuilder[
    MCFOpt,
    GTFOpt,
    QualityConfigFormV0Strict | QualityConfigId,
    QRMOpt,
    SWOpt,
    WHOpt,
    ResMC,
    ResGT,
    QualityConfigViewV0Strict,
    ResQRM,
    ResSW,
    ResWH,
]
ProjectBuilderWithoutQuorum = ProjectBuilder[
    MCFOpt,
    GTFOpt,
    QMFOpt,
    None,
    SWOpt,
    WHOpt,
    ResMC,
    ResGT,
    ResQM,
    None,
    ResSW,
    ResWH,
]
ProjectBuilderWithQuorum = ProjectBuilder[
    MCFOpt,
    GTFOpt,
    QMFOpt,
    QuorumConfigForm,
    SWOpt,
    WHOpt,
    ResMC,
    ResGT,
    ResQM,
    QuorumConfigView,
    ResSW,
    ResWH,
]
ProjectBuilderWithoutStatusWorkflow = ProjectBuilder[
    MCFOpt,
    GTFOpt,
    QMFOpt,
    QRMOpt,
    None,
    WHOpt,
    ResMC,
    ResGT,
    ResQM,
    ResQRM,
    None,
    ResWH,
]
ProjectBuilderWithStatusWorkflow = ProjectBuilder[
    MCFOpt,
    GTFOpt,
    QMFOpt,
    QRMOpt,
    StatusWorkflowForm,
    WHOpt,
    ResMC,
    ResGT,
    ResQM,
    ResQRM,
    StatusWorkflowConfigViewStrict,
    ResWH,
]
ProjectBuilderWithoutWebhook = ProjectBuilder[
    MCFOpt,
    GTFOpt,
    QMFOpt,
    QRMOpt,
    SWOpt,
    None,
    ResMC,
    ResGT,
    ResQM,
    ResQRM,
    ResSW,
    None,
]
ProjectBuilderWithWebhook = ProjectBuilder[
    MCFOpt,
    GTFOpt,
    QMFOpt,
    QRMOpt,
    SWOpt,
    WebhookFormStrict | str,
    ResMC,
    ResGT,
    ResQM,
    ResQRM,
    ResSW,
    WebhookViewStrict,
]
