# Copyright 2015-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_bus.resources.common.event import TenantEvent


class SCCPEndpointCreatedEvent(TenantEvent):
    service = 'confd'
    name = 'sccp_endpoint_created'
    routing_key_fmt = 'config.sccp_endpoint.created'

    def __init__(self, endpoint_sccp, tenant_uuid):
        super().__init__(endpoint_sccp, tenant_uuid)


class SCCPEndpointDeletedEvent(TenantEvent):
    service = 'confd'
    name = 'sccp_endpoint_deleted'
    routing_key_fmt = 'config.sccp_endpoint.deleted'

    def __init__(self, endpoint_sccp, tenant_uuid):
        super().__init__(endpoint_sccp, tenant_uuid)


class SCCPEndpointEditedEvent(TenantEvent):
    service = 'confd'
    name = 'sccp_endpoint_edited'
    routing_key_fmt = 'config.sccp_endpoint.edited'

    def __init__(self, endpoint_sccp, tenant_uuid):
        super().__init__(endpoint_sccp, tenant_uuid)
