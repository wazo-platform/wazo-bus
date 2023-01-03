# Copyright 2015-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_bus.resources.common.event import TenantEvent


class SIPEndpointCreatedEvent(TenantEvent):
    service = 'confd'
    name = 'sip_endpoint_created'
    routing_key_fmt = 'config.sip_endpoint.created'

    def __init__(self, endpoint_sip, tenant_uuid):
        super(SIPEndpointCreatedEvent, self).__init__(endpoint_sip, tenant_uuid)


class SIPEndpointDeletedEvent(TenantEvent):
    service = 'confd'
    name = 'sip_endpoint_deleted'
    routing_key_fmt = 'config.sip_endpoint.deleted'

    def __init__(self, endpoint_sip, tenant_uuid):
        super(SIPEndpointDeletedEvent, self).__init__(endpoint_sip, tenant_uuid)


class SIPEndpointEditedEvent(TenantEvent):
    service = 'confd'
    name = 'sip_endpoint_edited'
    routing_key_fmt = 'config.sip_endpoint.edited'

    def __init__(self, endpoint_sip, tenant_uuid):
        super(SIPEndpointEditedEvent, self).__init__(endpoint_sip, tenant_uuid)


class SIPEndpointTemplateCreatedEvent(TenantEvent):
    service = 'confd'
    name = 'sip_endpoint_template_created'
    routing_key_fmt = 'config.sip_endpoint_template.created'

    def __init__(self, endpoint_sip, tenant_uuid):
        super(SIPEndpointTemplateCreatedEvent, self).__init__(endpoint_sip, tenant_uuid)


class SIPEndpointTemplateDeletedEvent(TenantEvent):
    service = 'confd'
    name = 'sip_endpoint_template_deleted'
    routing_key_fmt = 'config.sip_endpoint_template.deleted'

    def __init__(self, endpoint_sip, tenant_uuid):
        super(SIPEndpointTemplateDeletedEvent, self).__init__(endpoint_sip, tenant_uuid)


class SIPEndpointTemplateEditedEvent(TenantEvent):
    service = 'confd'
    name = 'sip_endpoint_template_edited'
    routing_key_fmt = 'config.sip_endpoint_template.edited'

    def __init__(self, endpoint_sip, tenant_uuid):
        super(SIPEndpointTemplateEditedEvent, self).__init__(endpoint_sip, tenant_uuid)
