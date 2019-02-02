# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


class CallLogCreatedEvent(object):

    name = 'call_log_created'
    routing_key = 'call_log.created'

    def __init__(self, payload):
        self.required_acl = 'events.{}'.format(self.routing_key)
        self.payload = payload

    def marshal(self):
        return self.payload

    def __eq__(self, other):
        return self.payload == other.payload

    def __ne__(self, other):
        return not self == other


class CallLogUserCreatedEvent(object):

    name = 'call_log_user_created'
    routing_key_fmt = 'call_log.user.{}.created'

    def __init__(self, user_uuid, payload):
        self.routing_key = self.routing_key_fmt.format(user_uuid)
        self.required_acl = 'events.{}'.format(self.routing_key)
        self.payload = payload

    def marshal(self):
        return self.payload

    def __eq__(self, other):
        return self.payload == other.payload

    def __ne__(self, other):
        return not self == other
