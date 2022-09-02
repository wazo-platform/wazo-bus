# -*- coding: utf-8 -*-
# Copyright 2018-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals
from xivo_bus.resources.common.event import TenantEvent


class ContextContextsAssociatedEvent(TenantEvent):
    name = 'contexts_associated'
    routing_key_fmt = 'config.contexts.contexts.updated'

    def __init__(self, context_id, context_ids, tenant_uuid):
        content = {
            'context_id': context_id,
            'context_ids': context_ids,
        }
        super(ContextContextsAssociatedEvent, self).__init__(content, tenant_uuid)
