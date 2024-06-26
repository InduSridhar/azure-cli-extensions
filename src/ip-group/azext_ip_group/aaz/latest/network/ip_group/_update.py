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
    "network ip-group update",
)
class Update(AAZCommand):
    """Update an IP group.
    """

    _aaz_info = {
        "version": "2019-09-01",
        "resources": [
            ["mgmt-plane", "/subscriptions/{}/resourcegroups/{}/providers/microsoft.network/ipgroups/{}", "2019-09-01"],
        ]
    }

    AZ_SUPPORT_NO_WAIT = True

    AZ_SUPPORT_GENERIC_UPDATE = True

    def _handler(self, command_args):
        super()._handler(command_args)
        return self.build_lro_poller(self._execute_operations, self._output)

    _args_schema = None

    @classmethod
    def _build_arguments_schema(cls, *args, **kwargs):
        if cls._args_schema is not None:
            return cls._args_schema
        cls._args_schema = super()._build_arguments_schema(*args, **kwargs)

        # define Arg Group ""

        _args_schema = cls._args_schema
        _args_schema.ip_groups_name = AAZStrArg(
            options=["-n", "--name", "--ip-groups-name"],
            help="The name of the ipGroups.",
            required=True,
            id_part="name",
        )
        _args_schema.resource_group = AAZResourceGroupNameArg(
            required=True,
        )
        _args_schema.ip_addresses = AAZListArg(
            options=["--ip-addresses"],
            help="Space-separated list of IpAddress or IpAddressPrefix.",
            nullable=True,
        )
        _args_schema.tags = AAZDictArg(
            options=["--tags"],
            help="Space-separated tags: key[=value] [key[=value] ...]. Use \"\" to clear existing tags.",
            nullable=True,
        )

        ip_addresses = cls._args_schema.ip_addresses
        ip_addresses.Element = AAZStrArg(
            nullable=True,
        )

        tags = cls._args_schema.tags
        tags.Element = AAZStrArg(
            nullable=True,
        )

        # define Arg Group "Parameters"
        return cls._args_schema

    def _execute_operations(self):
        self.pre_operations()
        self.IpGroupsGet(ctx=self.ctx)()
        self.pre_instance_update(self.ctx.vars.instance)
        self.InstanceUpdateByJson(ctx=self.ctx)()
        self.InstanceUpdateByGeneric(ctx=self.ctx)()
        self.post_instance_update(self.ctx.vars.instance)
        yield self.IpGroupsCreateOrUpdate(ctx=self.ctx)()
        self.post_operations()

    @register_callback
    def pre_operations(self):
        pass

    @register_callback
    def post_operations(self):
        pass

    @register_callback
    def pre_instance_update(self, instance):
        pass

    @register_callback
    def post_instance_update(self, instance):
        pass

    def _output(self, *args, **kwargs):
        result = self.deserialize_output(self.ctx.vars.instance, client_flatten=True)
        return result

    class IpGroupsGet(AAZHttpOperation):
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
                "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/ipGroups/{ipGroupsName}",
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
                    "ipGroupsName", self.ctx.args.ip_groups_name,
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
                    "api-version", "2019-09-01",
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
            _UpdateHelper._build_schema_ip_group_read(cls._schema_on_200)

            return cls._schema_on_200

    class IpGroupsCreateOrUpdate(AAZHttpOperation):
        CLIENT_TYPE = "MgmtClient"

        def __call__(self, *args, **kwargs):
            request = self.make_request()
            session = self.client.send_request(request=request, stream=False, **kwargs)
            if session.http_response.status_code in [202]:
                return self.client.build_lro_polling(
                    self.ctx.args.no_wait,
                    session,
                    self.on_200_201,
                    self.on_error,
                    lro_options={"final-state-via": "azure-async-operation"},
                    path_format_arguments=self.url_parameters,
                )
            if session.http_response.status_code in [200, 201]:
                return self.client.build_lro_polling(
                    self.ctx.args.no_wait,
                    session,
                    self.on_200_201,
                    self.on_error,
                    lro_options={"final-state-via": "azure-async-operation"},
                    path_format_arguments=self.url_parameters,
                )

            return self.on_error(session.http_response)

        @property
        def url(self):
            return self.client.format_url(
                "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/ipGroups/{ipGroupsName}",
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
                    "ipGroupsName", self.ctx.args.ip_groups_name,
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
                    "api-version", "2019-09-01",
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

        def on_200_201(self, session):
            data = self.deserialize_http_content(session)
            self.ctx.set_var(
                "instance",
                data,
                schema_builder=self._build_schema_on_200_201
            )

        _schema_on_200_201 = None

        @classmethod
        def _build_schema_on_200_201(cls):
            if cls._schema_on_200_201 is not None:
                return cls._schema_on_200_201

            cls._schema_on_200_201 = AAZObjectType()
            _UpdateHelper._build_schema_ip_group_read(cls._schema_on_200_201)

            return cls._schema_on_200_201

    class InstanceUpdateByJson(AAZJsonInstanceUpdateOperation):

        def __call__(self, *args, **kwargs):
            self._update_instance(self.ctx.vars.instance)

        def _update_instance(self, instance):
            _instance_value, _builder = self.new_content_builder(
                self.ctx.args,
                value=instance,
                typ=AAZObjectType
            )
            _builder.set_prop("properties", AAZObjectType, typ_kwargs={"flags": {"client_flatten": True}})
            _builder.set_prop("tags", AAZDictType, ".tags")

            properties = _builder.get(".properties")
            if properties is not None:
                properties.set_prop("ipAddresses", AAZListType, ".ip_addresses")

            ip_addresses = _builder.get(".properties.ipAddresses")
            if ip_addresses is not None:
                ip_addresses.set_elements(AAZStrType, ".")

            tags = _builder.get(".tags")
            if tags is not None:
                tags.set_elements(AAZStrType, ".")

            return _instance_value

    class InstanceUpdateByGeneric(AAZGenericInstanceUpdateOperation):

        def __call__(self, *args, **kwargs):
            self._update_instance_by_generic(
                self.ctx.vars.instance,
                self.ctx.generic_update_args
            )


class _UpdateHelper:
    """Helper class for Update"""

    _schema_ip_group_read = None

    @classmethod
    def _build_schema_ip_group_read(cls, _schema):
        if cls._schema_ip_group_read is not None:
            _schema.etag = cls._schema_ip_group_read.etag
            _schema.id = cls._schema_ip_group_read.id
            _schema.location = cls._schema_ip_group_read.location
            _schema.name = cls._schema_ip_group_read.name
            _schema.properties = cls._schema_ip_group_read.properties
            _schema.tags = cls._schema_ip_group_read.tags
            _schema.type = cls._schema_ip_group_read.type
            return

        cls._schema_ip_group_read = _schema_ip_group_read = AAZObjectType()

        ip_group_read = _schema_ip_group_read
        ip_group_read.etag = AAZStrType(
            flags={"read_only": True},
        )
        ip_group_read.id = AAZStrType()
        ip_group_read.location = AAZStrType()
        ip_group_read.name = AAZStrType(
            flags={"read_only": True},
        )
        ip_group_read.properties = AAZObjectType(
            flags={"client_flatten": True},
        )
        ip_group_read.tags = AAZDictType()
        ip_group_read.type = AAZStrType(
            flags={"read_only": True},
        )

        properties = _schema_ip_group_read.properties
        properties.firewalls = AAZListType(
            flags={"read_only": True},
        )
        properties.ip_addresses = AAZListType(
            serialized_name="ipAddresses",
        )
        properties.provisioning_state = AAZStrType(
            serialized_name="provisioningState",
            flags={"read_only": True},
        )

        firewalls = _schema_ip_group_read.properties.firewalls
        firewalls.Element = AAZObjectType()

        _element = _schema_ip_group_read.properties.firewalls.Element
        _element.id = AAZStrType()

        ip_addresses = _schema_ip_group_read.properties.ip_addresses
        ip_addresses.Element = AAZStrType()

        tags = _schema_ip_group_read.tags
        tags.Element = AAZStrType()

        _schema.etag = cls._schema_ip_group_read.etag
        _schema.id = cls._schema_ip_group_read.id
        _schema.location = cls._schema_ip_group_read.location
        _schema.name = cls._schema_ip_group_read.name
        _schema.properties = cls._schema_ip_group_read.properties
        _schema.tags = cls._schema_ip_group_read.tags
        _schema.type = cls._schema_ip_group_read.type


__all__ = ["Update"]
