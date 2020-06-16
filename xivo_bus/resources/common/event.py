# -*- coding: utf-8 -*-
# Copyright 2013-2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals


class BaseEvent(object):

    def __init__(self):
        self.routing_key = self.routing_key_fmt.format(**self._body)
        self.required_acl = 'events.{}'.format(self.routing_key)

    def marshal(self):
        return self._body

    def __ne__(self, other):
        return not self == other

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self._body == other._body

    def __str__(self):
        return '{}({})'.format(self.__class__.__name__, self._body)

    def __repr__(self):
        return self.__str__()

    @classmethod
    def unmarshal(cls, body):
        return cls(**body)


# Deprecated and should not be used for new events
class ResourceConfigEvent(object):

    def __init__(self, resource_id):
        self.id = int(resource_id)

    def marshal(self):
        return {'id': self.id}

    @classmethod
    def unmarshal(cls, msg):
        return cls(msg['id'])

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return self.id != other.id


# Deprecated and should not be used for new events
class ArbitraryEvent(object):

    def __init__(self, name, body, required_acl=None):
        self.name = name
        self._body = dict(body)
        if required_acl:
            self.required_acl = required_acl

    def marshal(self):
        return self._body

    def __eq__(self, other):
        return (
            self.name == other.name
            and self._body == other._body
            and self.required_acl == other.required_acl
        )

    def __ne__(self, other):
        return self != other
