# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals


class _StatusUpdateEvent(object):

    def __init__(self, id_, status):
        self.id_ = id_
        self.status = status

    def marshal(self):
        return {
            self.id_field: self.id_,
            'status': self.status,
        }

    @classmethod
    def unmarshal(cls, msg):
        return cls(msg[cls.id_field],
                   msg['status'])

    def __eq__(self, other):
        return (self.id_ == other.id_
                and self.status == other.status)

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return '{}({}, {})'.format(
            self.__class__.__name__,
            repr(self.id_),
            repr(self.status),
        )


class AgentStatusUpdateEvent(_StatusUpdateEvent):

    name = 'agent_status_update'
    required_acl = 'events.statuses.agents'
    routing_key = 'status.agent'
    id_field = 'agent_id'

    STATUS_LOGGED_IN = 'logged_in'
    STATUS_LOGGED_OUT = 'logged_out'

    def __init__(self, id_, status):
        super(AgentStatusUpdateEvent, self).__init__(int(id_), status)
