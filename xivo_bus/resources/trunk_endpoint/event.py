# Copyright 2016-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_bus.resources.common.event import TenantEvent


class TrunkEndpointSIPAssociatedEvent(TenantEvent):
    service = 'confd'
    name = 'trunk_endpoint_sip_associated'
    routing_key_fmt = 'config.trunks.{trunk[id]}.endpoints.sip.{endpoint_sip[uuid]}.updated'

    def __init__(self, trunk, sip, tenant_uuid):
        content = {
            'trunk': trunk,
            'endpoint_sip': sip,
        }
        super(TrunkEndpointSIPAssociatedEvent, self).__init__(content, tenant_uuid)


class TrunkEndpointSIPDissociatedEvent(TenantEvent):
    service = 'confd'
    name = 'trunk_endpoint_sip_dissociated'
    routing_key_fmt = 'config.trunks.{trunk[id]}.endpoints.sip.{endpoint_sip[uuid]}.deleted'

    def __init__(self, trunk, sip, tenant_uuid):
        content = {
            'trunk': trunk,
            'endpoint_sip': sip,
        }
        super(TrunkEndpointSIPDissociatedEvent, self).__init__(content, tenant_uuid)


class TrunkEndpointIAXAssociatedEvent(TenantEvent):
    service = 'confd'
    name = 'trunk_endpoint_iax_associated'
    routing_key_fmt = 'config.trunks.{trunk[id]}.endpoints.iax.{endpoint_iax[id]}.updated'

    def __init__(self, trunk, iax, tenant_uuid):
        content = {
            'trunk': trunk,
            'endpoint_iax': iax,
        }
        super(TrunkEndpointIAXAssociatedEvent, self).__init__(content, tenant_uuid)


class TrunkEndpointIAXDissociatedEvent(TenantEvent):
    service = 'confd'
    name = 'trunk_endpoint_iax_dissociated'
    routing_key_fmt = 'config.trunks.{trunk[id]}.endpoints.iax.{endpoint_iax[id]}.deleted'

    def __init__(self, trunk, iax, tenant_uuid):
        content = {
            'trunk': trunk,
            'endpoint_iax': iax,
        }
        super(TrunkEndpointIAXDissociatedEvent, self).__init__(content, tenant_uuid)


class TrunkEndpointCustomAssociatedEvent(TenantEvent):
    service = 'confd'
    name = 'trunk_endpoint_custom_associated'
    routing_key_fmt = 'config.trunks.{trunk[id]}.endpoints.custom.{endpoint_custom[id]}.updated'

    def __init__(self, trunk, custom, tenant_uuid):
        content = {
            'trunk': trunk,
            'endpoint_custom': custom,
        }
        super(TrunkEndpointCustomAssociatedEvent, self).__init__(content, tenant_uuid)


class TrunkEndpointCustomDissociatedEvent(TenantEvent):
    service = 'confd'
    name = 'trunk_endpoint_custom_dissociated'
    routing_key_fmt = 'config.trunks.{trunk[id]}.endpoints.custom.{endpoint_custom[id]}.deleted'

    def __init__(self, trunk, custom, tenant_uuid):
        content = {
            'trunk': trunk,
            'endpoint_custom': custom,
        }
        super(TrunkEndpointCustomDissociatedEvent, self).__init__(content, tenant_uuid)
