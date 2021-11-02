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


class MeetingProgressEvent(BaseEvent):
    name = 'meeting_progress'
    routing_key_fmt = 'config.meetings.progress'

    def __init__(self, meeting, status):
        self._body = dict(meeting)
        self._body['status'] = status
        super(MeetingProgressEvent, self).__init__()


class UserMeetingProgressEvent(BaseEvent):
    name = 'meeting_user_progress'
    routing_key_fmt = 'config.users.{user_uuid}.meetings.progress'

    def __init__(self, meeting, user_uuid, status):
        self._body = dict(meeting)
        self._body['user_uuid'] = user_uuid
        self._body['status'] = status
        super(UserMeetingProgressEvent, self).__init__()


class _BaseParticipantMeetingEvent(BaseEvent):
    def __init__(self, meeting_uuid, participant_dict):
        self._body = {'meeting_uuid': meeting_uuid}
        self._body.update(participant_dict)
        super(_BaseParticipantMeetingEvent, self).__init__()


class ParticipantJoinedMeetingEvent(_BaseParticipantMeetingEvent):
    name = 'meeting_participant_joined'
    routing_key_fmt = 'meetings.{meeting_uuid}.participants.joined'

    def __init__(self, meeting_uuid, participant_dict):
        super(ParticipantJoinedMeetingEvent, self).__init__(
            meeting_uuid, participant_dict
        )


class ParticipantLeftMeetingEvent(_BaseParticipantMeetingEvent):
    name = 'meeting_participant_left'
    routing_key_fmt = 'meetings.{meeting_uuid}.participants.left'

    def __init__(self, meeting_uuid, participant_dict):
        super(ParticipantLeftMeetingEvent, self).__init__(
            meeting_uuid, participant_dict
        )


class UserParticipantJoinedMeetingEvent(_BaseParticipantMeetingEvent):
    name = 'meeting_user_participant_joined'
    routing_key_fmt = 'meetings.users.{user_uuid}.participants.joined'

    def __init__(self, meeting_uuid, participant_dict, user_uuid=None):
        super(UserParticipantJoinedMeetingEvent, self).__init__(
            meeting_uuid, participant_dict
        )
        if user_uuid:
            self.routing_key = self.routing_key_fmt.format(user_uuid=user_uuid)
            self.required_acl = (
                'events.users.{user_uuid}.meetings.participants.joined'.format(
                    user_uuid=user_uuid
                )
            )


class UserParticipantLeftMeetingEvent(_BaseParticipantMeetingEvent):
    name = 'meeting_user_participant_left'
    routing_key_fmt = 'meetings.users.{user_uuid}.participants.left'

    def __init__(self, meeting_uuid, participant_dict, user_uuid=None):
        super(UserParticipantLeftMeetingEvent, self).__init__(
            meeting_uuid, participant_dict
        )
        if user_uuid:
            self.routing_key = self.routing_key_fmt.format(user_uuid=user_uuid)
            self.required_acl = (
                'events.users.{user_uuid}.meetings.participants.left'.format(
                    user_uuid=user_uuid
                )
            )
