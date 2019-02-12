# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

from xivo_bus.resources.common.event import ResourceConfigEvent


class UserLineConfigEvent(ResourceConfigEvent):
    routing_key = 'config.user_line_association.{}'

    def __init__(self, user_uuid, user_id, line_id, main_user, main_line, tenant_uuid):
        self._body = {
            'user_uuid': str(user_uuid),
            'user_id': int(user_id),
            'line_id': int(line_id),
            'main_user': bool(main_user),
            'main_line': bool(main_line),
            'tenant_uuid': str(tenant_uuid),
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


class UserLineAssociatedEvent(UserLineConfigEvent):
    name = 'line_associated'
    routing_key = UserLineConfigEvent.routing_key.format('created')


class UserLineDissociatedEvent(UserLineConfigEvent):
    name = 'line_dissociated'
    routing_key = UserLineConfigEvent.routing_key.format('deleted')
