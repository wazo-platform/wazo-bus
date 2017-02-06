# -*- coding: utf-8 -*-

# Copyright 2015-2017 The Wazo Authors  (see the AUTHORS file)
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


class _BaseEvent(object):

    def __init__(self, data):
        self._data = data

    def marshal(self):
        return self._data

    def __eq__(self, other):
        return self._data == other._data

    def __ne__(self, other):
        return not self == other


class _CallEvent(_BaseEvent):

    def __init__(self, data):
        super(_CallEvent, self).__init__(data)
        user_uuid = data.get('user_uuid')
        if user_uuid:
            self.required_acl = 'events.calls.{}'.format(user_uuid)
        else:
            self.required_acl = None


class CreateCallEvent(_CallEvent):

    name = 'call_created'
    routing_key = 'calls.call.created'


class UpdateCallEvent(_CallEvent):

    name = 'call_updated'
    routing_key = 'calls.call.updated'


class EndCallEvent(_CallEvent):

    name = 'call_ended'
    routing_key = 'calls.call.ended'
