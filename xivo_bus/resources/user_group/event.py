# -*- coding: utf-8 -*-
# Copyright 2017-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals


class UserGroupConfigEvent(object):

    def __init__(self, user_uuid, group_ids):
        self.user_uuid = user_uuid
        self.group_ids = group_ids

    def marshal(self):
        return {
            'user_uuid': self.user_uuid,
            'group_ids': self.group_ids,
        }

    @classmethod
    def unmarshal(cls, msg):
        return cls(
            msg['user_uuid'],
            msg['group_ids'])

    def __eq__(self, other):
        return (self.user_uuid == other.user_uuid
                and self.group_ids == other.group_ids)

    def __ne__(self, other):
        return not self == other


class UserGroupsAssociatedEvent(UserGroupConfigEvent):
    name = 'groups_associated'
    routing_key = 'config.users.groups.updated'
