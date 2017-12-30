# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals


class _SoundConfigurationEvent(object):

    def __init__(self, sound_name):
        self._body = {
            'name': sound_name,
        }

    def marshal(self):
        return self._body

    def __ne__(self, other):
        return not self._body == other._body

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self._body == other._body

    @classmethod
    def unmarshal(cls, body):
        return cls(**body)


class CreateSoundEvent(_SoundConfigurationEvent):
    name = 'sound_created'
    routing_key = 'config.sounds.created'


class DeleteSoundEvent(_SoundConfigurationEvent):
    name = 'sound_deleted'
    routing_key = 'config.sounds.deleted'
