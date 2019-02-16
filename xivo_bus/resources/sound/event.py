# -*- coding: utf-8 -*-
# Copyright 2017-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

from ..common.event import BaseEvent


class _BaseSoundEvent(BaseEvent):

    def __init__(self, sound_name):
        self._body = {
            'name': sound_name,
        }
        super(_BaseSoundEvent, self).__init__()


class CreateSoundEvent(_BaseSoundEvent):
    name = 'sound_created'
    routing_key_fmt = 'config.sounds.created'


class DeleteSoundEvent(_BaseSoundEvent):
    name = 'sound_deleted'
    routing_key_fmt = 'config.sounds.deleted'
