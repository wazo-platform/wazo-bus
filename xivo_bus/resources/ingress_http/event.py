# Copyright 2021-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals
from xivo_bus.resources.common.event import TenantEvent


class IngressHTTPCreatedEvent(TenantEvent):
    name = 'ingress_http_created'
    routing_key_fmt = 'config.ingresses.http.created'

    def __init__(self, ingress_http, tenant_uuid):
        super(IngressHTTPCreatedEvent, self).__init__(ingress_http, tenant_uuid)


class IngressHTTPDeletedEvent(TenantEvent):
    name = 'ingress_http_deleted'
    routing_key_fmt = 'config.ingresses.http.deleted'

    def __init__(self, ingress_http, tenant_uuid):
        super(IngressHTTPDeletedEvent, self).__init__(ingress_http, tenant_uuid)


class IngressHTTPEditedEvent(TenantEvent):
    name = 'ingress_http_edited'
    routing_key_fmt = 'config.ingresses.http.edited'

    def __init__(self, ingress_http, tenant_uuid):
        super(IngressHTTPEditedEvent, self).__init__(ingress_http, tenant_uuid)
