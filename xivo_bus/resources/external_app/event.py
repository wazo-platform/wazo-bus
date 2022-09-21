# -*- coding: utf-8 -*-
# Copyright 2020-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals
from xivo_bus.resources.common.event import TenantEvent


class ExternalAppCreatedEvent(TenantEvent):
    service = 'confd'
    name = 'external_app_created'
    routing_key_fmt = 'config.external_apps.created'

    def __init__(self, app, tenant_uuid):
        super(ExternalAppCreatedEvent, self).__init__(app, tenant_uuid)


class ExternalAppDeletedEvent(TenantEvent):
    service = 'confd'
    name = 'external_app_deleted'
    routing_key_fmt = 'config.external_apps.deleted'

    def __init__(self, app, tenant_uuid):
        super(ExternalAppDeletedEvent, self).__init__(app, tenant_uuid)


class ExternalAppEditedEvent(TenantEvent):
    service = 'confd'
    name = 'external_app_edited'
    routing_key_fmt = 'config.external_apps.edited'

    def __init__(self, app, tenant_uuid):
        super(ExternalAppEditedEvent, self).__init__(app, tenant_uuid)
