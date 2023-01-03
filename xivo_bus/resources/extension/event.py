# Copyright 2013-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals
from xivo_bus.resources.common.event import TenantEvent


class ExtensionCreatedEvent(TenantEvent):
    service = 'confd'
    name = 'extension_created'
    routing_key_fmt = 'config.extensions.created'

    def __init__(self, extension_id, exten, context, tenant_uuid):
        content = {
            'id': int(extension_id),
            'exten': exten,
            'context': context,
        }
        super(ExtensionCreatedEvent, self).__init__(content, tenant_uuid)


class ExtensionDeletedEvent(TenantEvent):
    service = 'confd'
    name = 'extension_deleted'
    routing_key_fmt = 'config.extensions.deleted'

    def __init__(self, extension_id, exten, context, tenant_uuid):
        content = {
            'id': int(extension_id),
            'exten': exten,
            'context': context,
        }
        super(ExtensionDeletedEvent, self).__init__(content, tenant_uuid)


class ExtensionEditedEvent(TenantEvent):
    service = 'confd'
    name = 'extension_edited'
    routing_key_fmt = 'config.extensions.edited'

    def __init__(self, extension_id, exten, context, tenant_uuid):
        content = {
            'id': int(extension_id),
            'exten': exten,
            'context': context,
        }
        super(ExtensionEditedEvent, self).__init__(content, tenant_uuid)
