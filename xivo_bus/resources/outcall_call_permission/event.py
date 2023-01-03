# Copyright 2017-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_bus.resources.common.event import TenantEvent


class OutcallCallPermissionAssociatedEvent(TenantEvent):
    service = 'confd'
    name = 'outcall_call_permission_associated'
    routing_key_fmt = 'config.outcalls.{outcall_id}.callpermissions.updated'

    def __init__(self, outcall_id, call_permission_id, tenant_uuid):
        content = {
            'outcall_id': outcall_id,
            'call_permission_id': call_permission_id,
        }
        super(OutcallCallPermissionAssociatedEvent, self).__init__(content, tenant_uuid)


class OutcallCallPermissionDissociatedEvent(TenantEvent):
    service = 'confd'
    name = 'outcall_call_permission_dissociated'
    routing_key_fmt = 'config.outcalls.{outcall_id}.callpermissions.deleted'

    def __init__(self, outcall_id, call_permission_id, tenant_uuid):
        content = {
            'outcall_id': outcall_id,
            'call_permission_id': call_permission_id,
        }
        super(OutcallCallPermissionDissociatedEvent, self).__init__(
            content, tenant_uuid
        )
