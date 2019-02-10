# -*- coding: utf-8 -*-
# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


class _BaseEvent(object):

    def __init__(self):
        self.routing_key = self.routing_key_fmt.format(**self._body)
        self.required_acl = 'events.{}'.format(self.routing_key)

    def marshal(self):
        return self._body

    def __ne__(self, other):
        return not self == other

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self._body == other._body

    @classmethod
    def unmarshal(cls, body):
        return cls(body)


class PresenceUpdatedEvent(_BaseEvent):

    name = 'chatd_presence_updated'
    routing_key_fmt = 'chatd.users.{uuid}.presences.updated'

    def __init__(self, user):
        self._body = user
        super(PresenceUpdatedEvent, self).__init__()
