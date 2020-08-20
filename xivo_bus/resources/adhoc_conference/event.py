# Copyright 2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals
from xivo_bus.resources.common.event import BaseEvent


class AdhocConferenceCreatedUserEvent(BaseEvent):
    name = 'adhoc_conference_created'
    routing_key_fmt = 'adhoc_conferences.users.{user_uuid}.created'

    def __init__(self, conference_id, user_uuid):
        self._body = {'conference_id': conference_id, 'user_uuid': user_uuid}
        super(AdhocConferenceCreatedUserEvent, self).__init__()


class AdhocConferenceDeletedUserEvent(BaseEvent):
    name = 'adhoc_conference_deleted'
    routing_key_fmt = 'adhoc_conferences.users.{user_uuid}.deleted'

    def __init__(self, conference_id, user_uuid):
        self._body = {'conference_id': conference_id, 'user_uuid': user_uuid}
        super(AdhocConferenceDeletedUserEvent, self).__init__()


class AdhocConferenceParticipantJoinedUserEvent(BaseEvent):
    name = 'adhoc_conference_participant_joined'
    routing_key_fmt = 'adhoc_conferences.users.{user_uuid}.participants.joined'

    def __init__(self, conference_id, user_uuid, participant_call):
        self._body = {
            'conference_id': conference_id,
            'user_uuid': user_uuid,
            'participant_call': participant_call,
        }
        super(AdhocConferenceParticipantJoinedUserEvent, self).__init__()


class AdhocConferenceParticipantLeftUserEvent(BaseEvent):
    name = 'adhoc_conference_participant_left'
    routing_key_fmt = 'adhoc_conferences.users.{user_uuid}.participants.left'

    def __init__(self, conference_id, user_uuid, participant_call):
        self._body = {
            'conference_id': conference_id,
            'user_uuid': user_uuid,
            'participant_call': participant_call,
        }
        super(AdhocConferenceParticipantLeftUserEvent, self).__init__()
