# Copyright 2016-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_bus.resources.common.event import TenantEvent


class OutcallCreatedEvent(TenantEvent):
    service = 'confd'
    name = 'outcall_created'
    routing_key_fmt = 'config.outcalls.created'

    def __init__(self, outcall_id, tenant_uuid):
        content = {'id': outcall_id}
        super(OutcallCreatedEvent, self).__init__(content, tenant_uuid)


class OutcallDeletedEvent(TenantEvent):
    service = 'confd'
    name = 'outcall_deleted'
    routing_key_fmt = 'config.outcalls.deleted'

    def __init__(self, outcall_id, tenant_uuid):
        content = {'id': outcall_id}
        super(OutcallDeletedEvent, self).__init__(content, tenant_uuid)


class OutcallEditedEvent(TenantEvent):
    service = 'confd'
    name = 'outcall_edited'
    routing_key_fmt = 'config.outcalls.edited'

    def __init__(self, outcall_id, tenant_uuid):
        content = {'id': outcall_id}
        super(OutcallEditedEvent, self).__init__(content, tenant_uuid)
