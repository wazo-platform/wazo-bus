# -*- coding: utf-8 -*-

# Copyright (C) 2013-2015 Avencall
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

from __future__ import unicode_literals


class _StatusUpdateEvent(object):

    def __init__(self, id_, status):
        self.id_ = int(id_)
        self.status = status

    def marshal(self):
        return {
            self.id_field: self.id_,
            'status': self.status,
        }

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


class CallFormResultEvent(object):

    name = 'call_form_result'
    routing_key = 'call_form_result'

    def __init__(self, user_id, variables):
        self.user_id = int(user_id)
        self.variables = variables

    def marshal(self):
        return {
            'user_id': self.user_id,
            'variables': self.variables,
        }

    def __eq__(self, other):
        return (self.user_id == other.user_id
                and self.variables == other.variables)


class AgentStatusUpdateEvent(_StatusUpdateEvent):

    name = 'agent_status_update'
    routing_key = 'status.agent'
    id_field = 'agent_id'

    STATUS_LOGGED_IN = 'logged_in'
    STATUS_LOGGED_OUT = 'logged_out'


class EndpointStatusUpdateEvent(_StatusUpdateEvent):

    name = 'endpoint_status_update'
    routing_key = 'status.endpoint'
    id_field = 'endpoint_id'

    def __init__(self, id_, status):
        super(EndpointStatusUpdateEvent, self).__init__(id_, int(status))


class UserStatusUpdateEvent(_StatusUpdateEvent):

    name = 'user_status_update'
    routing_key = 'status.user'
    id_field = 'user_id'
