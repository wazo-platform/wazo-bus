# -*- coding: utf-8 -*-
# Copyright 2016-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals


class GroupMemberUserConfigEvent(object):

    def __init__(self, group_id, user_uuids):
        self.group_id = group_id
        self.user_uuids = user_uuids

    def marshal(self):
        return {
            'group_id': self.group_id,
            'user_uuids': self.user_uuids,
        }

    @classmethod
    def unmarshal(cls, msg):
        return cls(
            msg['group_id'],
            msg['user_uuids'])

    def __eq__(self, other):
        return (self.group_id == other.group_id
                and self.user_uuids == other.user_uuids)

    def __ne__(self, other):
        return not self == other


class GroupMemberUsersAssociatedEvent(GroupMemberUserConfigEvent):
    name = 'users_associated'
    routing_key = 'config.groups.members.users.updated'


class GroupMemberExtensionsConfigEvent(object):

    def __init__(self, group_id, extensions):
        self.group_id = group_id
        self.extensions = extensions

    def marshal(self):
        return {
            'group_id': self.group_id,
            'extensions': self.extensions,
        }

    @classmethod
    def unmarshal(cls, msg):
        return cls(
            msg['group_id'],
            msg['extensions'])

    def __eq__(self, other):
        return (self.group_id == other.group_id
                and self.extensions == other.extensions)

    def __ne__(self, other):
        return not self == other


class GroupMemberExtensionsAssociatedEvent(GroupMemberExtensionsConfigEvent):
    name = 'extensions_associated'
    routing_key = 'config.groups.members.extensions.updated'
