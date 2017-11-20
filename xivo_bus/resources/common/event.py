# -*- coding: utf-8 -*-
# Copyright (C) 2013-2017 The Wazo Authors  (see AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals


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


class ArbitraryEvent(object):

    def __init__(self, name, body, required_acl=None):
        self.name = name
        self._body = dict(body)
        if required_acl:
            self.required_acl = required_acl

    def marshal(self):
        return self._body
