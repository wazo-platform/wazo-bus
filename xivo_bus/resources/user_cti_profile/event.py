# -*- coding: utf-8 -*-

# Copyright (C) 2013-2014 Avencall
#
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

from xivo_bus.resources.common.event import ResourceConfigEvent


class UserCtiProfileConfigEvent(ResourceConfigEvent):
    routing_key = 'config.user_cti_profile_association.{}'

    def __init__(self, user_id, cti_profile_id, enabled):
        self.user_id = user_id
        self.cti_profile_id = cti_profile_id
        self.enabled = enabled

    def marshal(self):
        return {
            'user_id': self.user_id,
            'cti_profile_id': self.cti_profile_id,
            'enabled': self.enabled
        }

    @classmethod
    def unmarshal(cls, msg):
        return cls(
            msg['user_id'],
            msg['cti_profile_id'],
            msg['enabled'])


class UserCtiProfileEditedEvent(UserCtiProfileConfigEvent):
    name = 'cti_profile_edited'
    routing_key = UserCtiProfileConfigEvent.routing_key.format('edited')
