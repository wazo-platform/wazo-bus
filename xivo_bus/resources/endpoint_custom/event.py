# -*- coding: utf-8 -*-
# Copyright 2016-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals
from xivo_bus.resources.common.event import TenantEvent


class CustomEndpointCreatedEvent(TenantEvent):
    name = 'custom_endpoint_created'
    routing_key_fmt = 'config.custom_endpoint.created'

    def __init__(self, endpoint_iax, tenant_uuid):
        super(CustomEndpointCreatedEvent, self).__init__(endpoint_iax, tenant_uuid)


class CustomEndpointDeletedEvent(TenantEvent):
    name = 'custom_endpoint_deleted'
    routing_key_fmt = 'config.custom_endpoint.deleted'

    def __init__(self, endpoint_iax, tenant_uuid):
        super(CustomEndpointDeletedEvent, self).__init__(endpoint_iax, tenant_uuid)


class CustomEndpointEditedEvent(TenantEvent):
    name = 'custom_endpoint_edited'
    routing_key_fmt = 'config.custom_endpoint.edited'

    def __init__(self, endpoint_iax, tenant_uuid):
        super(CustomEndpointCreatedEvent, self).__init__(endpoint_iax, tenant_uuid)
