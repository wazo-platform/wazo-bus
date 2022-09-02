# -*- coding: utf-8 -*-
# Copyright 2016-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals
from xivo_bus.resources.common.event import TenantEvent


class OutcallTrunksAssociatedEvent(TenantEvent):
    name = 'outcall_trunks_associated'
    routing_key_fmt = 'config.outcalls.trunks.updated'

    def __init__(self, outcall_id, trunk_ids, tenant_uuid):
        content = {
            'outcall_id': outcall_id,
            'trunk_ids': trunk_ids,
        }
        super(OutcallTrunksAssociatedEvent, self).__init__(content, tenant_uuid)
