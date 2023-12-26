# Copyright 2016-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from ..common.event import TenantEvent


class OutcallTrunksAssociatedEvent(TenantEvent):
    service = 'confd'
    name = 'outcall_trunks_associated'
    routing_key_fmt = 'config.outcalls.trunks.updated'

    def __init__(self, outcall_id: int, trunk_ids: list[int], tenant_uuid: str):
        content = {
            'outcall_id': outcall_id,
            'trunk_ids': trunk_ids,
        }
        super().__init__(content, tenant_uuid)
