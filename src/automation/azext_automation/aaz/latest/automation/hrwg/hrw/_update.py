# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
#
# Code generated by aaz-dev-tools
# --------------------------------------------------------------------------------------------

# pylint: skip-file
# flake8: noqa

from azure.cli.core.aaz import *


@register_command(
    "automation hrwg hrw update",
)
class Update(AAZCommand):
    """Create a hybrid runbook worker.
    """

    _aaz_info = {
        "version": "2021-06-22",
        "resources": [
            ["mgmt-plane", "/subscriptions/{}/resourcegroups/{}/providers/microsoft.automation/automationaccounts/{}/hybridrunbookworkergroups/{}/hybridrunbookworkers/{}", "2021-06-22"],
        ]
    }

    AZ_SUPPORT_GENERIC_UPDATE = True

    def _handler(self, command_args):
        super()._handler(command_args)
        self._execute_operations()
        return self._output()

    _args_schema = None

    @classmethod
    def _build_arguments_schema(cls, *args, **kwargs):
        if cls._args_schema is not None:
            return cls._args_schema
        cls._args_schema = super()._build_arguments_schema(*args, **kwargs)

        # define Arg Group ""

        _args_schema = cls._args_schema
        _args_schema.automation_account_name = AAZStrArg(
            options=["--automation-account-name"],
            help="The name of the automation account.",
            required=True,
            id_part="name",
        )
        _args_schema.hybrid_runbook_worker_group_name = AAZStrArg(
            options=["--hybrid-runbook-worker-group-name"],
            help="The hybrid runbook worker group name",
            required=True,
            id_part="child_name_1",
        )
        _args_schema.hybrid_runbook_worker_id = AAZStrArg(
            options=["-n", "--name", "--hybrid-runbook-worker-id"],
            help="The hybrid runbook worker id",
            required=True,
            id_part="child_name_2",
        )
        _args_schema.resource_group = AAZResourceGroupNameArg(
            required=True,
        )

        # define Arg Group "Properties"

        _args_schema = cls._args_schema
        _args_schema.vm_resource_id = AAZStrArg(
            options=["--vm-resource-id"],
            arg_group="Properties",
            help="Azure Resource Manager Id for a virtual machine.",
            nullable=True,
        )
        return cls._args_schema

    def _execute_operations(self):
        self.HybridRunbookWorkersGet(ctx=self.ctx)()
        self.InstanceUpdateByJson(ctx=self.ctx)()
        self.InstanceUpdateByGeneric(ctx=self.ctx)()
        self.HybridRunbookWorkersCreate(ctx=self.ctx)()

    def _output(self, *args, **kwargs):
        result = self.deserialize_output(self.ctx.vars.instance, client_flatten=True)
        return result

    class HybridRunbookWorkersGet(AAZHttpOperation):
        CLIENT_TYPE = "MgmtClient"

        def __call__(self, *args, **kwargs):
            request = self.make_request()
            session = self.client.send_request(request=request, stream=False, **kwargs)
            if session.http_response.status_code in [200]:
                return self.on_200(session)

            return self.on_error(session.http_response)

        @property
        def url(self):
            return self.client.format_url(
                "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Automation/automationAccounts/{automationAccountName}/hybridRunbookWorkerGroups/{hybridRunbookWorkerGroupName}/hybridRunbookWorkers/{hybridRunbookWorkerId}",
                **self.url_parameters
            )

        @property
        def method(self):
            return "GET"

        @property
        def error_format(self):
            return "ODataV4Format"

        @property
        def url_parameters(self):
            parameters = {
                **self.serialize_url_param(
                    "automationAccountName", self.ctx.args.automation_account_name,
                    required=True,
                ),
                **self.serialize_url_param(
                    "hybridRunbookWorkerGroupName", self.ctx.args.hybrid_runbook_worker_group_name,
                    required=True,
                ),
                **self.serialize_url_param(
                    "hybridRunbookWorkerId", self.ctx.args.hybrid_runbook_worker_id,
                    required=True,
                ),
                **self.serialize_url_param(
                    "resourceGroupName", self.ctx.args.resource_group,
                    required=True,
                ),
                **self.serialize_url_param(
                    "subscriptionId", self.ctx.subscription_id,
                    required=True,
                ),
            }
            return parameters

        @property
        def query_parameters(self):
            parameters = {
                **self.serialize_query_param(
                    "api-version", "2021-06-22",
                    required=True,
                ),
            }
            return parameters

        @property
        def header_parameters(self):
            parameters = {
                **self.serialize_header_param(
                    "Accept", "application/json",
                ),
            }
            return parameters

        def on_200(self, session):
            data = self.deserialize_http_content(session)
            self.ctx.set_var(
                "instance",
                data,
                schema_builder=self._build_schema_on_200
            )

        _schema_on_200 = None

        @classmethod
        def _build_schema_on_200(cls):
            if cls._schema_on_200 is not None:
                return cls._schema_on_200

            cls._schema_on_200 = AAZObjectType()
            _build_schema_hybrid_runbook_worker_read(cls._schema_on_200)

            return cls._schema_on_200

    class HybridRunbookWorkersCreate(AAZHttpOperation):
        CLIENT_TYPE = "MgmtClient"

        def __call__(self, *args, **kwargs):
            request = self.make_request()
            session = self.client.send_request(request=request, stream=False, **kwargs)
            if session.http_response.status_code in [200]:
                return self.on_200(session)

            return self.on_error(session.http_response)

        @property
        def url(self):
            return self.client.format_url(
                "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Automation/automationAccounts/{automationAccountName}/hybridRunbookWorkerGroups/{hybridRunbookWorkerGroupName}/hybridRunbookWorkers/{hybridRunbookWorkerId}",
                **self.url_parameters
            )

        @property
        def method(self):
            return "PUT"

        @property
        def error_format(self):
            return "ODataV4Format"

        @property
        def url_parameters(self):
            parameters = {
                **self.serialize_url_param(
                    "automationAccountName", self.ctx.args.automation_account_name,
                    required=True,
                ),
                **self.serialize_url_param(
                    "hybridRunbookWorkerGroupName", self.ctx.args.hybrid_runbook_worker_group_name,
                    required=True,
                ),
                **self.serialize_url_param(
                    "hybridRunbookWorkerId", self.ctx.args.hybrid_runbook_worker_id,
                    required=True,
                ),
                **self.serialize_url_param(
                    "resourceGroupName", self.ctx.args.resource_group,
                    required=True,
                ),
                **self.serialize_url_param(
                    "subscriptionId", self.ctx.subscription_id,
                    required=True,
                ),
            }
            return parameters

        @property
        def query_parameters(self):
            parameters = {
                **self.serialize_query_param(
                    "api-version", "2021-06-22",
                    required=True,
                ),
            }
            return parameters

        @property
        def header_parameters(self):
            parameters = {
                **self.serialize_header_param(
                    "Content-Type", "application/json",
                ),
                **self.serialize_header_param(
                    "Accept", "application/json",
                ),
            }
            return parameters

        @property
        def content(self):
            _content_value, _builder = self.new_content_builder(
                self.ctx.args,
                value=self.ctx.vars.instance,
            )

            return self.serialize_content(_content_value)

        def on_200(self, session):
            data = self.deserialize_http_content(session)
            self.ctx.set_var(
                "instance",
                data,
                schema_builder=self._build_schema_on_200
            )

        _schema_on_200 = None

        @classmethod
        def _build_schema_on_200(cls):
            if cls._schema_on_200 is not None:
                return cls._schema_on_200

            cls._schema_on_200 = AAZObjectType()
            _build_schema_hybrid_runbook_worker_read(cls._schema_on_200)

            return cls._schema_on_200

    class InstanceUpdateByJson(AAZJsonInstanceUpdateOperation):

        def __call__(self, *args, **kwargs):
            self._update_instance(self.ctx.vars.instance)

        def _update_instance(self, instance):
            _instance_value, _builder = self.new_content_builder(
                self.ctx.args,
                value=instance,
                typ=AAZObjectType
            )
            _builder.set_prop("name", AAZStrType, ".hybrid_runbook_worker_id")
            _builder.set_prop("properties", AAZObjectType, ".", typ_kwargs={"flags": {"required": True, "client_flatten": True}})

            properties = _builder.get(".properties")
            if properties is not None:
                properties.set_prop("vmResourceId", AAZStrType, ".vm_resource_id")

            return _instance_value

    class InstanceUpdateByGeneric(AAZGenericInstanceUpdateOperation):

        def __call__(self, *args, **kwargs):
            self._update_instance_by_generic(
                self.ctx.vars.instance,
                self.ctx.generic_update_args
            )


