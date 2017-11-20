# -*- coding: utf-8 -*-
# Copyright (C) 2016 Avencall
# Copyright (C) 2016 Proformatique Inc.
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals


class UserEntityConfigEvent(object):

    def __init__(self, user_uuid, entity_id):
        self.user_uuid = user_uuid
        self.entity_id = entity_id

    def marshal(self):
        return {
            'user_uuid': self.user_uuid,
            'entity_id': self.entity_id,
        }

    @classmethod
    def unmarshal(cls, msg):
        return cls(
            msg['user_uuid'],
            msg['entity_id'])

    def __eq__(self, other):
        return (self.user_uuid == other.user_uuid and
                self.entity_id == other.entity_id)

    def __ne__(self, other):
        return not self == other


class UserEntityAssociatedEvent(UserEntityConfigEvent):
    name = 'entity_associated'

    def __init__(self, user_uuid, entity_id):
        super(UserEntityAssociatedEvent, self).__init__(user_uuid, entity_id)
        self.routing_key = 'config.users.{}.entities.updated'.format(self.user_uuid)
        self.required_acl = 'events.{}'.format(self.routing_key)
