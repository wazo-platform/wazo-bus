# -*- coding: utf-8 -*-
# Copyright 2017-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals
from xivo_bus.resources.common.event import TenantEvent


class SoundCreatedEvent(TenantEvent):
    name = 'sound_created'
    routing_key_fmt = 'config.sounds.created'

    def __init__(self, sound_name, tenant_uuid):
        content = {'name': sound_name}
        super(SoundCreatedEvent, self).__init__(content, tenant_uuid)


class SoundDeletedEvent(TenantEvent):
    name = 'sound_deleted'
    routing_key_fmt = 'config.sounds.deleted'

    def __init__(self, sound_name, tenant_uuid):
        content = {'name': sound_name}
        super(SoundDeletedEvent, self).__init__(content, tenant_uuid)