_schema_hybrid_runbook_worker_read = None


def _build_schema_hybrid_runbook_worker_read(_schema):
    global _schema_hybrid_runbook_worker_read
    if _schema_hybrid_runbook_worker_read is not None:
        _schema.id = _schema_hybrid_runbook_worker_read.id
        _schema.name = _schema_hybrid_runbook_worker_read.name
        _schema.properties = _schema_hybrid_runbook_worker_read.properties
        _schema.system_data = _schema_hybrid_runbook_worker_read.system_data
        _schema.type = _schema_hybrid_runbook_worker_read.type
        return

    _schema_hybrid_runbook_worker_read = AAZObjectType()

    hybrid_runbook_worker_read = _schema_hybrid_runbook_worker_read
    hybrid_runbook_worker_read.id = AAZStrType(
        flags={"read_only": True},
    )
    hybrid_runbook_worker_read.name = AAZStrType(
        flags={"read_only": True},
    )
    hybrid_runbook_worker_read.properties = AAZObjectType(
        flags={"client_flatten": True},
    )
    hybrid_runbook_worker_read.system_data = AAZObjectType(
        serialized_name="systemData",
        flags={"read_only": True},
    )
    hybrid_runbook_worker_read.type = AAZStrType(
        flags={"read_only": True},
    )

    properties = _schema_hybrid_runbook_worker_read.properties
    properties.ip = AAZStrType()
    properties.last_seen_date_time = AAZStrType(
        serialized_name="lastSeenDateTime",
    )
    properties.registered_date_time = AAZStrType(
        serialized_name="registeredDateTime",
    )
    properties.vm_resource_id = AAZStrType(
        serialized_name="vmResourceId",
    )
    properties.worker_name = AAZStrType(
        serialized_name="workerName",
    )
    properties.worker_type = AAZStrType(
        serialized_name="workerType",
    )

    system_data = _schema_hybrid_runbook_worker_read.system_data
    system_data.created_at = AAZStrType(
        serialized_name="createdAt",
        flags={"read_only": True},
    )
    system_data.created_by = AAZStrType(
        serialized_name="createdBy",
        flags={"read_only": True},
    )
    system_data.created_by_type = AAZStrType(
        serialized_name="createdByType",
        flags={"read_only": True},
    )
    system_data.last_modified_at = AAZStrType(
        serialized_name="lastModifiedAt",
        flags={"read_only": True},
    )
    system_data.last_modified_by = AAZStrType(
        serialized_name="lastModifiedBy",
        flags={"read_only": True},
    )
    system_data.last_modified_by_type = AAZStrType(
        serialized_name="lastModifiedByType",
        flags={"read_only": True},
    )

    _schema.id = _schema_hybrid_runbook_worker_read.id
    _schema.name = _schema_hybrid_runbook_worker_read.name
    _schema.properties = _schema_hybrid_runbook_worker_read.properties
    _schema.system_data = _schema_hybrid_runbook_worker_read.system_data
    _schema.type = _schema_hybrid_runbook_worker_read.type


__all__ = ["Update"]
