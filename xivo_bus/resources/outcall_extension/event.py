# -*- coding: utf-8 -*-
# Copyright 2016-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals
from xivo_bus.resources.common.event import TenantEvent


class OutcallExtensionAssociatedEvent(TenantEvent):
    service = 'confd'
    name = 'outcall_extension_associated'
    routing_key_fmt = 'config.outcalls.extensions.updated'

    def __init__(self, outcall_id, extension_id, tenant_uuid):
        content = {
            'outcall_id': outcall_id,
            'extension_id': extension_id,
        }
        super(OutcallExtensionAssociatedEvent, self).__init__(content, tenant_uuid)


class OutcallExtensionDissociatedEvent(TenantEvent):
    service = 'confd'
    name = 'outcall_extension_dissociated'
    routing_key_fmt = 'config.outcalls.extensions.deleted'

    def __init__(self, outcall_id, extension_id, tenant_uuid):
        content = {
            'outcall_id': outcall_id,
            'extension_id': extension_id,
        }
        super(OutcallExtensionDissociatedEvent, self).__init__(content, tenant_uuid)
