# -*- coding: utf-8 -*-

# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
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
