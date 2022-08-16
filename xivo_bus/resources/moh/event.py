# -*- coding: utf-8 -*-
# Copyright 2019-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals
from xivo_bus.resources.common.event import TenantEvent


class MOHCreatedEvent(TenantEvent):
    name = 'moh_created'
    routing_key_fmt = 'config.moh.created'

    def __init__(self, moh, tenant_uuid):
        super(MOHCreatedEvent, self).__init__(moh, tenant_uuid)


class MOHDeletedEvent(TenantEvent):
    name = 'moh_deleted'
    routing_key_fmt = 'config.moh.deleted'

    def __init__(self, moh, tenant_uuid):
        super(MOHDeletedEvent, self).__init__(moh, tenant_uuid)


class MOHEditedEvent(TenantEvent):
    name = 'moh_edited'
    routing_key_fmt = 'config.moh.edited'

    def __init__(self, moh, tenant_uuid):
        super(MOHEditedEvent, self).__init__(moh, tenant_uuid)
