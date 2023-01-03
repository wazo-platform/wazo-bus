# Copyright 2018-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_bus.resources.common.event import TenantEvent


class IAXEndpointCreatedEvent(TenantEvent):
    service = 'confd'
    name = 'iax_endpoint_created'
    routing_key_fmt = 'config.iax_endpoint.created'

    def __init__(self, endpoint_iax, tenant_uuid):
        super(IAXEndpointCreatedEvent, self).__init__(endpoint_iax, tenant_uuid)


class IAXEndpointDeletedEvent(TenantEvent):
    service = 'confd'
    name = 'iax_endpoint_deleted'
    routing_key_fmt = 'config.iax_endpoint.deleted'

    def __init__(self, endpoint_iax, tenant_uuid):
        super(IAXEndpointDeletedEvent, self).__init__(endpoint_iax, tenant_uuid)


class IAXEndpointEditedEvent(TenantEvent):
    service = 'confd'
    name = 'iax_endpoint_edited'
    routing_key_fmt = 'config.iax_endpoint.edited'

    def __init__(self, endpoint_iax, tenant_uuid):
        super(IAXEndpointEditedEvent, self).__init__(endpoint_iax, tenant_uuid)
