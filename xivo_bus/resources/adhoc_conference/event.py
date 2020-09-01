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
    name = 'conference_adhoc_created'
    routing_key_fmt = 'conferences.users.{user_uuid}.adhoc.created'


class AdhocConferenceDeletedUserEvent(AdhocConferenceUserEvent):
    name = 'conference_adhoc_deleted'
    routing_key_fmt = 'conferences.users.{user_uuid}.adhoc.deleted'


class AdhocConferenceParticipantUserEvent(BaseEvent):
    def __init__(self, conference_id, user_uuid, participant_call):
        self._body = {
            'conference_id': conference_id,
            'call_id': participant_call['call_id'],
        }
        self.routing_key_fmt = self.routing_key_fmt.format(user_uuid=user_uuid)
        super(AdhocConferenceParticipantUserEvent, self).__init__()


class AdhocConferenceParticipantJoinedUserEvent(AdhocConferenceParticipantUserEvent):
    name = 'conference_adhoc_participant_joined'
    routing_key_fmt = 'conferences.users.{user_uuid}.adhoc.participants.joined'


class AdhocConferenceParticipantLeftUserEvent(AdhocConferenceParticipantUserEvent):
    name = 'conference_adhoc_participant_left'
    routing_key_fmt = 'conferences.users.{user_uuid}.adhoc.participants.left'
