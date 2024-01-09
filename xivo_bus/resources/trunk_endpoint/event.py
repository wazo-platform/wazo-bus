# Copyright 2016-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from ..common.event import TenantEvent
from ..common.types import UUIDStr
from .types import EndpointCustomDict, EndpointIAXDict, EndpointSIPDict, TrunkDict


class TrunkEndpointSIPAssociatedEvent(TenantEvent):
    service = 'confd'
    name = 'trunk_endpoint_sip_associated'
    routing_key_fmt = (
        'config.trunks.{trunk[id]}.endpoints.sip.{endpoint_sip[uuid]}.updated'
    )

    def __init__(
        self,
        trunk: TrunkDict,
        sip: EndpointSIPDict,
        tenant_uuid: UUIDStr,
    ):
        content = {
            'trunk': trunk,
            'endpoint_sip': sip,
        }
        super().__init__(content, tenant_uuid)


class TrunkEndpointSIPDissociatedEvent(TenantEvent):
    service = 'confd'
    name = 'trunk_endpoint_sip_dissociated'
    routing_key_fmt = (
        'config.trunks.{trunk[id]}.endpoints.sip.{endpoint_sip[uuid]}.deleted'
    )

    def __init__(
        self,
        trunk: TrunkDict,
        sip: EndpointSIPDict,
        tenant_uuid: UUIDStr,
    ):
        content = {
            'trunk': trunk,
            'endpoint_sip': sip,
        }
        super().__init__(content, tenant_uuid)


class TrunkEndpointIAXAssociatedEvent(TenantEvent):
    service = 'confd'
    name = 'trunk_endpoint_iax_associated'
    routing_key_fmt = (
        'config.trunks.{trunk[id]}.endpoints.iax.{endpoint_iax[id]}.updated'
    )

    def __init__(
        self,
        trunk: TrunkDict,
        iax: EndpointIAXDict,
        tenant_uuid: UUIDStr,
    ):
        content = {
            'trunk': trunk,
            'endpoint_iax': iax,
        }
        super().__init__(content, tenant_uuid)


class TrunkEndpointIAXDissociatedEvent(TenantEvent):
    service = 'confd'
    name = 'trunk_endpoint_iax_dissociated'
    routing_key_fmt = (
        'config.trunks.{trunk[id]}.endpoints.iax.{endpoint_iax[id]}.deleted'
    )

    def __init__(
        self,
        trunk: TrunkDict,
        iax: EndpointIAXDict,
        tenant_uuid: UUIDStr,
    ):
        content = {
            'trunk': trunk,
            'endpoint_iax': iax,
        }
        super().__init__(content, tenant_uuid)


class TrunkEndpointCustomAssociatedEvent(TenantEvent):
    service = 'confd'
    name = 'trunk_endpoint_custom_associated'
    routing_key_fmt = (
        'config.trunks.{trunk[id]}.endpoints.custom.{endpoint_custom[id]}.updated'
    )

    def __init__(
        self,
        trunk: TrunkDict,
        custom: EndpointCustomDict,
        tenant_uuid: UUIDStr,
    ):
        content = {
            'trunk': trunk,
            'endpoint_custom': custom,
        }
        super().__init__(content, tenant_uuid)


class TrunkEndpointCustomDissociatedEvent(TenantEvent):
    service = 'confd'
    name = 'trunk_endpoint_custom_dissociated'
    routing_key_fmt = (
        'config.trunks.{trunk[id]}.endpoints.custom.{endpoint_custom[id]}.deleted'
    )

    def __init__(
        self,
        trunk: TrunkDict,
        custom: EndpointCustomDict,
        tenant_uuid: UUIDStr,
    ):
        content = {
            'trunk': trunk,
            'endpoint_custom': custom,
        }
        super().__init__(content, tenant_uuid)
