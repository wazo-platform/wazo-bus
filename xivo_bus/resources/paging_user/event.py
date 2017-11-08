# -*- coding: utf-8 -*-

# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
#
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals


class PagingMemberUserConfigEvent(object):

    def __init__(self, paging_id, user_uuids):
        self.paging_id = paging_id
        self.user_uuids = user_uuids

    def marshal(self):
        return {
            'paging_id': self.paging_id,
            'user_uuids': self.user_uuids,
        }

    @classmethod
    def unmarshal(cls, msg):
        return cls(
            msg['paging_id'],
            msg['user_uuids'])

    def __eq__(self, other):
        return (self.paging_id == other.paging_id and
                self.user_uuids == other.user_uuids)

    def __ne__(self, other):
        return not self == other


class PagingCallerUsersAssociatedEvent(PagingMemberUserConfigEvent):
    name = 'users_associated'
    routing_key = 'config.pagings.callers.users.updated'


class PagingMemberUsersAssociatedEvent(PagingMemberUserConfigEvent):
    name = 'users_associated'
    routing_key = 'config.pagings.members.users.updated'
