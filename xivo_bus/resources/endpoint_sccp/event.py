# -*- coding: utf-8 -*-
# Copyright 2015-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals
from xivo_bus.resources.common.event import TenantEvent


class SCCPEndpointCreatedEvent(TenantEvent):
    name = 'sccp_endpoint_created'
    routing_key_fmt = 'config.sccp_endpoint.created'

    def __init__(self, endpoint_sccp, tenant_uuid):
        super(SCCPEndpointCreatedEvent, self).__init__(endpoint_sccp, tenant_uuid)


class SCCPEndpointDeletedEvent(TenantEvent):
    name = 'sccp_endpoint_deleted'
    routing_key_fmt = 'config.sccp_endpoint.deleted'

    def __init__(self, endpoint_sccp, tenant_uuid):
        super(SCCPEndpointDeletedEvent, self).__init__(endpoint_sccp, tenant_uuid)


class SCCPEndpointEditedEvent(TenantEvent):
    name = 'sccp_endpoint_edited'
    routing_key_fmt = 'config.sccp_endpoint.edited'

    def __init__(self, endpoint_sccp, tenant_uuid):
        super(SCCPEndpointEditedEvent, self).__init__(endpoint_sccp, tenant_uuid)
