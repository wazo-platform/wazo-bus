# -*- coding: utf-8 -*-

# Copyright (C) 2013-2014 Avencall
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

    def __init__(self, xivo_id, id_, status):
        self.xivo_id = xivo_id
        self.id_ = int(id_)
        self.status = status

    def marshal(self):
        return {
            'xivo_id': self.xivo_id,
            self.id_field: self.id_,
            'status': self.status,
        }

    def __eq__(self, other):
        return (self.xivo_id == other.xivo_id
                and self.id_ == other.id_
                and self.status == other.status)


class CallFormResultEvent(object):

    name = 'call_form_result'

    def __init__(self, user_id, variables):
        self.user_id = int(user_id)
        self.variables = variables

    def marshal(self):
        return {
            'user_id': self.user_id,
            'variables': self.variables,
        }


class EndpointStatusUpdateEvent(_StatusUpdateEvent):

    name = 'endpoint_status_update'
    id_field = 'endpoint_id'


class UserStatusUpdateEvent(_StatusUpdateEvent):

    name = 'user_status_update'
    id_field = 'user_id'
