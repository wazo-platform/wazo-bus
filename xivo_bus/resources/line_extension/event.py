# Copyright 2013-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_bus.resources.common.event import TenantEvent


class LineExtensionAssociatedEvent(TenantEvent):
    service = 'confd'
    name = 'line_extension_associated'
    routing_key_fmt = 'config.line_extension_associated.updated'

    def __init__(self, line_id, extension_id, tenant_uuid):
        content = {'line_id': line_id, 'extension_id': extension_id}
        super(LineExtensionAssociatedEvent, self).__init__(content, tenant_uuid)


class LineExtensionDissociatedEvent(TenantEvent):
    service = 'confd'
    name = 'line_extension_dissociated'
    routing_key_fmt = 'config.line_extension_associated.deleted'

    def __init__(self, line_id, extension_id, tenant_uuid):
        content = {'line_id': line_id, 'extension_id': extension_id}
        super(LineExtensionDissociatedEvent, self).__init__(content, tenant_uuid)
