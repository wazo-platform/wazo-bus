# Copyright 2020-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_bus.resources.common.event import TenantEvent


class ExternalAppCreatedEvent(TenantEvent):
    service = 'confd'
    name = 'external_app_created'
    routing_key_fmt = 'config.external_apps.created'

    def __init__(self, app, tenant_uuid):
        super().__init__(app, tenant_uuid)


class ExternalAppDeletedEvent(TenantEvent):
    service = 'confd'
    name = 'external_app_deleted'
    routing_key_fmt = 'config.external_apps.deleted'

    def __init__(self, app, tenant_uuid):
        super().__init__(app, tenant_uuid)


class ExternalAppEditedEvent(TenantEvent):
    service = 'confd'
    name = 'external_app_edited'
    routing_key_fmt = 'config.external_apps.edited'

    def __init__(self, app, tenant_uuid):
        super().__init__(app, tenant_uuid)
