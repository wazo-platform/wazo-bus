# Copyright 2016-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_bus.resources.common.event import TenantEvent


class OutcallTrunksAssociatedEvent(TenantEvent):
    service = 'confd'
    name = 'outcall_trunks_associated'
    routing_key_fmt = 'config.outcalls.trunks.updated'

    def __init__(self, outcall_id, trunk_ids, tenant_uuid):
        content = {
            'outcall_id': outcall_id,
            'trunk_ids': trunk_ids,
        }
        super(OutcallTrunksAssociatedEvent, self).__init__(content, tenant_uuid)
