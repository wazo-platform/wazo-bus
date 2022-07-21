# -*- coding: utf-8 -*-
# Copyright 2016-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals
from xivo_bus.resources.common.event import TenantEvent


class IVRCreatedEvent(TenantEvent):
    name = 'ivr_created'
    routing_key_fmt = 'config.ivr.created'

    def __init__(self, ivr_id, tenant_uuid):
        content = {'id': ivr_id}
        super(IVRCreatedEvent, self).__init__(content, tenant_uuid)


class IVRDeletedEvent(TenantEvent):
    name = 'ivr_deleted'
    routing_key_fmt = 'config.ivr.deleted'

    def __init__(self, ivr_id, tenant_uuid):
        content = {'id': ivr_id}
        super(IVRDeletedEvent, self).__init__(content, tenant_uuid)


class IVREditedEvent(TenantEvent):
    name = 'ivr_edited'
    routing_key_fmt = 'config.ivr.edited'

    def __init__(self, ivr_id, tenant_uuid):
        content = {'id': ivr_id}
        super(IVREditedEvent, self).__init__(content, tenant_uuid)
