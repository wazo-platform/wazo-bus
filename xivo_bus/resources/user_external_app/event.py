# -*- coding: utf-8 -*-
# Copyright 2020-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals
from xivo_bus.resources.common.event import TenantEvent


class UserExternalAppCreatedEvent(TenantEvent):
    service = 'confd'
    name = 'user_external_app_created'
    routing_key_fmt = 'config.user_external_apps.created'

    def __init__(self, app, tenant_uuid):
        super(UserExternalAppCreatedEvent, self).__init__(app, tenant_uuid)


class UserExternalAppDeletedEvent(TenantEvent):
    service = 'confd'
    name = 'user_external_app_deleted'
    routing_key_fmt = 'config.user_external_apps.deleted'

    def __init__(self, app, tenant_uuid):
        super(UserExternalAppDeletedEvent, self).__init__(app, tenant_uuid)


class UserExternalAppEditedEvent(TenantEvent):
    service = 'confd'
    name = 'user_external_app_edited'
    routing_key_fmt = 'config.user_external_apps.edited'

    def __init__(self, app, tenant_uuid):
        super(UserExternalAppEditedEvent, self).__init__(app, tenant_uuid)
