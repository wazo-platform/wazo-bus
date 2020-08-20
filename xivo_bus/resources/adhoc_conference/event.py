# Copyright 2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals
from xivo_bus.resources.common.event import BaseEvent


class AdhocConferenceUserEvent(BaseEvent):
    def __init__(self, conference_id, user_uuid):
        self._body = {'conference_id': conference_id}
        self.routing_key_fmt = self.routing_key_fmt.format(user_uuid=user_uuid)
        super(AdhocConferenceUserEvent, self).__init__()


class AdhocConferenceCreatedUserEvent(AdhocConferenceUserEvent):
    name = 'adhoc_conference_created'
    routing_key_fmt = 'adhoc_conferences.users.{user_uuid}.created'


class AdhocConferenceDeletedUserEvent(AdhocConferenceUserEvent):
    name = 'adhoc_conference_deleted'
    routing_key_fmt = 'adhoc_conferences.users.{user_uuid}.deleted'


class AdhocConferenceParticipantUserEvent(BaseEvent):
    def __init__(self, conference_id, user_uuid, participant_call):
        self._body = {
            'conference_id': conference_id,
            'participant_call': participant_call,
        }
        self.routing_key_fmt = self.routing_key_fmt.format(user_uuid=user_uuid)
        super(AdhocConferenceParticipantUserEvent, self).__init__()


class AdhocConferenceParticipantJoinedUserEvent(AdhocConferenceParticipantUserEvent):
    name = 'adhoc_conference_participant_joined'
    routing_key_fmt = 'adhoc_conferences.users.{user_uuid}.participants.joined'


class AdhocConferenceParticipantLeftUserEvent(AdhocConferenceParticipantUserEvent):
    name = 'adhoc_conference_participant_left'
    routing_key_fmt = 'adhoc_conferences.users.{user_uuid}.participants.left'
