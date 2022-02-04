# Copyright 2021-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


class MockEvent(object):
    def __init__(self, name, routing_key=None, required_acl=None, **kwargs):
        self.name = name
        self.routing_key = routing_key
        self.required_acl = required_acl
        self._body = kwargs

    def marshal(self):
        return {k: v for k, v in self._body.items()}
