# Copyright 2016-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_bus.resources.common.event import TenantEvent


class CustomEndpointCreatedEvent(TenantEvent):
    service = 'confd'
    name = 'custom_endpoint_created'
    routing_key_fmt = 'config.custom_endpoint.created'

    def __init__(self, endpoint_iax, tenant_uuid):
        super().__init__(endpoint_iax, tenant_uuid)


class CustomEndpointDeletedEvent(TenantEvent):
    service = 'confd'
    name = 'custom_endpoint_deleted'
    routing_key_fmt = 'config.custom_endpoint.deleted'

    def __init__(self, endpoint_iax, tenant_uuid):
        super().__init__(endpoint_iax, tenant_uuid)


class CustomEndpointEditedEvent(TenantEvent):
    service = 'confd'
    name = 'custom_endpoint_edited'
    routing_key_fmt = 'config.custom_endpoint.edited'

    def __init__(self, endpoint_iax, tenant_uuid):
        super().__init__(endpoint_iax, tenant_uuid)
