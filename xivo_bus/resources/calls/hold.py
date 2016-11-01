# -*- coding: utf-8 -*-

# Copyright (C) 2016 Avencall
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


class _BaseHoldEvent(object):

    def __init__(self, call_id, user_uuid=None):
        self._call_id = call_id
        self._user_uuid = user_uuid
        self.required_acl = 'events.calls.{}'.format(user_uuid) if user_uuid else None

    def marshal(self):
        return {'call_id': self._call_id,
                'user_uuid': self._user_uuid}

    @classmethod
    def unmarshal(cls, msg):
        return cls(msg['call_id'], msg['user_uuid'])

    def __eq__(self, other):
        return self.marshal() == other.marshal()

    def __ne__(self, other):
        return not self == other


class CallOnHoldEvent(_BaseHoldEvent):

    name = 'call_held'
    routing_key = 'calls.hold.created'


class CallResumeEvent(_BaseHoldEvent):

    name = 'call_resumed'
    routing_key = 'calls.hold.deleted'
