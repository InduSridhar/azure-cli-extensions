# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------

from ._models_py3 import AppResource
from ._models_py3 import AppResourceCollection
from ._models_py3 import AppResourceProperties
from ._models_py3 import ApplicationInsightsAgentVersions
from ._models_py3 import AvailableOperations
from ._models_py3 import AvailableRuntimeVersions
from ._models_py3 import BindingResource
from ._models_py3 import BindingResourceCollection
from ._models_py3 import BindingResourceProperties
from ._models_py3 import CertificateProperties
from ._models_py3 import CertificateResource
from ._models_py3 import CertificateResourceCollection
from ._models_py3 import CloudErrorBody
from ._models_py3 import ClusterResourceProperties
from ._models_py3 import ConfigServerGitProperty
from ._models_py3 import ConfigServerProperties
from ._models_py3 import ConfigServerResource
from ._models_py3 import ConfigServerSettings
from ._models_py3 import ConfigServerSettingsErrorRecord
from ._models_py3 import ConfigServerSettingsValidateResult
from ._models_py3 import CustomDomainProperties
from ._models_py3 import CustomDomainResource
from ._models_py3 import CustomDomainResourceCollection
from ._models_py3 import CustomDomainValidatePayload
from ._models_py3 import CustomDomainValidateResult
from ._models_py3 import DeploymentInstance
from ._models_py3 import DeploymentResource
from ._models_py3 import DeploymentResourceCollection
from ._models_py3 import DeploymentResourceProperties
from ._models_py3 import DeploymentSettings
from ._models_py3 import Error
from ._models_py3 import GitPatternRepository
from ._models_py3 import LogFileUrlResponse
from ._models_py3 import LogSpecification
from ._models_py3 import ManagedIdentityProperties
from ._models_py3 import MetricDimension
from ._models_py3 import MetricSpecification
from ._models_py3 import MonitoringSettingProperties
from ._models_py3 import MonitoringSettingResource
from ._models_py3 import NameAvailability
from ._models_py3 import NameAvailabilityParameters
from ._models_py3 import NetworkProfile
from ._models_py3 import NetworkProfileOutboundIPs
from ._models_py3 import OperationDetail
from ._models_py3 import OperationDisplay
from ._models_py3 import OperationProperties
from ._models_py3 import PersistentDisk
from ._models_py3 import ProxyResource
from ._models_py3 import RegenerateTestKeyRequestPayload
from ._models_py3 import RequiredTraffic
from ._models_py3 import Resource
from ._models_py3 import ResourceSku
from ._models_py3 import ResourceSkuCapabilities
from ._models_py3 import ResourceSkuCollection
from ._models_py3 import ResourceSkuLocationInfo
from ._models_py3 import ResourceSkuRestrictionInfo
from ._models_py3 import ResourceSkuRestrictions
from ._models_py3 import ResourceSkuZoneDetails
from ._models_py3 import ResourceUploadDefinition
from ._models_py3 import ServiceResource
from ._models_py3 import ServiceResourceList
from ._models_py3 import ServiceSpecification
from ._models_py3 import Sku
from ._models_py3 import SkuCapacity
from ._models_py3 import SupportedRuntimeVersion
from ._models_py3 import TemporaryDisk
from ._models_py3 import TestKeys
from ._models_py3 import TrackedResource
from ._models_py3 import UserSourceInfo

from ._app_platform_management_client_enums import ActionType
from ._app_platform_management_client_enums import AppResourceProvisioningState
from ._app_platform_management_client_enums import ConfigServerState
from ._app_platform_management_client_enums import DeploymentResourceProvisioningState
from ._app_platform_management_client_enums import DeploymentResourceStatus
from ._app_platform_management_client_enums import ManagedIdentityType
from ._app_platform_management_client_enums import MonitoringSettingState
from ._app_platform_management_client_enums import ProvisioningState
from ._app_platform_management_client_enums import ResourceSkuRestrictionsReasonCode
from ._app_platform_management_client_enums import ResourceSkuRestrictionsType
from ._app_platform_management_client_enums import RuntimeVersion
from ._app_platform_management_client_enums import SkuScaleType
from ._app_platform_management_client_enums import SupportedRuntimePlatform
from ._app_platform_management_client_enums import SupportedRuntimeValue
from ._app_platform_management_client_enums import TestKeyType
from ._app_platform_management_client_enums import TrafficDirection
from ._app_platform_management_client_enums import UserSourceType
from ._patch import __all__ as _patch_all
from ._patch import *  # type: ignore # pylint: disable=unused-wildcard-import
from ._patch import patch_sdk as _patch_sdk

__all__ = [
    "AppResource",
    "AppResourceCollection",
    "AppResourceProperties",
    "ApplicationInsightsAgentVersions",
    "AvailableOperations",
    "AvailableRuntimeVersions",
    "BindingResource",
    "BindingResourceCollection",
    "BindingResourceProperties",
    "CertificateProperties",
    "CertificateResource",
    "CertificateResourceCollection",
    "CloudErrorBody",
    "ClusterResourceProperties",
    "ConfigServerGitProperty",
    "ConfigServerProperties",
    "ConfigServerResource",
    "ConfigServerSettings",
    "ConfigServerSettingsErrorRecord",
    "ConfigServerSettingsValidateResult",
    "CustomDomainProperties",
    "CustomDomainResource",
    "CustomDomainResourceCollection",
    "CustomDomainValidatePayload",
    "CustomDomainValidateResult",
    "DeploymentInstance",
    "DeploymentResource",
    "DeploymentResourceCollection",
    "DeploymentResourceProperties",
    "DeploymentSettings",
    "Error",
    "GitPatternRepository",
    "LogFileUrlResponse",
    "LogSpecification",
    "ManagedIdentityProperties",
    "MetricDimension",
    "MetricSpecification",
    "MonitoringSettingProperties",
    "MonitoringSettingResource",
    "NameAvailability",
    "NameAvailabilityParameters",
    "NetworkProfile",
    "NetworkProfileOutboundIPs",
    "OperationDetail",
    "OperationDisplay",
    "OperationProperties",
    "PersistentDisk",
    "ProxyResource",
    "RegenerateTestKeyRequestPayload",
    "RequiredTraffic",
    "Resource",
    "ResourceSku",
    "ResourceSkuCapabilities",
    "ResourceSkuCollection",
    "ResourceSkuLocationInfo",
    "ResourceSkuRestrictionInfo",
    "ResourceSkuRestrictions",
    "ResourceSkuZoneDetails",
    "ResourceUploadDefinition",
    "ServiceResource",
    "ServiceResourceList",
    "ServiceSpecification",
    "Sku",
    "SkuCapacity",
    "SupportedRuntimeVersion",
    "TemporaryDisk",
    "TestKeys",
    "TrackedResource",
    "UserSourceInfo",
    "ActionType",
    "AppResourceProvisioningState",
    "ConfigServerState",
    "DeploymentResourceProvisioningState",
    "DeploymentResourceStatus",
    "ManagedIdentityType",
    "MonitoringSettingState",
    "ProvisioningState",
    "ResourceSkuRestrictionsReasonCode",
    "ResourceSkuRestrictionsType",
    "RuntimeVersion",
    "SkuScaleType",
    "SupportedRuntimePlatform",
    "SupportedRuntimeValue",
    "TestKeyType",
    "TrafficDirection",
    "UserSourceType",
]
__all__.extend([p for p in _patch_all if p not in __all__])
_patch_sdk()
