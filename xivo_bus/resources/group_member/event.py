# -*- coding: utf-8 -*-
# Copyright 2016-2021 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

from ..common.event import BaseEvent


class _GroupMemberConfigEvent(BaseEvent):

    def __init__(self, **body):
        self._body = body
        super(_GroupMemberConfigEvent, self).__init__()


class GroupMemberUsersAssociatedEvent(_GroupMemberConfigEvent):
    name = 'users_associated'
    routing_key_fmt = 'config.groups.members.users.updated'


class GroupMemberExtensionsAssociatedEvent(_GroupMemberConfigEvent):
    name = 'extensions_associated'
    routing_key_fmt = 'config.groups.members.extensions.updated'
