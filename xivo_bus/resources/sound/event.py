# Copyright 2017-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from ..common.event import TenantEvent


class SoundCreatedEvent(TenantEvent):
    service = 'confd'
    name = 'sound_created'
    routing_key_fmt = 'config.sounds.created'

    def __init__(self, sound_name: str, tenant_uuid: str):
        content = {'name': sound_name}
        super().__init__(content, tenant_uuid)


class SoundDeletedEvent(TenantEvent):
    service = 'confd'
    name = 'sound_deleted'
    routing_key_fmt = 'config.sounds.deleted'

    def __init__(self, sound_name: str, tenant_uuid: str):
        content = {'name': sound_name}
        super().__init__(content, tenant_uuid)
