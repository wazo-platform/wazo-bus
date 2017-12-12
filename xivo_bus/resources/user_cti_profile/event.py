# -*- coding: utf-8 -*-
# Copyright 2013-2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

from xivo_bus.resources.common.event import ResourceConfigEvent


class UserCtiProfileConfigEvent(ResourceConfigEvent):
    routing_key = 'config.user_cti_profile_association.{}'

    def __init__(self, user_id, cti_profile_id, enabled):
        self._body = {
            'user_id': user_id,
            'cti_profile_id': cti_profile_id,
            'enabled': enabled
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


class UserCtiProfileEditedEvent(UserCtiProfileConfigEvent):
    name = 'cti_profile_edited'
    routing_key = UserCtiProfileConfigEvent.routing_key.format('edited')
