# Copyright 2016-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_bus.resources.common.event import TenantEvent


class ConferenceExtensionAssociatedEvent(TenantEvent):
    service = 'confd'
    name = 'conference_extension_associated'
    routing_key_fmt = 'config.conferences.extensions.updated'

    def __init__(self, conference_id, extension_id, tenant_uuid):
        content = {
            'conference_id': conference_id,
            'extension_id': extension_id,
        }
        super().__init__(content, tenant_uuid)


class ConferenceExtensionDissociatedEvent(TenantEvent):
    service = 'confd'
    name = 'conference_extension_dissociated'
    routing_key_fmt = 'config.conferences.extensions.deleted'

    def __init__(self, conference_id, extension_id, tenant_uuid):
        content = {
            'conference_id': conference_id,
            'extension_id': extension_id,
        }
        super().__init__(content, tenant_uuid)
