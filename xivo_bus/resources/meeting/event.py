# Copyright 2021 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

from ..common.event import BaseEvent


class _BaseMeetingEvent(BaseEvent):

    def __init__(self, meeting):
        self._body = meeting
        super(_BaseMeetingEvent, self).__init__()


class CreateMeetingEvent(_BaseMeetingEvent):
    name = 'meeting_created'
    routing_key_fmt = 'config.meetings.created'


class EditMeetingEvent(_BaseMeetingEvent):
    name = 'meeting_updated'
    routing_key_fmt = 'config.meetings.updated'


class DeleteMeetingEvent(_BaseMeetingEvent):
    name = 'meeting_deleted'
    routing_key_fmt = 'config.meetings.deleted'
