# -*- coding: utf-8 -*-
# Copyright 2017-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals
from xivo_bus.resources.common.event import TenantEvent


class OutcallCallPermissionAssociatedEvent(TenantEvent):
    name = 'outcall_call_permission_associated'
    routing_key_fmt = 'config.outcalls.{outcall_id}.callpermission.updated'

    def __init__(self, outcall_id, call_permission_id, tenant_uuid):
        content = {
            'outcall_id': outcall_id,
            'call_permission_id': call_permission_id,
        }
        super(OutcallCallPermissionAssociatedEvent, self).__init__(content, tenant_uuid)


class OutcallCallPermissionDissociatedEvent(TenantEvent):
    name = 'outcall_call_permission_dissociated'
    routing_key_fmt = 'config.outcalls.{outcall_id}.callpermission.deleted'

    def __init__(self, outcall_id, call_permission_id, tenant_uuid):
        content = {
            'outcall_id': outcall_id,
            'call_permission_id': call_permission_id,
        }
        super(OutcallCallPermissionDissociatedEvent, self).__init__(
            content, tenant_uuid
        )
