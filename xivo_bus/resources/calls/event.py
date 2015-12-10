# -*- coding: utf-8 -*-

# Copyright (C) 2015 Avencall
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


class _CallEvent(object):

    def __init__(self, data):
        self._data = data

    def marshal(self):
        return {'data': self._data }

    def __eq__(self, other):
        return (self._data == other._data)

    def __ne__(self, other):
        return not self == other


class CreateCallEvent(_CallEvent):

    name = 'call_created'
    routing_key = 'calls.call.created'


class UpdateCallEvent(_CallEvent):

    name = 'call_updated'
    routing_key = 'calls.call.updated'


class EndCallEvent(_CallEvent):

    name = 'call_ended'
    routing_key = 'calls.call.ended'


class CreateWaitingRoomEvent(_CallEvent):

    name = 'waiting_room_created'
    routing_key = 'calls.waiting_room.created'


class UpdateWaitingRoomEvent(_CallEvent):

    name = 'waiting_room_updated'
    routing_key = 'calls.waiting_room.updated'


class DeleteWaitingRoomEvent(_CallEvent):

    name = 'waiting_room_deleted'
    routing_key = 'calls.waiting_room.deleted'


class JoinCallWaitingRoomEvent(_CallEvent):

    name = 'waiting_room_call_joined'
    routing_key = 'calls.waiting_room.call.joined'


class LeftCallWaitingRoomEvent(_CallEvent):

    name = 'waiting_room_call_left'
    routing_key = 'calls.waiting_room.call.left'


class JoinCallIncomingRoomEvent(_CallEvent):

    name = 'incoming_room_call_joined'
    routing_key = 'calls.incoming_room.call.joined'


class LeftCallIncomingRoomEvent(_CallEvent):

    name = 'incoming_room_call_left'
    routing_key = 'calls.incoming_room.call.left'


class StartBlindTransferEvent(_CallEvent):

    name = 'blind_transfer_started'
    routing_key = 'calls.transfer.blind.started'


class CompletedBlindTransferEvent(_CallEvent):

    name = 'blind_transfer_completed'
    routing_key = 'calls.transfer.blind.completed'


class CancelBlindTransferEvent(_CallEvent):

    name = 'blind_transfer_canceled'
    routing_key = 'calls.transfer.blind.canceled'
